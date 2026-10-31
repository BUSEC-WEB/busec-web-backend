from itertools import count
from typing import Any

_todos: dict[int, Any] = {}
_ids = count(1)


def list_todos() -> list[dict[str, Any]]:
    return list(_todos.values())


def get_todo(todo_id: int) -> dict[str, Any] | None:
    return _todos.get(todo_id)


def create_todo(title: str) -> dict[str, Any]:
    todo: dict[str, Any] = {"id": next(_ids), "title": title, "done": False}
    _todos[todo["id"]] = todo
    return todo


def update_todo(todo_id: int, **fields: Any) -> dict[str, Any] | None:
    todo = _todos.get(todo_id)
    if todo:
        todo.update(fields)
    return todo


def delete_todo(todo_id: int) -> bool:
    return _todos.pop(todo_id, None) is not None
