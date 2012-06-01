from django.db import models
from django.contrib.auth.models import User

from dateutil.relativedelta import relativedelta
import redis

import datetime
import re

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
    user = models.ForeignKey(User)

    redis = redis.StrictRedis(host='localhost', port=6379, db=0)

    def massage_date(self, date):
        if isinstance(date, datetime.date):
            date = date.strftime("%Y-%m-%d")
        assert re.match("^\d{4}-\d{2}-\d{2}$", date)
        return date

    def get_date_key(self, date):
        date_str = self.massage_date(date)
        key = "user:%s:goal:%s:%s" % (self.user_id, self.id, date_str)
        return key

    def get_date_count(self, date):
        key = self.get_date_key(date)
        count = int(self.redis.get(key) or 0)
        return count

    def incr(self, date, incr):
        return self.redis.incr(self.get_date_key(date), incr)

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
