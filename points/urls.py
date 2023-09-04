from django.urls import path

from .views import CouponCreateView, CouponListView

urlpatterns = [
    path("", CouponListView.as_view(), name="coupon_list"),
    path("create/", CouponCreateView.as_view(), name="coupon_create"),
]
