from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Item, ItemVariation, OrganisationProfile, Reservation


class AccountAdmin(UserAdmin):
    list_display = (
        "organisation_name",
        "username",
        "contact_person",
        "address",
        "phone",
        "notes",
    )
    readonly_fields = ("username",)
    list_display_links = ("username", "organisation_name")

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class VariationAdmin(admin.ModelAdmin):
    list_display = (
        "item",
        "size",
        "fabric_design",
        "on_stock",
        "reserved_quantity",
        "saldo",
    )
    list_filter = ("size",)


class ReservationAdmin(admin.ModelAdmin):
    list_display = ("reservation_number", "status", "created_at")


# Register your models here.

admin.site.register(Item)
admin.site.register(ItemVariation, VariationAdmin)
admin.site.register(OrganisationProfile, AccountAdmin)
admin.site.register(Reservation, ReservationAdmin)
