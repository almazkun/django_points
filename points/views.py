from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django_tables2 import SingleTableView

from .forms import CouponForm
from .models import Coupon
from .tables import CouponTable


class CouponListView(SingleTableView):
    model = Coupon
    template_name = "points/coupon_list.html"
    table_class = CouponTable


class CouponCreateView(CreateView):
    model = Coupon
    form_class = CouponForm
    template_name = "points/coupon_create.html"
    success_url = reverse_lazy("coupon_list")
