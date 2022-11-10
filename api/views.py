from rest_framework import generics, viewsets, status, views
from rest_framework.mixins import UpdateModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from api.my_permissions import IsTeacherPermissions
from api.serializers import EvaluationSerializer, SetEvaluationSerializer
from services.get_evaluations_of_quarter import get_evaluation_of_quarter, get_now_quarter
from diary.models import MyUser, Quarter, BookWithClass, Evaluation
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


class ApiSetEvaluation(UpdateModelMixin, CreateModelMixin, generics.GenericAPIView):
    serializer_class = SetEvaluationSerializer
    queryset = Evaluation.objects.all()

    def post(self, request, *args, **kwargs):
        my_request = request.POST.copy()
        my_request.setdefault('item', self.request.user.teacher.item.pk)
        my_request.setdefault('quarter', get_now_quarter().pk)
        serializer = self.serializer_class(data=my_request)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def put(self, request, *args, **kwargs):
        return self.update(request, args, kwargs)


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
