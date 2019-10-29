from django.core.management.base import BaseCommand
import random
from django.contrib.admin.utils import flatten

from django_seed import Seed

from lists import models as list_models
from users import models as user_models
from rooms import models as room_models


class Command(BaseCommand):

    CRED = "\033[91m"
    CEND = "\033[0m"

    help = "Fake list 생성"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default="1", type=int, help="몇개의 리스트를 생성할지 넘겨주는 인자"
        )

    def handle(self, *args, **options):

        number = int(options.get("number", 1))
        rooms = room_models.Room.objects.all()
        users = user_models.User.objects.all()

        seeder = Seed.seeder()
        seeder.add_entity(
            list_models.List, number, {"user": lambda x: random.choice(users)}
        )
        created_lists = seeder.execute()
        clean_lists = flatten(list(created_lists.values()))

        for pk in clean_lists:
            list_model = list_models.List.objects.get(pk=pk)
            to_add = rooms[random.randint(0, 5) : random.randint(6, 30)]
            list_model.rooms.add(*to_add)

        self.stdout.write(self.CRED + "List 생성!" + self.CEND)

