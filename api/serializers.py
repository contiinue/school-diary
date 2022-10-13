from rest_framework import serializers
from diary.models import Evaluation, MyUser


class EvaluationSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    evaluation = serializers.ListField(child=serializers.IntegerField())

    def create(self, validated_data):
        Evaluation.objects.create(**validated_data)

