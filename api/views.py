from rest_framework import generics, viewsets
from api.my_permissions import IsTeacherPermissions
from api.serializers import EvaluationSerializer, SetEvaluationSerializer
from services.get_evaluations_of_quarter import get_evaluation_of_quarter
from diary.models import MyUser


class ApiEvaluation(viewsets.ViewSet, generics.ListAPIView):
    serializer_class = EvaluationSerializer
    permission_classes = (IsTeacherPermissions, )

    def get_queryset(self):
        users = MyUser.objects.filter(
            student__learned_class__number_class=self.kwargs.get('class_number'),
            student__learned_class__slug=self.kwargs.get('slug_name')
        )
        for i in users:
            i.evaluation = [i.evaluation for i in
                            get_evaluation_of_quarter(i, self.request.user.teacher.item.book_name)]

        return users


class ApiSetEvaluation(viewsets.ViewSet, generics.CreateAPIView):
    serializer_class = SetEvaluationSerializer
    permission_classes = (IsTeacherPermissions,)
