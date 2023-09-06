from rest_framework import serializers

from points import validators
from points.models import Coupon


class CouponSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(required=True)

    class Meta:
        model = Coupon
        fields = ["user_id"]

    def validate(self, data):
        data = super().validate(data)
        validators.coupon_is_used(self.instance)
        validators.coupon_is_expired(self.instance)
        validators.coupon_is_already_used(self.instance, data["user_id"])
        return data

    def update(self, instance, validated_data):
        user_id = validated_data["user_id"]
        instance.used_by.create(user_id=user_id)
        instance.is_used = True
        instance.save(update_fields=["is_used"])
        return instance

    def to_representation(self, instance):
        return {
            "code": instance.code,
            "value": instance.value,
        }
