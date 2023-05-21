from django.db import models
from django.db.models import Sum


class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        # Забираем queryset с записями больше 0
        return self.get_queryset().filter(votes__gt=0)

    def dislikes(self):
        # Забираем queryset с записями меньше 0
        return self.get_queryset().filter(votes__lt=0)

    def sum_rating(self):
        # Забираем суммарный рейтинг
        return self.get_queryset().aggregate(Sum('votes')).get('votes__sum') or 0

    def questions(self):
        return self.get_queryset().filter(content_type__model='Question')

    def answers(self):
        return self.get_queryset().filter(content_type__model='Answer')


class QuestionManager(models.Manager):
    use_for_related_fields = True

    def new_questions(self):
        return self.get_queryset().order_by('-date_published')

    def hot_questions(self):
        return self.get_queryset().order_by('-rating')