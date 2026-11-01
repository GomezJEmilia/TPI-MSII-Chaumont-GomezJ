"""Reglas de negocio, independientes del almacenamiento y de la consola."""

from collections import Counter
from dataclasses import replace
from typing import Optional

from .models import AcademicRequest, Category, Priority, RequestDraft, Status
from .repository import RequestRepository


NEXT_STATUS = {
    Status.PENDING: Status.IN_PROGRESS,
    Status.IN_PROGRESS: Status.RESOLVED,
}


class RequestService:
    def __init__(self, repository: RequestRepository):
        self._repository = repository

    def register(self, draft: RequestDraft):
        self._validate_draft(draft)
        request = AcademicRequest(
            id=self._repository.next_request_id(),
            student_id=draft.student_id,
            category=draft.category,
            priority=draft.priority,
            description=draft.description.strip(),
        )
        self._repository.save(request)
        return request.as_dict()

    def _validate_draft(self, draft: RequestDraft) -> None:
        if not isinstance(draft, RequestDraft):
            raise ValueError("Invalid request data")
        if not isinstance(draft.student_id, int) or isinstance(draft.student_id, bool):
            raise ValueError("Invalid student id")
        if not self._repository.student_exists(draft.student_id):
            raise ValueError("Student not found")
        if not isinstance(draft.category, Category):
            raise ValueError("Invalid category")
        if not isinstance(draft.priority, Priority):
            raise ValueError("Invalid priority")
        if not isinstance(draft.description, str) or not draft.description.strip():
            raise ValueError("Description is required")
        if len(draft.description.strip()) > 120:
            raise ValueError("Description is too long")

    def _get_request(self, request_id: int) -> AcademicRequest:
        if not isinstance(request_id, int) or isinstance(request_id, bool):
            raise ValueError("Invalid request id")
        request = self._repository.get(request_id)
        if request is None:
            raise ValueError("Request not found")
        return request

    def assign_area(self, request_id: int, area_id: int):
        if not isinstance(area_id, int) or isinstance(area_id, bool):
            raise ValueError("Invalid area id")
        if not self._repository.area_exists(area_id):
            raise ValueError("Area not found")
        request = self._get_request(request_id)
        if request.status == Status.RESOLVED:
            raise ValueError("Resolved request cannot be assigned")
        updated = replace(request, area_id=area_id)
        self._repository.save(updated)
        return updated.as_dict()

    def change_status(self, request_id: int, new_status: str):
        request = self._get_request(request_id)
        try:
            status = Status(new_status)
        except ValueError as error:
            raise ValueError("Invalid status") from error
        if NEXT_STATUS.get(request.status) != status:
            raise ValueError("Invalid status transition")
        updated = replace(request, status=status)
        self._repository.save(updated)
        return updated.as_dict()

    def list_requests(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        area_id: Optional[int] = None,
    ):
        if status is not None:
            try:
                status = Status(status)
            except ValueError as error:
                raise ValueError("Invalid status") from error
        if priority is not None:
            try:
                priority = Priority(priority)
            except ValueError as error:
                raise ValueError("Invalid priority") from error
        if area_id is not None:
            if not isinstance(area_id, int) or isinstance(area_id, bool):
                raise ValueError("Invalid area id")
            if not self._repository.area_exists(area_id):
                raise ValueError("Area not found")
        return [
            request.as_dict()
            for request in self._repository.list_all()
            if (status is None or request.status == status)
            and (priority is None or request.priority == priority)
            and (area_id is None or request.area_id == area_id)
        ]

    def report(self):
        requests = self._repository.list_all()
        statuses = Counter(request.status.value for request in requests)
        priorities = Counter(request.priority.value for request in requests)
        return {
            "total": len(requests),
            "by_status": {status.value: statuses[status.value] for status in Status},
            "by_priority": {priority.value: priorities[priority.value] for priority in Priority},
        }
