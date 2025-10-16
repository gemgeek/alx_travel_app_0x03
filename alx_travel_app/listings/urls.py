from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BookingViewSet
from .views import initiate_payment, verify_payment

router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listing')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
    path('initiate-payment/<int:booking_id>/', initiate_payment, name='initiate-payment'),
    path('verify-payment/<str:tx_ref>/', verify_payment, name='verify-payment'),
]