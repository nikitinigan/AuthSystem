from datetime import datetime, timedelta


mock_projects = {
    1: {
        "id": 1,
        "name": "Разработка API",
        "description": "Создание системы аутентификации",
        "owner_id": 1,  
        "status": "active",
        "created_at": datetime.now() - timedelta(days=30),
        "budget": 50000,
        "team": [1, 2, 3]
    },
    2: {
        "id": 2,
        "name": "Маркетинг Q2",
        "description": "Рекламная кампания",
        "owner_id": 2,
        "status": "planning",
        "created_at": datetime.now() - timedelta(days=15),
        "budget": 15000,
        "team": [2, 4, 5]
    },
}

mock_tasks = {
    1: {
        "id": 1,
        "title": "Написать документацию API",
        "project_id": 1,
        "assignee_id": 2,
        "creator_id": 1,
        "status": "in_progress",
        "priority": "high",
        "due_date": datetime.now() + timedelta(days=7)
    },
    2: {
        "id": 2,
        "title": "Миграции БД",
        "project_id": 1,
        "assignee_id": 3,
        "creator_id": 1,
        "status": "completed",
        "priority": "medium",
        "due_date": datetime.now() - timedelta(days=1)
    },
}

mock_reports = {
    1: {
        "id": 1,
        "name": "Еженедельный отчет",
        "project_id": 1,
        "author_id": 2,
        "content": "Выполнено 80% задач",
        "created_at": datetime.now() - timedelta(days=1),
        "is_confidential": False
    },
}