import email
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# dev_9
# class QuestionForm(forms.ModelForm):

#     class Meta:
#         model = Question  # form 과 모델을 연결
#         fields = ["subject", "content"]  # QuestionForm에서 사용할 Question 모델의 속성


# class AnswerForm(forms.ModelForm):

#     class Meta:
#         model = Answer  # form 과 모델을 연결
#         fields = ["content"]
#         labels = {"content": "답변내용"}


# 이메일 필드가 없으면 입력하지 않아도 가입가능
# form.cleaned_data["email"] 사용 가능
class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")  # 필수 입력이 됨

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")
