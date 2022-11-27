from rest_framework import serializers
from diary.models import Evaluation, MyUser, StudentRegistration


class StudentRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentRegistration
        fields = "__all__"


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = "__all__"


class EvaluationSerializer(serializers.ModelSerializer):
    evaluation = serializers.SerializerMethodField("_get_evaluations_data")

    class Meta:
        model = MyUser
        fields = ("id", "first_name", "last_name", "evaluation")

    @staticmethod
    def _get_evaluations_data(model: MyUser) -> list:
        return [(i.pk, i.evaluation, i.date) for i in model.evaluation]


class SetEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = ("id", "student", "evaluation", "item", "quarter", "date")
