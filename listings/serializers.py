from rest_framework import serializers
from .models import Listing, Booking, Review
from django.utils import timezone
from django.db.models import Q


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = [
            "id", "title", "description", "price", "location",
            "available_from", "available_to",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "id", "listing", "user_email",
            "start_date", "end_date", "status",
            "created_at",
        ]
        read_only_fields = ["id", "status", "created_at"]

    def validate(self, attrs):
        listing = attrs.get("listing") or getattr(
            self.instance, "listing", None)
        start = attrs.get("start_date") or getattr(
            self.instance, "start_date", None)
        end = attrs.get("end_date") or getattr(self.instance, "end_date", None)

        if not all([listing, start, end]):
            return attrs

        if end < start:
            raise serializers.ValidationError(
                "end_date must be on or after start_date.")

        # Listing availability window
        if start < listing.available_from:
            raise serializers.ValidationError(
                "Start date is before listing availability.")

        if listing.available_to and end > listing.available_to:
            raise serializers.ValidationError(
                "End date is after listing availability.")

        # Overlap check (exclude cancelled & current instance)
        qs = Booking.objects.filter(
            listing=listing,
            status__in=["pending", "confirmed"],
        ).filter(
            Q(start_date__lte=end) & Q(end_date__gte=start)
        )
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError(
                "Dates overlap with an existing booking.")

        # Optional: prevent full past bookings
        if end < timezone.now().date():
            raise serializers.ValidationError(
                "Cannot create bookings entirely in the past.")

        return attrs


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "id", "listing", "user_email", "rating", "comment", "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError(
                "Rating must be between 1 and 5.")
        return value
