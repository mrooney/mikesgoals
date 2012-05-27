from django.db import models

import datetime
from dateutil.relativedelta import relativedelta

class Goal(models.Model):
    FREQ_DAILY = 1
    FREQ_WEEKLY = 2
    FREQ_MONTHLY = 3
    FREQ_YEARLY = 4
    FREQ_CHOICES = (
            (FREQ_DAILY, "daily"),
            (FREQ_WEEKLY, "weekly"),
            (FREQ_MONTHLY, "monthly"),
            (FREQ_YEARLY, "yearly"),
            )

    name = models.TextField()
    frequency = models.IntegerField(choices=FREQ_CHOICES)

    def get_trailing_dates(self, for_date=None):
        if for_date is None:
            for_date = datetime.date.today()

        delta = datetime.timedelta(days=1)
        if self.frequency == self.FREQ_WEEKLY:
            while for_date.isoweekday() > 1:
                for_date -= datetime.timedelta(days=1)
            delta = delta * 7
        elif self.frequency == self.FREQ_MONTHLY:
            for_date = datetime.date(for_date.year, for_date.month, 1)
            delta = relativedelta(months=1)
        elif self.frequency == self.FREQ_YEARLY:
            for_date = datetime.date(for_date.year, 1, 1)
            delta = relativedelta(years=1)

        results = [for_date - delta * x for x in range(6, -1, -1)]
        return results
