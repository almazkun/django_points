from django.forms import ModelForm

from .models import Coupon


class CouponForm(ModelForm):
    class Meta:
        model = Coupon
        fields = ["value", "active_from", "active_before", "is_multiple"]
