from django.test import TestCase
from django.urls import reverse
from datetime import datetime, date

from core.models import Record


class IndexViewTestCase(TestCase):

    def setUp(self):
        self.record = Record.objects.create(
            id = 1,
            quote='citacao', 
            author='autor', 
            author_link='http://www', 
            born='nascimento', 
            place='local', 
            description='descricao',
            image='imagem')
        

    def test_view_url_exists_at_index(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_index(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'index.html')

    def test_form_in_view_index(self):

        response = self.client.post(reverse('index'), {
                    'date': date.today(),
                    'time': datetime.now().time()
                    })
        self.assertEqual(response.status_code, 200)

 
    def test_view_url_exists_at_data(self):
        response = self.client.get('/dados/')
        self.assertEqual(response.status_code, 200)

    def test_context_exists_at_data(self):
        response = self.client.get(reverse('data'))
        self.assertEquals(len(response.context['records']),1)
        
    

    def test_view_url_error_404_data_id(self):
        response = self.client.get(reverse('data_id', kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_data_id(self):
        response = self.client.get(reverse('data_id', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)
        

    def test_view_url_exists_at_dataframe(self):
        response = self.client.get('/dataframe/')
        self.assertEqual(response.status_code, 200)


    def test_view_url_exists_at_log(self):
        response = self.client.get('/log/')
        self.assertEqual(response.status_code, 200)


    
        



    


    
    


    

    
