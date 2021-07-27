from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    """
    Below you will see the community question model
    for the community message board.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_title = models.CharField(max_length=250)
    question_message = models.TextField(max_length=1000)
    date_created = models.DateField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Answer(models.Model):
    """
    Below you will see the answer question model
    for the community message board.
    """
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_message = models.TextField(max_length=1000)
    date_created = models.DateField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
