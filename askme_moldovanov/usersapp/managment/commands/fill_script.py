from app.models import Users, Question, Answer, Tag, LikeQuestion, LikeAnswer

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from app.management.commands._factories import (
    UsersFactory,
    QuestionFactory,
    AnswerFactory,
    TagFactory,
    LikeQuestionFactory,
    LikeAnswerFactory
)

import random


class Command(BaseCommand):
    help = 'Fill the database'

    def add_arguments(self, parser):
        parser.add_argument('ratio', nargs='?', type=int, default=10000)

    @transaction.atomic
    def handle(self, *args, **options):
        models = [Users, Question, Answer, Tag, LikeQuestion, LikeAnswer]
        for m in models:
            m.objects.all().delete()

        ratio = options['ratio']

        profiles = Users.objects.bulk_create(UsersFactory() for _ in range(ratio))

        tags = Tag.objects.bulk_create(TagFactory() for _ in range(ratio))

        questions = []
        for _ in range(ratio * 10):
            question = QuestionFactory.create(profile=random.choice(profiles),
                                              tags=random.choices(tags, k=random.choice([1, 2, 3])))
            questions.append(question)

        answers = [AnswerFactory(
            profile=random.choice(profiles),
            question=random.choice(questions)
        ) for _ in range(ratio * 100)]
        Answer.objects.bulk_create(answers)

        likeans = []
        for _ in range(ratio * 200):
            flag = random.choice([True, False])
            like = LikeAnswerFactory(
                profile=random.choice(profiles),
                question=random.choice(questions) if flag else None,
                answer=random.choice(answers) if not flag else None
            )
            likeans.append(like)
        LikeAnswer.objects.bulk_create(likeans)

        likequest = []
        for _ in range(ratio * 200):
            flag = random.choice([True, False])
            like = LikeQuestionFactory(
                profile=random.choice(profiles),
                question=random.choice(questions) if flag else None,
                answer=random.choice(answers) if not flag else None
            )
            likequest.append(like)
        LikeAnswer.objects.bulk_create(likequest)