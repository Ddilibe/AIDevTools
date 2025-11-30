"""Pytest configuration and fixtures."""

import pytest
from todos.models import Todo


@pytest.fixture
def todo_factory():
    """Factory fixture for creating test todos."""

    def create_todo(title="Test Todo", description="", completed=False):
        return Todo.objects.create(
            title=title,
            description=description,
            completed=completed,
        )

    return create_todo


@pytest.fixture
def sample_todo(db):
    """Fixture that creates a sample todo."""
    return Todo.objects.create(
        title="Sample Todo",
        description="This is a sample todo for testing",
        completed=False,
    )


@pytest.fixture
def completed_todo(db):
    """Fixture that creates a completed todo."""
    return Todo.objects.create(
        title="Completed Todo",
        description="This is a completed todo",
        completed=True,
    )


@pytest.fixture
def multiple_todos(db):
    """Fixture that creates multiple todos."""
    todos = []
    for i in range(5):
        todo = Todo.objects.create(
            title=f"Todo {i+1}",
            description=f"Description {i+1}",
            completed=(i % 2 == 0),
        )
        todos.append(todo)
    return todos


@pytest.fixture
def client():
    """Fixture for Django test client."""
    from django.test import Client

    return Client()
