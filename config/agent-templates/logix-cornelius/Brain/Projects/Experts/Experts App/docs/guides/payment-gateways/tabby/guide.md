---
title: "Tabby Payment Gateway — Next.js integration guide"
date: "2026-04-11"
tags: ["project/experts", "topic/guides", "topic/payments", "topic/tabby", "tech/nextjs"]
category: "docs/experts-guides"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs/guides/guides-index|Guides index]]
- [[Projects/Experts/Experts App/docs/guides/payment-gateways/payment-gateways-index|Payment gateways index]]
- [[Projects/Experts/Experts App/docs/guides/payment-gateways/tabby/capture|Tabby capture flow]]
- [[Projects/Experts/Experts App/docs/guides/payment-gateways/tabby/full-test-checklist|Tabby QA checklist]]
- [[Projects/Experts/Experts App/docs/guides/payment-gateways/question|QUESTION — payload shapes]]

Tabby Payment Gateway Integration Guide for Next.js

Integrating Tabby Payment Gateway (Test Mode) in Next.js (Modular Setup)

1. Environment Setup and Credentials

To start, sign up on the Tabby Merchant Dashboard and obtain your API keys and Merchant Code. Tabby provides a Secret API Key (for server-side calls) and a Public API Key (for frontend snippets), with separate keys for Test and Live modes. In a Next.js app, store these in environment variables and load them based on environment:

Secret Key (Test vs. Live) – used on the server for API calls (e.g. TABBY_SECRET_KEY_TEST and TABBY_SECRET_KEY_LIVE). The Tabby API expects this in an HTTP Authorization header as Bearer <secret_key> when you make requests. Never expose this key to the client.

Public Key – used on the client for Tabby’s JavaScript widgets (e.g. NEXT_PUBLIC_TABBY_PUBLIC_KEY_TEST / NEXT_PUBLIC_TABBY_PUBLIC_KEY_LIVE). This key is safe to use in frontend code.

Merchant Code – a code identifying your store/country (e.g. "SA" for Saudi Arabia). You’ll get this from Tabby. It may differ for test vs. production if you have separate sandbox accounts; otherwise use the same. Store it as an env var (e.g. NEXT_PUBLIC_TABBY_MERCHANT_CODE).

Configure your Next.js app to load the appropriate keys per environment. For example, in development use the test keys and in production use live keys (you can use separate .env files or runtime config). On the server, you’ll reference process.env.TABBY_SECRET_KEY for API calls, and on the client use process.env.NEXT_PUBLIC_TABBY_PUBLIC_KEY and merchant code for widget initialization.

1. Modular Architecture – Client & Server Setup

Structure the Tabby integration as a module similar to your existing Stripe or “Noon” payment gateway modules. This typically means creating a Tabby service or utility with clearly separated responsibilities:

Server-side Tabby API helper: functions to interact with Tabby’s REST API (e.g. createCheckoutSession, checkEligibility, capturePayment, etc.). These will use the Secret Key and Tabby’s endpoints. For example, a createCheckoutSession(order) function will construct the JSON payload and POST to Tabby’s checkout API.

Client-side components/scripts: UI elements to display the Tabby payment option and widget. For example, a React component that conditionally renders the Tabby payment method, and initializes Tabby’s widget if needed. This will utilize the Public Key and Tabby’s provided JS library.

By adopting a modular interface (similar to your Stripe integration), the rest of your app can remain agnostic to payment provider specifics. For instance, you might implement a PaymentGateway interface with methods like initializePayment() and handleWebhook() – and your Tabby module provides the Tabby-specific implementation of those. Ensure the module reads config (keys, URLs) from env so it works in both test and live modes.

1. Pre-Scoring Check (Eligibility) Implementation

Before presenting Tabby as a payment option, perform a background pre-scoring check to verify the customer is eligible. Tabby’s API supports an “eligibility check” via the same checkout endpoint, using a minimal payload. According to Tabby, this background pre-scoring determines if the customer can use Tabby before you display it at checkout. The steps are:

Trigger the check at checkout when you have the order total and customer info. For example, when the user reaches the payment step (and has provided email and phone), call your server (Next.js API route) to perform the Tabby eligibility check.

Call Tabby’s Checkout API (POST <https://api.tabby.ai/api/v2/checkout>) with a minimal payload containing:

amount and currency of the order,

buyer info (at least email and phone),

your merchant_code.
Use the test Secret Key in the Authorization: Bearer ... header for this API call. For example:

// pages/api/tabby/check-eligibility.js
export default async function handler(req, res) {
const { amount, currency, buyerEmail, buyerPhone } = req.body;
const payload = {
payment: {
amount: amount.toFixed(2),
currency: currency,
buyer: { email: buyerEmail, phone: buyerPhone }
},
merchant_code: process.env.TABBY_MERCHANT_CODE
};
const tabbyRes = await fetch('<https://api.tabby.ai/api/v2/checkout>', {
method: 'POST',
headers: {
'Authorization': `Bearer ${process.env.TABBY_SECRET_KEY}`, // Secret Key (test)
'Content-Type': 'application/json'
},
body: JSON.stringify(payload)
});
const data = await tabbyRes.json();
res.status(200).json(data);
}

This payload is very minimal (Tabby accepts even just phone and email for pre-check). For example, Tabby’s docs show an eligibility payload like:

{
"payment": {
"amount": "340.00",
"currency": "SAR",
"buyer": {
"email": "[email protected]",
"phone": "+966500000001"
}
},
"merchant_code": "your_merchant_code"
}

Interpret the response on your server or pass it back to the client. The response will have a status field indicating eligibility. If status: "created", the customer is eligible to use Tabby; if status: "rejected", they are not. For example:

Eligible (status: "created") – proceed to show the Tabby payment option in the UI.

Rejected (status: "rejected") – do not show Tabby (or show it as disabled with a message). You can retrieve a rejection_reason explaining why (e.g. amount too high/low), which you might use for an error message if needed.

Frontend handling: Based on the response, update the UI. In a React state, you might set tabbyEligible = true/false. If eligible, render the Tabby payment radio button/option. If not, either hide the option or display a notice (Tabby’s best practice is to hide it on rejection to avoid confusion). Ensure to handle cases where the API call fails or times out – Tabby recommends a fail-safe approach: if the check cannot be completed (error), default to showing Tabby as a payment option. (This way, a temporary error in checking doesn’t wrongly exclude the payment method.) Include loading states in the UI while the check is in progress for a good user experience.

By performing this pre-scoring check, you guarantee that only customers who can actually use Tabby will see it as an option at checkout.

1. Hosted Checkout Flow Implementation (Tabby Session Creation)

The hosted checkout flow redirects the user to Tabby’s website to complete payment (OTP verification and card linking). Once the user clicks “Place Order” with Tabby selected, you need to create a Tabby payment session and send the user to the Hosted Payment Page (HPP). The implementation involves your server creating the session and your frontend handling the redirect:

Server-side (Next.js API Route) – Create Tabby Checkout Session:

Gather order details needed by Tabby. This includes: total amount, currency, customer info (name, email, phone), shipping address (if applicable), and an itemized list of products in the order. Tabby’s API allows you to send a rich payload (order items, shipping, order history, etc.), and providing more detail can improve approval rates. At minimum, you must send the amount, currency, buyer info, and merchant URLs for redirects.

Prepare the session payload. It should have a structure like:

{
"payment": {
"amount": "100.00",
"currency": "SAR",
"buyer": {
"name": "Customer Name",
"email": "[email protected]",
"phone": "+9665XXXXXXX",
"dob": "1990-01-01"
},
"shipping_address": {
"city": "Riyadh",
"address": "Some street",
"zip": "12345"
},
"order": {
"reference_id": "ORDER123",
"items": [
{
"title": "Course XYZ", "quantity": 1, "unit_price": "100.00",
"reference_id": "SKU123", "category": "Course", "description": "Online Course",
"image_url": "https://example.com/course.png"
}
]
}
// (Optional: buyer_history, order_history, etc. for better scoring)
},
"lang": "en",
"merchant_code": "YOUR_MERCHANT_CODE",
"merchant_urls": {
"success": "<https://your-site.com/checkout/success>",
"cancel": "<https://your-site.com/checkout/cancel>",
"failure": "<https://your-site.com/checkout/failure>"
}
}

This JSON will be sent to POST /api/v2/checkout. Notice the merchant_urls: these are the return URLs that Tabby will redirect the customer to after the payment attempt. You must provide URLs for success, cancel, and failure outcomes. (Make sure these routes/pages exist in your app – for example, a success page to show order confirmation, a cancel page to handle an aborted payment, etc.)

Call the Tabby API to create the session. Using your Secret Key for auth, send the payload to the Tabby Checkout API endpoint. For example:

// pages/api/tabby/create-session.js
export default async function handler(req, res) {
const order = /_get order details from req.body or DB _/;
const payload = { /_ construct as above with order data and URLs_/ };

const apiRes = await fetch('<https://api.tabby.ai/api/v2/checkout>', {
method: 'POST',
headers: {
'Authorization': `Bearer ${process.env.TABBY_SECRET_KEY}`, // Secret key
'Content-Type': 'application/json',
'X-Merchant-Code': process.env.TABBY_MERCHANT_CODE // include if provided by Tabby
},
body: JSON.stringify(payload)
});
const data = await apiRes.json();
if (data.configuration?.available_products?.installments[0]?.web_url) {
res.status(200).json({ checkoutUrl: data.configuration.available_products.installments[0].web_url });
// Also, you may store data.payment.id from response for tracking
} else {
res.status(400).json({ error: 'Unable to create Tabby session', status: data.status });
}
}

Tabby’s response will include a payment.id (the Tabby payment identifier) and a web_url for the hosted payment page. Validate that you received a web_url and that status is not "rejected" before proceeding. If web_url is missing or status is rejected, the payment cannot proceed – handle this by informing the user (e.g., show the rejection reason or ask for a different method). In most successful cases, status will be "created" and you get a valid web_url. Save the payment.id for later use (like verifying or capturing payment).

Client-side – Redirect to Tabby: 4. Once your frontend receives the checkoutUrl from the API response, redirect the customer to that URL. This is the Tabby Hosted Payment Page where the user will verify their phone (OTP) and complete the payment. You can redirect by setting window.location.href = checkoutUrl, or if using Next.js Router, router.push(checkoutUrl). (Some implementations open it in a new tab or popup – ensure popups are not blocked, or stick to same-window navigation for simplicity.)

Handle the return from Tabby. After the user completes or cancels the flow on Tabby’s side, Tabby will redirect back to one of the URLs you provided:

Success URL if the payment was authorized successfully,

Cancel URL if the user voluntarily canceled,

Failure URL if Tabby rejected the payment.
These URLs will have a payment_id query parameter appended (the Tabby payment ID). For example: <https://your-site.com/checkout/success?payment_id=abc-12345>. On your success page, you should verify the payment status on the backend (don’t trust the query param alone). We will handle that verification via webhook in the next steps. For canceled or failed, you can display an appropriate message to the user (Tabby’s docs provide suggested messages for cancellation or failure reasons).

Note: Do not mark the order as paid just because the user reached your success page. Always confirm via backend (webhook or API) that the payment is truly authorized and later captured. The success page can show a “Processing your payment…” message while your server finalizes the confirmation asynchronously.

1. Inline Checkout Widget Flow (Using Tabby Inline Card)

If you prefer not to redirect customers away from your site, Tabby offers an Inline Widget (if supported for web) via a JavaScript snippet. This widget (often called TabbyCard) embeds the Tabby checkout experience in your checkout page. The flow still involves creating a session under the hood, but the user interaction (OTP entry, card info) happens in a modal/iframe on your site.

Setup the TabbyCard snippet:

Include Tabby’s script on your checkout page. In Next.js, you can add an external script in the <Head> or use the next/script component. Add:

<script src="https://checkout.tabby.ai/tabby-card.js" async></script>

(Including it with async or defer is fine, as long as it’s loaded by the time you need to initialize the widget.) This script will provide a global constructor TabbyCard on the browser.

Add a container element in your checkout page’s JSX where the widget will render. For example: <div id="tabbyCard"></div>. You might place this in the payment section, and only show it if Tabby is selected. The Tabby docs suggest placing it under the Tabby payment option and toggling its visibility when Tabby is chosen.

Initialize the widget once the user is eligible and chooses Tabby as the payment method. After you’ve done the pre-check and the user selects “Pay with Tabby”, you’ll call the TabbyCard constructor to render the widget. For example, in a React effect hook:

import { useEffect } from 'react';
// ...
useEffect(() => {
if (selectedPaymentMethod === 'tabby' && isTabbyEligible && window.TabbyCard) {
new window.TabbyCard({
selector: '#tabbyCard', // the container div
currency: 'SAR',
price: totalAmount.toFixed(2),// order amount
lang: 'en', // or 'ar'
publicKey: process.env.NEXT_PUBLIC_TABBY_PUBLIC_KEY,
merchantCode: process.env.NEXT_PUBLIC_TABBY_MERCHANT_CODE,
// optional customization:
size: 'wide', theme: 'black', header: true
});
}
}, [selectedPaymentMethod, isTabbyEligible]);

This will mount the Tabby installment payment card UI into the #tabbyCard div. The widget will display the payment breakdown or form provided by Tabby. For instance, it may show the installment plan (“Pay in 4. No interest, no fees.”) and then guide the user through OTP verification directly on your page.

Create Tabby session when submitting. With the inline flow, you still need to create the payment session. In many cases, the Tabby widget can handle opening the payment flow, but you might need to initiate the session via your backend when the user confirms the order. There are two ways this might happen:

Option A: Widget handles it: The TabbyCard widget might internally call Tabby’s API (using the public key) to create a session and then load the payment iframe. If this is the case, your job is mostly done once the widget is initialized; you should still listen for success/failure events (likely via webhook or by Tabby redirecting within the iframe).

Option B: Your code handles it: Alternatively, you can have the “Place Order” button call your server to create the session (just like the hosted flow), but instead of redirecting the entire page, you might get a web_url and then instruct Tabby to load it in the widget/iframe. The TabbyCard snippet might provide an API for this, or simply calling new TabbyCard(...) with the parameters as above might automatically do it after pre-scoring.

In practice, Tabby’s official snippet suggests that if the pre-scoring was status: "created", calling new TabbyCard({...}) will embed the checkout card. Ensure that this is done after you have done the eligibility check (in the code example above, we only call it if isTabbyEligible is true). The TabbyCard will then handle the rest of the flow. For example, it may pop up an OTP input and payment authorization flow in that embedded frame.

Note: When using the inline widget, you still define merchant_urls (success, cancel, failure) in the session creation. Tabby will likely use those to redirect or communicate the result. If the widget is an iframe, Tabby might redirect the iframe to your success URL, which you need to detect. Often, integrations listen for a message or check the URL of the iframe, but an easier method is still using webhooks for final confirmation (since the user stays on the page).

For a robust implementation, treat the inline flow similar to hosted in terms of backend logic: create the session on order submission, and rely on webhooks to confirm payment status. The main difference is the user’s experience – staying on your site. Always test this flow thoroughly, as it might be updated by Tabby. (If Tabby’s docs or support confirm that simply using TabbyCard after an eligibility check is enough, that means the widget is doing the heavy lifting with your public key.)

If Tabby’s inline mode is not fully available or if any issue arises, you can fall back to the hosted redirect flow which is fully supported. The hosted flow is the primary approach recommended (redirecting to Tabby’s secure page), with the widget being an enhancement for user experience if supported.

1. Webhook Handling for Payment Status Updates

Whether you use hosted or inline, do not consider a payment complete until you verify it on your backend. Tabby provides webhooks to notify you of payment status changes in real-time. Implementing a webhook handler ensures you catch the scenario where a user might not return to your site (e.g. they closed the browser on the thank-you page) or simply to double-check that Tabby approved the payment.

Webhook Setup: In Tabby’s dashboard or via API, register a webhook endpoint (URL) for your application. This should be a publicly accessible URL (Tabby won’t call localhost – use a tool like Ngrok for local testing). You can register webhooks via Tabby’s API by providing your endpoint URL and a secret for signature verification. For example, Tabby’s API POST /api/v1/webhooks accepts: a JSON body with url, an optional header object containing a custom header name and a random secret value that Tabby will use to sign requests. You should also indicate if this webhook is for test mode (is_test: true) during registration in sandbox environment.

Tabby will send webhook POST requests to your URL for various events: chiefly when a payment is authorized, when it’s captured, and when it’s closed (completed). The webhook payload is JSON and includes the payment status and details (amount, payment id, etc.). For example, on authorization you’ll see "status": "authorized" (note: in webhook payload it’s lowercase).

Implement the Next.js API route (serverless function) to handle webhooks, e.g. at /api/webhooks/tabby.js:

Verify the signature: Tabby will send a custom header (whatever you defined, e.g. X-Webhook-Signature) with each request. In your handler, read the raw request body and this header. Use the same secret value you gave Tabby at registration to calculate an HMAC SHA256 hash of the request body, and compare it to the signature header. If they don’t match, respond with 401 or 400 and do nothing (the request might be forged). This ensures only genuine Tabby calls are processed. (Make sure to configure Next.js to not parse the body for this route, or use the raw body from req.socket for hashing, since the exact bytes are needed for HMAC.).

Parse the event: Once verified, parse the JSON body. Determine the event type from the data. Key fields:

status: e.g. "authorized", "rejected", "closed", etc.

id: Tabby payment ID.

There may be arrays like captures or refunds with details if those occurred.

is_test: true/false (to distinguish test mode).

order.reference_id: the order ID you sent in the session payload (if you included one).

Update order status / Capture if needed:

If status is "authorized" – This means the customer’s downpayment was authorized by Tabby (the initial payment is successful). At this point, you should mark the order as paid (or awaiting capture) in your system and then capture the payment via Tabby. Tabby requires you to send a Capture request to confirm you want to finalize/settle the payment. Capture is done by calling Tabby’s POST /v1/payments/{id}/captures endpoint with your secret key. (This step tells Tabby to disburse the funds to you; until captured, the payment might remain only authorized.) You can perform this capture immediately upon an "authorized" webhook if your business process is to complete the order instantly. In code, you might call a helper like tabby.capturePayment(paymentId). After a successful capture, Tabby’s next webhook (or a subsequent field in the same webhook) will indicate the payment is captured/closed.

If status is "closed" – The payment is fully completed and closed (Tabby uses “closed” to mean the payment was captured and finalized). You might get this after you issue the capture request. No further action required except maybe logging it.

If status is "rejected" – The payment was not approved by Tabby (e.g. risk checks failed). In this case, mark the order as failed payment, and perhaps notify the user to use another method.

If status is "expired" – The session expired because the user didn’t complete in time (by default, Tabby sessions expire after ~30 minutes). Treat it similar to cancellation – the user did not finalize payment.

Also handle "authorized" event with capture info: Tabby may send an "authorized" webhook again when capture is done, with capture details in the payload (captures array). And a final webhook when status changes to "closed". Typically, you only need to act on the first authorization (to capture) and possibly on rejection.

Respond quickly: Return a 200 OK response to Tabby immediately after processing. Any non-200 or timeout will make Tabby retry the webhook (which is good if your handling failed, but try to avoid duplicates by handling idempotently). Tabby expects a 200 to consider the webhook delivered. For example:

// pages/api/webhooks/tabby.js
import crypto from 'crypto';
export const config = { api: { bodyParser: false } }; // disable body parsing

export default async function handler(req, res) {
const signature = req.headers['x-webhook-signature']; // header name as you set
const secret = process.env.TABBY_WEBHOOK_SECRET; // the "value" you provided
// Get raw body buffer
const rawBody = await new Promise((resolve, reject) => {
let data = [];
req.on('data', chunk => data.push(chunk));
req.on('end', () => resolve(Buffer.concat(data)));
req.on('error', err => reject(err));
});
// Verify HMAC SHA256
const expectedSig = crypto.createHmac('sha256', secret).update(rawBody).digest('hex');
if (signature !== expectedSig) {
return res.status(401).send('Invalid signature');
}
// Parse the JSON
const event = JSON.parse(rawBody.toString('utf8'));
const status = event.status; // e.g. "authorized"
const paymentId = event.id;
const orderRef = event.order?.reference_id;
try {
if (status === 'authorized') {
// TODO: mark order as paid or awaiting shipment
// Capture payment:
await capturePayment(paymentId); // (implement API call to /captures)
} else if (status === 'rejected') {
// TODO: mark order payment as failed
}
// (Handle other statuses if needed)
} catch (err) {
console.error('Error handling Tabby webhook:', err);
// You might still return 200 to avoid endless retries, depending on error
}
res.status(200).send('OK'); // acknowledge receipt
}

The above is a rough example to illustrate signature verification and event handling. Use your app’s services to update order/payment records accordingly. Important: Only trust the webhook (or a direct API query to Tabby) for final payment status, not the frontend redirect alone.

Security tip: When registering the webhook, choose a strong random secret value. Tabby will use it to sign payloads (HMAC) so you can verify authenticity. Check the signature as shown to ensure the request is from Tabby and not tampered with.

Once webhooks are in place, your system will be promptly updated when the user completes the Tabby payment. This is crucial for a seamless enrollment: e.g., you can enroll the student in the course only after receiving an “authorized” event (and capturing it).

1. Conditional Rendering for Saudi Users with Valid Phone

Tabby is currently available in certain Middle East markets (KSA, UAE, Kuwait). We will enable it only for users in Saudi Arabia, and only if they provide a valid Saudi mobile number (since Tabby uses the phone for OTP). Here’s how to enforce that:

Detect Saudi users: This can be based on the user’s selected country in billing/shipping address or profile. If your app captures the user’s country, check if it’s Saudi Arabia (country code "SA" or country name). Alternatively, if your site is specifically for KSA, you may assume all users are local. If you also serve other countries, add a condition if (country === 'SA').

Validate Saudi mobile format: Saudi mobile numbers typically start with 05 (local format) or +9665 (international format). They are 9 digits (excluding country code). Examples: 0500000001 (local) is the same as +966500000001 (international). Tabby accepts various formats for phone as long as they represent a valid number. You should ensure the input is present and looks like a Saudi number. A simple check in JavaScript could be:

function isValidSaudiPhone(phone) {
// Remove non-numeric except +
const digits = phone.replace(/[^\d+]/g, '');
return (/^(\+9665\d{8})$/.test(digits)    // +966 followed by 8 digits
       || /^05\d{8}$/.test(digits)); // or 05 followed by 8 digits
}

This regex checks for either “+9665XXXXXXXX” or “05XXXXXXXX”. You might also allow “9665XXXXXXXX” (without the plus) and “5XXXXXXXX” (without leading 0) since Tabby’s API is flexible, but normalizing to one format (e.g., storing +966 format) is recommended.

Implement conditional UI logic: In your payment options component, wrap the Tabby option in a condition that the user is eligible by country and phone. For example:

const isKSA = billingAddress.country === 'SA';
const hasValidPhone = isValidSaudiPhone(buyerPhone);
// and include result from Tabby pre-scoring check:
const showTabby = isKSA && hasValidPhone && tabbyEligible;
...
{showTabby && (

  <div className="payment-option">
    <input type="radio" id="payTabby" name="paymentMethod" value="tabby" onChange={...} />
    <label htmlFor="payTabby">
      <img src="/tabby-logo.png" alt="Tabby" width={60}/> Pay in 4 with Tabby
    </label>
    {/* TabbyCard widget container */}
    {selectedMethod === 'tabby' && <div id="tabbyCard"></div>}
  </div>
)}

In this snippet, the Tabby option (radio button and label) only renders if showTabby is true. This ensures users outside KSA or without a proper KSA phone won’t even see the Tabby choice. You can decide to be more granular – for example, if the country is KSA but the phone is invalid, you might show Tabby but greyed out with a tooltip “Enter a valid Saudi phone to enable Tabby.” However, since the phone is part of checkout form, it’s reasonable to validate the phone field separately and only call the pre-check when it’s valid.

Phone number normalization: If a user enters a phone like 0501234567, consider converting it to +966501234567 before sending to Tabby, for consistency. Tabby’s API will accept 0501234567 or 5001234567 or +966501234567 all as the same number, but prefixing with +966 is a good practice.

By enforcing these conditions, you ensure that only Saudi customers with the required contact info can attempt to use Tabby. This prevents offering “Pay with Tabby” to, say, an international student or someone without a Saudi number (which would likely result in a rejection).

1. Putting It All Together and Testing

With the above components, the integration flows as:

The user enters their details (including a +966 phone) and proceeds to checkout.

Your frontend calls the pre-scoring API. If eligible (created), you show the Tabby payment option. (If not, Tabby is hidden or disabled).

If the user selects Tabby, you may display the TabbyCard widget (inline mode) after eligibility. The UI shows something like “Pay in 4 with Tabby” along with any installment breakdown provided by the widget.

When the user clicks “Place Order” with Tabby:

Hosted flow: Your code calls create-session API route, gets web_url, and redirects the user to Tabby’s hosted page. The user completes OTP and card entry there, then gets redirected back to your success/cancel URL.

Inline flow: The TabbyCard widget pops up the OTP verification and card details form right on the page (or in an embedded frame). The user completes it without leaving the site.

Your backend, meanwhile, receives a webhook when the payment is authorized. It verifies the signature and then marks the order as paid and captures the payment via Tabby API. Tabby then sends a follow-up webhook confirming the payment is closed (completed).

Finally, you can update the order status (enroll the user in the course/event) and show the confirmation page. The frontend on the success page might poll or wait for confirmation if needed, but since the webhook will likely arrive almost instantly around the redirect, you can also simply trust that if the user is on success page, it’s probably authorized and do a server check. For absolute certainty, do a quick GET to your server to fetch the updated order payment status (which your webhook handler would have set).

Test in Sandbox (Tabby Test Mode): Use Tabby’s provided test scenarios to ensure each flow works. Tabby offers specific test phone numbers and OTP codes: for example, phone +966500000001 with any email will simulate an approved payment (OTP code is always 8888 in test environment for verification). A phone ending in 002 (e.g. +966500000002) will simulate a rejected eligibility scenario. Try the following in test mode:

Successful payment: Use a “positive” test phone (e.g. +966500000001). Go through checkout choosing Tabby, enter OTP 8888 on the Tabby page, and ensure you land on the success page and your system records an authorized & captured payment. Verify in Tabby’s dashboard or via retrieve API that status is CLOSED (which means captured).

Pre-scoring rejection: Use +966500000002. The Tabby option should become unavailable after the check (either hidden or showing an error “Tabby cannot approve this purchase”).

Cancellation flow: Start a payment with +966500000001 but when on Tabby’s HPP, click “Back to store” to cancel. Tabby should redirect to your cancel URL, and your UI should show a cancellation message (like “You aborted the payment. Please retry or use another method.”). Ensure the cart is not cleared in this case so the user can attempt again.

Failure flow: You can simulate a failure by using a “negative” test flow if provided (Tabby docs mention one for failure). For instance, use the success test phone but perhaps an OTP of 0000 might trigger failure (or using a phone like ...0003 if documented). In failure, Tabby goes to failure URL and you should show a rejection message.

After testing thoroughly in Test Mode, you can switch to Live Mode by using your live secret and public keys, and updating any configuration (ensure your webhook is_test is set to false or register a new webhook URL for production if needed). Double-check that the merchant_code and other parameters are correct for live. Once live, run a small live transaction (perhaps with a low-value purchase) to verify end-to-end flow with a real OTP and card (Tabby’s production will actually charge the card).

1. References and Resources

Tabby API Reference & Integration Guide – The official Tabby documentation (docs.tabby.ai) is very useful. In particular, see the Checkout Flow section for how eligibility check vs. session creation works, and the API Reference for request/response models (e.g., Create Session payload and response).

Tabby On-site Messaging & Snippets – Tabby’s docs on promotional and checkout snippets show how to use the tabby-card.js and TabbyCard component on the frontend. This was used to integrate the inline widget.

Webhook Documentation – Refer to Tabby’s Webhook guide for details on registering webhooks and handling payloads. It outlines the expected events and the order in which you’ll receive them. Always keep your webhook endpoint secure by verifying signatures.

Tabby Testing Guidelines – Tabby provides test data and scenarios in their documentation. This is helpful for QA before going live.

Next.js and Payment Integration – While not Tabby-specific, ensure you follow Next.js best practices (using API routes for server-side calls, not exposing secrets, and handling async calls properly). The modular approach means your Tabby service could live in lib/tabby.js (for server functions) and your UI in a component, communicating via those API routes.

By following this guide, you have a fully integrated Tabby payment option in your Next.js application, enabling eligible Saudi users to enroll in courses/events with “Buy Now, Pay Later” flexibility. This integration is designed to be modular and extensible, mirroring the structure of your existing payment gateways, and can be maintained or expanded (e.g., enabling Tabby for UAE by adding the UAE merchant code and adjusting phone validation) as needed. Good luck, and happy coding with Tabby!
