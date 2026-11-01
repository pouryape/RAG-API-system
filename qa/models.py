from django.db import models


class QuestionAnswer(models.Model):
    question = models.TextField()
    answer = models.TextField()
    sources = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question[:100]
