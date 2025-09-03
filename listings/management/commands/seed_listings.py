from django.core.management.base import BaseCommand
from django.utils import timezone
from listings.models import Listing, Booking, Review
from random import randint, choice
from datetime import timedelta


class Command(BaseCommand):
    help = "Seed the database with sample listings, bookings, and reviews"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Seeding data..."))

        # Clear existing
        Review.objects.all().delete()
        Booking.objects.all().delete()
        Listing.objects.all().delete()

        # Seed Listings
        listings = []
        for i in range(5):
            listing = Listing.objects.create(
                title=f"Sample Listing {i+1}",
                description="This is a sample travel listing.",
                price=randint(50, 500),
                location=choice(["Accra", "Kumasi", "Takoradi", "Cape Coast"]),
                available_from=timezone.now().date(),
                available_to=timezone.now().date() + timedelta(days=90),
            )
            listings.append(listing)

        # Seed Bookings
        bookings = []
        for i in range(10):
            listing = choice(listings)
            start = timezone.now().date() + timedelta(days=randint(1, 30))
            end = start + timedelta(days=randint(1, 7))
            booking = Booking.objects.create(
                listing=listing,
                user_email=f"user{i+1}@example.com",
                start_date=start,
                end_date=end,
                status=choice(["pending", "confirmed", "cancelled"]),
            )
            bookings.append(booking)

        # Seed Reviews
        for i in range(15):
            listing = choice(listings)
            Review.objects.create(
                listing=listing,
                user_email=f"reviewer{i+1}@example.com",
                rating=randint(1, 5),
                comment="Nice place to stay!" if randint(0, 1) else "",
            )

        self.stdout.write(self.style.SUCCESS(
            "✅ Database seeded successfully!"))
