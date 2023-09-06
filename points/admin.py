from django.contrib import admin

from .models import Coupon, UserCoupon


class CouponAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "value",
        "active_from",
        "active_before",
        "is_multiple",
        "is_used",
    )
    list_filter = (
        "name",
        "value",
        "active_from",
        "active_before",
        "is_multiple",
        "is_used",
    )
    search_fields = (
        "name",
        "code",
        "value",
        "active_from",
        "active_before",
        "is_multiple",
        "is_used",
    )
    ordering = ("active_from", "active_before")


class UserCouponAdmin(admin.ModelAdmin):
    list_display = ("user_id", "coupon")
    list_filter = ("user_id", "coupon")
    search_fields = ("user_id", "coupon")


admin.site.register(Coupon, CouponAdmin)
admin.site.register(UserCoupon, UserCouponAdmin)
