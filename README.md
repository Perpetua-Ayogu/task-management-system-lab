# Task Management System Lab

This project uses the three Python starter files supplied in Canvas. `main.py` runs the menu, and the `task_manager` package holds task operations and input validation. Tasks are stored as a list of dictionaries while the program is running.

Run from the project folder:

```bash
python3 main.py
```

Run the tests:

```bash
python3 -m unittest discover -s tests -v
```

The menu adds tasks, marks a numbered task complete, lists pending tasks, and shows completion progress. Titles and descriptions cannot be blank. Due dates must be valid dates in `YYYY-MM-DD` format.
