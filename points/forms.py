from django.forms import ModelForm

from .models import Coupon


class CouponForm(ModelForm):
    class Meta:
        model = Coupon
        fields = ["name", "value", "active_from", "active_before", "is_multiple"]
