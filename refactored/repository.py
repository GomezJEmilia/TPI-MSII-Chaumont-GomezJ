"""Acceso a datos: interfaz pequeña e implementación en memoria."""

from typing import Dict, List, Optional, Protocol

from .models import AcademicRequest, Area, Student


class RequestRepository(Protocol):
    def student_exists(self, student_id: int) -> bool:
        ...

    def area_exists(self, area_id: int) -> bool:
        ...

    def next_request_id(self) -> int:
        ...

    def save(self, request: AcademicRequest) -> None:
        ...

    def get(self, request_id: int) -> Optional[AcademicRequest]:
        ...

    def list_all(self) -> List[AcademicRequest]:
        ...


class InMemoryRequestRepository:
    def __init__(self):
        self._students: Dict[int, Student] = {
            1: Student(1, "Ana Pérez"),
            2: Student(2, "Martín López"),
            3: Student(3, "Lucía Gómez"),
        }
        self._areas: Dict[int, Area] = {
            1: Area(1, "Secretaría Académica"),
            2: Area(2, "Coordinación de Carrera"),
        }
        self._requests: Dict[int, AcademicRequest] = {}
        self._next_id = 1

    def student_exists(self, student_id: int) -> bool:
        return student_id in self._students

    def area_exists(self, area_id: int) -> bool:
        return area_id in self._areas

    def next_request_id(self) -> int:
        request_id = self._next_id
        self._next_id += 1
        return request_id

    def save(self, request: AcademicRequest) -> None:
        self._requests[request.id] = request

    def get(self, request_id: int) -> Optional[AcademicRequest]:
        return self._requests.get(request_id)

    def list_all(self) -> List[AcademicRequest]:
        return list(self._requests.values())
