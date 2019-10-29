from django.core.management.base import BaseCommand
import random
from datetime import datetime, timedelta
from django.contrib.admin.utils import flatten

from django_seed import Seed

from reservations import models as reservation_models
from users import models as user_models
from rooms import models as room_models


class Command(BaseCommand):

    CRED = "\033[91m"
    CEND = "\033[0m"

    help = "Fake reservation 생성"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default="1", type=int, help="몇개의 예약 생성할지 넘겨주는 인자"
        )

    def handle(self, *args, **options):

        number = int(options.get("number", 1))
        rooms = room_models.Room.objects.all()
        users = user_models.User.objects.all()

        seeder = Seed.seeder()
        seeder.add_entity(
            reservation_models.Reservation,
            number,
            {
                "status": lambda x: random.choice(["pending", "confirmed", "canceled"]),
                "guest": lambda x: random.choice(users),
                "room": lambda x: random.choice(rooms),
                "check_in": lambda x: datetime.now(),
                "check_out": lambda x: datetime.now()
                + timedelta(days=random.randint(3, 25)),
            },
        )

        seeder.execute()

        self.stdout.write(self.CRED + "reservation 생성!" + self.CEND)

