from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import QuestionAnswer
from .serializers import QuestionSerializer, QuestionAnswerSerializer
from .services import ask_question


class AskQuestionAPIView(APIView):
    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        question = serializer.validated_data['question']
        result = ask_question(question)

        QuestionAnswer.objects.create(
            question=question,
            answer=result['answer'],
            sources=result['sources'],
        )

        return Response({
            'question': question,
            'answer': result['answer'],
            'sources': result['sources'],
        }, status=status.HTTP_200_OK)


class QuestionAnswerListAPIView(ListAPIView):
    queryset = QuestionAnswer.objects.all().order_by('-created_at')
    serializer_class = QuestionAnswerSerializer
