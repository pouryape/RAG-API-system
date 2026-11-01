from django.contrib import admin

from .models import QuestionAnswer


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at')
    search_fields = ('question', 'answer')
    readonly_fields = ('question', 'answer', 'sources', 'created_at')
    list_filter = ('created_at',)
