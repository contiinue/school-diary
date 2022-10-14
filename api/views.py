from rest_framework import generics, mixins, viewsets, views
from rest_framework.response import Response

from api.serializers import EvaluationSerializer, SetEvaluationSerializer
from diary.get_quarter import get_evaluation_of_quarter
from diary.models import Evaluation, MyUser


class ApiEvaluation(generics.ListCreateAPIView):
    serializer_class = EvaluationSerializer

    def get_queryset(self):
        users = MyUser.objects.filter(
            student__learned_class__number_class=1,
            student__learned_class__slug='a'
        )
        user = list()
        for i in users:
            user.append(
                {'user': i.pk,
                 'first_name': i.first_name,
                 'last_name': i.last_name,
                 'evaluation': [i.evaluation for i in
                                get_evaluation_of_quarter(i, self.request.user.teacher.item.book_name)],
                 }
            )
        return user


# class ApiSetEvaluation(generics.CreateAPIView):
#     serializer_class = SetEvaluationSerializer
