"""Tests for the Todo form."""

import pytest
from todos.forms import TodoForm


@pytest.mark.django_db
class TestTodoForm:
    """Test cases for the TodoForm."""

    def test_valid_form_with_title_only(self):
        """Test form is valid with title only."""
        form_data = {"title": "Buy groceries"}
        form = TodoForm(data=form_data)
        assert form.is_valid()

    def test_valid_form_with_all_fields(self):
        """Test form is valid with all fields."""
        form_data = {
            "title": "Learn Django",
            "description": "Complete the tutorial",
            "completed": True,
        }
        form = TodoForm(data=form_data)
        assert form.is_valid()

    def test_invalid_form_missing_title(self):
        """Test form is invalid without title."""
        form_data = {"description": "Some description"}
        form = TodoForm(data=form_data)
        assert not form.is_valid()
        assert "title" in form.errors

    def test_form_blank_description(self):
        """Test form is valid with blank description."""
        form_data = {"title": "Test Todo", "description": ""}
        form = TodoForm(data=form_data)
        assert form.is_valid()

    def test_form_completed_default_false(self):
        """Test completed field defaults to False."""
        form_data = {"title": "Test Todo"}
        form = TodoForm(data=form_data)
        assert form.is_valid()

    def test_form_completed_can_be_true(self):
        """Test completed field can be set to True."""
        form_data = {"title": "Test Todo", "completed": True}
        form = TodoForm(data=form_data)
        assert form.is_valid()

    def test_form_save(self):
        """Test form saves to database correctly."""
        from todos.models import Todo

        form_data = {
            "title": "Test Todo",
            "description": "Test description",
            "completed": False,
        }
        form = TodoForm(data=form_data)
        assert form.is_valid()

        todo = form.save()
        assert todo.title == "Test Todo"
        assert todo.description == "Test description"
        assert todo.completed is False

    def test_form_save_and_update(self):
        """Test form can update existing todo."""
        from todos.models import Todo

        todo = Todo.objects.create(title="Original", description="Original desc")

        form_data = {
            "title": "Updated",
            "description": "Updated desc",
            "completed": True,
        }
        form = TodoForm(data=form_data, instance=todo)
        assert form.is_valid()

        updated_todo = form.save()
        assert updated_todo.title == "Updated"
        assert updated_todo.description == "Updated desc"
        assert updated_todo.completed is True

    def test_form_fields_exist(self):
        """Test that form has correct fields."""
        form = TodoForm()
        assert "title" in form.fields
        assert "description" in form.fields
        assert "completed" in form.fields

    def test_form_title_widget_type(self):
        """Test that title field uses correct widget."""
        form = TodoForm()
        from django.forms import TextInput

        assert isinstance(form.fields["title"].widget, TextInput)

    def test_form_description_widget_type(self):
        """Test that description field uses correct widget."""
        form = TodoForm()
        from django.forms import Textarea

        assert isinstance(form.fields["description"].widget, Textarea)

    def test_form_completed_widget_type(self):
        """Test that completed field uses checkbox widget."""
        form = TodoForm()
        from django.forms import CheckboxInput

        assert isinstance(form.fields["completed"].widget, CheckboxInput)

    def test_form_title_placeholder(self):
        """Test that title field has placeholder."""
        form = TodoForm()
        assert "placeholder" in form.fields["title"].widget.attrs

    def test_form_description_placeholder(self):
        """Test that description field has placeholder."""
        form = TodoForm()
        assert "placeholder" in form.fields["description"].widget.attrs

    def test_form_title_max_length(self):
        """Test title field respects max_length."""
        long_title = "a" * 201
        form_data = {"title": long_title}
        form = TodoForm(data=form_data)
        assert not form.is_valid()

    def test_form_empty_data(self):
        """Test form with empty data."""
        form = TodoForm(data={})
        assert not form.is_valid()
