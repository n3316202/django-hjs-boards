from django.shortcuts import redirect, render
from django.contrib.auth import logout, login, authenticate

from common.forms import UserForm


# Create your views here.
def logout_view(request):
    logout(request)
    return redirect("index")


# http://127.0.0.1:8000/common/signup/
# dev_15
def signup(request):

    print(request)

    if request.method == "POST":
        # request.POST.get("username")
        # request.POST.get("password1")
        # request.POST.get("password2")

        form = UserForm(request.POST)

        if form.is_valid():
            
            form.save() # DB 저장

            #회원가입 하자 마자,  로그인을 시켜줌
            username = form.cleaned_data.get("username") #request.POST.get("username",'')
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인

            return redirect("index")
    else:
        form = UserForm()

    return render(request, "common/signup.html", {"form": form})
