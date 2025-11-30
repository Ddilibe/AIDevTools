from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from .models import Todo
from .forms import TodoForm


class TodoListView(ListView):
    """Display all todos."""

    model = Todo
    template_name = "todos/todo_list.html"
    context_object_name = "todos"
    paginate_by = 10


class TodoDetailView(DetailView):
    """Display a single todo."""

    model = Todo
    template_name = "todos/todo_detail.html"
    context_object_name = "todo"


class TodoCreateView(CreateView):
    """Create a new todo."""

    model = Todo
    form_class = TodoForm
    template_name = "todos/todo_form.html"
    success_url = reverse_lazy("todo_list")


class TodoUpdateView(UpdateView):
    """Update an existing todo."""

    model = Todo
    form_class = TodoForm
    template_name = "todos/todo_form.html"
    success_url = reverse_lazy("todo_list")


class TodoDeleteView(DeleteView):
    """Delete a todo."""

    model = Todo
    template_name = "todos/todo_confirm_delete.html"
    success_url = reverse_lazy("todo_list")


def toggle_todo(request, pk):
    """Toggle the completed status of a todo."""
    todo = get_object_or_404(Todo, pk=pk)
    todo.completed = not todo.completed
    todo.save()
    return redirect("todo_list")
