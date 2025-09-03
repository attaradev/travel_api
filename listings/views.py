from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Listing, Booking, Review
from .serializers import ListingSerializer, BookingSerializer, ReviewSerializer

# If you created a Celery task, import it (optional but recommended)
try:
    from .tasks import send_booking_email
except Exception:
    send_booking_email = None


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all().order_by("-created_at")
    serializer_class = ListingSerializer

    # Simple filtering by location via ?location=Accra
    def get_queryset(self):
        qs = super().get_queryset()
        location = self.request.query_params.get("location")
        if location:
            qs = qs.filter(location__icontains=location)
        return qs


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related(
        "listing").all().order_by("-created_at")
    serializer_class = BookingSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        listing_id = self.request.query_params.get("listing")
        status_param = self.request.query_params.get("status")
        if listing_id:
            qs = qs.filter(listing_id=listing_id)
        if status_param:
            qs = qs.filter(status=status_param)
        return qs

    def perform_create(self, serializer):
        booking = serializer.save(status="pending")
        # Fire-and-forget email via Celery if available
        if send_booking_email:
            subject = "Your booking request was received"
            body = f"Thanks! We’re processing your booking #{booking.id} for {booking.listing.title}."
            send_booking_email.delay(booking.user_email, subject, body)

    @action(detail=True, methods=["post"])
    def confirm(self, request, pk=None):
        booking = self.get_object()
        if booking.status == "cancelled":
            return Response({"detail": "Cannot confirm a cancelled booking."},
                            status=status.HTTP_400_BAD_REQUEST)
        booking.status = "confirmed"
        booking.save(update_fields=["status"])
        return Response(self.get_serializer(booking).data)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if booking.status == "cancelled":
            return Response({"detail": "Already cancelled."}, status=status.HTTP_400_BAD_REQUEST)
        booking.status = "cancelled"
        booking.save(update_fields=["status"])
        return Response(self.get_serializer(booking).data)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related(
        "listing").all().order_by("-created_at")
    serializer_class = ReviewSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        listing_id = self.request.query_params.get("listing")
        if listing_id:
            qs = qs.filter(listing_id=listing_id)
        return qs
