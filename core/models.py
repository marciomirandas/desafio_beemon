from django.db import models
from stdimage.models import StdImageField
import uuid


def get_file_path(_instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return 'records/' + str(filename)


class Base(models.Model):
    created = models.DateField('Data de Criação', auto_now_add=True)
    modified = models.DateField('Data de Modificação', auto_now=True)
    active = models.BooleanField('Ativo', default=True)

    class Meta:
        abstract = True


class Record(Base):
    quote = models.TextField('Citação')
    author = models.CharField('Autor', max_length=200)
    tag = models.TextField('Tag')
    pag = models.TextField('Page')
    image = StdImageField('Imagem', upload_to=get_file_path, variations={'thumb': {'width': 480, 'height': 480, 'crop': True}})
    
    class Meta:
        verbose_name = 'Registro'
        verbose_name_plural = 'Registros'

    def __str__(self):
        return self.author
