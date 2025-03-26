from urllib import response
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from pybo.forms import AnswerForm, QuestionForm
from pybo.models import Answer, Question
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url="common:login")  # dev_16
def question_create(request):

    print(request.POST.get("content"))

    if request.method == "POST":

        form = QuestionForm(request.POST)

        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user  # dev_16
            question.create_date = timezone.now()
            question.save()
            return redirect("pybo:index")

    else:
        form = QuestionForm()

    context = {"form": form}
    return render(request, "pybo/question_form.html", context)


# dev_17
@login_required(login_url="common:login")
def question_modify(request, question_id):

    question = get_object_or_404(Question, pk=question_id)

    if request.user != question.author:
        messages.error(request, "수정 권한이 없습니다.")
        return redirect("pybo:detail", question_id=question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)

        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            question.save()
            return redirect("pybo:detail", question_id=question.id)
    else:
        form = QuestionForm(instance=question)

    context = {"form": form}
    return render(request, "pybo/question_form.html", context)


@login_required(login_url="common:login")
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.user != question.author:
        messages.error(request, "삭제권한이 없습니다")
        return redirect("pybo:detail", question_id=question_id)

    question.delete()
    return redirect("pybo:index")


@login_required(login_url="common:login")
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.user == question.author:
        messages.error(request, "본인이 작성한 글은 추천할수 없습니다.")
    else:
        question.voter.add(request.user)

    return redirect("pybo:detail", question_id=question.id)
