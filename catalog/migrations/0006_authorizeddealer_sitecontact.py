from django.db import migrations, models


def create_sample_contact_and_dealers(apps, schema_editor):
    SiteContact = apps.get_model("catalog", "SiteContact")
    AuthorizedDealer = apps.get_model("catalog", "AuthorizedDealer")
    SiteContact.objects.get_or_create(pk=1)
    AuthorizedDealer.objects.bulk_create([
        AuthorizedDealer(business_name="Harmony Music House", city="Mumbai", address="12 Music Market, Andheri West", phone="+91 98765 43210"),
        AuthorizedDealer(business_name="Capital Instrument Co.", city="Delhi", address="44 Connaught Place", phone="+91 98765 43211"),
        AuthorizedDealer(business_name="South Sound Studio", city="Bengaluru", address="8 Brigade Road", phone="+91 98765 43212"),
    ])


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0005_use_original_product_images"),
    ]

    operations = [
        migrations.CreateModel(
            name="AuthorizedDealer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("business_name", models.CharField(max_length=150)),
                ("city", models.CharField(max_length=100)),
                ("address", models.TextField()),
                ("phone", models.CharField(blank=True, max_length=40)),
                ("is_active", models.BooleanField(default=True)),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["city", "order", "business_name"]},
        ),
        migrations.CreateModel(
            name="SiteContact",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("address", models.TextField(default="12 Music Market, Andheri West\nMumbai, Maharashtra 400001, India")),
                ("email", models.EmailField(default="hello@paasili.in", max_length=254)),
                ("facebook_url", models.URLField(default="https://www.facebook.com/paasili")),
                ("instagram_url", models.URLField(default="https://www.instagram.com/paasili")),
            ],
            options={"verbose_name": "Site contact", "verbose_name_plural": "Site contact"},
        ),
        migrations.RunPython(create_sample_contact_and_dealers, migrations.RunPython.noop),
    ]
