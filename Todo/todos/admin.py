from django.contrib import admin
from .models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ("title", "completed", "created_at", "updated_at")
    list_filter = ("completed", "created_at")
    search_fields = ("title", "description")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Task Information", {"fields": ("title", "description")}),
        ("Status", {"fields": ("completed",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
