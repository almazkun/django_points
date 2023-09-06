from django.urls import path

from .views import CouponCreateView, CouponListView, CouponRedeemView

urlpatterns = [
    path("", CouponListView.as_view(), name="coupon_list"),
    path("create/", CouponCreateView.as_view(), name="coupon_create"),
    path("redeem/<str:code>/", CouponRedeemView.as_view(), name="coupon_redeem"),
]
