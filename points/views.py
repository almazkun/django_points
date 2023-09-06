from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django_tables2 import SingleTableView
from rest_framework.generics import UpdateAPIView

from points.forms import CouponForm
from points.models import Coupon
from points.serializers import CouponSerializer
from points.tables import CouponTable


class CouponListView(SingleTableView):
    model = Coupon
    template_name = "points/coupon_list.html"
    table_class = CouponTable


class CouponCreateView(CreateView):
    model = Coupon
    form_class = CouponForm
    template_name = "points/coupon_create.html"
    success_url = reverse_lazy("coupon_list")


class CouponRedeemView(UpdateAPIView):
    """Redeem a coupon

    This view is used to redeem a coupon. It accepts a user_id and returns the coupon.value.

    Single Coupon (Coupon.is_multiple == False) can only be redeemed once per user.
    Multiple Coupon (Coupon.is_multiple == True) can be redeemed multiple times by the different users.
    Coupon can only be redeemed if it is active and not expired.
    """

    serializer_class = CouponSerializer
    queryset = Coupon.objects.all()
    lookup_field = "code"
    http_method_names = ["put"]

    @transaction.atomic
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
