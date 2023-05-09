from app.models import Users, Question, Answer, Tag, LikeQuestion, LikeAnswer

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.core import management


class Command(BaseCommand):
    help = 'Fill the database'

    @transaction.atomic
    def handle(self, *args, **options):
        models = [Users, Question, Answer, Tag, LikeQuestion, LikeAnswer]
        for m in models:
            m.objects.all().delete()