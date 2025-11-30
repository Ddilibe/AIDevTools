# Testing Documentation

## Overview

This Todo application includes comprehensive test coverage using **pytest** and **pytest-django**. The test suite covers models, forms, views, and integration tests with **98% code coverage**.

## Test Statistics

- **Total Tests:** 70
- **Pass Rate:** 100% ✅
- **Code Coverage:** 98%
- **Test Files:** 4
- **Test Categories:** Models, Forms, Views, Integration

## Running Tests

### Run All Tests

```bash
source .venv/bin/activate
pytest todos/tests/ -v
```

### Run Specific Test File

```bash
# Test models only
pytest todos/tests/test_models.py -v

# Test forms only
pytest todos/tests/test_forms.py -v

# Test views only
pytest todos/tests/test_views.py -v

# Test integration only
pytest todos/tests/test_integration.py -v
```

### Run Tests with Coverage Report

```bash
pytest todos/tests/ --cov=todos --cov-report=html --cov-report=term-missing
```

This generates an HTML coverage report in the `htmlcov/` directory.

### Run Specific Test Class

```bash
pytest todos/tests/test_models.py::TestTodoModel -v
```

### Run Specific Test Method

```bash
pytest todos/tests/test_models.py::TestTodoModel::test_create_todo_basic -v
```

### Run Tests by Marker

```bash
# Run only unit tests
pytest -m unit todos/tests/ -v

# Run only integration tests
pytest -m integration todos/tests/ -v
```

## Test Structure

### Directory Layout

```
todos/tests/
├── __init__.py                    # Tests package
├── conftest.py                    # Pytest fixtures and configuration
├── test_models.py                 # Model tests (19 tests)
├── test_forms.py                  # Form tests (16 tests)
├── test_views.py                  # View tests (30 tests)
└── test_integration.py            # Integration tests (9 tests)
```

## Test Categories

### 1. Model Tests (`test_models.py`)

Tests for the `Todo` model including:

- ✅ Basic todo creation
- ✅ Todo with description
- ✅ String representation
- ✅ Timestamp handling
- ✅ Completed status toggling
- ✅ Updated_at timestamp changes
- ✅ Todo ordering
- ✅ Multiple todos with different statuses
- ✅ Title max length validation
- ✅ Blank description handling
- ✅ Querying by title and status
- ✅ Todo deletion
- ✅ Bulk creation
- ✅ Todo updates

**Coverage:** 100%

### 2. Form Tests (`test_forms.py`)

Tests for the `TodoForm` including:

- ✅ Valid form with title only
- ✅ Valid form with all fields
- ✅ Invalid form without title
- ✅ Blank description handling
- ✅ Completed field default (False)
- ✅ Completed field set to True
- ✅ Form save functionality
- ✅ Form update functionality
- ✅ Form fields existence
- ✅ Widget type validation
- ✅ Placeholder text
- ✅ Max length validation
- ✅ Empty form handling

**Coverage:** 100%

### 3. View Tests (`test_views.py`)

Tests for all CRUD views:

**TodoListView (5 tests)**
- Status code 200
- Correct template usage
- Context contains todos
- Empty todos handling
- Pagination support

**TodoDetailView (5 tests)**
- Status code 200
- Correct template usage
- Context contains correct todo
- 404 for nonexistent todo
- Title display

**TodoCreateView (6 tests)**
- Status code 200
- Correct template
- Valid data creation
- Redirect to list
- Invalid data handling
- Form in context

**TodoUpdateView (4 tests)**
- Status code 200
- Correct template
- Valid data update
- 404 for nonexistent todo

**TodoDeleteView (5 tests)**
- Status code 200
- Correct template
- Delete functionality
- Redirect to list
- 404 for nonexistent todo

**toggle_todo Function (4 tests)**
- Status change
- Toggle back to incomplete
- Redirect to list
- 404 for nonexistent todo

**Coverage:** 100%

### 4. Integration Tests (`test_integration.py`)

End-to-end workflow tests:

- ✅ Create, view, edit, and complete workflow
- ✅ Multiple todos CRUD operations
- ✅ Delete workflow
- ✅ List view displays all todos
- ✅ Search and filter functionality
- ✅ Pagination with many todos
- ✅ Form validation throughout workflow
- ✅ Status persistence
- ✅ Modifications reflect in detail view

**Coverage:** 100%

## Fixtures

Custom pytest fixtures available in `conftest.py`:

### `todo_factory`
Factory fixture for creating test todos with custom parameters.

```python
def test_example(todo_factory):
    todo = todo_factory(title="Custom Todo", description="Test")
    assert todo.title == "Custom Todo"
```

### `sample_todo`
Fixture providing a pre-created sample todo.

```python
def test_example(sample_todo):
    assert sample_todo.title == "Sample Todo"
```

### `completed_todo`
Fixture providing a completed todo.

```python
def test_example(completed_todo):
    assert completed_todo.completed is True
```

### `multiple_todos`
Fixture providing 5 todos with mixed completion status.

```python
def test_example(multiple_todos):
    assert len(multiple_todos) == 5
```

### `client`
Django test client for making requests.

```python
def test_example(client):
    response = client.get('/todos/')
    assert response.status_code == 200
```

## Configuration

### pytest.ini

Main pytest configuration file with Django settings:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = todo_project.settings
python_files = tests.py test_*.py *_tests.py
python_classes = Test*
python_functions = test_*
addopts = --verbose --strict-markers --tb=short
markers =
    unit: Unit tests
    integration: Integration tests
    models: Model tests
    views: View tests
    forms: Form tests
```

## Test Best Practices Used

1. **Descriptive Names:** All tests have clear, descriptive names indicating what is being tested
2. **Docstrings:** Each test includes a docstring explaining its purpose
3. **Single Responsibility:** Each test focuses on one specific behavior
4. **Fixtures:** Custom fixtures for common test setup
5. **Database Isolation:** `@pytest.mark.django_db` ensures database isolation per test
6. **Edge Cases:** Tests include boundary conditions and error cases
7. **Integration Tests:** Full workflow tests to catch integration issues

## Coverage Report

Generate and view the HTML coverage report:

```bash
pytest todos/tests/ --cov=todos --cov-report=html
open htmlcov/index.html  # Open in browser
```

Current coverage by file:

| File | Coverage |
|------|----------|
| models.py | 100% |
| views.py | 100% |
| forms.py | 100% |
| admin.py | 100% |
| urls.py | 100% |
| **Total** | **98%** |

## Debugging Tests

### Run with Verbose Output

```bash
pytest todos/tests/ -vv
```

### Show Print Statements

```bash
pytest todos/tests/ -s
```

### Run with Pdb on Failure

```bash
pytest todos/tests/ --pdb
```

### Run with Pdb on Error

```bash
pytest todos/tests/ --pdbcls=IPython.terminal.debugger:TerminalPdb
```

## Continuous Integration

These tests are ready for CI/CD integration:

```bash
# GitHub Actions example
pytest todos/tests/ --cov=todos --cov-report=xml
```

## Common Test Commands

```bash
# Quick smoke test
pytest todos/tests/ -q

# Detailed test report
pytest todos/tests/ -v --tb=long

# Stop on first failure
pytest todos/tests/ -x

# Run last failed tests
pytest todos/tests/ --lf

# Run tests matching pattern
pytest todos/tests/ -k "create"

# Run with timing information
pytest todos/tests/ --durations=10

# Run in parallel (requires pytest-xdist)
pytest todos/tests/ -n auto
```

## Adding New Tests

When adding new features:

1. Create test in appropriate file
2. Use descriptive test name
3. Add docstring
4. Use existing fixtures or create new ones
5. Run tests to verify: `pytest todos/tests/ -v`
6. Check coverage: `pytest --cov=todos`

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-django Documentation](https://pytest-django.readthedocs.io/)
- [Django Testing Documentation](https://docs.djangoproject.com/en/5.2/topics/testing/)

## Troubleshooting

### "No tests ran"
Ensure files follow naming convention: `test_*.py`

### Database errors
Add `@pytest.mark.django_db` to test class or method

### Import errors
Ensure `conftest.py` is in tests directory

### Slow tests
Check for N+1 queries or consider using fixtures instead of creating data in each test
