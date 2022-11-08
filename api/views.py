from rest_framework import generics, viewsets
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from api.my_permissions import IsTeacherPermissions
from api.serializers import EvaluationSerializer, SetEvaluationSerializer, SchoolTimetableSerializer
from services.get_evaluations_of_quarter import get_evaluation_of_quarter, get_now_quarter
from diary.models import MyUser, Quarter, BookWithClass
from datetime import date, timedelta


class ApiEvaluation(viewsets.ViewSet, generics.ListAPIView):
    serializer_class = EvaluationSerializer
    permission_classes = (IsTeacherPermissions,)

    def get_queryset(self):
        users = MyUser.objects.filter(
            student__learned_class__number_class=self.kwargs.get('class_number'),
            student__learned_class__slug=self.kwargs.get('slug_name')
        )
        for i in users:
            i.evaluation = [(i.pk, i.evaluation, i.date) for i in
                            get_evaluation_of_quarter(i, self.request.user.teacher.item.book_name)]
        return users


class ApiSetEvaluation(viewsets.ViewSet, generics.CreateAPIView, UpdateModelMixin):
    serializer_class = SetEvaluationSerializer
    permission_classes = (IsTeacherPermissions,)


class SchoolTimetableApi(APIView):

    def get(self, request, *args, **kwargs):
        return Response({'dates': self.get_queryset()})

    def get_queryset(self) -> list[str]:
        quarter = get_now_quarter()
        time_table = BookWithClass.objects.get(
            student_class__number_class=self.kwargs.get('class_number'),
            student_class__slug=self.kwargs.get('slug_name'),
            time_table__item__book_name=self.request.user.teacher.item.book_name
        )
        return self.get_days_of_quarter(
            quarter.start, quarter.end, [i.number_of_week_day() for i in time_table.time_table.lesson_date.all()]
        )

    @staticmethod
    def get_days_of_quarter(start: date, end: date, week_day: list) -> list[str]:
        total_days: int = (end - start).days + 1
        all_days = [start + timedelta(days=day) for day in range(total_days)]
        return [day.strftime('%Y-%m-%d') for day in all_days if day.weekday() in week_day]
