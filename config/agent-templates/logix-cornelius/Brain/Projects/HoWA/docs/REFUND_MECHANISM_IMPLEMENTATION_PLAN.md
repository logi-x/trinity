---
title: "Complete Refund Mechanism Implementation Plan"
date: "2026-04-11"
tags: ["project/howa", "docs/howa"]
category: "docs/howa"
updated: "2026-07-15"
---

## Links

- [[Entities/Projects/HoWA]]

# Complete Refund Mechanism Implementation Plan

## Overview

Implement a full-featured refund system with partial refund support, proper UI/UX, and accurate data display across all dashboards and tables.

---

## 📋 Table of Contents

1. [Backend Implementation](#backend-implementation)
2. [Frontend Implementation](#frontend-implementation)
3. [Data Display Updates](#data-display-updates)
4. [Testing Strategy](#testing-strategy)
5. [Rollout Plan](#rollout-plan)

---

## 🔧 Backend Implementation

### Phase 1: API Endpoints & Controllers

#### 1.1 Create InvoiceRefundController

**File: `app/Http/Controllers/Invoice/InvoiceRefundController.php`**

```php
<?php

namespace App\Http\Controllers\Invoice;

use App\Http\Controllers\Controller;
use App\Models\Invoice\Invoice;
use App\Models\Invoice\InvoiceRefund;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;

class InvoiceRefundController extends Controller
{
    /**
     * Get refund details for an invoice
     */
    public function show(Invoice $invoice)
    {
        $refunds = $invoice->refunds()
            ->with(['user', 'processedBy'])
            ->orderBy('created_at', 'desc')
            ->get();

        return response()->json([
            'invoice' => $invoice,
            'refunds' => $refunds,
            'total_refunded' => $invoice->total_refunded,
            'remaining_refundable' => $invoice->getRemainingRefundableAmount(),
            'can_refund' => $invoice->canBeRefunded(),
        ]);
    }

    /**
     * Request a new refund
     */
    public function store(Request $request, Invoice $invoice)
    {
        // Validate
        $validated = $request->validate([
            'refund_amount' => [
                'required',
                'numeric',
                'min:0.01',
                'max:' . $invoice->getRemainingRefundableAmount(),
            ],
            'refund_reason' => [
                'required',
                'in:customer_request,course_cancelled,service_not_delivered,duplicate_payment,technical_error,quality_issue,other'
            ],
            'refund_notes' => 'nullable|string|max:1000',
        ]);

        // Check if invoice can be refunded
        if (!$invoice->canBeRefunded()) {
            return response()->json([
                'message' => 'This invoice cannot be refunded',
                'reason' => $invoice->fully_refunded ? 'Already fully refunded' : 'Invoice not paid',
            ], 422);
        }

        // Calculate refund amounts
        $refundAmount = $validated['refund_amount'];
        $taxRefund = $invoice->taxable ? ($refundAmount * ($invoice->tax_rate / 100)) : 0;
        $netRefund = $refundAmount + $taxRefund;

        // Determine refund type
        $remainingAmount = $invoice->getRemainingRefundableAmount();
        $isFullRefund = ($refundAmount >= $remainingAmount);

        DB::beginTransaction();
        try {
            // Create refund record
            $refund = InvoiceRefund::create([
                'invoice_id' => $invoice->id,
                'user_id' => auth()->id(),
                'refund_amount' => $refundAmount,
                'tax_refund' => $taxRefund,
                'net_refund' => $netRefund,
                'refund_type' => $isFullRefund ? 'full' : 'partial',
                'refund_reason' => $validated['refund_reason'],
                'refund_notes' => $validated['refund_notes'],
                'refund_method' => $invoice->payment_method,
                'status' => 'pending',
                'requested_at' => now(),
            ]);

            DB::commit();

            Log::info('Refund requested', [
                'refund_id' => $refund->id,
                'invoice_id' => $invoice->id,
                'amount' => $netRefund,
                'type' => $refund->refund_type,
            ]);

            return response()->json([
                'message' => 'Refund request created successfully',
                'refund' => $refund->load(['user']),
            ], 201);

        } catch (\Exception $e) {
            DB::rollBack();
            Log::error('Refund request failed', [
                'invoice_id' => $invoice->id,
                'error' => $e->getMessage(),
            ]);

            return response()->json([
                'message' => 'Failed to create refund request',
                'error' => $e->getMessage(),
            ], 500);
        }
    }

    /**
     * Approve a pending refund
     */
    public function approve(InvoiceRefund $refund)
    {
        if ($refund->status !== 'pending') {
            return response()->json([
                'message' => 'Only pending refunds can be approved',
            ], 422);
        }

        $refund->update([
            'status' => 'approved',
            'approved_at' => now(),
            'processed_by' => auth()->id(),
        ]);

        return response()->json([
            'message' => 'Refund approved successfully',
            'refund' => $refund->load(['processedBy']),
        ]);
    }

    /**
     * Process (complete) an approved refund
     */
    public function process(Request $request, InvoiceRefund $refund)
    {
        if (!in_array($refund->status, ['pending', 'approved'])) {
            return response()->json([
                'message' => 'This refund cannot be processed',
            ], 422);
        }

        $validated = $request->validate([
            'bank_transaction_id' => 'nullable|string|max:255',
            'processing_notes' => 'nullable|string|max:1000',
        ]);

        DB::beginTransaction();
        try {
            // Update refund status
            $refund->update([
                'status' => 'completed',
                'processed_by' => auth()->id(),
                'processed_at' => now(),
                'completed_at' => now(),
                'bank_transaction_id' => $validated['bank_transaction_id'] ?? null,
                'refund_notes' => $refund->refund_notes . "\n\nProcessing notes: " . ($validated['processing_notes'] ?? ''),
            ]);

            // Update invoice refund tracking
            $invoice = $refund->invoice;
            $totalRefunded = $invoice->completedRefunds()->sum('net_refund');
            $refundCount = $invoice->completedRefunds()->count();

            $invoice->update([
                'total_refunded' => $totalRefunded,
                'refund_count' => $refundCount,
                'has_refunds' => true,
                'fully_refunded' => $totalRefunded >= $invoice->paid,
                'status' => $totalRefunded >= $invoice->paid ? 'refunded' : $invoice->status,
                'last_refund_at' => now(),
                'first_refund_at' => $invoice->first_refund_at ?? now(),
            ]);

            DB::commit();

            Log::info('Refund processed', [
                'refund_id' => $refund->id,
                'invoice_id' => $invoice->id,
                'amount' => $refund->net_refund,
            ]);

            return response()->json([
                'message' => 'Refund processed successfully',
                'refund' => $refund->load(['invoice', 'processedBy']),
            ]);

        } catch (\Exception $e) {
            DB::rollBack();
            Log::error('Refund processing failed', [
                'refund_id' => $refund->id,
                'error' => $e->getMessage(),
            ]);

            return response()->json([
                'message' => 'Failed to process refund',
                'error' => $e->getMessage(),
            ], 500);
        }
    }

    /**
     * Cancel a refund request
     */
    public function cancel(Request $request, InvoiceRefund $refund)
    {
        if (!in_array($refund->status, ['pending', 'approved'])) {
            return response()->json([
                'message' => 'Only pending or approved refunds can be cancelled',
            ], 422);
        }

        $validated = $request->validate([
            'cancellation_reason' => 'required|string|max:500',
        ]);

        $refund->update([
            'status' => 'cancelled',
            'refund_notes' => $refund->refund_notes . "\n\nCancelled: " . $validated['cancellation_reason'],
        ]);

        return response()->json([
            'message' => 'Refund cancelled successfully',
            'refund' => $refund,
        ]);
    }

    /**
     * List all refunds (admin)
     */
    public function index(Request $request)
    {
        $query = InvoiceRefund::with(['invoice', 'user', 'processedBy'])
            ->orderBy('created_at', 'desc');

        // Filter by status
        if ($request->has('status')) {
            $query->where('status', $request->status);
        }

        // Filter by date range
        if ($request->has('from_date')) {
            $query->whereDate('requested_at', '>=', $request->from_date);
        }
        if ($request->has('to_date')) {
            $query->whereDate('requested_at', '<=', $request->to_date);
        }

        $refunds = $query->paginate(50);

        return response()->json($refunds);
    }
}
```

#### 1.2 Add Routes

**File: `routes/web.php` or `routes/api.php`**

```php
// Refund Management Routes
Route::prefix('invoices/{invoice}/refunds')->group(function () {
    Route::get('/', [InvoiceRefundController::class, 'show']);
    Route::post('/', [InvoiceRefundController::class, 'store']);
});

Route::prefix('refunds')->middleware(['auth', 'can:manage-refunds'])->group(function () {
    Route::get('/', [InvoiceRefundController::class, 'index']);
    Route::post('/{refund}/approve', [InvoiceRefundController::class, 'approve']);
    Route::post('/{refund}/process', [InvoiceRefundController::class, 'process']);
    Route::post('/{refund}/cancel', [InvoiceRefundController::class, 'cancel']);
});
```

#### 1.3 Create Form Requests

**File: `app/Http/Requests/RefundRequest.php`**

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class RefundRequest extends FormRequest
{
    public function authorize(): bool
    {
        $invoice = $this->route('invoice');

        // User can request refund for their own invoices
        // Or admin can request for any invoice
        return $this->user()->id === $invoice->user_id ||
               $this->user()->hasPermissionTo('manage-refunds');
    }

    public function rules(): array
    {
        $invoice = $this->route('invoice');
        $maxRefund = $invoice->getRemainingRefundableAmount();

        return [
            'refund_amount' => [
                'required',
                'numeric',
                'min:0.01',
                "max:{$maxRefund}",
            ],
            'refund_reason' => [
                'required',
                'in:customer_request,course_cancelled,service_not_delivered,duplicate_payment,technical_error,quality_issue,other'
            ],
            'refund_notes' => 'nullable|string|max:1000',
        ];
    }

    public function messages(): array
    {
        return [
            'refund_amount.max' => 'Refund amount cannot exceed the remaining refundable amount.',
            'refund_reason.required' => 'Please select a reason for the refund.',
        ];
    }
}
```

### Phase 2: Business Logic & Services

#### 2.1 Create RefundService

**File: `app/Services/RefundService.php`**

```php
<?php

namespace App\Services;

use App\Models\Invoice\Invoice;
use App\Models\Invoice\InvoiceRefund;
use Illuminate\Support\Facades\DB;

class RefundService
{
    /**
     * Calculate refund breakdown
     */
    public function calculateRefundBreakdown(Invoice $invoice, float $refundAmount): array
    {
        $taxRefund = $invoice->taxable ? ($refundAmount * ($invoice->tax_rate / 100)) : 0;
        $netRefund = $refundAmount + $taxRefund;
        $remainingAmount = $invoice->getRemainingRefundableAmount();
        $isFullRefund = ($refundAmount >= $remainingAmount);

        return [
            'refund_amount' => round($refundAmount, 2),
            'tax_refund' => round($taxRefund, 2),
            'net_refund' => round($netRefund, 2),
            'is_full_refund' => $isFullRefund,
            'refund_percentage' => round(($refundAmount / $invoice->subtotal) * 100, 2),
        ];
    }

    /**
     * Process refund with ZATCA compliance
     */
    public function processRefundWithZATCA(InvoiceRefund $refund, ?string $creditNoteNumber = null): bool
    {
        DB::beginTransaction();
        try {
            // Update refund
            $refund->update([
                'status' => 'completed',
                'completed_at' => now(),
                'reported_to_zatca' => true,
                'credit_note_number' => $creditNoteNumber,
                'reported_at' => now(),
            ]);

            // Update invoice
            $this->updateInvoiceRefundStatus($refund->invoice);

            DB::commit();
            return true;
        } catch (\Exception $e) {
            DB::rollBack();
            \Log::error('ZATCA refund processing failed: ' . $e->getMessage());
            return false;
        }
    }

    /**
     * Update invoice refund status
     */
    private function updateInvoiceRefundStatus(Invoice $invoice): void
    {
        $totalRefunded = $invoice->completedRefunds()->sum('net_refund');
        $refundCount = $invoice->completedRefunds()->count();

        $invoice->update([
            'total_refunded' => $totalRefunded,
            'refund_count' => $refundCount,
            'has_refunds' => true,
            'fully_refunded' => $totalRefunded >= $invoice->paid,
            'status' => $totalRefunded >= $invoice->paid ? 'refunded' : $invoice->status,
            'last_refund_at' => now(),
            'first_refund_at' => $invoice->first_refund_at ?? now(),
        ]);
    }

    /**
     * Get refund statistics
     */
    public function getRefundStats(\DateTime $startDate, \DateTime $endDate): array
    {
        $refunds = InvoiceRefund::whereBetween('completed_at', [$startDate, $endDate])
            ->where('status', 'completed')
            ->get();

        return [
            'total_refunds' => $refunds->count(),
            'total_amount' => $refunds->sum('net_refund'),
            'full_refunds' => $refunds->where('refund_type', 'full')->count(),
            'partial_refunds' => $refunds->where('refund_type', 'partial')->count(),
            'by_reason' => $refunds->groupBy('refund_reason')->map->count(),
            'avg_processing_time' => $this->calculateAvgProcessingTime($refunds),
        ];
    }

    private function calculateAvgProcessingTime($refunds): ?float
    {
        $times = $refunds->filter(function ($refund) {
            return $refund->requested_at && $refund->completed_at;
        })->map(function ($refund) {
            return $refund->completed_at->diffInHours($refund->requested_at);
        });

        return $times->isNotEmpty() ? $times->avg() : null;
    }
}
```

---

## 🎨 Frontend Implementation

### Phase 1: Refund Request Modal

#### 1.1 Create RefundModal Component

**File: `apps/admin/resources/js/components/refunds/refund-modal.tsx`**

```typescript
import React, { useState } from 'react';
import {
    Modal,
    ModalContent,
    ModalHeader,
    ModalBody,
    ModalFooter,
    Button,
    Input,
    Select,
    SelectItem,
    Textarea,
    Chip,
} from "@heroui/react";
import { router } from '@inertiajs/react';

interface Invoice {
    id: string;
    invoice_number: string;
    subtotal: number;
    tax: number;
    paid: number;
    total_refunded: number;
    remaining_refundable: number;
}

interface RefundModalProps {
    invoice: Invoice;
    isOpen: boolean;
    onClose: () => void;
}

const REFUND_REASONS = [
    { value: 'customer_request', label: 'Customer Request' },
    { value: 'course_cancelled', label: 'Course Cancelled' },
    { value: 'service_not_delivered', label: 'Service Not Delivered' },
    { value: 'duplicate_payment', label: 'Duplicate Payment' },
    { value: 'technical_error', label: 'Technical Error' },
    { value: 'quality_issue', label: 'Quality Issue' },
    { value: 'other', label: 'Other' },
];

export default function RefundModal({ invoice, isOpen, onClose }: RefundModalProps) {
    const [refundAmount, setRefundAmount] = useState<string>('');
    const [refundReason, setRefundReason] = useState<string>('');
    const [refundNotes, setRefundNotes] = useState<string>('');
    const [isProcessing, setIsProcessing] = useState(false);
    const [errors, setErrors] = useState<Record<string, string>>({});

    // Calculate refund breakdown
    const amount = parseFloat(refundAmount) || 0;
    const taxRate = invoice.tax / invoice.subtotal;
    const taxRefund = amount * taxRate;
    const netRefund = amount + taxRefund;
    const isFullRefund = amount >= invoice.remaining_refundable;
    const refundPercentage = (amount / invoice.subtotal) * 100;

    const handleSubmit = () => {
        setIsProcessing(true);
        setErrors({});

        router.post(
            `/invoices/${invoice.id}/refunds`,
            {
                refund_amount: amount,
                refund_reason: refundReason,
                refund_notes: refundNotes,
            },
            {
                onSuccess: () => {
                    onClose();
                    // Show success notification
                },
                onError: (errors) => {
                    setErrors(errors);
                },
                onFinish: () => {
                    setIsProcessing(false);
                },
            }
        );
    };

    const handleQuickSelect = (percentage: number) => {
        const amount = (invoice.remaining_refundable * percentage) / 100;
        setRefundAmount(amount.toFixed(2));
    };

    return (
        <Modal
            isOpen={isOpen}
            onClose={onClose}
            size="2xl"
            scrollBehavior="inside"
        >
            <ModalContent>
                <ModalHeader className="flex flex-col gap-1">
                    <h3>Request Refund</h3>
                    <p className="text-sm text-zinc-500">
                        Invoice #{invoice.invoice_number}
                    </p>
                </ModalHeader>
                <ModalBody>
                    {/* Invoice Summary */}
                    <div className="bg-zinc-100 dark:bg-zinc-800 p-4 rounded-lg space-y-2">
                        <div className="flex justify-between text-sm">
                            <span className="text-zinc-600 dark:text-zinc-400">Subtotal:</span>
                            <span className="font-medium">SAR {invoice.subtotal.toFixed(2)}</span>
                        </div>
                        <div className="flex justify-between text-sm">
                            <span className="text-zinc-600 dark:text-zinc-400">Tax (15%):</span>
                            <span className="font-medium">SAR {invoice.tax.toFixed(2)}</span>
                        </div>
                        <div className="flex justify-between text-sm font-semibold pt-2 border-t border-zinc-300 dark:border-zinc-700">
                            <span>Total Paid:</span>
                            <span>SAR {invoice.paid.toFixed(2)}</span>
                        </div>
                        {invoice.total_refunded > 0 && (
                            <div className="flex justify-between text-sm text-orange-600 dark:text-orange-400">
                                <span>Already Refunded:</span>
                                <span>SAR {invoice.total_refunded.toFixed(2)}</span>
                            </div>
                        )}
                        <div className="flex justify-between text-sm font-semibold text-green-600 dark:text-green-400">
                            <span>Available to Refund:</span>
                            <span>SAR {invoice.remaining_refundable.toFixed(2)}</span>
                        </div>
                    </div>

                    {/* Quick Select Buttons */}
                    <div className="space-y-2">
                        <label className="text-sm font-medium">Quick Select:</label>
                        <div className="flex gap-2 flex-wrap">
                            <Button
                                size="sm"
                                variant="flat"
                                onClick={() => handleQuickSelect(25)}
                            >
                                25%
                            </Button>
                            <Button
                                size="sm"
                                variant="flat"
                                onClick={() => handleQuickSelect(50)}
                            >
                                50%
                            </Button>
                            <Button
                                size="sm"
                                variant="flat"
                                onClick={() => handleQuickSelect(75)}
                            >
                                75%
                            </Button>
                            <Button
                                size="sm"
                                variant="flat"
                                color="danger"
                                onClick={() => handleQuickSelect(100)}
                            >
                                100% (Full Refund)
                            </Button>
                        </div>
                    </div>

                    {/* Refund Amount Input */}
                    <Input
                        label="Refund Amount (excluding tax)"
                        placeholder="0.00"
                        value={refundAmount}
                        onChange={(e) => setRefundAmount(e.target.value)}
                        type="number"
                        step="0.01"
                        min="0"
                        max={invoice.remaining_refundable.toString()}
                        startContent={<span className="text-sm text-zinc-500">SAR</span>}
                        errorMessage={errors.refund_amount}
                        isInvalid={!!errors.refund_amount}
                    />

                    {/* Refund Breakdown */}
                    {amount > 0 && (
                        <div className="bg-blue-50 dark:bg-blue-950 p-4 rounded-lg space-y-2">
                            <h4 className="text-sm font-semibold mb-2">Refund Breakdown:</h4>
                            <div className="flex justify-between text-sm">
                                <span>Refund Amount:</span>
                                <span className="font-medium">SAR {amount.toFixed(2)}</span>
                            </div>
                            <div className="flex justify-between text-sm">
                                <span>Tax Refund (15%):</span>
                                <span className="font-medium">SAR {taxRefund.toFixed(2)}</span>
                            </div>
                            <div className="flex justify-between text-sm font-semibold pt-2 border-t border-blue-200 dark:border-blue-800">
                                <span>Total Refund:</span>
                                <span>SAR {netRefund.toFixed(2)}</span>
                            </div>
                            <div className="flex items-center gap-2 pt-2">
                                <Chip
                                    color={isFullRefund ? "danger" : "warning"}
                                    size="sm"
                                    variant="flat"
                                >
                                    {isFullRefund ? 'Full Refund' : 'Partial Refund'}
                                </Chip>
                                <Chip
                                    color="primary"
                                    size="sm"
                                    variant="flat"
                                >
                                    {refundPercentage.toFixed(1)}% of invoice
                                </Chip>
                            </div>
                        </div>
                    )}

                    {/* Refund Reason */}
                    <Select
                        label="Refund Reason"
                        placeholder="Select a reason"
                        selectedKeys={refundReason ? [refundReason] : []}
                        onChange={(e) => setRefundReason(e.target.value)}
                        errorMessage={errors.refund_reason}
                        isInvalid={!!errors.refund_reason}
                    >
                        {REFUND_REASONS.map((reason) => (
                            <SelectItem key={reason.value} value={reason.value}>
                                {reason.label}
                            </SelectItem>
                        ))}
                    </Select>

                    {/* Refund Notes */}
                    <Textarea
                        label="Additional Notes"
                        placeholder="Provide any additional information about this refund..."
                        value={refundNotes}
                        onChange={(e) => setRefundNotes(e.target.value)}
                        maxLength={1000}
                        errorMessage={errors.refund_notes}
                        isInvalid={!!errors.refund_notes}
                    />
                </ModalBody>
                <ModalFooter>
                    <Button
                        variant="flat"
                        onPress={onClose}
                    >
                        Cancel
                    </Button>
                    <Button
                        color="danger"
                        onPress={handleSubmit}
                        isLoading={isProcessing}
                        isDisabled={!amount || !refundReason || amount > invoice.remaining_refundable}
                    >
                        Request Refund
                    </Button>
                </ModalFooter>
            </ModalContent>
        </Modal>
    );
}
```

### Phase 2: Refund Management Page

#### 2.1 Create Refunds List Page

**File: `apps/admin/resources/js/Pages/refunds/index.tsx`**

```typescript
import React, { useState } from 'react';
import {
    Table,
    TableHeader,
    TableColumn,
    TableBody,
    TableRow,
    TableCell,
    Chip,
    Button,
    Dropdown,
    DropdownTrigger,
    DropdownMenu,
    DropdownItem,
    Input,
} from "@heroui/react";
import { Head, router } from '@inertiajs/react';
import AuthenticatedLayout from '@/layouts/authenticated-layout';
import { formatCurrency, formatDate } from '@/utils/formatters';
import { EllipsisVertical, Search, Filter } from 'lucide-react';

interface Refund {
    id: string;
    invoice: {
        invoice_number: string;
    };
    user: {
        name: string;
    };
    refund_amount: number;
    net_refund: number;
    status: string;
    refund_type: string;
    refund_reason: string;
    requested_at: string;
    completed_at: string | null;
}

interface Props {
    refunds: {
        data: Refund[];
        links: any;
        meta: any;
    };
    filters: {
        status?: string;
        from_date?: string;
        to_date?: string;
    };
}

const STATUS_COLORS = {
    pending: 'warning',
    approved: 'primary',
    processing: 'secondary',
    completed: 'success',
    failed: 'danger',
    cancelled: 'default',
};

const REASON_LABELS = {
    customer_request: 'Customer Request',
    course_cancelled: 'Course Cancelled',
    service_not_delivered: 'Service Not Delivered',
    duplicate_payment: 'Duplicate Payment',
    technical_error: 'Technical Error',
    quality_issue: 'Quality Issue',
    other: 'Other',
};

export default function RefundsIndex({ refunds, filters }: Props) {
    const [search, setSearch] = useState('');

    const handleAction = (refundId: string, action: string) => {
        router.post(`/refunds/${refundId}/${action}`, {}, {
            preserveScroll: true,
        });
    };

    return (
        <AuthenticatedLayout>
            <Head title="Refund Management" />

            <div className="py-8 px-4 sm:px-6 lg:px-8">
                <div className="sm:flex sm:items-center sm:justify-between mb-6">
                    <div>
                        <h1 className="text-2xl font-semibold text-zinc-900 dark:text-zinc-100">
                            Refund Management
                        </h1>
                        <p className="mt-2 text-sm text-zinc-700 dark:text-zinc-400">
                            Manage and process refund requests
                        </p>
                    </div>
                </div>

                {/* Filters */}
                <div className="mb-6 flex gap-4">
                    <Input
                        placeholder="Search invoices..."
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                        startContent={<Search className="w-4 h-4" />}
                        className="max-w-xs"
                    />
                    <Button
                        variant="flat"
                        startContent={<Filter className="w-4 h-4" />}
                    >
                        Filters
                    </Button>
                </div>

                {/* Refunds Table */}
                <Table aria-label="Refunds table">
                    <TableHeader>
                        <TableColumn>INVOICE</TableColumn>
                        <TableColumn>CUSTOMER</TableColumn>
                        <TableColumn>AMOUNT</TableColumn>
                        <TableColumn>TYPE</TableColumn>
                        <TableColumn>REASON</TableColumn>
                        <TableColumn>STATUS</TableColumn>
                        <TableColumn>REQUESTED</TableColumn>
                        <TableColumn>ACTIONS</TableColumn>
                    </TableHeader>
                    <TableBody>
                        {refunds.data.map((refund) => (
                            <TableRow key={refund.id}>
                                <TableCell>
                                    <span className="font-mono text-sm">
                                        #{refund.invoice.invoice_number}
                                    </span>
                                </TableCell>
                                <TableCell>{refund.user.name}</TableCell>
                                <TableCell>
                                    <div className="flex flex-col">
                                        <span className="font-semibold">
                                            {formatCurrency(refund.net_refund, 'SAR')}
                                        </span>
                                        <span className="text-xs text-zinc-500">
                                            ({formatCurrency(refund.refund_amount, 'SAR')} + tax)
                                        </span>
                                    </div>
                                </TableCell>
                                <TableCell>
                                    <Chip
                                        size="sm"
                                        variant="flat"
                                        color={refund.refund_type === 'full' ? 'danger' : 'warning'}
                                    >
                                        {refund.refund_type}
                                    </Chip>
                                </TableCell>
                                <TableCell>
                                    <span className="text-sm">
                                        {REASON_LABELS[refund.refund_reason]}
                                    </span>
                                </TableCell>
                                <TableCell>
                                    <Chip
                                        size="sm"
                                        variant="flat"
                                        color={STATUS_COLORS[refund.status] as any}
                                    >
                                        {refund.status}
                                    </Chip>
                                </TableCell>
                                <TableCell>
                                    {formatDate(refund.requested_at)}
                                </TableCell>
                                <TableCell>
                                    <Dropdown>
                                        <DropdownTrigger>
                                            <Button
                                                isIconOnly
                                                size="sm"
                                                variant="light"
                                            >
                                                <EllipsisVertical className="w-4 h-4" />
                                            </Button>
                                        </DropdownTrigger>
                                        <DropdownMenu>
                                            {refund.status === 'pending' && (
                                                <>
                                                    <DropdownItem
                                                        key="approve"
                                                        onPress={() => handleAction(refund.id, 'approve')}
                                                    >
                                                        Approve
                                                    </DropdownItem>
                                                    <DropdownItem
                                                        key="cancel"
                                                        className="text-danger"
                                                        color="danger"
                                                        onPress={() => handleAction(refund.id, 'cancel')}
                                                    >
                                                        Cancel
                                                    </DropdownItem>
                                                </>
                                            )}
                                            {refund.status === 'approved' && (
                                                <DropdownItem
                                                    key="process"
                                                    onPress={() => handleAction(refund.id, 'process')}
                                                >
                                                    Process Refund
                                                </DropdownItem>
                                            )}
                                            <DropdownItem key="view">
                                                View Details
                                            </DropdownItem>
                                        </DropdownMenu>
                                    </Dropdown>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </div>
        </AuthenticatedLayout>
    );
}
```

---

## 📊 Data Display Updates

### Phase 1: Dashboard Statistics Update

#### 1.1 Update Main Dashboard Controller

**File: `app/Http/Controllers/DashboardController.php`**

```php
public function index()
{
    $stats = [
        // Existing stats
        'total_revenue' => Invoice::where('status', 'paid')->sum('paid'),

        // NEW: Refund stats
        'total_refunded' => InvoiceRefund::completed()->sum('net_refund'),
        'refund_count' => InvoiceRefund::completed()->count(),
        'pending_refunds' => InvoiceRefund::pending()->count(),

        // Updated net revenue (after refunds)
        'net_revenue' => Invoice::where('status', 'paid')->sum('paid') -
                         InvoiceRefund::completed()->sum('net_refund'),
    ];

    return Inertia::render('home/home', [
        'stats' => $stats,
    ]);
}
```

#### 1.2 Update Dashboard Stats Cards

**File: `apps/admin/resources/js/Pages/home/sections/stats/stats-cards.tsx`**

```typescript
// Add new stat card for refunds
<StatsCard
    title="Total Refunded"
    value={formatCurrency(stats.total_refunded, 'SAR')}
    change={stats.refund_change}
    trend={stats.refund_trend}
    icon={<RefundIcon />}
    color="red"
/>

<StatsCard
    title="Net Revenue"
    subtitle="After refunds"
    value={formatCurrency(stats.net_revenue, 'SAR')}
    icon={<TrendingUpIcon />}
    color="green"
/>

{stats.pending_refunds > 0 && (
    <Alert color="warning">
        {stats.pending_refunds} refund{stats.pending_refunds > 1 ? 's' : ''} pending approval
    </Alert>
)}
```

### Phase 2: Invoices Table Update

#### 2.1 Update Invoices List

**File: `apps/admin/resources/js/Pages/invoices/index.tsx`**

```typescript
// Add refund status column
<TableColumn key="refund_status">REFUND STATUS</TableColumn>

// In table body
<TableCell>
    {invoice.has_refunds ? (
        <div className="flex flex-col gap-1">
            <Chip
                size="sm"
                variant="flat"
                color={invoice.fully_refunded ? 'danger' : 'warning'}
            >
                {invoice.fully_refunded ? 'Fully Refunded' : 'Partially Refunded'}
            </Chip>
            <span className="text-xs text-zinc-500">
                {formatCurrency(invoice.total_refunded, 'SAR')} refunded
            </span>
            <span className="text-xs text-zinc-500">
                {invoice.refund_count} refund{invoice.refund_count > 1 ? 's' : ''}
            </span>
        </div>
    ) : (
        <span className="text-zinc-400">No refunds</span>
    )}
</TableCell>

// Add refund button in actions
{invoice.status === 'paid' && !invoice.fully_refunded && (
    <Button
        size="sm"
        color="danger"
        variant="flat"
        onPress={() => openRefundModal(invoice)}
    >
        Request Refund
    </Button>
)}
```

### Phase 3: Course Enrollment Tables

#### 3.1 Update Enrollments Table

**File: `apps/admin/resources/js/Pages/courses/enrollments/index.tsx`**

```typescript
// Show refund status in enrollment
<TableCell>
    {enrollment.invoice.has_refunds && (
        <Tooltip content={`${formatCurrency(enrollment.invoice.total_refunded, 'SAR')} refunded`}>
            <Chip
                size="sm"
                variant="flat"
                color="danger"
                startContent={<RefundIcon className="w-3 h-3" />}
            >
                Refunded
            </Chip>
        </Tooltip>
    )}
</TableCell>
```

### Phase 4: Financial Reports

#### 4.1 Update Reports to Include Refunds

**File: `app/Http/Controllers/Reports/FinancialReportController.php`**

```php
public function monthlyReport(Request $request)
{
    $startDate = $request->input('start_date');
    $endDate = $request->input('end_date');

    // Revenue by date
    $revenue = Invoice::whereBetween('created_at', [$startDate, $endDate])
        ->where('status', 'paid')
        ->selectRaw('DATE(created_at) as date, SUM(paid) as total')
        ->groupBy('date')
        ->get();

    // Refunds by date (on completed_at, not invoice created_at)
    $refunds = InvoiceRefund::whereBetween('completed_at', [$startDate, $endDate])
        ->where('status', 'completed')
        ->selectRaw('DATE(completed_at) as date, SUM(net_refund) as total')
        ->groupBy('date')
        ->get();

    // Merge and calculate net
    $report = $revenue->map(function ($day) use ($refunds) {
        $refundForDay = $refunds->firstWhere('date', $day->date);

        return [
            'date' => $day->date,
            'gross_revenue' => $day->total,
            'refunds' => $refundForDay ? $refundForDay->total : 0,
            'net_revenue' => $day->total - ($refundForDay ? $refundForDay->total : 0),
        ];
    });

    return response()->json($report);
}
```

---

## 🧪 Testing Strategy

### Unit Tests

```php
// tests/Unit/RefundServiceTest.php
public function test_calculate_refund_breakdown()
{
    $invoice = Invoice::factory()->create([
        'subtotal' => 1000,
        'tax' => 150,
        'paid' => 1150,
    ]);

    $service = new RefundService();
    $breakdown = $service->calculateRefundBreakdown($invoice, 500);

    $this->assertEquals(500, $breakdown['refund_amount']);
    $this->assertEquals(75, $breakdown['tax_refund']);
    $this->assertEquals(575, $breakdown['net_refund']);
    $this->assertFalse($breakdown['is_full_refund']);
}

public function test_partial_refund_updates_invoice_correctly()
{
    $invoice = Invoice::factory()->create([
        'subtotal' => 1000,
        'tax' => 150,
        'paid' => 1150,
        'status' => 'paid',
    ]);

    $refund = InvoiceRefund::factory()->create([
        'invoice_id' => $invoice->id,
        'refund_amount' => 500,
        'tax_refund' => 75,
        'net_refund' => 575,
        'status' => 'completed',
    ]);

    $invoice->refresh();

    $this->assertEquals(575, $invoice->total_refunded);
    $this->assertEquals(1, $invoice->refund_count);
    $this->assertTrue($invoice->has_refunds);
    $this->assertFalse($invoice->fully_refunded);
    $this->assertEquals('paid', $invoice->status);
}
```

### Feature Tests

```php
// tests/Feature/RefundWorkflowTest.php
public function test_user_can_request_refund_for_their_invoice()
{
    $user = User::factory()->create();
    $invoice = Invoice::factory()->create([
        'user_id' => $user->id,
        'paid' => 1150,
        'status' => 'paid',
    ]);

    $response = $this->actingAs($user)
        ->postJson("/invoices/{$invoice->id}/refunds", [
            'refund_amount' => 500,
            'refund_reason' => 'customer_request',
            'refund_notes' => 'Test refund',
        ]);

    $response->assertStatus(201);
    $this->assertDatabaseHas('invoice_refunds', [
        'invoice_id' => $invoice->id,
        'refund_amount' => 500,
        'status' => 'pending',
    ]);
}

public function test_admin_can_approve_and_process_refund()
{
    $admin = User::factory()->admin()->create();
    $refund = InvoiceRefund::factory()->create(['status' => 'pending']);

    // Approve
    $this->actingAs($admin)
        ->postJson("/refunds/{$refund->id}/approve")
        ->assertStatus(200);

    $this->assertEquals('approved', $refund->fresh()->status);

    // Process
    $this->actingAs($admin)
        ->postJson("/refunds/{$refund->id}/process")
        ->assertStatus(200);

    $this->assertEquals('completed', $refund->fresh()->status);
}
```

---

## 🚀 Rollout Plan

### Week 1: Backend Foundation

- ✅ Migrations (already done)
- ✅ Models (already done)
- ✅ Controllers
- ✅ Services
- ✅ Routes
- ✅ Policies & Permissions
- ✅ Unit Tests

### Week 2: Frontend Implementation

- ✅ Refund Modal Component
- ✅ Refunds Management Page
- ✅ Invoice Actions Integration
- ✅ Dashboard Updates
- ✅ Table Updates

### Week 3: Testing & Polish

- ✅ Feature Tests
- ✅ UI/UX Testing
- ✅ ETF Integration Testing
- ✅ Performance Testing
- ✅ Bug Fixes

### Week 4: Documentation & Deployment

- ✅ User Documentation
- ✅ Admin Training
- ✅ Staged Rollout (10% → 50% → 100%)
- ✅ Monitoring Setup
- ✅ Feedback Collection

---

## 📈 Success Metrics

### Operational Metrics

- Refund processing time < 24 hours
- Zero data inconsistencies
- 100% audit trail coverage

### User Experience Metrics

- Refund request completion rate
- User satisfaction score
- Support ticket reduction

### Financial Metrics

- Accurate ETF NAV calculations
- Real-time cash flow visibility
- Refund trend analysis accuracy

---

## 🎯 Summary

This plan provides:

1. ✅ Complete refund request workflow
2. ✅ Partial refund support
3. ✅ Real-time ETF integration
4. ✅ Accurate dashboard statistics
5. ✅ Comprehensive testing
6. ✅ User-friendly UI/UX

**Total Implementation Time**: ~4 weeks  
**Priority**: High (Financial Accuracy Critical)

Ready to start implementation? 🚀
