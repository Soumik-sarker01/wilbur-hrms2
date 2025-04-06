from django.contrib import admin
from .models import TaskEntry

@admin.register(TaskEntry)
class TaskEntryAdmin(admin.ModelAdmin):
    list_display = ("date", "order_id", "client", "status", "due_date")
    list_filter = ("status", "date", "client")
    search_fields = ("order_id", "client")
