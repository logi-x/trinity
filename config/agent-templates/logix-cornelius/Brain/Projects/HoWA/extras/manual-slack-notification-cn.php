<?php

$invoice = \App\Models\Invoice\Invoice::find("63acfe53-a4ec-4993-b7bf-9c4ad8a8796e");

$refundService = app(\App\Services\RefundService::class);
$breakdown = $refundService->calculateRefundBreakdown($invoice, $invoice->paid);

$refundData = [
    'partial' => false,
    'partial_amount' => $invoice->paid,
    'amount' => $invoice->paid,
    'action' => 'refund',
    'refund_id' => $invoice->id,
    'processed_by' => 86, // null for gateway-initiated, user_id for admin-initiated
    'statuses' => [
        'refund_status' => '✅',
        'zatca_status' => '✅', // Will be updated after ZATCA processing
        'credit_note_status' => '✅',
        'email_status' => '✅', // Will be updated after email processing
        'overall_status' => '✅' // Will be updated after ZATCA processing
    ]
];

$enrollment = \App\Models\Courses\Course\Enrolment::find($invoice->enrolment_id);

\App\Jobs\Refund\SendRefundNotification::dispatch($refundData, $invoice, $enrollment, $enrollment->course, $enrollment->user)->onQueue('admin_notifications');
