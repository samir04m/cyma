from django.contrib import admin
from .models import *

@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'depressionScore', 'anxietyScore', 'stressScore', 'globalScore', 'date']
    readonly_fields = ['date']

@admin.register(RegistrationToken)
class RegistrationTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'name', 'active', 'creation_date', 'user', 'user_registration_date')
    list_filter = ('active', 'creation_date')
    search_fields = ('token', 'name', 'user__username')
    ordering = ('-creation_date',)
    readonly_fields = ['creation_date']