from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy

#logi
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm #ユーザーの新規登録
from django.contrib.auth import login #認証してログインすると自動ページ遷移する

from todoapp.models import Task

# def taskList(request):
#    return HttpResponse("<h1>Hello Django</h1>")

#クラスベースビューで、値をDBからとってくる作業
#クラスベースビューがあれば、関数をつくる必要がなり。Djangoで元から用意されている。
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"

    # ユーザーごとのデータのみを表示させる制御
    #get_context_dataはListViewが持っている関数。それをここでカスタマイズする。
    def get_context_data(self, **kwargs):
        #superで親を指定(ここでは元のデータをひっぱってきている) 
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(user=self.request.user)
        
        #検索機能
        searchInputText = self.request.GET.get("search") or ""
        # print(searchInputText)
        if searchInputText:
            # filterの方法はDjangoのQuerySetAPIリファレンスにあり
            context["tasks"] = context["tasks"].filter(title__startswith=searchInputText)
        context["search"] = searchInputText
        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "task"

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title","description","completed"]
    success_url = reverse_lazy("tasks")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("tasks")

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("tasks")

class TaskListLoginView(LoginView):
    fields = "__all__"
    template_name = "todoapp/login.html"
    def get_success_url(self):
        return reverse_lazy("tasks")

#ユーザーの新規登録
class RegisterTodoApp(FormView):
    template_name = "todoapp/register.html"
    form_class = UserCreationForm #Djangoが提供する標準のユーザー登録フォーム
    success_url = reverse_lazy("tasks")

    def form_valid(self,form):
        user = form.save() #送信されたデータをもとに新しいユーザーを作成してDBに登録
        if user is not None: #ユーザーが正常に作成されたかどうか
            login(self.request,user) #認証を行う（ログインする）
        return super().form_valid(form) #オーバーライドして戻す