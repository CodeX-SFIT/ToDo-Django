from django.contrib import admin
from .models import TodoItem

# Register your models here.
class TodoItemAdmin(admin.ModelAdmin):
    list_display = [
        'id','text','created_at','created_by'
    ]

admin.site.register(TodoItem, TodoItemAdmin)
