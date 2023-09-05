from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

SUPERUSER_USERNAME = settings.SUPERUSER_USERNAME
SUPERUSER_EMAIL = settings.SUPERUSER_EMAIL
SUPERUSER_PASSWORD = settings.SUPERUSER_PASSWORD


class Command(BaseCommand):
    def handle(self, *args, **options):
        self._create_superuser()
        self._create_coupons()

    def _create_superuser(self):
        self.stdout.write("Creating superuser...")
        if (
            SUPERUSER_USERNAME
            and not get_user_model()
            .objects.filter(username=SUPERUSER_USERNAME)
            .exists()
        ):
            u = get_user_model().objects.create_superuser(
                username=SUPERUSER_USERNAME,
                email=SUPERUSER_EMAIL,
            )
            u.set_password(SUPERUSER_PASSWORD)
            u.save()
            self.stdout.write(self.style.SUCCESS("Superuser created!"))

    def _create_coupons(self):
        self.stdout.write("Creating coupons...")
        from django.utils import timezone

        from points.models import Coupon

        today, plus_one_year = timezone.now(), timezone.now() + timezone.timedelta(
            days=365
        )

        for i in range(1, 6):
            Coupon.objects.create(
                name=f"Coupon {i}",
                value=i * 5,
                active_from=today,
                active_before=plus_one_year,
                is_multiple=not bool(i % 2),
            )
        self.stdout.write(self.style.SUCCESS("Coupons created!"))
