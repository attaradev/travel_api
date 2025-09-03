from django.db import models
from django.utils import timezone


class Listing(models.Model):
    """Represents a travel listing (hotel, tour, etc.)."""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200)
    available_from = models.DateField(default=timezone.now)
    available_to = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Booking(models.Model):
    """Represents a user’s booking for a listing."""
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]

    listing = models.ForeignKey(
        Listing, related_name="bookings", on_delete=models.CASCADE)
    user_email = models.EmailField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} for {self.user_email}"


class Review(models.Model):
    """A review left by a user on a listing."""
    listing = models.ForeignKey(
        Listing, related_name="reviews", on_delete=models.CASCADE)
    user_email = models.EmailField()
    rating = models.PositiveSmallIntegerField()  # 1–5
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.rating}/5 for {self.listing.title}"
