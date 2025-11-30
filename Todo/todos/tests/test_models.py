"""Tests for the Todo model."""

import pytest
from datetime import datetime
from todos.models import Todo


@pytest.mark.django_db
class TestTodoModel:
    """Test cases for the Todo model."""

    def test_create_todo_basic(self):
        """Test creating a basic todo with title only."""
        todo = Todo.objects.create(title="Buy groceries")

        assert todo.id is not None
        assert todo.title == "Buy groceries"
        assert todo.description == ""
        assert todo.completed is False

    def test_create_todo_with_description(self):
        """Test creating a todo with title and description."""
        todo = Todo.objects.create(
            title="Learn Django",
            description="Complete the Django tutorial and build a project",
        )

        assert todo.title == "Learn Django"
        assert todo.description == "Complete the Django tutorial and build a project"
        assert todo.completed is False

    def test_todo_string_representation(self):
        """Test the string representation of a todo."""
        todo = Todo.objects.create(title="Test Todo")
        assert str(todo) == "Test Todo"

    def test_todo_timestamps(self):
        """Test that timestamps are set correctly."""
        todo = Todo.objects.create(title="Test Todo")

        assert todo.created_at is not None
        assert todo.updated_at is not None
        assert isinstance(todo.created_at, datetime)
        assert isinstance(todo.updated_at, datetime)

    def test_todo_created_updated_same_on_creation(self):
        """Test that created_at and updated_at are the same on creation."""
        todo = Todo.objects.create(title="Test Todo")
        # Allow for small time differences due to processing
        time_diff = (todo.updated_at - todo.created_at).total_seconds()
        assert time_diff < 1

    def test_toggle_todo_completed(self):
        """Test toggling the completed status."""
        todo = Todo.objects.create(title="Test Todo")
        assert todo.completed is False

        todo.completed = True
        todo.save()

        todo.refresh_from_db()
        assert todo.completed is True

    def test_todo_updated_at_changes_on_update(self):
        """Test that updated_at changes when todo is modified."""
        import time

        todo = Todo.objects.create(title="Test Todo")
        original_updated_at = todo.updated_at

        time.sleep(0.01)  # Ensure time difference
        todo.title = "Updated Todo"
        todo.save()

        assert todo.updated_at > original_updated_at

    def test_todo_ordering(self):
        """Test that todos are ordered by created_at (newest first)."""
        todo1 = Todo.objects.create(title="Todo 1")
        todo2 = Todo.objects.create(title="Todo 2")
        todo3 = Todo.objects.create(title="Todo 3")

        todos = list(Todo.objects.all())
        assert todos[0].id == todo3.id
        assert todos[1].id == todo2.id
        assert todos[2].id == todo1.id

    def test_multiple_todos_with_different_statuses(self):
        """Test creating multiple todos with different statuses."""
        todo1 = Todo.objects.create(title="Todo 1", completed=False)
        todo2 = Todo.objects.create(title="Todo 2", completed=True)
        todo3 = Todo.objects.create(title="Todo 3", completed=False)

        assert Todo.objects.filter(completed=False).count() == 2
        assert Todo.objects.filter(completed=True).count() == 1

    def test_todo_max_title_length(self):
        """Test that title field has max_length of 200."""
        long_title = "a" * 200
        todo = Todo.objects.create(title=long_title)
        assert len(todo.title) == 200

    def test_todo_blank_description(self):
        """Test that description can be blank."""
        todo = Todo.objects.create(title="Test", description="")
        assert todo.description == ""

    def test_todo_query_by_title(self):
        """Test querying todos by title."""
        Todo.objects.create(title="Python Learning")
        Todo.objects.create(title="Django Mastery")

        python_todos = Todo.objects.filter(title__icontains="Python")
        assert python_todos.count() == 1
        assert python_todos.first().title == "Python Learning"

    def test_todo_query_by_completed_status(self):
        """Test querying todos by completed status."""
        Todo.objects.create(title="Todo 1", completed=True)
        Todo.objects.create(title="Todo 2", completed=False)
        Todo.objects.create(title="Todo 3", completed=True)

        completed = Todo.objects.filter(completed=True)
        pending = Todo.objects.filter(completed=False)

        assert completed.count() == 2
        assert pending.count() == 1

    def test_delete_todo(self):
        """Test deleting a todo."""
        todo = Todo.objects.create(title="Test Todo")
        todo_id = todo.id

        todo.delete()

        with pytest.raises(Todo.DoesNotExist):
            Todo.objects.get(id=todo_id)

    def test_bulk_create_todos(self):
        """Test creating multiple todos in bulk."""
        todos = [
            Todo(title="Todo 1"),
            Todo(title="Todo 2"),
            Todo(title="Todo 3"),
        ]
        Todo.objects.bulk_create(todos)

        assert Todo.objects.count() == 3

    def test_todo_update(self):
        """Test updating a todo."""
        todo = Todo.objects.create(title="Original Title", description="Original")

        todo.title = "Updated Title"
        todo.description = "Updated Description"
        todo.save()

        todo.refresh_from_db()
        assert todo.title == "Updated Title"
        assert todo.description == "Updated Description"
