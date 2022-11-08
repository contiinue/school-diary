from rest_framework import serializers
from diary.models import Evaluation, MyUser


class EvaluationSerializer(serializers.ModelSerializer):
    evaluation = serializers.ListField(child=serializers.ListField(), read_only=True)

    class Meta:
        model = MyUser
        fields = (
            'id', 'first_name', 'last_name', 'evaluation'
        )


class SetEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = ('id', 'student', 'evaluation', 'item', 'quarter')
        # read_only_fields = ('id', 'student', 'item', 'quarter')


class SchoolTimetableSerializer(serializers.Serializer):
    some = serializers.CharField(max_length=30)


