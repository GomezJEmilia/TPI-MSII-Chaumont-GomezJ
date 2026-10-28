"""Estructuras del dominio y vocabulario permitido."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Category(str, Enum):
    CERTIFICATE = "certificate"
    SCHEDULE = "schedule"
    OTHER = "other"


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Status(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"


@dataclass(frozen=True)
class Student:
    id: int
    name: str


@dataclass(frozen=True)
class Area:
    id: int
    name: str


@dataclass(frozen=True)
class RequestDraft:
    student_id: int
    category: Category
    priority: Priority
    description: str


@dataclass(frozen=True)
class AcademicRequest:
    id: int
    student_id: int
    category: Category
    priority: Priority
    description: str
    status: Status = Status.PENDING
    area_id: Optional[int] = None

    def as_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "category": self.category.value,
            "priority": self.priority.value,
            "description": self.description,
            "status": self.status.value,
            "area_id": self.area_id,
        }
