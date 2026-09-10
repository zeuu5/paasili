from django.db import models
from django.utils.text import slugify


class InstrumentFamily(models.TextChoices):
    TRUMPET = "trumpet", "Trumpet"
    EUPHONIUM = "euphonium", "Euphonium"
    TROMBONE = "trombone", "Trombone"
    CORNET = "cornet", "Cornet"
    TUBA = "tuba", "Tuba"
    FLUGELHORN = "flugelhorn", "Flugelhorn"
    SAXOPHONE = "saxophone", "Saxophone"
    SIDE_DRUM = "side-drum", "Side drum"
    BASS_DRUM = "bass-drum", "Bass drum"
    OTHER = "other", "Other"


class Product(models.Model):
    """A brass instrument displayed in the public catalogue."""

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    model_number = models.CharField(max_length=50, blank=True)
    family = models.CharField(max_length=20, choices=InstrumentFamily.choices)
    short_description = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    mrp = models.DecimalField("MRP", max_digits=10, decimal_places=2)
    main_image = models.ImageField(upload_to="products/", blank=True, null=True)
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = f"{self.model_number}-{self.name}" if self.model_number else self.name
            self.slug = slugify(base)
        super().save(*args, **kwargs)


class DealerRegistration(models.Model):
    """A prospective dealer's application submitted from the public website."""

    business_name = models.CharField(max_length=150)
    contact_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=40)
    city = models.CharField(max_length=100)
    gst_number = models.CharField("GST number", max_length=15, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    is_contacted = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.business_name} — {self.city}"


class AuthorizedDealer(models.Model):
    """A dealer shown in the public city finder."""

    business_name = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=40, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["city", "order", "business_name"]

    def __str__(self):
        return f"{self.business_name} — {self.city}"


class SiteContact(models.Model):
    """Editable company contact and social profile details."""

    address = models.TextField(default="12 Music Market, Andheri West\nMumbai, Maharashtra 400001, India")
    email = models.EmailField(default="hello@paasili.in")
    facebook_url = models.URLField(default="https://www.facebook.com/paasili")
    instagram_url = models.URLField(default="https://www.instagram.com/paasili")

    class Meta:
        verbose_name = "Site contact"
        verbose_name_plural = "Site contact"

    def __str__(self):
        return "Paasili contact details"
