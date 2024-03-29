from django.shortcuts import render, redirect, get_object_or_404

from hospital_site.models import Patient, Doctor
from django import forms
from django.core.validators import ValidationError

class LoginForm(forms.Form):
    username = forms.fields.CharField(
        required=True,
        label="用户名",
        widget=forms.widgets.TextInput({"placeholder":"请输入用户名","class":"form-control"})
    )
    password = forms.fields.CharField(
        required=True,
        label="密码",
        widget=forms.widgets.PasswordInput({"placeholder":"请输入密码","class":"form-control"})
    )

def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login/login.html", {"form": form})
    
    form = LoginForm(data=request.POST)
    if form.is_valid():
        login_type = request.POST.get('login_type')
        user_model = Patient if login_type == 'patient_login' else Doctor
        user = user_model.objects.filter(**form.cleaned_data).first()

        if user:
            # 验证成功，跳转到主页
            request.session["info"] = {'id': user.id, 'login_type': login_type}
            if login_type == 'patient_login':
                return redirect("/patient/home/")
            else:
                return redirect("/doctor/home/")    
        else:
            # 验证失败，增加错误并重新渲染
            form.add_error("password", "用户名或密码不正确")
            return render(request, "login/login.html", {"form": form})
    
    return render(request, "login/login.html", {"form": form})


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'username', 'password', 'gender']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        # 检查数据库中是否已经存在相同的用户名
        if Patient.objects.filter(username=username).exists():
            raise ValidationError("该用户名已被使用，请重新填写")
        return username
    
    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['username'].required = True
        self.fields['password'].required = True

def enroll(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            return redirect('/login/')
    else:
        form = PatientForm()
    
    return render(request, "login/enroll.html", {"form": form})

def logout(request):
    request.session.clear()
    return redirect('/login/')
