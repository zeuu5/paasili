from django.contrib import admin
from django.utils.html import format_html

from .models import AuthorizedDealer, DealerRegistration, Product, SiteContact


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("thumbnail", "name", "model_number", "family", "mrp", "is_published", "is_featured", "order")
    list_filter = ("family", "is_published", "is_featured")
    search_fields = ("name", "model_number", "short_description")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("mrp", "is_published", "is_featured", "order")
    list_display_links = ("name",)
    ordering = ("order", "name")
    fieldsets = (
        ("Instrument identity", {"fields": ("name", "model_number", "family", "slug")}),
        ("Catalogue content", {"fields": ("short_description", "description", "main_image", "mrp")}),
        ("Visibility", {"fields": ("is_published", "is_featured", "order")}),
    )

    @admin.display(description="Image")
    def thumbnail(self, product):
        if not product.main_image:
            return "-"
        return format_html(
            '<img src="{}" width="52" height="52" style="object-fit:contain;background:#f1eee7;padding:4px">',
            product.main_image.url,
        )


@admin.register(DealerRegistration)
class DealerRegistrationAdmin(admin.ModelAdmin):
    list_display = ("business_name", "contact_name", "city", "gst_number", "email", "created_at", "is_contacted")
    list_filter = ("is_contacted", "created_at")
    search_fields = ("business_name", "contact_name", "gst_number", "email", "city")
    readonly_fields = ("created_at",)
    list_editable = ("is_contacted",)
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    actions = ("mark_contacted", "mark_not_contacted")
    fieldsets = (
        ("Dealer contact", {"fields": ("business_name", "contact_name", "city")}),
        ("Business details", {"fields": ("gst_number", "phone", "email")}),
        ("Follow-up", {"fields": ("is_contacted", "created_at")}),
    )

    @admin.action(description="Mark selected applications as contacted")
    def mark_contacted(self, request, queryset):
        queryset.update(is_contacted=True)

    @admin.action(description="Mark selected applications as not contacted")
    def mark_not_contacted(self, request, queryset):
        queryset.update(is_contacted=False)


@admin.register(AuthorizedDealer)
class AuthorizedDealerAdmin(admin.ModelAdmin):
    list_display = ("business_name", "city", "phone", "is_active", "order")
    list_filter = ("is_active", "city")
    search_fields = ("business_name", "city", "address", "phone")
    list_editable = ("is_active", "order")
    ordering = ("city", "order", "business_name")


@admin.register(SiteContact)
class SiteContactAdmin(admin.ModelAdmin):
    list_display = ("__str__", "email")

    def has_add_permission(self, request):
        return not SiteContact.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.site_header = "Paasili Instruments administration"
admin.site.site_title = "Paasili admin"
admin.site.index_title = "Manage your instrument catalogue and dealer network"
