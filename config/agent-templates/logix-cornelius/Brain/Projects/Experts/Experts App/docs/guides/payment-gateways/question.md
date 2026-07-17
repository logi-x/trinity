---
title: "Payment gateways — payload shapes (Stripe, Noon, Tabby)"
date: "2026-04-11"
tags: ["project/experts", "topic/guides", "topic/payments", "topic/payment-gateways"]
category: "docs/experts-guides"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs/guides/guides-index|Guides index]]
- [[Projects/Experts/Experts App/docs/guides/payment-gateways/payment-gateways-index|Payment gateways index]]
- [[Projects/Experts/Experts App/docs/guides/payment-gateways/session-resume-reinitiate|Incomplete payment — resume vs reinitiate]]
- [[Projects/Experts/Experts App/docs/guides/payment-gateways/noon/guide|Noon guide]]
- [[Projects/Experts/Experts App/docs/guides/payment-gateways/tabby/guide|Tabby guide]]

Did you take an account for different payload/response shapes, between stripe (test), Noon and Tabby?

Noon (Initiate) Payload: currently working as expected, and correctly implemented

POST <https://api-test.sa.noonpayments.com/payment/v1/order>

{
"apiOperation": "INITIATE",
"order": {
"reference": "NPAEORD0011223",
"amount": "{{Amount}}",
"currency": "{{Currency}}",
"name": "Sample order name 1",
"channel": "{{Channel}}",
"category": "{{OrderCategory}}",
"items": [
{
"name": "3-Liter Pressure Cooker",
"quantity": 1,
"unitPrice": 1086.96
}
],
"ipAddress": "172.20.74.100"
},
"billing": {
"address": {
"street": "Nasser Rashid Lootah Building, Al Maktoum Road",
"city": "Port Saeed",
"stateProvince": "Dubai",
"country": "AE",
"postalCode": "12345"
},
"contact": {
"firstName": "John",
"lastName": "Doe",
"phone": "966530828121",
"mobilePhone": "966530828121",
"email": "<john.doe@xyz.com>"
}
},
"shipping": {
"address": {
"street": "Rashid Building, Al Maktoum Road",
"city": "Riyadh",
"stateProvince": "Riyadh",
"country": "SA",
"postalCode": "12345"
},
"contact": {
"firstName": "John",
"lastName": "Doe",
"phone": "966530828121",
"mobilePhone": "966530828121",
"email": "<john.doe@xyz.com>"
}
},
"configuration": {
"tokenizeCc": "true",
"returnUrl": "{{YourReturnURL}}",
"locale": "en"
}
}

Noon (Initiate) Response: currently working as expected, and correctly implemented

{
"resultCode": 0,
"message": "Processed successfully",
"resultClass": 0,
"classDescription": "",
"actionHint": "",
"requestReference": "5fe9c227-98fc-41d4-ba15-17fadd7175fe",
"result": {
"nextActions": "ADD_PAYMENT_INFO",
"order": {
"type": "CIT",
"status": "INITIATED",
"creationTime": "2026-02-05T14:22:36.8937219Z",
"errorCode": 0,
"id": 9682293479599239,
"amount": 10.0,
"currency": "SAR",
"name": "Sample order name 1",
"reference": "NPAEORD0011223",
"category": "pay",
"channel": "Web",
"ipAddress": "172.20.74.100"
},
"configuration": {
"tokenizeCc": true,
"returnUrl": "<https://app.dev.experts.com.sa/profile>",
"locale": "en"
},
"business": {
"id": "experts_app",
"name": "Experts App Organizing Events Recorded Courses"
},
"checkoutData": {
"postUrl": "<https://checkout-stg.sa.noonpayments.com/en/default/index?info=u5EyC6%2FAvx6UJRCmOq%2BqU5X6zdKwGEIeL8nmWgS7NYVhx4FubmUruU2fw8d2GbDCug%3D%3D>",
"jsUrl": "<https://checkout-stg.sa.noonpayments.com/en/scripts/checkout?url=https%3A%2F%2Fcheckout-stg.sa.noonpayments.com%2Fen%2Fdefault%2Findex%3Finfo%3Du5EyC6%252FAvx6UJRCmOq%252BqU5X6zdKwGEIeL8nmWgS7NYVhx4FubmUruU2fw8d2GbDCug%253D%253D>"
},
"deviceFingerPrint": {
"sessionId": "9682293479599239"
},
"paymentOptions": [
{
"method": "CARD_SANDBOX",
"type": "Card",
"action": "Card",
"data": {
"supportedCardBrands": [
"VISA",
"MASTERCARD",
"MADA"
],
"encryptionSettings": {
"key": {
"type": "RSA",
"pemFormatedKey": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA375CpWqy5u3w/TXeya7l\nS+LhXkpq8x54jDfzqgIfBBDb48NBRfY28IJ3/lEJLbESPcfe1dcLPr+rGHzLuyDD\nOWph5ZYY7lodKX6QCX3EAakkha/4mJhPxqHbuyVXiM02iLBTgtA/cB7ptS2tSVF7\nVjSJ2Snm9ZN38OEiEYVzADYyRJN4bfkhYdTcW23jTna1DHg4nYGz1COUHbBPS7f/\nd0meYaRH4dUway+F0+8DbiVd8pzkfDu7o4/oQL+eH2O1gyGtxSVkVoHU5UUB2qPj\nFGN4Mea9Fw0ubJrAKdjw6G94VUV8q4ti1cwd6f5px6aDE7lLk7vctNnGOGPACmTQ\n0QIDAQAB\n-----END PUBLIC KEY-----\n"
}
},
"cvvRequired": "True"
}
},
{
"method": "ApplePay_Sandbox",
"type": "ApplePay",
"action": "ApplePay",
"data": {
"merchantIdentifier": "merchant.com.noonpayments.sa.stg-checkout",
"paymentRequest": {
"countryCode": "SA",
"currencyCode": "SAR",
"total": {
"label": "Experts App Organizing Events Recorded Courses",
"amount": 10.0
},
"supportedNetworks": [
"visa",
"masterCard",
"maestro",
"mada"
],
"merchantCapabilities": [
"supports3DS"
]
}
}
}
]
}
}

Tabby (Initiate) Payload:
POST <https://api.tabby.ai/api/v2/checkout>
{
"payment": {
"amount": "100",
"currency": "{{currency}}",
"description": "string",
"buyer": {
"phone": "+966530828121",
"email": "<ahmed.sulaimani@hotmail.com>",
"name": "string",
"dob": "2019-08-24"
},
"buyer_history": {
"registered_since": "2019-08-24T14:15:22Z",
"loyalty_level": 0,
"wishlist_count": 0,
"is_social_networks_connected": true,
"is_phone_number_verified": true,
"is_email_verified": true
},
"order": {
"tax_amount": "0.00",
"shipping_amount": "0.00",
"discount_amount": "0.00",
"updated_at": "2019-08-24T14:15:22Z",
"reference_id": "string",
"items": [
{
"title": "string",
"description": "string",
"quantity": 1,
"unit_price": "0.00",
"discount_amount": "0.00",
"reference_id": "string",
"image_url": "http://example.com",
"product_url": "http://example.com",
"gender": "Male",
"category": "string",
"color": "string",
"product_material": "string",
"size_type": "string",
"size": "string",
"brand": "string"
}
]
},
"order_history": [
{
"purchased_at": "2019-08-24T14:15:22Z",
"amount": "0.00",
"payment_method": "card",
"status": "new",
"buyer": {
"phone": "+966530828121",
"email": "ahmed.sulaimani@hotmail.com",
"name": "string",
"dob": "2019-08-24"
},
"shipping_address": {
"city": "string",
"address": "string",
"zip": "string"
},
"items": [
{
"title": "string",
"description": "string",
"quantity": 1,
"unit_price": "0.00",
"discount_amount": "0.00",
"reference_id": "string",
"image_url": "http://example.com",
"product_url": "http://example.com",
"ordered": 0,
"captured": 0,
"shipped": 0,
"refunded": 0,
"gender": "Male",
"category": "string",
"color": "string",
"product_material": "string",
"size_type": "string",
"size": "string",
"brand": "string"
}
]
}
],
"shipping_address": {
"city": "string",
"address": "string",
"zip": "string"
},
"meta": {
"order_id": "#1234",
"customer": "#customer-id"
}
},
"lang": "en",
"merchant_code": "{{merchant_code}}",
"merchant_urls": {
"success": "<https://your-store/success>",
"cancel": "<https://your-store/cancel>",
"failure": "<https://your-store/failure>"
}
}

Noon Get Order Details Request:

GET <https://api-test.sa.noonpayments.com/payment/v1/order/{{OrderId}}>

Noon Get Order Details Response:

{
"resultCode": 0,
"message": "Processed successfully",
"resultClass": 0,
"classDescription": "",
"actionHint": "",
"requestReference": "5605c2bd-b201-4247-9784-7c3262f7b24e",
"result": {
"nextActions": "REFUND",
"transactions": [
{
"type": "SALE",
"authorizationCode": "538706",
"creationTime": "2025-02-27T08:23:52.303Z",
"status": "SUCCESS",
"amountRefunded": 0,
"stan": "77344",
"rrn": "505808077344",
"id": "91664374086450001",
"amount": 2,
"currency": "SAR"
}
],
"order": {
"status": "CAPTURED",
"creationTime": "2025-02-27T08:18:57.27Z",
"totalAuthorizedAmount": 2,
"totalCapturedAmount": 2,
"totalRefundedAmount": 0,
"totalRemainingAmount": 0,
"totalReversedAmount": 0,
"totalSalesAmount": 2,
"errorCode": 0,
"id": 166437408645,
"amount": 2,
"currency": "SAR",
"name": "Enrolment in HoWA Symposium...",
"reference": "HOWA20250227111856O5HWQ",
"category": "pay",
"channel": "Web",
"ipAddress": "200.22.50.165"
},
"billing": {
"address": {
"postalCode": "00000",
"street": "Not Set",
"city": "Not Set",
"stateProvince": "Not Set",
"country": "SA"
},
"contact": {
"firstName": "Ahmed",
"lastName": "Sulaimani",
"phone": "5530828128",
"mobilePhone": "5530828128",
"email": "<ahmed.sulaimani@hotmail.com>"
}
},
"paymentDetails": {
"instrument": "CARD",
"tokenIdentifier": "b832d0a1-4700-4b52-9bd0-ea16c0d4699d",
"mode": "Card",
"integratorAccount": "CARD",
"paymentInfo": "484783xxxxxx9006",
"cardType": "DEBIT",
"payerInfo": "Ahmed Sulaimani",
"localBrand": "MADA",
"brand": "VISA",
"scheme": "VISA",
"cardAlias": "590f8413-40d4-4046-b9d3-a5f6e83d9bb8",
"expiryMonth": "3",
"expiryYear": "2029",
"isNetworkToken": "FALSE",
"cardCategory": "CLASSIC",
"cardCountry": "SA",
"cardCountryName": "Saudi Arabia",
"cardIssuerName": "AL RAJHI BANKING AND INVESTMENT CORP.",
"cardIssuerPhone": "4433 92 000 + 966 or 33 334 601 +966",
"cardIssuerWebsite": "<http://www.alrajhibank.com.sa/>"
}
}
}

Tabby (Initiate) Response:

{
"id": "dc07547e-4eba-4cd0-8daf-612b0149b9a7",
"warnings": null,
"configuration": {
"currency": "SAR",
"app_type": "",
"new_customer": false,
"available_limit": null,
"min_limit": null,
"available_products": {
"installments": [
{
"downpayment": "25.00",
"downpayment_percent": "25",
"downpayment_increased_reason": null,
"amount_to_pay": "75.00",
"old_downpayment_total": null,
"downpayment_total": "25.00",
"total_service_fee": "0.00",
"service_fee_policy": "per_installment",
"order_amount": "100.00",
"next_payment_date": "2025-03-26T00:00:00Z",
"installments": [
{
"due_date": "2025-03-26",
"old_amount": null,
"amount": "25.00",
"principal": "25.00",
"service_fee": "0.00"
},
{
"due_date": "2025-04-26",
"old_amount": null,
"amount": "25.00",
"principal": "25.00",
"service_fee": "0.00"
},
{
"due_date": "2025-05-26",
"old_amount": null,
"amount": "25.00",
"principal": "25.00",
"service_fee": "0.00"
}
],
"pay_after_delivery": false,
"pay_per_installment": "25.00",
"web_url": "https://checkout.tabby.ai/?apiKey=pk_e3256a7b-ae3c-4cac-ad76-1147b7cf5eb3&lang=ara&merchantCode=baythikmahon&product=installments&sessionId=dc07547e-4eba-4cd0-8daf-612b0149b9a7",
"qr_code": "https://api.tabby.ai/api/v2/checkout/dc07547e-4eba-4cd0-8daf-612b0149b9a7/hpp_link_qr?gis=u&product_type=installments",
"original_type": null,
"status": "unknown",
"id": 109875,
"installments_count": 3,
"installment_period": "P1M",
"service_fee": "0.00"
}
]
},
"extra_available_products": {},
"country": "SAU",
"expires_at": "2025-02-26T14:30:34Z",
"is_bank_card_required": false,
"blocked_until": null,
"hide_closing_icon": false,
"pos_provider": null,
"is_tokenized": false,
"disclaimer": "",
"help": "For questions about returns, please contact the store. Returns are processed at the same branch. For questions about your payment, get help at help.tabby.ai.",
"is_ipqs_required": false,
"monthly_billing": {
"due_day": 28
},
"products": {
"installments": {
"type": "installments",
"is_available": true,
"rejection_reason": null
}
},
"order_details_mode": "none"
},
"api_url": "<https://tabby.ai/s/55obna>",
"token": null,
"flow": "web",
"payment": {
"id": "ce61756b-1489-46fb-8351-0b2f0d5a17d8",
"created_at": "2025-02-26T14:10:34Z",
"expires_at": "2025-02-26T14:30:34Z",
"status": "CREATED",
"is_test": false,
"product": {
"type": "",
"installments_count": 0,
"installment_period": "P0D"
},
"amount": "100",
"currency": "SAR",
"description": "string",
"buyer": {
"id": null,
"name": "string",
"email": "<ahmed.sulaimani@hotmail.com>",
"phone": "+966530828121",
"dob": "2019-08-24"
},
"shipping_address": {
"city": "string",
"address": "string",
"zip": "string"
},
"order": {
"reference_id": "string",
"updated_at": "2019-08-24T14:15:22Z",
"tax_amount": "0",
"shipping_amount": "0",
"discount_amount": "0",
"items": [
{
"reference_id": "string",
"title": "string",
"description": "string",
"quantity": 1,
"unit_price": "0",
"image_url": "http://example.com",
"product_url": "http://example.com",
"gender": "Male",
"category": "string",
"color": "string",
"product_material": "string",
"size_type": "string",
"size": "string",
"brand": "string",
"is_refundable": null
}
]
},
"captures": [],
"refunds": [],
"buyer_history": {
"registered_since": "2019-08-24T14:15:22Z",
"loyalty_level": 0,
"wishlist_count": 0,
"is_social_networks_connected": true,
"is_phone_number_verified": true,
"is_email_verified": true
},
"order_history": [
{
"purchased_at": "2019-08-24T14:15:22Z",
"amount": "0",
"payment_method": "card",
"status": "new",
"buyer": {
"id": null,
"name": "string",
"email": "ahmed.sulaimani@hotmail.com",
"phone": "+966530828121",
"dob": "2019-08-24"
},
"shipping_address": {
"city": "string",
"address": "string",
"zip": "string"
},
"items": [
{
"reference_id": "string",
"title": "string",
"description": "string",
"quantity": 1,
"unit_price": "0",
"image_url": "http://example.com",
"product_url": "http://example.com",
"gender": "Male",
"category": "string",
"color": "string",
"product_material": "string",
"size_type": "string",
"size": "string",
"brand": "string",
"is_refundable": null,
"ordered": 0,
"captured": 0,
"shipped": 0,
"refunded": 0
}
]
}
],
"meta": {
"customer": "#customer-id",
"order_id": "#1234"
},
"cancelable": false
},
"status": "created",
"customer": {
"id": null,
"phone": "+966530828121",
"email": "<ahmed.sulaimani@hotmail.com>",
"is_identity_auth_skipped": null
},
"juicyscore": {
"session_id": "",
"referrer": "",
"time_zone": "",
"useragent": ""
},
"merchant_urls": {
"success": "<https://your-store/success>",
"cancel": "<https://your-store/cancel>",
"failure": "<https://your-store/failure>"
},
"product_type": null,
"lang": "ara",
"locale": "ar-SA",
"seon_session_id": null,
"merchant": {
"name": "اكاديمية بيت الحكمةonline",
"address": "none, none",
"logo": ""
},
"merchant_code": "",
"terms_accepted": false,
"promo": null,
"installment_plan": {
"installments": null
},
"is_ipqs_requested": false
}

Tabby Get Order Details Request:

GET <https://api.tabby.ai/api/v2/payments/{{payment_id}}>

Tabby Get Order Details Response:

{
"id": "dad4fb42-6948-44eb-b28d-af927d58b680",
"created_at": "2025-02-26T01:02:17Z",
"expires_at": "2026-02-26T01:03:27Z",
"status": "CLOSED",
"is_test": false,
"product": {
"type": "installments",
"installments_count": 3,
"installment_period": "P1M"
},
"amount": "500",
"currency": "SAR",
"description": "string",
"buyer": {
"id": null,
"name": "rahma alhazmi",
"email": "<dr.rahmaalhazmiortho@gmail.com>",
"phone": "+966599576783",
"dob": "2025-02-12"
},
"shipping_address": {
"city": "",
"address": "",
"zip": ""
},
"order": {
"reference_id": "3280",
"updated_at": "2025-02-26T01:02:17Z",
"tax_amount": "0",
"shipping_amount": "0",
"discount_amount": "0",
"items": [
{
"reference_id": "117",
"title": "(Online) HoWA Ramadan Live 2",
"description": "(Online) HoWA Ramadan Live 2",
"quantity": 1,
"unit_price": "500",
"image_url": "https://howa.edu.sa/storage/courses/list/117/1LfSFlUqgAXYRdepA88l1gCFXnuqrEVrcxzIDO4m.jpg",
"product_url": "https://howa.edu.sa/storage/courses/list/117/1LfSFlUqgAXYRdepA88l1gCFXnuqrEVrcxzIDO4m.jpg",
"gender": "Male",
"category": "string",
"color": "string",
"product_material": "string",
"size_type": "string",
"size": "string",
"brand": "string",
"is_refundable": null
}
]
},
"captures": [
{
"id": "f1433d85-23e6-46be-a18e-84734545d378",
"created_at": "2025-02-26T01:03:28Z",
"amount": "500",
"tax_amount": "0",
"shipping_amount": "0",
"discount_amount": "0",
"items": [],
"reference_id": ""
}
],
"refunds": [],
"buyer_history": {
"registered_since": "0001-01-01T00:00:00Z",
"loyalty_level": 0,
"wishlist_count": 0,
"is_social_networks_connected": null,
"is_phone_number_verified": null,
"is_email_verified": null
},
"order_history": [],
"meta": {
"customer": "4027",
"order_id": "3280"
},
"cancelable": false
}
