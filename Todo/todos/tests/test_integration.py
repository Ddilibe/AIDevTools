"""Integration tests for the Todo application."""

import pytest
from django.test import Client
from django.urls import reverse
from todos.models import Todo


@pytest.mark.django_db
class TestTodoIntegration:
    """Integration tests for complete todo workflows."""

    def test_create_view_edit_and_complete_workflow(self):
        """Test complete workflow: create, view, edit, and complete todo."""
        client = Client()

        # Step 1: Create a todo
        create_data = {"title": "Learn Django", "description": "Complete the tutorial"}
        response = client.post(reverse("todo_create"), create_data)
        assert response.status_code == 302

        # Step 2: Verify todo was created
        todo = Todo.objects.get(title="Learn Django")
        assert todo.completed is False

        # Step 3: View the todo
        response = client.get(reverse("todo_detail", args=[todo.pk]))
        assert response.status_code == 200
        assert "Learn Django" in response.content.decode()

        # Step 4: Update the todo
        update_data = {
            "title": "Learn Django Advanced",
            "description": "Complete advanced tutorial",
            "completed": False,
        }
        response = client.post(reverse("todo_update", args=[todo.pk]), update_data)
        assert response.status_code == 302

        todo.refresh_from_db()
        assert todo.title == "Learn Django Advanced"

        # Step 5: Mark as complete
        response = client.get(reverse("todo_toggle", args=[todo.pk]))
        assert response.status_code == 302

        todo.refresh_from_db()
        assert todo.completed is True

    def test_multiple_todos_crud_operations(self):
        """Test CRUD operations with multiple todos."""
        client = Client()

        # Create multiple todos
        todos_data = [
            {"title": "Todo 1", "description": "First task"},
            {"title": "Todo 2", "description": "Second task"},
            {"title": "Todo 3", "description": "Third task"},
        ]

        for data in todos_data:
            response = client.post(reverse("todo_create"), data)
            assert response.status_code == 302

        # Verify all todos exist
        assert Todo.objects.count() == 3

        # Mark first and third as complete
        todos = Todo.objects.all().order_by("title")
        client.get(reverse("todo_toggle", args=[todos[0].pk]))
        client.get(reverse("todo_toggle", args=[todos[2].pk]))

        # Verify status
        completed = Todo.objects.filter(completed=True).count()
        pending = Todo.objects.filter(completed=False).count()
        assert completed == 2
        assert pending == 1

    def test_delete_workflow(self):
        """Test deletion workflow."""
        client = Client()

        # Create a todo
        response = client.post(reverse("todo_create"), {"title": "Todo to delete"})
        todo = Todo.objects.get(title="Todo to delete")
        todo_pk = todo.pk

        # Get delete confirmation page
        response = client.get(reverse("todo_delete", args=[todo_pk]))
        assert response.status_code == 200
        assert "Delete" in response.content.decode()

        # Confirm deletion
        response = client.post(reverse("todo_delete", args=[todo_pk]))
        assert response.status_code == 302

        # Verify deletion
        assert not Todo.objects.filter(pk=todo_pk).exists()

    def test_list_view_shows_all_todos(self):
        """Test that list view displays all created todos."""
        client = Client()

        # Create todos
        todos = [
            {"title": "Work Task", "description": "Complete report"},
            {"title": "Personal Task", "description": "Buy groceries"},
        ]

        for data in todos:
            client.post(reverse("todo_create"), data)

        # View list
        response = client.get(reverse("todo_list"))
        content = response.content.decode()

        assert "Work Task" in content
        assert "Personal Task" in content

    def test_search_and_filter_functionality(self):
        """Test searching for todos by title."""
        # Create todos
        Todo.objects.create(title="Python Learning", description="Learn Python")
        Todo.objects.create(title="Django Tutorial", description="Learn Django")
        Todo.objects.create(title="Python Django", description="Full stack")

        # Search for Python
        python_todos = Todo.objects.filter(title__icontains="Python")
        assert python_todos.count() == 2

        # Search for Django
        django_todos = Todo.objects.filter(title__icontains="Django")
        assert django_todos.count() == 2

    def test_pagination_with_many_todos(self):
        """Test pagination functionality with many todos."""
        client = Client()

        # Create 25 todos (more than 10 per page)
        for i in range(25):
            client.post(
                reverse("todo_create"),
                {"title": f"Todo {i+1}", "description": f"Description {i+1}"},
            )

        # Get first page
        response = client.get(reverse("todo_list"))
        assert response.status_code == 200
        assert response.context["is_paginated"] is True
        assert len(response.context["todos"]) == 10

        # Get second page
        response = client.get(reverse("todo_list") + "?page=2")
        assert response.status_code == 200
        assert len(response.context["todos"]) == 10

    def test_form_validation_in_workflow(self):
        """Test form validation throughout workflow."""
        client = Client()

        # Try to create todo without title
        response = client.post(
            reverse("todo_create"), {"description": "No title provided"}
        )
        assert response.status_code == 200
        assert Todo.objects.count() == 0

        # Create valid todo
        response = client.post(
            reverse("todo_create"), {"title": "Valid Todo", "description": "With title"}
        )
        assert response.status_code == 302
        assert Todo.objects.count() == 1

    def test_status_persistence(self):
        """Test that todo completion status persists."""
        client = Client()

        # Create and complete a todo
        client.post(reverse("todo_create"), {"title": "Test Todo"})
        todo = Todo.objects.get(title="Test Todo")

        # Toggle completion multiple times
        for i in range(3):
            client.get(reverse("todo_toggle", args=[todo.pk]))
            todo.refresh_from_db()
            expected_status = (i + 1) % 2 == 1
            assert todo.completed == expected_status

    def test_modification_reflects_in_detail_view(self):
        """Test that modifications appear in detail view."""
        client = Client()

        # Create todo
        client.post(reverse("todo_create"), {"title": "Original"})
        todo = Todo.objects.get(title="Original")

        # View detail
        response = client.get(reverse("todo_detail", args=[todo.pk]))
        assert "Original" in response.content.decode()

        # Update todo
        client.post(
            reverse("todo_update", args=[todo.pk]),
            {"title": "Updated", "description": "New description"},
        )

        # View detail again
        response = client.get(reverse("todo_detail", args=[todo.pk]))
        assert "Updated" in response.content.decode()
        assert "New description" in response.content.decode()
