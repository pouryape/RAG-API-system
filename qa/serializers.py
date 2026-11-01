from rest_framework import serializers

from .models import QuestionAnswer


class QuestionSerializer(serializers.Serializer):
    question = serializers.CharField(min_length=3, max_length=1000)


class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = '__all__'
