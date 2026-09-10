from django.db import migrations


ORIGINAL_IMAGES = {
    "trumpet": "products/trumpet.jpeg",
    "euphonium": "products/euphonium.jpeg",
    "side-drum": "products/side drum.jpg",
    "bass-drum": "products/bass drum.jpeg",
    "saxophone": "products/saxophone.jpeg",
}


def use_original_images(apps, schema_editor):
    Product = apps.get_model("catalog", "Product")
    for family, image_path in ORIGINAL_IMAGES.items():
        Product.objects.filter(family=family).update(main_image=image_path)


def restore_sample_images(apps, schema_editor):
    Product = apps.get_model("catalog", "Product")
    sample_images = {
        "trumpet": "products/sample-trumpet.png",
        "euphonium": "products/sample-euphonium.jpg",
        "side-drum": "products/sample-side-drum.png",
        "bass-drum": "products/sample-bass-drum.png",
        "saxophone": "products/sample-saxophone.svg",
    }
    for family, image_path in sample_images.items():
        Product.objects.filter(family=family).update(main_image=image_path)


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0004_remove_dealerregistration_country_and_more"),
    ]

    operations = [
        migrations.RunPython(use_original_images, restore_sample_images),
    ]
