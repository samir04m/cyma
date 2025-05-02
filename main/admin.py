from django.contrib import admin
from .models import *

@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'depressionScore', 'anxietyScore', 'stressScore', 'globalScore', 'date']
    readonly_fields = ['date']

@admin.register(RegistrationToken)
class RegistrationTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'user', 'active', 'creation_date', 'user_registration_date')
    list_filter = ('active', 'creation_date')
    search_fields = ('token', 'user__username', 'user__email')
    ordering = ('-creation_date',)