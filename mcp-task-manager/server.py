import json
import os
from typing import Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Task Manager")
DATA_FILE = "tasks.json"


def load_tasks() -> list[dict[str, Any]]:
    """Load tasks from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks: list[dict[str, Any]]) -> None:
    """Save tasks to the JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)


def get_next_id(tasks: list[dict[str, Any]]) -> int:
    """Generate the next task ID."""
    return max((task["id"] for task in tasks), default=0) + 1


@mcp.tool()
def add_task(title: str, description: str = "", priority: str = "medium") -> str:
    """Create a new task with optional description and priority ('low', 'medium', 'high')."""
    if not isinstance(title, str):
        return "Error: Task title must be text."
    title = title.strip()
    if not title:
        return "Error: Task title cannot be empty."

    priority_normalized = priority.strip().lower() if isinstance(priority, str) else "medium"
    if priority_normalized not in ["low", "medium", "high"]:
        priority_normalized = "medium"

    tasks = load_tasks()
    new_task = {
        "id": get_next_id(tasks),
        "title": title,
        "description": description.strip() if isinstance(description, str) else "",
        "priority": priority_normalized,
        "completed": False,
    }
    tasks.append(new_task)
    save_tasks(tasks)

    return (
        f"Task created successfully.\n"
        f"ID: {new_task['id']}\n"
        f"Title: {new_task['title']}\n"
        f"Priority: {new_task['priority'].capitalize()}\n"
        f"Status: Pending"
    )


@mcp.tool()
def list_tasks() -> str:
    """List all tasks."""
    tasks = load_tasks()
    if not tasks:
        return "No tasks found."

    result = ["All Tasks:", ""]
    for task in tasks:
        status = "Completed" if task["completed"] else "Pending"
        priority = task.get("priority", "medium").capitalize()
        result.append(
            f"ID: {task['id']} | Title: {task['title']} | Priority: {priority} | Status: {status}"
        )
        if task["description"]:
            result.append(f"  Description: {task['description']}")
    return "\n".join(result)


@mcp.tool()
def get_task(task_id: int) -> str:
    """Get a single task by its ID."""
    if not isinstance(task_id, int):
        return "Error: Task ID must be an integer."

    for task in load_tasks():
        if task["id"] == task_id:
            status = "Completed" if task["completed"] else "Pending"
            priority = task.get("priority", "medium").capitalize()
            return (
                f"Task Details:\n"
                f"ID: {task['id']}\n"
                f"Title: {task['title']}\n"
                f"Description: {task['description'] or 'No description'}\n"
                f"Priority: {priority}\n"
                f"Status: {status}"
            )
    return f"Error: Task with ID {task_id} was not found."


@mcp.tool()
def update_task(task_id: int, title: str = "", description: str = "") -> str:
    """Update the title and/or description of an existing task."""
    if not isinstance(task_id, int):
        return "Error: Task ID must be an integer."

    title = title.strip() if isinstance(title, str) else ""
    description = description.strip() if isinstance(description, str) else ""

    if not title and not description:
        return "Error: Please provide a new title or description to update."

    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            if title:
                task["title"] = title
            if description:
                task["description"] = description
            save_tasks(tasks)
            return (
                f"Task {task_id} updated successfully.\n"
                f"Title: {task['title']}\n"
                f"Description: {task['description'] or 'No description'}\n"
                f"Priority: {task.get('priority', 'medium').capitalize()}\n"
                f"Status: {'Completed' if task['completed'] else 'Pending'}"
            )
    return f"Error: Task with ID {task_id} was not found."


@mcp.tool()
def set_priority(task_id: int, priority: str) -> str:
    """Set the priority of a task ('low', 'medium', or 'high')."""
    if not isinstance(task_id, int):
        return "Error: Task ID must be an integer."

    if not isinstance(priority, str):
        return "Error: Priority must be text."

    priority_normalized = priority.strip().lower()
    allowed_priorities = ["low", "medium", "high"]
    if priority_normalized not in allowed_priorities:
        return f"Error: Invalid priority '{priority}'. Allowed values are: low, medium, high."

    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["priority"] = priority_normalized
            save_tasks(tasks)
            return (
                f"Priority for task {task_id} updated successfully.\n"
                f"Title: {task['title']}\n"
                f"Priority: {priority_normalized.capitalize()}"
            )
    return f"Error: Task with ID {task_id} was not found."


@mcp.tool()
def complete_task(task_id: int) -> str:
    """Mark a task as completed."""
    if not isinstance(task_id, int):
        return "Error: Task ID must be an integer."

    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            if task["completed"]:
                return f"Task {task_id} is already completed."
            task["completed"] = True
            save_tasks(tasks)
            return (
                f"Task {task_id} completed successfully.\n"
                f"Title: {task['title']}"
            )
    return f"Error: Task with ID {task_id} was not found."


@mcp.tool()
def delete_task(task_id: int) -> str:
    """Delete a task."""
    if not isinstance(task_id, int):
        return "Error: Task ID must be an integer."

    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            return (
                f"Task deleted successfully.\n"
                f"ID: {task['id']}\n"
                f"Title: {task['title']}"
            )
    return f"Error: Task with ID {task_id} was not found."


@mcp.resource("tasks://pending")
def pending_tasks() -> str:
    """Read-only resource showing all pending tasks."""
    pending = [task for task in load_tasks() if not task["completed"]]
    if not pending:
        return "No pending tasks."

    result = ["Pending Tasks:", ""]
    for task in pending:
        priority = task.get("priority", "medium").capitalize()
        result.append(f"ID: {task['id']} | Title: {task['title']} | Priority: {priority}")
    return "\n".join(result)


@mcp.prompt()
def review_pending_tasks() -> str:
    """Prompt template to review and prioritize pending tasks."""
    pending = pending_tasks()
    return (
        f"Here are the current pending tasks:\n{pending}\n\n"
        "Please analyze these tasks, prioritize them from highest to lowest urgency, "
        "and suggest a concrete plan to tackle them."
    )


@mcp.prompt()
def break_down_task(task_id: int) -> str:
    """Prompt template to break down a specific task into sub-tasks."""
    task_details = get_task(task_id)
    return (
        f"Here are the task details:\n{task_details}\n\n"
        "Please break down this task into 3-5 smaller, actionable checklist items."
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
