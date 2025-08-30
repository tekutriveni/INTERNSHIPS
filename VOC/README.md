# Personal To-Do List Application

A simple command-line based task management system built with Python. This application allows you to manage tasks with features like adding, editing, deleting, categorizing, and tracking completion status. Tasks are persistently stored in a JSON file for easy access across sessions.

## Features

- **Add Tasks**: Create new tasks with a title, optional description, and category.
- **View Tasks**: Display all tasks or filter by category or completion status.
- **Edit Tasks**: Modify existing tasks (title, description, or category).
- **Mark Tasks**: Mark tasks as completed or incomplete, with timestamps for completion.
- **Delete Tasks**: Remove tasks by their unique ID.
- **Search Tasks**: Find tasks by searching for keywords in the title, description, or category.
- **Task Statistics**: View stats like total tasks, completed/incomplete counts, and category breakdowns.
- **Category Management**: Organize tasks into predefined or custom categories (e.g., Work, Personal, Urgent).
- **Persistent Storage**: Tasks are saved to a `tasks.json` file for persistence.
- **User-Friendly Interface**: Simple command-line menu for easy navigation.

## Requirements

- Python 3.6 or higher
- No external libraries required (uses standard libraries: `json`, `os`, `datetime`)

## Installation

1. **Clone or Download the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Ensure Python is Installed**:
   Verify that Python 3 is installed by running:
   ```bash
   python3 --version
   ```

3. **Run the Application**:
   Execute the `task.py` script:
   ```bash
   python3 task.py
   ```

## Usage

1. **Start the Application**:
   Run the script to launch the interactive menu:
   ```bash
   python3 task.py
   ```

2. **Menu Options**:
   - **1. Add Task**: Enter a title, optional description, and category.
   - **2. View All Tasks**: Display all tasks, grouped by category.
   - **3. View Incomplete Tasks Only**: Show only tasks that are not completed.
   - **4. Mark Task as Completed**: Mark a task as done by its ID.
   - **5. Mark Task as Incomplete**: Revert a task to incomplete status.
   - **6. Edit Task**: Modify a task’s title, description, or category.
   - **7. Delete Task**: Remove a task by its ID (with confirmation).
   - **8. Search Tasks**: Search tasks by keywords in title, description, or category.
   - **9. View Statistics**: Display task counts and completion rates.
   - **10. Filter by Category**: View tasks in a specific category.
   - **11. List Categories**: Show all available categories.
   - **0. Exit**: Save tasks and exit the application.

3. **Task Storage**:
   - Tasks are automatically saved to `tasks.json` in the same directory as `task.py`.
   - The file is created if it doesn’t exist and updated after each operation.

4. **Example Workflow**:
   - Add a task: Select option 1, enter "Finish report" as the title, "Complete Q3 analysis" as the description, and "Work" as the category.
   - View tasks: Select option 2 to see all tasks, grouped by category.
   - Mark completed: Select option 4, enter the task ID (e.g., 1) to mark it as done.
   - Search: Select option 8, enter "report" to find tasks with "report" in their title or description.

## File Structure

- `task.py`: The main Python script containing the application logic.
- `tasks.json`: Generated file that stores tasks and metadata (created automatically on first save).

## Notes

- **Task IDs**: Each task is assigned a unique ID for easy reference.
- **Categories**: Default categories include Work, Personal, Urgent, General, Health, and Learning. Custom categories are supported.
- **Error Handling**: The application handles invalid inputs and file errors gracefully.
- **Persistence**: Tasks are saved after most operations (add, edit, delete, mark complete/incomplete).
- **Keyboard Interrupt**: Press `Ctrl+C` to exit the application safely.

## Example Output

```
📝 PERSONAL TO-DO LIST APPLICATION
==================================================
1.  ➕ Add Task
2.  👁️  View All Tasks
3.  👁️  View Incomplete Tasks Only
4.  ✅ Mark Task as Completed
5.  ↩️  Mark Task as Incomplete
6.  ✏️  Edit Task
7.  🗑️  Delete Task
8.  🔍 Search Tasks
9.  📊 View Statistics
10. 📁 Filter by Category
11. 📋 List Categories
0.  🚪 Exit
==================================================
Choose an option (0-11):
```

## Troubleshooting

- **File not found errors**: Ensure `tasks.json` is writable in the script’s directory.
- **Invalid input**: The application prompts for valid input if you enter incorrect data (e.g., non-numeric input for task ID).
- **Corrupted JSON file**: If `tasks.json` is corrupted, delete it and start fresh (existing tasks will be lost).
