"""Versión inicial del sistema de solicitudes académicas.

Funciona, pero concentra datos, validaciones y reglas en una sola clase.
Se conserva sin modificar para que el diagnóstico sea verificable.
"""


class AcademicRequestApp:
    def __init__(self):
        self.students = {
            1: {"id": 1, "name": "Ana Pérez"},
            2: {"id": 2, "name": "Martín López"},
            3: {"id": 3, "name": "Lucía Gómez"},
        }
        self.areas = {
            1: {"id": 1, "name": "Secretaría Académica"},
            2: {"id": 2, "name": "Coordinación de Carrera"},
        }
        self.requests = []
        self.next_id = 1

    def register(self, student_id, category, priority, description):
        if student_id not in self.students:
            raise ValueError("Student not found")
        if category not in ("certificate", "schedule", "other"):
            raise ValueError("Invalid category")
        if priority not in ("low", "medium", "high"):
            raise ValueError("Invalid priority")
        if not isinstance(description, str) or not description.strip():
            raise ValueError("Description is required")
        if len(description.strip()) > 120:
            raise ValueError("Description is too long")
        request = {
            "id": self.next_id,
            "student_id": student_id,
            "category": category,
            "priority": priority,
            "description": description.strip(),
            "status": "pending",
            "area_id": None,
        }
        self.requests.append(request)
        self.next_id += 1
        return dict(request)

    def assign_area(self, request_id, area_id):
        if area_id not in self.areas:
            raise ValueError("Area not found")
        found = None
        for request in self.requests:
            if request["id"] == request_id:
                found = request
                break
        if found is None:
            raise ValueError("Request not found")
        if found["status"] == "resolved":
            raise ValueError("Resolved request cannot be assigned")
        found["area_id"] = area_id
        return dict(found)

    def change_status(self, request_id, new_status):
        found = None
        for request in self.requests:
            if request["id"] == request_id:
                found = request
                break
        if found is None:
            raise ValueError("Request not found")
        if new_status not in ("pending", "in_progress", "resolved"):
            raise ValueError("Invalid status")
        if found["status"] == "pending" and new_status != "in_progress":
            raise ValueError("Invalid status transition")
        if found["status"] == "in_progress" and new_status != "resolved":
            raise ValueError("Invalid status transition")
        if found["status"] == "resolved":
            raise ValueError("Invalid status transition")
        found["status"] = new_status
        return dict(found)

    def list_requests(self, status=None, priority=None, area_id=None):
        if status is not None and status not in ("pending", "in_progress", "resolved"):
            raise ValueError("Invalid status")
        if priority is not None and priority not in ("low", "medium", "high"):
            raise ValueError("Invalid priority")
        if area_id is not None and area_id not in self.areas:
            raise ValueError("Area not found")
        result = []
        for request in self.requests:
            if status is not None and request["status"] != status:
                continue
            if priority is not None and request["priority"] != priority:
                continue
            if area_id is not None and request["area_id"] != area_id:
                continue
            result.append(dict(request))
        return result

    def report(self):
        pending = 0
        in_progress = 0
        resolved = 0
        low = 0
        medium = 0
        high = 0
        for request in self.requests:
            if request["status"] == "pending":
                pending += 1
            if request["status"] == "in_progress":
                in_progress += 1
            if request["status"] == "resolved":
                resolved += 1
            if request["priority"] == "low":
                low += 1
            if request["priority"] == "medium":
                medium += 1
            if request["priority"] == "high":
                high += 1
        return {
            "total": len(self.requests),
            "by_status": {
                "pending": pending,
                "in_progress": in_progress,
                "resolved": resolved,
            },
            "by_priority": {"low": low, "medium": medium, "high": high},
        }
