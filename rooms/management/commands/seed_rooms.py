from django.core.management.base import BaseCommand
import random
from django.contrib.admin.utils import flatten
from django_seed import Seed

from users import models as user_models
from rooms import models as room_models


class Command(BaseCommand):

    CRED = "\033[91m"
    CEND = "\033[0m"

    help = "Fake Rooms 생성"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default="1", type=int, help="몇개의 방 생성할지 넘겨주는 인자"
        )

    def handle(self, *args, **options):
        number = options.get("number", 1)
        seeder = Seed.seeder()

        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        houserules = room_models.HouseRule.objects.all()

        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.company(),
                "city": lambda x: seeder.faker.city(),
                "address": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "price": lambda x: random.randint(1, 100) * 1000,
                "beds": lambda x: random.randint(1, 5),
                "guests": lambda x: random.randint(1, 10),
                "bedrooms": lambda x: random.randint(1, 5),
                "baths": lambda x: random.randint(1, 5),
            },
        )
        created_rooms = seeder.execute()
        created_clean = flatten(list(created_rooms.values()))

        for pk in created_clean:
            room = room_models.Room.objects.get(pk=pk)

            for i in range(3, random.randint(10, 30)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"room_photos/{random.randint(1,31)}.webp",
                )
            for a in amenities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.amenities.add(a)
            for f in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(f)
            for h in houserules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.room_rules.add(h)
        self.stdout.write(self.CRED + f"{number}개 Room 생성!" + self.CEND)

