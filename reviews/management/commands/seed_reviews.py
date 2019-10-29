from django.core.management.base import BaseCommand
import random

from django_seed import Seed

from reviews import models as review_models
from users import models as user_models
from rooms import models as room_models


class Command(BaseCommand):

    CRED = "\033[91m"
    CEND = "\033[0m"

    help = "Fake Review 생성"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default="1", type=int, help="몇개의 리뷰를 생성할지 넘겨주는 인자"
        )

    def handle(self, *args, **options):

        number = int(options.get("number", 1))
        rooms = room_models.Room.objects.all()
        users = user_models.User.objects.all()

        seeder = Seed.seeder()
        seeder.add_entity(
            review_models.Review,
            number,
            {
                "accuracy": lambda x: random.randint(0, 6),
                "location": lambda x: random.randint(0, 6),
                "communication": lambda x: random.randint(0, 6),
                "check_in": lambda x: random.randint(0, 6),
                "cleanliness": lambda x: random.randint(0, 6),
                "value": lambda x: random.randint(0, 6),
                "user": lambda x: random.choice(users),
                "room": lambda x: random.choice(rooms),
            },
        )
        seeder.execute()

        self.stdout.write(self.CRED + "Review 생성!" + self.CEND)

