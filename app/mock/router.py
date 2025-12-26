from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
from app.exceptions import ProjectNotFoundException
from app.users.dependencies import get_current_user, require_roles
from app.mock.data import mock_projects, mock_tasks, mock_reports
from app.mock.permissons import (
    check_project_access,
    filter_projects_by_role,
    filter_tasks_by_role,
)

router_mock = APIRouter(
    prefix="/mock",
    tags=["Тестовые Данные"],
)

@router_mock.get("/projects")
async def get_projects(current_user = Depends(get_current_user)):
    return filter_projects_by_role(current_user.id, current_user.role)

@router_mock.get("/projects/{project_id}")
async def get_project(
    project_id: int,
    current_user = Depends(get_current_user)
):
    return check_project_access(project_id, current_user.id, current_user.role)

@router_mock.post("/projects")
async def create_project(
    project_data: dict,
    current_user = Depends(require_roles(["admin", "manager"]))
):
    """Создать проект (только менеджеры и админы)"""
    new_id = max(mock_projects.keys()) + 1 if mock_projects else 1
    mock_projects[new_id] = {
        "id": new_id,
        "name": project_data.get("name", "Новый проект"),
        "description": project_data.get("description", ""),
        "owner_id": current_user.id,
        "status": "planning",
        "created_at": datetime.now(),
        "budget": project_data.get("budget", 0),
        "team": [current_user.id]
    }
    return {"id": new_id, "message": "Проект создан"}

@router_mock.delete("/projects/{project_id}")
async def delete_project(
    project_id: int,
    current_user = Depends(require_roles("admin"))
):
    """Удалить проект (только админ)"""
    if project_id not in mock_projects:
        raise ProjectNotFoundException
    
    del mock_projects[project_id]
    return {"message": f"Проект {project_id} удален"}

@router_mock.get("/tasks")
async def get_tasks(current_user = Depends(get_current_user)):
    """Получить задачи (фильтрация по роли)"""
    return filter_tasks_by_role(current_user.id, current_user.role)

@router_mock.post("/tasks")
async def create_task(
    task_data: dict,
    current_user = Depends(get_current_user)
):
    """Создать задачу (только если есть доступ к проекту)"""
    project_id = task_data.get("project_id")
    
    check_project_access(project_id, current_user.id, current_user.role)
    new_id = max(mock_tasks.keys()) + 1 if mock_tasks else 1
    mock_tasks[new_id] = {
        "id": new_id,
        "title": task_data.get("title", "Новая задача"),
        "project_id": project_id,
        "assignee_id": task_data.get("assignee_id", current_user.id),
        "creator_id": current_user.id,
        "status": "todo",
        "priority": task_data.get("priority", "medium"),
        "due_date": datetime.now() + timedelta(days=7)
    }
    return {"id": new_id, "message": "Задача создана"}

@router_mock.get("/reports")
async def get_reports(current_user = Depends(require_roles(["admin", "manager"]))):
    """Получить отчеты (только менеджеры и админы)"""
    return list(mock_reports.values())

@router_mock.post("/reports")
async def create_report(
    report_data: dict,
    current_user = Depends(require_roles(["admin", "manager"]))
):
    """Создать отчет (только менеджеры и админы)"""
    new_id = max(mock_reports.keys()) + 1 if mock_reports else 1
    mock_reports[new_id] = {
        "id": new_id,
        "name": report_data.get("name", "Без названия"),
        "project_id": report_data.get("project_id"),
        "author_id": current_user.id,
        "content": report_data.get("content", ""),
        "created_at": datetime.now(),
        "is_confidential": report_data.get("is_confidential", False)
    }
    return {"id": new_id, "message": "Отчет создан"}