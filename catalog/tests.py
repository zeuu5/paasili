from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import DealerRegistration, Product


class ProductViewsTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Signature Bb Trumpet",
            model_number="P-450",
            family="trumpet",
            short_description="A professional brass trumpet.",
            mrp=Decimal("125000.00"),
            is_featured=True,
        )

    def test_catalogue_shows_published_product_and_mrp(self):
        response = self.client.get(reverse("catalog:product_list"))
        self.assertContains(response, self.product.name)
        self.assertContains(response, "125000.00")

    def test_product_detail_is_public(self):
        response = self.client.get(reverse("catalog:product_detail", args=[self.product.slug]))
        self.assertContains(response, self.product.model_number)


class DealerRegistrationTests(TestCase):
    def test_valid_registration_is_saved(self):
        response = self.client.post(reverse("catalog:dealer_registration"), {
            "business_name": "Brass House",
            "contact_name": "Asha Kumar",
            "email": "asha@example.com",
            "phone": "+91 9876543210",
            "city": "Mumbai",
            "gst_number": "27ABCDE1234F1Z5",
        })
        self.assertRedirects(response, reverse("catalog:dealer_registration"))
        self.assertEqual(DealerRegistration.objects.count(), 1)
        self.assertEqual(DealerRegistration.objects.get().business_name, "Brass House")

    def test_invalid_gst_number_is_rejected(self):
        response = self.client.post(reverse("catalog:dealer_registration"), {
            "business_name": "Brass House",
            "contact_name": "Asha Kumar",
            "email": "asha@example.com",
            "phone": "+91 9876543210",
            "city": "Mumbai",
            "gst_number": "not-a-gst",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a valid 15-character GST number.")
        self.assertEqual(DealerRegistration.objects.count(), 0)
