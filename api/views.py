from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from api.my_permissions import IsTeacherPermissions
from api.serializers import (
    EvaluationSerializer,
    SetEvaluationSerializer,
    MyUserSerializer,
    StudentRegistrationSerializer,
)
from services.get_evaluations_of_quarter import (
    get_now_quarter,
)
from diary.models import MyUser, BookWithClass, Evaluation, StudentRegistration, Quarter
from datetime import date, timedelta


class MyUserApi(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer


class StudentApi(viewsets.ModelViewSet):
    queryset = StudentRegistration.objects.all()
    serializer_class = StudentRegistrationSerializer


class ApiSetEvaluation(
    viewsets.GenericViewSet,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
):
    serializer_class = SetEvaluationSerializer
    permission_classes = (IsTeacherPermissions,)
    queryset = Evaluation.objects.all()

    @action(url_path="get_evaluations", detail=False, methods=["get"])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(url_path="set_evaluation", detail=False)
    def post(self, request):
        serializer = self.serializer_class(data=self.get_data(request))
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response({"invalid data": False})

    def put(self, request, *args, **kwargs):
        return self.update(request, args, kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, args, kwargs)

    @staticmethod
    def get_data(request) -> dict:
        my_request = request.POST.copy()
        my_request.setdefault("item", request.user.teacher.item.pk)
        return my_request

    def get_serializer(self, *args, **kwargs):
        if self.request.GET:
            kwargs.setdefault("context", self.get_serializer_context())
            return EvaluationSerializer(*args, **kwargs)
        return super(ApiSetEvaluation, self).get_serializer(*args, **kwargs)

    def get_queryset(self):
        if self.request.GET:
            quarter = get_now_quarter(self.request.GET.get("quarter", False))
            users = MyUser.objects.filter(
                student__learned_class__number_class=self.request.GET.get(
                    "class_number"
                ),
                student__learned_class__slug=self.request.GET.get("slug_name"),
            )
            for user in users:
                user.evaluation = user.evaluation_set.filter(quarter=quarter)
            return users
        return super(ApiSetEvaluation, self).get_queryset()


class SchoolTimetableApi(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"dates": self.get_queryset()})

    def get_queryset(self) -> list[str]:
        quarter = (
            Quarter.objects.get(pk=self.request.GET.get("quarter"))
            if self.request.GET.get("quarter")
            else get_now_quarter()
        )

        time_table = BookWithClass.objects.select_related(
            "time_table", "student_class"
        ).get(
            student_class__number_class=self.kwargs.get("class_number"),
            student_class__slug=self.kwargs.get("slug_name"),
            time_table__item__book_name=self.request.user.teacher.item.book_name,
            time_table__quarter__pk=quarter.pk,
        )
        return self.get_days_of_quarter(
            quarter.start,
            quarter.end,
            [i.number_of_week_day() for i in time_table.time_table.lesson_date.all()],
        )

    @staticmethod
    def get_days_of_quarter(start: date, end: date, week_day: list) -> list[str]:
        total_days: int = (end - start).days + 1
        all_days = [start + timedelta(days=day) for day in range(total_days)]
        return [
            day.strftime("%Y-%m-%d") for day in all_days if day.weekday() in week_day
        ]
