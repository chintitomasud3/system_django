# System Backend Django

A Django backend application with task management and system monitoring capabilities.

## Features

- **Task Management** (`tasks` app): CRUD operations for task management with Kanban and List views
- **System Monitoring** (`system_info` app): Real-time system information display including CPU, memory, disk, and network stats

## Requirements

- Python 3.8+
- Django 4.2+
- psutil 5.9+

## Installation

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
python manage.py migrate
python manage.py runserver
```

## Apps

- `/tasks/` - Task management dashboard
- `/system/` - System information monitoring