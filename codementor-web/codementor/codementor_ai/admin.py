from django.contrib import admin
from .models import CodeReview, TestCase, CodeDebug

# Register your models here.
admin.site.register(CodeReview)
admin.site.register(TestCase)
admin.site.register(CodeDebug)
