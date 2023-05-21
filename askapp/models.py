from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from askapp.managers import LikeDislikeManager, QuestionManager


QUESTIONS = [
    {
        'title': f'Question {i}',
        'text': f'Text {i}',
    } for i in range(6)
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(verbose_name='Avatar')
    nickname = models.CharField(max_length=100, verbose_name='Nickname')

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


class Question(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')
    text = models.TextField(verbose_name='Text')
    date_published = models.DateTimeField(verbose_name='Date published')
    is_published = models.BooleanField(verbose_name='Is published')
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    votes = GenericRelation('Like', related_query_name='questions')
    rating = models.IntegerField(default=0, verbose_name='Rating')
    objects = QuestionManager()

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def tags(self):
        return self.tag_set.get_queryset()

    def answers(self):
        return self.answer_set.get_queryset()


class Answer(models.Model):
    text = models.TextField(verbose_name='Text')
    correct = models.BooleanField(verbose_name='Correct')
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    date_published = models.DateTimeField(verbose_name='Date published')
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    votes = GenericRelation('Like', related_query_name='answers')
    rating = models.IntegerField(default=0, verbose_name='Rating')

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'


class Like(models.Model):
    LIKE = 1
    DISLIKE = -1
    DEFAULT = 0

    VOTES = (
        (DISLIKE, 'dislike'),
        (LIKE, 'like')
    )

    votes = models.IntegerField(choices=VOTES, default=DEFAULT, verbose_name='Votes')
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default='')
    object_id = models.PositiveIntegerField(default=0, verbose_name='Object id')
    content_object = GenericForeignKey('content_type', 'object_id')
    objects = LikeDislikeManager()

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'


class Tag(models.Model):
    tag = models.CharField(max_length=100, verbose_name='Tag')
    question = models.ManyToManyField('Question', related_query_name='tags')

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def questions(self):
        return self.question.all()
