import uuid

from django.db import models


def generate_code():
    while True:
        candidate = "SHI" + uuid.uuid4().hex[:7].upper()
        if not Coupon.objects.filter(code=candidate).exists():
            return candidate


# Create your models here.
class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Coupon(BaseModel):
    name = models.CharField("Name", max_length=255, help_text="Coupon name")
    value = models.PositiveSmallIntegerField("Value", help_text="Coupon value")

    active_from = models.DateTimeField("Active from", help_text="2023-01-01 00:00:00")
    active_before = models.DateTimeField(
        "Active before", help_text="2023-12-31 23:59:59"
    )

    is_multiple = models.BooleanField(
        "Multiple", default=False, help_text="Multiple use"
    )
    is_used = models.BooleanField("Used", default=False)

    code = models.CharField(
        "Code", max_length=10, unique=True, default=generate_code, editable=False
    )
