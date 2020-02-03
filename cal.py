import calendar
from django.utils import timezone


class Day:
    def __init__(self, number, past, month, year):
        self.number = number
        self.past = past
        self.month = month
        self.year = year


class Calendar(calendar.Calendar):
    def __init__(self, year, month):
        super().__init__(firstweekday=6)
        self.year = year
        self.month = month
        self.day_names = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")
        self.months = (
            "January",
            "February",
            "March",
            "Aprill",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        )

    def get_month(self):
        return self.months[self.month - 1]

    def get_days(self):
        weeks = self.monthdays2calendar(self.year, self.month)
        days = []

        now = timezone.now()
        today = now.day
        month = now.month

        for week in weeks:
            # _ 는 2번쨰 변수를 무시한다는 뜻
            for day, _ in week:

                past = False
                if month == self.month:
                    if day <= today:
                        past = True
                new_day = Day(day, past, month=self.month, year=self.year)
                days.append(new_day)

        return days
