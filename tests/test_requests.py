import unittest

from initial.app import AcademicRequestApp
from refactored.models import Category, Priority, RequestDraft
from refactored.repository import InMemoryRequestRepository
from refactored.service import RequestService


def enum_or_raw(enum_type, value):
    try:
        return enum_type(value)
    except ValueError:
        return value


def build_system(version):
    if version == "initial":
        return AcademicRequestApp()
    return RequestService(InMemoryRequestRepository())


def register(system, version, student_id, category, priority, description):
    if version == "initial":
        return system.register(student_id, category, priority, description)

    draft = RequestDraft(
        student_id=student_id,
        category=enum_or_raw(Category, category),
        priority=enum_or_raw(Priority, priority),
        description=description,
    )
    return system.register(draft)


class RequestBehaviorTests(unittest.TestCase):
    def test_register_assign_and_change_status_in_both_versions(self):
        for version in ("initial", "refactored"):
            with self.subTest(version=version):
                system = build_system(version)
                created = register(
                    system, version, 1, "certificate", "high",
                    "  Constancia de alumno  "
                )

                self.assertEqual(created["id"], 1)
                self.assertEqual(created["description"], "Constancia de alumno")
                self.assertEqual(created["status"], "pending")

                assigned = system.assign_area(1, 1)
                self.assertEqual(assigned["area_id"], 1)

                started = system.change_status(1, "in_progress")
                self.assertEqual(started["status"], "in_progress")

                resolved = system.change_status(1, "resolved")
                self.assertEqual(resolved["status"], "resolved")

    def test_filters_and_report_in_both_versions(self):
        for version in ("initial", "refactored"):
            with self.subTest(version=version):
                system = build_system(version)
                register(system, version, 1, "certificate", "high", "Constancia")
                register(system, version, 2, "schedule", "low", "Consulta de horario")
                system.assign_area(1, 1)
                system.change_status(1, "in_progress")

                self.assertEqual(
                    [row["id"] for row in system.list_requests(status="in_progress")],
                    [1],
                )
                self.assertEqual(
                    [row["id"] for row in system.list_requests(priority="low")],
                    [2],
                )
                self.assertEqual(
                    [row["id"] for row in system.list_requests(area_id=1)],
                    [1],
                )
                self.assertEqual(
                    system.report(),
                    {
                        "total": 2,
                        "by_status": {
                            "pending": 1,
                            "in_progress": 1,
                            "resolved": 0,
                        },
                        "by_priority": {
                            "low": 1,
                            "medium": 0,
                            "high": 1,
                        },
                    },
                )

    def test_invalid_student_does_not_create_a_request(self):
        for version in ("initial", "refactored"):
            with self.subTest(version=version):
                system = build_system(version)

                with self.assertRaisesRegex(ValueError, "Student not found"):
                    register(system, version, 99, "other", "medium", "Consulta")

                self.assertEqual(system.report()["total"], 0)

    def test_empty_and_long_descriptions_are_rejected(self):
        for version in ("initial", "refactored"):
            with self.subTest(version=version):
                system = build_system(version)

                with self.assertRaisesRegex(ValueError, "Description is required"):
                    register(system, version, 1, "other", "medium", "   ")

                with self.assertRaisesRegex(ValueError, "Description is too long"):
                    register(system, version, 1, "other", "medium", "x" * 121)

                self.assertEqual(system.report()["total"], 0)

    def test_invalid_category_and_priority_are_rejected(self):
        for version in ("initial", "refactored"):
            with self.subTest(version=version):
                system = build_system(version)

                with self.assertRaisesRegex(ValueError, "Invalid category"):
                    register(system, version, 1, "unknown", "medium", "Consulta")

                with self.assertRaisesRegex(ValueError, "Invalid priority"):
                    register(system, version, 1, "other", "urgent", "Consulta")

                self.assertEqual(system.report()["total"], 0)

    def test_invalid_status_transition_does_not_change_state(self):
        for version in ("initial", "refactored"):
            with self.subTest(version=version):
                system = build_system(version)
                register(system, version, 1, "other", "medium", "Consulta")

                with self.assertRaisesRegex(
                    ValueError, "Invalid status transition"
                ):
                    system.change_status(1, "resolved")

                self.assertEqual(system.list_requests()[0]["status"], "pending")

    def test_resolved_request_cannot_be_reassigned(self):
        for version in ("initial", "refactored"):
            with self.subTest(version=version):
                system = build_system(version)
                register(system, version, 1, "other", "medium", "Consulta")
                system.change_status(1, "in_progress")
                system.change_status(1, "resolved")

                with self.assertRaisesRegex(
                    ValueError, "Resolved request cannot be assigned"
                ):
                    system.assign_area(1, 2)

    def test_public_results_are_equivalent(self):
        results = []

        for version in ("initial", "refactored"):
            system = build_system(version)
            register(system, version, 1, "certificate", "high", "Constancia")
            register(system, version, 3, "schedule", "medium", "Cambio de horario")
            system.assign_area(1, 2)
            system.change_status(1, "in_progress")
            results.append((system.list_requests(), system.report()))

        self.assertEqual(results[0], results[1])

    def test_refactored_rejects_boolean_identifiers(self):
        system = build_system("refactored")

        with self.assertRaisesRegex(ValueError, "Invalid student id"):
            system.register(
                RequestDraft(True, Category.OTHER, Priority.LOW, "Consulta")
            )

        register(system, "refactored", 1, "other", "low", "Consulta")

        with self.assertRaisesRegex(ValueError, "Invalid request id"):
            system.change_status(True, "in_progress")

        with self.assertRaisesRegex(ValueError, "Invalid area id"):
            system.assign_area(1, True)


if __name__ == "__main__":
    unittest.main()
