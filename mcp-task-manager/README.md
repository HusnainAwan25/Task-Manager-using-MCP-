# MCP Task Manager

A beginner-friendly Model Context Protocol (MCP) server for managing tasks.

## Features

Tools:

1. `add_task` - Create a new task (with title, description, priority).
2. `list_tasks` - List all tasks with status and priority.
3. `get_task` - Get one task by ID.
4. `update_task` - Update the title and/or description of a task.
5. `set_priority` - Set task priority (`low`, `medium`, `high`).
6. `complete_task` - Mark a task as completed.
7. `delete_task` - Delete a task.

Bonus resource:

- `tasks://pending` - Read-only list of pending tasks.

Prompts:

- `review_pending_tasks` - Review and prioritize all pending tasks.
- `break_down_task` - Break down a specific task into actionable sub-tasks.

## Technology

- Python 3.10+
- MCP Python SDK
- JSON file storage
- stdio transport
- MCP Inspector

## Installation

### Windows PowerShell

```powershell
python --version
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Mac/Linux

```bash
python3 --version
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python server.py
```

The server uses MCP stdio transport and is intended to be connected to an MCP client/Inspector.

## Tool Examples

### add_task

Inputs:
- `title`: text, required
- `description`: text, optional

Example:
```text
title: Complete MCP Lab
description: Finish the Task Manager assignment
```

### list_tasks

No input.

### get_task

Input:
```text
task_id: 1
```

### update_task

Inputs:
- `task_id`: integer, required
- `title`: text, optional
- `description`: text, optional

Example:
```text
task_id: 1
title: Updated Task Title
description: Updated description details
```

### set_priority

Inputs:
- `task_id`: integer, required
- `priority`: text, required (`low`, `medium`, or `high`)

Example:
```text
task_id: 1
priority: high
```

### complete_task

Input:
```text
task_id: 1
```

### delete_task

Input:
```text
task_id: 1
```

## Error Handling

The server returns clear messages for:
- Empty titles
- Invalid task IDs
- Non-existent task IDs
- Already completed tasks

The server stores data in `tasks.json`; no database or cloud service is required.

## Suggested Demo

1. Connect the server to MCP Inspector.
2. Show all five tools.
3. Add a task.
4. List tasks.
5. Get the task by ID.
6. Complete the task.
7. List tasks again.
8. Demonstrate an invalid task ID.
9. Show the `tasks://pending` resource.

## Project Structure

```text
mcp-task-manager/
├── server.py
├── tasks.json
├── requirements.txt
├── README.md
└── .gitignore
```

## Author

Muhammad Husnain

## Lab

MCP Lab Activity - Beginner Edition
