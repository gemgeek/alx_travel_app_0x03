# 🛫 ALX Travel App - Payment Integration

This project integrates the Chapa Payment Gateway into the Django backend to handle secure booking payments.

## Features

-   **Payment Initiation:** An endpoint `/api/listings/initiate-payment/<booking_id>/` that communicates with Chapa to generate a secure payment link.
-   **Payment Verification:** A callback endpoint `/api/listings/verify-payment/<tx_ref>/` that Chapa uses to confirm the payment status.
-   **Database Tracking:** A `Payment` model that logs the status (`Pending`, `Completed`, `Failed`) of each transaction.
