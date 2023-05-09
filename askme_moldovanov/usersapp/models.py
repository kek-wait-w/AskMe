from django.db import models
from django.contrib.auth.models import User


class Users(models.Model):
    user_name = models.CharField(max_length=255)
    id_user = models.IntegerField()
    profile = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField()


class Question(models.Model):
    text_question = models.CharField(max_length=255)
    id_question = models.IntegerField()
    id_user = models.ForeignKey('Users', on_delete=models.SET_NULL, null=True)
    id_tag = models.ForeignKey('Tag', on_delete=models.PROTECT)


class Answer(models.Model):
    text_answer = models.CharField(max_length=255)
    id_answer = models.IntegerField()
    id_user = models.ForeignKey('Users', on_delete=models.SET_NULL, null=True)


class Tag(models.Model):
    text_tag = models.CharField(max_length=255)
    id_tag = models.IntegerField()


class LikeQuestion(models.Model):
    count = models.IntegerField()
    id_question = models.ForeignKey('Question', on_delete=models.SET_NULL, null=True)


class LikeAnswer(models.Model):
    count = models.IntegerField()
    id_answer = models.ForeignKey('Answer', on_delete=models.SET_NULL, null=True)

