from django.urls import path

from .views import AskQuestionAPIView, QuestionAnswerListAPIView

urlpatterns = [
    path('ask/', AskQuestionAPIView.as_view()),
    path('history/', QuestionAnswerListAPIView.as_view()),
]
