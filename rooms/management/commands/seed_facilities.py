from django.core.management.base import BaseCommand
from rooms import models as room_models


class Command(BaseCommand):

    CRED = "\033[91m"
    CEND = "\033[0m"

    help = "Facilities 생성"

    # def add_arguments(self, parser):
    #     parser.add_argument("--times", help="몇번 호출할지")

    def handle(self, *args, **options):
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]

        for fa in facilities:
            queryLeng = len(room_models.Amenity.objects.filter(name=fa))
            if queryLeng == 0:
                room_models.Facility.objects.create(name=fa)
                self.stdout.write(self.CRED + fa + " Facility 생성!" + self.CEND)

