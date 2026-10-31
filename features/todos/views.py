from typing import Any

from drf_spectacular.utils import extend_schema
from rest_framework import status  # pyright: ignore[reportMissingTypeStubs]
from rest_framework.request import Request  # pyright: ignore[reportMissingTypeStubs]
from rest_framework.response import Response  # pyright: ignore[reportMissingTypeStubs]
from rest_framework.views import APIView  # pyright: ignore[reportMissingTypeStubs]
from features.todos.store import (
    list_todos,
    get_todo,
    create_todo,
    update_todo,
    delete_todo,
)  # pyright: ignore[reportUnknownVariableType]
from features.todos.serializers import TodoSerializer


@extend_schema(tags=["todos"])
class TodoListView(APIView):
    serializer_class = TodoSerializer

    @extend_schema(responses=TodoSerializer(many=True))
    def get(self, request: Request):
        return Response(TodoSerializer(list_todos(), many=True).data)

    def post(self, request: Request):
        serializer = TodoSerializer(data=request.data)  # type: ignore
        serializer.is_valid(raise_exception=True)
        todo: dict[str, Any] = create_todo(serializer.validated_data["title"])  # type: ignore
        return Response(TodoSerializer(todo).data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["todos"])
class TodoDetailView(APIView):
    serializer_class = TodoSerializer

    def get(self, request: Request, todo_id: int):
        todo = get_todo(todo_id)
        if not todo:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(TodoSerializer(todo).data)

    def patch(self, request: Request, todo_id: int):
        serializer = TodoSerializer(data=request.data, partial=True)  # type: ignore
        serializer.is_valid(raise_exception=True)
        todo: dict[str, Any] | None = update_todo(todo_id, **serializer.validated_data)  # type: ignore
        if not todo:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(TodoSerializer(todo).data)

    def delete(self, request: Request, todo_id: int):
        if not delete_todo(todo_id):
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
