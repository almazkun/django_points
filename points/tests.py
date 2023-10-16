from django.test import TestCase
from django.urls import reverse

from points.models import Coupon


# Create your tests here.
class TestViews(TestCase):
    def setUp(self):
        self.c = self.client
        self._create_coupon = lambda kwargs: Coupon.objects.create(**kwargs)

    def test_redeem_view(self):
        data = {"user_id": "user123"}
        coupon = self._create_coupon(
            {
                "name": "single_valid",
                "value": 5,
                "active_from": "2023-01-01T00:00:00+06:00",
                "active_before": "2023-12-31T23:59:59+06:00",
                "is_multiple": False,
            }
        )
        endpoint = reverse("coupon_redeem", kwargs={"code": coupon.code})
        response = self.c.put(endpoint, data, content_type="application/json")
        coupon.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"code": coupon.code, "value": coupon.value})
        self.assertEqual(coupon.used_by.count(), 1)
        self.assertEqual(coupon.used_by.first().user_id, "user123")
        self.assertEqual(coupon.is_used, True)

        response = self.c.put(endpoint, data, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": ["Coupon is already used."]})

        #
        coupon = self._create_coupon(
            {
                "name": "multiple_valid",
                "value": 5,
                "active_from": "2023-01-01T00:00:00+06:00",
                "active_before": "2023-12-31T23:59:59+06:00",
                "is_multiple": True,
            }
        )
        endpoint = reverse("coupon_redeem", kwargs={"code": coupon.code})
        response = self.c.put(endpoint, data, content_type="application/json")
        coupon.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"code": coupon.code, "value": coupon.value})
        self.assertEqual(coupon.used_by.count(), 1)
        self.assertEqual(coupon.used_by.first().user_id, "user123")
        self.assertEqual(coupon.is_used, True)

        response = self.c.put(endpoint, data, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"detail": ["Coupon is already redeemed by user123."]}
        )

        response = self.c.put(
            endpoint, {"user_id": "user456"}, content_type="application/json"
        )
        coupon.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"code": coupon.code, "value": coupon.value})
        self.assertEqual(coupon.used_by.count(), 2)

        #
        coupon = self._create_coupon(
            {
                "name": "expired",
                "value": 5,
                "active_from": "1000-01-01T00:00:00+06:00",
                "active_before": "1000-12-31T23:59:59+06:00",
                "is_multiple": False,
            }
        )
        endpoint = reverse("coupon_redeem", kwargs={"code": coupon.code})
        response = self.c.put(endpoint, data, content_type="application/json")
        coupon.refresh_from_db()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": ["Coupon is expired."]})
        self.assertEqual(coupon.used_by.count(), 0)
        self.assertEqual(coupon.is_used, False)

        #
        coupon = self._create_coupon(
            {
                "name": "not_active",
                "value": 5,
                "active_from": "3000-01-01T00:00:00+06:00",
                "active_before": "3000-12-31T23:59:59+06:00",
                "is_multiple": False,
            }
        )
        endpoint = reverse("coupon_redeem", kwargs={"code": coupon.code})
        response = self.c.put(endpoint, data, content_type="application/json")
        coupon.refresh_from_db()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": ["Coupon is not active yet."]})
        self.assertEqual(coupon.used_by.count(), 0)
        self.assertEqual(coupon.is_used, False)

        #
        endpoint = reverse("coupon_redeem", kwargs={"code": "not_exists"})
        response = self.c.put(endpoint, data, content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Not found."})
