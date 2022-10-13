from rest_framework import generics, mixins, viewsets, views
from rest_framework.response import Response

from api.serializers import EvaluationSerializer
from diary.get_quarter import get_evaluation_of_quarter
from diary.models import Evaluation, MyUser


class ApiSetEvaluation(views.APIView):
    def get(self, request, class_number, slug_name):
        users = MyUser.objects.filter(
            student__learned_class__number_class=class_number,
            student__learned_class__slug=slug_name
        )
        user = list()
        for i in users:
            user.append(
                {'user': i.pk,
                 'first_name': i.first_name,
                 'last_name': i.last_name,
                 'evaluation': [i.evaluation for i in
                                get_evaluation_of_quarter(i, request.user.teacher.item.book_name)],

                 }
            )
        return Response({'users': EvaluationSerializer(user, many=True).data})

    def post(self, request, *args, **kwargs):
        return self.create(request, args, kwargs)