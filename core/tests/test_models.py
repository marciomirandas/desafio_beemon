import uuid
from django.test import TestCase
from model_mommy import mommy

from core.models import get_file_path


class GetFilePathTestCase(TestCase):

    def setUp(self):
        self.filename = f'{uuid.uuid4()}.png'

    def test_get_file_path(self):
        arquivo = get_file_path(None, 'teste.png')
        self.assertTrue(len(arquivo), len(self.filename))


class RecordTestCase(TestCase):

    def setUp(self):
        self.record = mommy.make('Record')

    def test_str(self):
        self.assertEquals(str(self.record), self.record.author)


class TagTestCase(TestCase):

    def setUp(self):
        self.tag = mommy.make('Tag')

    def test_str(self):
        self.assertEquals(str(self.tag), self.tag.name)
        self.assertLess
