from django.shortcuts import render,redirect
from django.views import View
from Todo.models import *
from Todo.forms import TodoForm
# Create your views here.


class HomeView(View):
    def get(self,request,*args,**kwargs):
        return render(request,"index.html")
     
class TodoListView(View):
    def get(self,request,*args,**kwarg):
        todolist=Todo.objects.all()
        return render(request,"todolist.html",{"data":todolist})

class TodoAddView(View):
    def get(self,request,*args,**kwarg):
        form=TodoForm()
        context={"form":form}
        return render(request,"add.html",context)
    
    def post(self,request):
        form_data=TodoForm(data=request.POST)
        if form_data.is_valid():
            title=form_data.cleaned_data.get('title')
            desc=form_data.cleaned_data.get('description')
            Todo.objects.create(title=title,description=desc)
            return redirect('list')
        return render(request,"editTodo.html",{"form":form_data})

class DeleteTodo(View):
    def get(self,request,**kwargs):
        tid=kwargs.get('id')
        Todo.objects.get(id=tid).delete()
        return redirect('list')
    
class EditView(View):
    def get(self,request,**kwargs):
        tid=kwargs.get('id')
        todo=Todo.objects.get(id=tid)
        form=TodoForm(initial={"title":todo.title,"description":todo.description})
        return render(request,"editTodo.html",{"form":form})

    def post(self,request,**kwargs):
        tid=kwargs.get('id')
        todo=Todo.objects.get(id=tid)
        form_data=TodoForm(data=request.POST)
        if form_data.is_valid():
            title=form_data.cleaned_data.get('title')
            desc=form_data.cleaned_data.get('description')
            todo.title=title
            todo.description=desc
            todo.save()
            return redirect('list')
        return render(request,"editTodo.html",{"form":form_data})

class UpdateStatusView(View):
    def get(self,request,**kwargs):
        tid=kwargs.get('id')
        todo=Todo.objects.get(id=tid)
        todo.status="Completed"
        todo.save()
        return redirect('list')