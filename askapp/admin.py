from django.contrib import admin

from .models import Profile, Question, Answer, Like, Tag
from . import models

admin.site.register(models.Profile)
admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.Like)
admin.site.register(models.Tag)