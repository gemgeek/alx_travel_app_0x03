from celery import shared_task
from django.core.mail import send_mail
import time 

@shared_task
def send_booking_confirmation_email(booking_id, user_email, listing_name):
    """
    Sends a booking confirmation email asynchronously.

    Args:
        booking_id (int): ID of the new booking.
        user_email (str): The email address of the user.
        listing_name (str): Name of the listing that was booked.
    """

    time.sleep(5) 

    subject = f'Booking Confirmation for {listing_name}'
    message = (
        f'Dear user, \n\n'
        f'Your booking (ID: {booking_id}) for the listing "{listing_name}" '
        f'has been successfully confirmed. \n\n'
        f'Thank you for booking with us!'
    )
    from_email = 'no-reply@alxtravel.com' 
    recipient_list = [user_email]

    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )

    print(f"Successfully sent email for Booking ID: {booking_id} to {user_email}")