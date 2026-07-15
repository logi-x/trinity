<?php

$enrollment = Enrolment::find("3a20395a-5a47-4f1c-bbd2-ecb9a4a59312")->load([
    'timing' => function ($query) {
        $query->select('id', 'date', 'start_time', 'end_time');
    },
    'course' => function ($query) {
        $query->select('id', 'title');
    },
    'user' => function ($query) {
        $query->select('id', 'full_name', 'email');
    },
    'invoice'
]);
$user = User::find("2574");

$invoice = Invoice::find("302330f4-c378-4e0f-9017-692944aa7a33")->load([
    'attachment' => function ($query) {
        $query->select('id', 'name', 'path', 'type', 'extension', 'mime', 'url', 'hashed_name');
    }
]);

$admins = [];

$mergedPhoneNumbers = [];

$data = (object) [
    'enrollment' => $enrollment->load([
        'timing' => function ($query) {
            $query->select('id', 'date', 'start_time', 'end_time');
        },
        'course' => function ($query) {
            $query->select('id', 'title', 'multiple');
        },
        'user' => function ($query) {
            $query->select('id', 'full_name', 'email');
        },
    ]),
    'invoice' => $invoice->load([
        'attachment' => function ($query) {
            $query->select('id', 'name', 'path', 'type', 'extension', 'mime', 'url', 'hashed_name');
        }
    ]),
    'user' => $user,
    'statuses' => [
        'zatca_status' => '✅',
        'invoice_status' => '✅',
        'email_status' => '❌',
        'overall_status' => '❌'
    ],
    'payment_method' => 'payment_link'
];

SendEnrollmentNotifications::dispatch(
    [
        'user_id' => $user->id,
        'enrollment_id' => $enrollment->id,
        'invoice_id' => $invoice->id,
        'statuses' => $data->statuses,
        'source' => $data->payment_method
    ],
    $admins,
    $mergedPhoneNumbers

)->onQueue('client_notifications');
