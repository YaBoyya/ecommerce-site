from django.db.models import Avg, Func
from django.db.models.manager import Manager
from django.db.models.query import QuerySet


class Round2(Func):
    function = "ROUND"
    template = "%(function)s(%(expressions)s::numeric, 2)"


class ProductManager(Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().annotate(
            rating=Round2(Avg('review__rating'))
        )
