from django.urls import path
from .views import index, data, data_id, dataframe, log


urlpatterns = [
    path('', index, name='index'),
    path('dados/', data, name='data'),
    path('dados-<int:id>/', data_id, name='data_id'),
    path('dataframe/', dataframe, name='dataframe'),
    path('log/', log, name='log'),
    
]
