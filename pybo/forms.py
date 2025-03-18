from attr import fields
from django import forms

from pybo.models import Question


# dev_9
class QuestionForm(forms.MoelForm):
    class Meta:
        model = Question  # form 과 모델을 연결
        fields = ["subject", "content"]  # QuestionForm에서 사용할 Question 모델의 속성
