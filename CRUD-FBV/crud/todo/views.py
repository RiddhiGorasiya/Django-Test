from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Todo
from .forms import TodoForm
from myapp.models import User

@login_required
def todo_list(request):
    profile = User.objects.filter(user=request.user).first()
    if profile.role != "Developer":
        messages.error(request, "Only developers can access the TODO list.")
        return redirect('addandshow')

    todos = Todo.objects.filter(user=profile).order_by('-created_at')
    return render(request, 'todo/todo_list.html', {'todos': todos})

@login_required
def todo_create(request):
    profile = User.objects.filter(user=request.user).first()
    if profile.role != "Developer":
        messages.error(request, "Only developers can create tasks.")
        return redirect('todo_list')

    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = profile
            todo.save()
            messages.success(request, "Task added successfully!")
            return redirect('todo_list')
    else:
        form = TodoForm()
    return render(request, 'todo/todo_form.html', {'form': form})

@login_required
def todo_update(request, id):
    profile = User.objects.filter(user=request.user).first()
    todo = get_object_or_404(Todo, id=id, user=profile)

    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully!")
            return redirect('todo_list')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todo/todo_form.html', {'form': form})

@login_required
def todo_delete(request, id):
    profile = User.objects.filter(user=request.user).first()
    todo = get_object_or_404(Todo, id=id, user=profile)

    if request.method == 'POST':
        todo.delete()
        messages.success(request, "Task deleted successfully!")
        return redirect('todo_list')

    return render(request, 'todo/todo_confirm_delete.html', {'todo': todo})
