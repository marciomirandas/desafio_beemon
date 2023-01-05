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
    author = models.CharField('Autor', max_length=100)
    author_link = models.CharField('Link do Autor', max_length=200)
    born = models.CharField('Nascimento', max_length=100)
    place = models.CharField('Local', max_length=100)
    description = models.TextField('Descrição')
    image = StdImageField('Imagem', upload_to=get_file_path, variations={'thumb': {'width': 270, 'height': 127, 'crop': True}})
    
    class Meta:
        verbose_name = 'Registro'
        verbose_name_plural = 'Registros'

    def __str__(self):
        return self.author


class Tag(Base):
    name = models.CharField('Nome', max_length=100)
    link = models.URLField('link')
    record = models.ForeignKey('core.Record', verbose_name='Tag', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name
