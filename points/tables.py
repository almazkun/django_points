import django_tables2 as tables

from .models import Coupon


class CouponTable(tables.Table):
    class Meta:
        model = Coupon
        template_name = "django_tables2/bootstrap5.html"
        attrs = {"class": "table table-striped table-bordered table-hover"}
        fields = [
            "code",
            "value",
            "active_from",
            "active_before",
            "is_multiple",
            "is_used",
        ]
