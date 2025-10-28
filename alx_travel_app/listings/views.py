import os
import requests
import json
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Payment, Booking 
from rest_framework import viewsets
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer
from .tasks import send_booking_confirmation_email

@csrf_exempt
def initiate_payment(request, booking_id):
    if request.method == 'POST':
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return JsonResponse({'error': 'Booking not found'}, status=404)

        # Generate a unique transaction reference
        tx_ref = f"chapa-tx-{booking_id}-{uuid.uuid4()}"

        # Chapa API details
        chapa_url = "https://api.chapa.co/v1/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {os.environ.get('CHAPA_SECRET_KEY')}",
            "Content-Type": "application/json"
        }
        payload = {
            "amount": str(booking.total_price), 
            "currency": "ETB",
            "email": booking.user.email, 
            "first_name": booking.user.first_name,
            "last_name": booking.user.last_name,
            "tx_ref": tx_ref,
            "callback_url": f"http://localhost:8000/api/listings/verify-payment/{tx_ref}/", 
            "return_url": "http://localhost:3000/booking-success/", 
            "customization[title]": "Travel App Booking",
            "customization[description]": f"Payment for booking of {booking.listing.title}"
        }

        try:
            response = requests.post(chapa_url, headers=headers, data=json.dumps(payload))
            response_data = response.json()

            if response_data.get("status") == "success":
                # Create a payment record
                Payment.objects.create(
                    booking=booking,
                    amount=booking.total_price,
                    transaction_ref=tx_ref,
                    status='Pending'
                )
                return JsonResponse(response_data)
            else:
                return JsonResponse({'error': 'Failed to initiate payment', 'details': response_data}, status=400)

        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def verify_payment(request, tx_ref):
    chapa_url = f"https://api.chapa.co/v1/transaction/verify/{tx_ref}"
    headers = {
        "Authorization": f"Bearer {os.environ.get('CHAPA_SECRET_KEY')}"
    }

    try:
        response = requests.get(chapa_url, headers=headers)
        response_data = response.json()

        if response_data.get("status") == "success":
            try:
                payment = Payment.objects.get(transaction_ref=tx_ref)
                payment.status = 'Completed'
                payment.save()

                return JsonResponse({'status': 'Payment verified successfully'})
            except Payment.DoesNotExist:
                return JsonResponse({'error': 'Payment record not found'}, status=404)
        else:
            # Update payment status to Failed
            Payment.objects.filter(transaction_ref=tx_ref).update(status='Failed')
            return JsonResponse({'error': 'Payment verification failed', 'details': response_data}, status=400)

    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)

def perform_create(self, serializer):
    booking_instance = serializer.save()

    booking_id = booking_instance.id
    user_email = self.request.user.email  
    listing_name = booking_instance.listing.name 

    send_booking_confirmation_email.delay(
        booking_id, 
        user_email, 
        listing_name
    )        
