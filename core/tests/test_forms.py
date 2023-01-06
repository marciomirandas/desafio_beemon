from django.test import TestCase
from core.forms import IndexForm

import datetime


class IndexFormTestCase(TestCase):

    def test_index_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = IndexForm(data={'date': date})
        self.assertFalse(form.is_valid())

    
    def test_index_form_date_today(self):
        date = datetime.date.today()
        form = IndexForm(data={'date': date})
        self.assertFalse(form.is_valid())

