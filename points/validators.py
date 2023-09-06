from django.utils import timezone
from rest_framework.serializers import ValidationError

from points.models import Coupon


def coupon_is_used(coupon: Coupon) -> None:
    # Not multiple coupons can be used only once
    if not coupon.is_multiple and coupon.is_used:
        raise ValidationError({"detail": ["Coupon is already used."]})


def coupon_is_expired(coupon: Coupon) -> None:
    # Check if coupon is active and not expired
    now = timezone.now()
    if coupon.active_from > now:
        raise ValidationError({"detail": ["Coupon is not active yet."]})
    if coupon.active_before < now:
        raise ValidationError({"detail": ["Coupon is expired."]})


def coupon_is_already_used(coupon: Coupon, user_id: str) -> None:
    # Coupons can be used only once per user
    if user_id in coupon.used_by.values_list("user_id", flat=True):
        raise ValidationError({"detail": [f"Coupon is already redeemed by {user_id}."]})
