from django.contrib import admin
from .models import Record, Tag

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('author', 'created', 'modified')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'record', 'created', 'modified')
