from datetime import date

import stripe
from django.db.models import F
from django.http import HttpResponse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from kombu.utils import json
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from api.create_payment_session import create_session
from api.my_permissions import IsTeacherPermissions
from api.serializers import (
    EvaluationSerializer,
    MyUserSerializer,
    SetEvaluationSerializer,
    StudentRegistrationSerializer,
)

from diary.models import (
    Evaluation,
    MyUser,
    StudentRegistration,
    SchoolTimetable,
    School,
)
from services.get_evaluations_of_quarter import get_now_quarter


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

    @action(methods=["post"], url_path="set_evaluation", detail=False)
    def set_evaluation(self, request):
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
        """set teacher item to request."""
        my_request = request.POST.copy()
        my_request.setdefault("item", request.user.teacher.item.pk)
        my_request.setdefault(
            "quarter", get_now_quarter(request.GET.get("quarter", False)).pk
        )
        return my_request

    def get_serializer(self, *args, **kwargs):
        if self.request.GET:
            kwargs.setdefault("context", self.get_serializer_context())
            return EvaluationSerializer(*args, **kwargs)
        return super(ApiSetEvaluation, self).get_serializer(*args, **kwargs)

    def get_queryset(self):
        """Get students with their grades for the quarter."""
        if self.request.GET:
            quarter = get_now_quarter(self.request.GET.get("quarter", False))
            users = MyUser.objects.filter(
                student__learned_class__number_class=self.request.GET.get(
                    "class_number"
                ),
                student__learned_class__slug=self.request.GET.get("slug_name"),
                school=self.request.user.school,
            )
            for user in users:
                user.evaluation = user.evaluation_set.filter(quarter=quarter)
            return users
        return super(ApiSetEvaluation, self).get_queryset()


class SchoolTimetableApi(APIView):
    def get(self, request, *args, **kwargs):
        """Get timetable of quarter."""
        dates = self.get_queryset()
        if dates is None:
            return Response(status=HTTP_204_NO_CONTENT)
        return Response({"dates": self.get_queryset()})

    def get_queryset(self) -> list[str] | None:
        """Get timetable dates or None"""
        quarter = get_now_quarter(self.request.GET.get("quarter", False))
        try:
            time_table = SchoolTimetable.objects.select_related(
                "item", "student_class", "quarter"
            ).get(
                student_class__number_class=self.kwargs.get("class_number"),
                student_class__slug=self.kwargs.get("slug_name"),
                student_class__school=self.request.user.school,
                item=self.request.user.teacher.item,
                quarter=quarter,
            )
            return self.get_days_of_quarter(
                quarter.start,
                quarter.end,
                [i.number_of_week_day() for i in time_table.lesson_date.all()],
            )
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_days_of_quarter(start: date, end: date, week_day: list) -> list[str]:
        """Get dates between start and end"""
        total_days: int = (end - start).days + 1
        all_days = [start + timezone.timedelta(days=day) for day in range(total_days)]
        return [
            day.strftime("%Y-%m-%d") for day in all_days if day.weekday() in week_day
        ]


class StripeApi(ViewSet):
    @action(methods=["post"], detail=False)
    def create_stripe_session(self, request):
        session = create_session(int(request.data["month"]), request.user.school.pk)
        return Response(data={"id": session.id}, status=303)

    @action(methods=["post"], detail=False, url_path="update_subscribe")
    def update_subscribe(self, request):
        School.objects.get(pk=request.user.school.pk).update()

    @csrf_exempt
    @action(methods=["post"], detail=False)
    def webhook(self, request):
        payload = request.body
        try:
            event = stripe.Event.construct_from(json.loads(payload), stripe.api_key)
        except ValueError:
            return HttpResponse(status=HTTP_400_BAD_REQUEST)

        if event.type == "payment_intent.succeeded":
            school_id, count_month = event["data"]["object"]["metadata"].get(
                "school_id", None
            ), event["data"]["object"]["metadata"].get("count_month", None)
            School.objects.filter(pk=school_id).update(
                paid_to=F("paid_to") + timezone.timedelta(days=int(count_month) * 30)
            )

        return HttpResponse(status=HTTP_200_OK)
