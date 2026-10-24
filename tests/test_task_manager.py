import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from main import main
from task_manager.task_utils import (
    add_task,
    calculate_progress,
    mark_task_as_complete,
    tasks,
    view_pending_tasks,
)
from task_manager.validation import (
    validate_due_date,
    validate_task_description,
    validate_task_title,
)


class TaskManagerTests(unittest.TestCase):
    def setUp(self):
        tasks.clear()

    def test_validation_rejects_empty_text_and_invalid_dates(self):
        with redirect_stdout(io.StringIO()):
            self.assertFalse(validate_task_title("  "))
            self.assertFalse(validate_task_description(""))
            self.assertFalse(validate_due_date("2026-02-30"))
            self.assertFalse(validate_due_date("10/24/2026"))
        self.assertTrue(validate_task_title("Groceries"))
        self.assertTrue(validate_task_description("Buy milk"))
        self.assertTrue(validate_due_date("2026-10-24"))

    def test_add_task_only_stores_valid_details(self):
        with redirect_stdout(io.StringIO()):
            self.assertIsNone(add_task(" ", "Buy milk", "2026-10-24"))
            self.assertIsNone(add_task("Groceries", " ", "2026-10-24"))
            self.assertIsNone(add_task("Groceries", "Buy milk", "bad date"))
            added = add_task(" Groceries ", " Buy milk ", "2026-10-24")
        self.assertEqual(len(tasks), 1)
        self.assertEqual(added, {
            "title": "Groceries",
            "description": "Buy milk",
            "due_date": "2026-10-24",
            "completed": False,
        })

    def test_completion_pending_tasks_and_progress(self):
        with redirect_stdout(io.StringIO()):
            add_task("Groceries", "Buy milk", "2026-10-24")
            add_task("Laundry", "Wash clothes", "2026-10-25")
            self.assertFalse(mark_task_as_complete(9))
            self.assertTrue(mark_task_as_complete(0))
            self.assertFalse(mark_task_as_complete(0))
            output = io.StringIO()
            with redirect_stdout(output):
                pending = view_pending_tasks()
        self.assertEqual([task["title"] for task in pending], ["Laundry"])
        self.assertIn("2. Laundry", output.getvalue())
        self.assertEqual(calculate_progress(), 50)

    def test_empty_list_and_menu(self):
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(calculate_progress(), 0)
            self.assertEqual(view_pending_tasks(), [])
        self.assertIn("No tasks currently.", output.getvalue())
        self.assertIn("No pending tasks.", output.getvalue())

        responses = iter(["1", "Groceries", "Buy milk", "2026-10-24", "2", "1", "3", "4", "5"])
        with patch("builtins.input", side_effect=lambda prompt: next(responses)):
            with redirect_stdout(output):
                main()
        self.assertTrue(tasks[0]["completed"])
        self.assertIn("Progress: 100%", output.getvalue())
        self.assertIn("Exiting the program...", output.getvalue())


if __name__ == "__main__":
    unittest.main()
