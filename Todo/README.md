# Todo Application

A simple yet elegant Todo application built with **Django** and **Python**. Manage your tasks efficiently with a clean and intuitive interface.

## Features

✨ **Core Features:**
- ✅ Create, read, update, and delete todos
- 📝 Add titles and detailed descriptions
- ✔️ Mark todos as complete/incomplete
- 📅 Track creation and update timestamps
- 🎯 Pagination support for large todo lists
- 🔐 Django Admin interface for advanced management

## Tech Stack

- **Backend:** Django 5.2
- **Database:** SQLite (default)
- **Frontend:** Bootstrap 5
- **Package Manager:** uv (Python)

## Quick Start

### 1. Clone and Setup

```bash
cd /home/mangino/Documents/DataTalks/Todo
source .venv/bin/activate
```

### 2. Run Migrations

```bash
python manage.py migrate
```

### 3. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

### 4. Start Development Server

```bash
python manage.py runserver
```

The application will be available at:
- **Todo App:** http://127.0.0.1:8000/todos/
- **Django Admin:** http://127.0.0.1:8000/admin/

## Project Structure

```
.
├── .venv/                          # Virtual environment
├── todo_project/                   # Main Django project
│   ├── settings.py                 # Project settings
│   ├── urls.py                     # Main URL configuration
│   └── wsgi.py                     # WSGI config
├── todos/                          # Todo app
│   ├── models.py                   # Todo model definition
│   ├── views.py                    # CRUD views
│   ├── forms.py                    # Todo form
│   ├── urls.py                     # App URL patterns
│   ├── admin.py                    # Admin configuration
│   ├── migrations/                 # Database migrations
│   └── templates/todos/            # HTML templates
│       ├── base.html               # Base template
│       ├── todo_list.html          # Todo list view
│       ├── todo_detail.html        # Todo detail view
│       ├── todo_form.html          # Create/edit form
│       └── todo_confirm_delete.html # Delete confirmation
├── manage.py                       # Django management script
└── db.sqlite3                      # SQLite database
```

## Usage

### View All Todos
Navigate to http://127.0.0.1:8000/todos/ to see all your todos.

### Create a New Todo
Click the "➕ Add Todo" button and fill in the form.

### Edit a Todo
Click "Edit" on any todo to modify its title, description, or completion status.

### Mark as Complete/Incomplete
Click "Mark Complete" or "Mark Incomplete" to toggle the status.

### Delete a Todo
Click "Delete" and confirm the deletion.

## Testing

This application includes comprehensive test coverage with **70 tests** and **98% code coverage**.

### Run All Tests

```bash
source .venv/bin/activate
pytest todos/tests/ -v
```

### Run Tests with Coverage Report

```bash
./run_tests.sh
# or
pytest todos/tests/ --cov=todos --cov-report=html --cov-report=term-missing
```

### Test Statistics

- **Total Tests:** 70
- **Pass Rate:** 100% ✅
- **Code Coverage:** 98%
- **Test Types:**
  - 19 Model tests
  - 16 Form tests
  - 30 View tests
  - 9 Integration tests

### View Coverage Report

```bash
open htmlcov/index.html
```

For detailed testing documentation, see [TESTING.md](TESTING.md)

## Admin Panel

Access the Django admin at http://127.0.0.1:8000/admin/ with your superuser credentials.

Features:
- View all todos
- Filter by completion status and creation date
- Search todos by title or description
- Bulk edit operations

## API Views

The application provides the following URL patterns:

| URL | View | Name |
|-----|------|------|
| `/todos/` | TodoListView | `todo_list` |
| `/todos/todo/<id>/` | TodoDetailView | `todo_detail` |
| `/todos/create/` | TodoCreateView | `todo_create` |
| `/todos/todo/<id>/update/` | TodoUpdateView | `todo_update` |
| `/todos/todo/<id>/delete/` | TodoDeleteView | `todo_delete` |
| `/todos/todo/<id>/toggle/` | toggle_todo | `todo_toggle` |

## Installation & Development

### Install Dependencies with uv

```bash
# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate

# Install Django
uv pip install django
```

### Create Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Database

The application uses **SQLite** by default. The database file is `db.sqlite3`.

To reset the database:
```bash
python manage.py flush
```

## Customization

### Models
Edit `todos/models.py` to add more fields or modify the Todo model.

### Views
Edit `todos/views.py` to change view logic or add new views.

### Templates
Edit templates in `todos/templates/todos/` to customize the UI.

### Settings
Edit `todo_project/settings.py` for project-wide configurations.

## Security Notes

⚠️ **Important:**
- Change `SECRET_KEY` in `todo_project/settings.py` for production
- Set `DEBUG = False` in production
- Use environment variables for sensitive data
- Set up proper `ALLOWED_HOSTS` in production

## Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Static Files Not Loading
```bash
python manage.py collectstatic
```

### Database Issues
```bash
python manage.py migrate --run-syncdb
```

## Future Enhancements

- 📱 Mobile app version
- 🔔 Todo notifications and reminders
- 👥 Multi-user support with authentication
- 🏷️ Categories and tags
- 🔍 Advanced filtering and search
- 📊 Statistics and dashboard
- 🌙 Dark mode theme

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please check the Django documentation:
- [Django Official Documentation](https://docs.djangoproject.com/)
- [Django Models](https://docs.djangoproject.com/en/5.2/topics/db/models/)
- [Django Views](https://docs.djangoproject.com/en/5.2/topics/http/views/)
