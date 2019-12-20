from django.core.management.base import BaseCommand

from django_seed import Seed
from users import models as user_models


class Command(BaseCommand):

    CRED = "\033[91m"
    CEND = "\033[0m"

    help = "Fake Users 생성"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default="1", type=int, help="몇개의 유저를 생성할지 넘겨주는 인자"
        )

    def handle(self, *args, **options):
        number = int(options.get("number", 1))
        seeder = Seed.seeder()
        seeder.add_entity(
            user_models.User,
            number,
            {
                "is_staff": False,
                "is_superuser": False,
                "avatar": "avatar_photos/image1.jpg",
            },
        )
        seeder.execute()

        self.stdout.write(self.CRED + "User 생성!" + self.CEND)

