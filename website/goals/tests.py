from django.utils import unittest

import datetime

from goals.test_helpers import ExtendedTestCase
from goals import models

d = datetime.date
start = d(2012, 5, 27)

class GoalsTests(ExtendedTestCase):
    def signup_user(self):
        users = models.User.objects.count()
        self.post("/signup/", {"email": "user{}@example.com".format(users), "password": "foobar", "deck": "0"})
        return models.User.objects.get(id=users+1)

    def test_404(self):
        self.assertStatus(404, '/foobar/')

    def test_home(self):
        self.assertStatus(200, '/')

    def test_login(self):
        self.assertStatus(200, '/login/')

    def test_signup(self):
        self.assertStatus(200, '/signup/')
        user = self.signup_user()
        self.assertEqual(1, user.id)

    def test_daily(self):
        g = models.Goal(name="foo", frequency=models.Goal.FREQ_DAILY)

        self.assertEqual(
                g.get_trailing_dates(for_date=start),
                [d(2012, 5, day) for day in range(21, 28)])

    def test_weekly(self):
        g = models.Goal(name="foo", frequency=models.Goal.FREQ_WEEKLY)
        expected = [d(2012,5,7), d(2012,5,14), d(2012,5,21)]

        self.assertEqual(g.get_trailing_dates(for_date=start)[-3:], expected)
        self.assertEqual(g.get_trailing_dates(for_date=d(2012,5,21))[-3:], expected)

    def test_monthly(self):
        g = models.Goal(name="foo", frequency=models.Goal.FREQ_MONTHLY)

        self.assertEqual(
                g.get_trailing_dates(for_date=start),
                [d(2011,11,1), d(2011,12,1), d(2012,1,1), d(2012,2,1), d(2012,3,1), d(2012,4,1), d(2012,5,1)])

    def test_yearly(self):
        g = models.Goal(name="foo", frequency=models.Goal.FREQ_YEARLY)
        self.assertEqual(
                g.get_trailing_dates(for_date=start),
                [d(2006,1,1), d(2007,1,1), d(2008,1,1), d(2009,1,1), d(2010,1,1), d(2011,1,1), d(2012,1,1)])
