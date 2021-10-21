from django.contrib import admin
from django.contrib.admin.decorators import register
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import *

CustomUser = get_user_model()

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Patient)
admin.site.register(FoodTests)
admin.site.register(SptTests)
admin.site.register(Spt_tests_done_by_patients)
admin.site.register(Food_tests_done_by_patients)

