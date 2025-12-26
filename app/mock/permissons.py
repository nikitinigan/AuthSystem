from app.exceptions import ProjectAccessDeniedException, ProjectNotFoundException
from .data import mock_projects, mock_tasks


def check_project_access(project_id: int, user_id: int, user_role: str):
    if project_id not in mock_projects:
        raise ProjectNotFoundException
    
    project = mock_projects[project_id]
    
    if user_role == "admin":
        return project
    
    elif user_role == "manager":
        if project["owner_id"] == user_id or user_id in project.get("team", []):
            return project
    
    elif project["owner_id"] == user_id:
        return project
    
    raise ProjectAccessDeniedException

def filter_projects_by_role(user_id: int, user_role: str):
    projects = list(mock_projects.values())
    
    if user_role == "admin":
        return projects
    
    elif user_role == "manager":
        return [
            p for p in projects 
            if p["owner_id"] == user_id or user_id in p.get("team", [])
        ]
    
    else:
        return [
            p for p in projects 
            if p["owner_id"] == user_id
        ]


def filter_tasks_by_role(user_id: int, user_role: str):
    tasks = list(mock_tasks.values())
    
    if user_role == "admin":
        return tasks
    
    elif user_role == "manager":
        manager_projects = [
            p_id for p_id, p in mock_projects.items()
            if p["owner_id"] == user_id or user_id in p.get("team", [])
        ]
        return [
            t for t in tasks 
            if t["project_id"] in manager_projects
        ]
    
    else:
        return [
            t for t in tasks 
            if t["assignee_id"] == user_id or t.get("creator_id") == user_id
        ]