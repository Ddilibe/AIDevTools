"""Tests for the Todo views."""

import pytest
from django.test import Client
from django.urls import reverse
from todos.models import Todo


@pytest.mark.django_db
class TestTodoListView:
    """Test cases for TodoListView."""

    def test_list_view_status_code_200(self):
        """Test that todo list view returns 200 status."""
        client = Client()
        response = client.get(reverse("todo_list"))
        assert response.status_code == 200

    def test_list_view_uses_correct_template(self):
        """Test that list view uses correct template."""
        client = Client()
        response = client.get(reverse("todo_list"))
        assert "todos/todo_list.html" in [t.name for t in response.templates]

    def test_list_view_context_contains_todos(self):
        """Test that context contains todos list."""
        Todo.objects.create(title="Todo 1")
        Todo.objects.create(title="Todo 2")

        client = Client()
        response = client.get(reverse("todo_list"))
        assert "todos" in response.context
        assert len(response.context["todos"]) == 2

    def test_list_view_empty_todos(self):
        """Test list view with no todos."""
        client = Client()
        response = client.get(reverse("todo_list"))
        assert response.status_code == 200
        assert len(response.context["todos"]) == 0

    def test_list_view_pagination(self):
        """Test that list view supports pagination."""
        for i in range(15):
            Todo.objects.create(title=f"Todo {i+1}")

        client = Client()
        response = client.get(reverse("todo_list"))
        assert "is_paginated" in response.context
        assert response.context["is_paginated"] is True


@pytest.mark.django_db
class TestTodoDetailView:
    """Test cases for TodoDetailView."""

    def test_detail_view_status_code_200(self):
        """Test that todo detail view returns 200 status."""
        todo = Todo.objects.create(title="Test Todo")
        client = Client()
        response = client.get(reverse("todo_detail", args=[todo.pk]))
        assert response.status_code == 200

    def test_detail_view_uses_correct_template(self):
        """Test that detail view uses correct template."""
        todo = Todo.objects.create(title="Test Todo")
        client = Client()
        response = client.get(reverse("todo_detail", args=[todo.pk]))
        assert "todos/todo_detail.html" in [t.name for t in response.templates]

    def test_detail_view_context_contains_todo(self):
        """Test that context contains correct todo."""
        todo = Todo.objects.create(title="Test Todo", description="Test description")
        client = Client()
        response = client.get(reverse("todo_detail", args=[todo.pk]))
        assert response.context["todo"] == todo

    def test_detail_view_404_for_nonexistent_todo(self):
        """Test that detail view returns 404 for nonexistent todo."""
        client = Client()
        response = client.get(reverse("todo_detail", args=[999]))
        assert response.status_code == 404

    def test_detail_view_displays_title(self):
        """Test that detail view displays todo title."""
        todo = Todo.objects.create(title="My Important Task")
        client = Client()
        response = client.get(reverse("todo_detail", args=[todo.pk]))
        assert "My Important Task" in response.content.decode()


@pytest.mark.django_db
class TestTodoCreateView:
    """Test cases for TodoCreateView."""

    def test_create_view_status_code_200(self):
        """Test that create view returns 200 status."""
        client = Client()
        response = client.get(reverse("todo_create"))
        assert response.status_code == 200

    def test_create_view_uses_correct_template(self):
        """Test that create view uses correct template."""
        client = Client()
        response = client.get(reverse("todo_create"))
        assert "todos/todo_form.html" in [t.name for t in response.templates]

    def test_create_view_post_valid_data(self):
        """Test creating a todo with valid data."""
        client = Client()
        data = {"title": "New Todo", "description": "New description"}
        response = client.post(reverse("todo_create"), data)

        assert response.status_code == 302  # Redirect after successful creation
        assert Todo.objects.filter(title="New Todo").exists()

    def test_create_view_redirects_to_list(self):
        """Test that create view redirects to list after creation."""
        client = Client()
        data = {"title": "New Todo"}
        response = client.post(reverse("todo_create"), data)
        assert response.url == reverse("todo_list")

    def test_create_view_post_invalid_data(self):
        """Test creating a todo with invalid data."""
        client = Client()
        data = {"description": "No title"}
        response = client.post(reverse("todo_create"), data)

        assert response.status_code == 200  # Form re-rendered
        assert not Todo.objects.filter(description="No title").exists()

    def test_create_view_form_in_context(self):
        """Test that create view has form in context."""
        client = Client()
        response = client.get(reverse("todo_create"))
        assert "form" in response.context


@pytest.mark.django_db
class TestTodoUpdateView:
    """Test cases for TodoUpdateView."""

    def test_update_view_status_code_200(self):
        """Test that update view returns 200 status."""
        todo = Todo.objects.create(title="Original")
        client = Client()
        response = client.get(reverse("todo_update", args=[todo.pk]))
        assert response.status_code == 200

    def test_update_view_uses_correct_template(self):
        """Test that update view uses correct template."""
        todo = Todo.objects.create(title="Original")
        client = Client()
        response = client.get(reverse("todo_update", args=[todo.pk]))
        assert "todos/todo_form.html" in [t.name for t in response.templates]

    def test_update_view_post_valid_data(self):
        """Test updating a todo with valid data."""
        todo = Todo.objects.create(title="Original")
        client = Client()
        data = {"title": "Updated", "description": "Updated description"}
        response = client.post(reverse("todo_update", args=[todo.pk]), data)

        assert response.status_code == 302
        todo.refresh_from_db()
        assert todo.title == "Updated"

    def test_update_view_404_for_nonexistent_todo(self):
        """Test that update view returns 404 for nonexistent todo."""
        client = Client()
        response = client.get(reverse("todo_update", args=[999]))
        assert response.status_code == 404


@pytest.mark.django_db
class TestTodoDeleteView:
    """Test cases for TodoDeleteView."""

    def test_delete_view_status_code_200(self):
        """Test that delete view returns 200 status."""
        todo = Todo.objects.create(title="Test Todo")
        client = Client()
        response = client.get(reverse("todo_delete", args=[todo.pk]))
        assert response.status_code == 200

    def test_delete_view_uses_correct_template(self):
        """Test that delete view uses correct template."""
        todo = Todo.objects.create(title="Test Todo")
        client = Client()
        response = client.get(reverse("todo_delete", args=[todo.pk]))
        assert "todos/todo_confirm_delete.html" in [t.name for t in response.templates]

    def test_delete_view_post_deletes_todo(self):
        """Test that delete view removes todo from database."""
        todo = Todo.objects.create(title="Test Todo")
        todo_pk = todo.pk

        client = Client()
        response = client.post(reverse("todo_delete", args=[todo_pk]))

        assert response.status_code == 302
        assert not Todo.objects.filter(pk=todo_pk).exists()

    def test_delete_view_redirects_to_list(self):
        """Test that delete view redirects to list after deletion."""
        todo = Todo.objects.create(title="Test Todo")
        client = Client()
        response = client.post(reverse("todo_delete", args=[todo.pk]))
        assert response.url == reverse("todo_list")

    def test_delete_view_404_for_nonexistent_todo(self):
        """Test that delete view returns 404 for nonexistent todo."""
        client = Client()
        response = client.get(reverse("todo_delete", args=[999]))
        assert response.status_code == 404


@pytest.mark.django_db
class TestToggleTodoView:
    """Test cases for toggle_todo view."""

    def test_toggle_todo_changes_status(self):
        """Test that toggle changes completed status."""
        todo = Todo.objects.create(title="Test Todo", completed=False)
        client = Client()
        response = client.get(reverse("todo_toggle", args=[todo.pk]))

        assert response.status_code == 302
        todo.refresh_from_db()
        assert todo.completed is True

    def test_toggle_todo_back_to_incomplete(self):
        """Test toggling completed todo back to incomplete."""
        todo = Todo.objects.create(title="Test Todo", completed=True)
        client = Client()
        response = client.get(reverse("todo_toggle", args=[todo.pk]))

        todo.refresh_from_db()
        assert todo.completed is False

    def test_toggle_todo_redirects_to_list(self):
        """Test that toggle redirects to list."""
        todo = Todo.objects.create(title="Test Todo")
        client = Client()
        response = client.get(reverse("todo_toggle", args=[todo.pk]))
        assert response.url == reverse("todo_list")

    def test_toggle_todo_404_for_nonexistent(self):
        """Test toggle returns 404 for nonexistent todo."""
        client = Client()
        response = client.get(reverse("todo_toggle", args=[999]))
        assert response.status_code == 404
