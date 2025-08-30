#!/usr/bin/env python3
"""
Personal To-Do List Application
A simple command-line based task management system with JSON persistence.

Features:
- Add, view, edit, and delete tasks
- Task categorization (Work, Personal, Urgent, etc.)
- Mark tasks as completed
- Persistent storage using JSON
- Search and filter functionality
"""

import json
import os
import datetime
from typing import List, Optional


class Task:
    """Represents a single task with title, description, category, and completion status."""
    
    def __init__(self, title: str, description: str = "", category: str = "General", 
                 completed: bool = False, created_date: str = None, task_id: int = None):
        self.title = title
        self.description = description
        self.category = category
        self.completed = completed
        self.created_date = created_date or datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.task_id = task_id
        self.completed_date = None
    
    def mark_completed(self):
        """Mark the task as completed and record the completion date."""
        self.completed = True
        self.completed_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def mark_incomplete(self):
        """Mark the task as incomplete."""
        self.completed = False
        self.completed_date = None
    
    def to_dict(self) -> dict:
        """Convert task to dictionary for JSON serialization."""
        return {
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'completed': self.completed,
            'created_date': self.created_date,
            'task_id': self.task_id,
            'completed_date': self.completed_date
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create Task object from dictionary."""
        task = cls(
            title=data['title'],
            description=data.get('description', ''),
            category=data.get('category', 'General'),
            completed=data.get('completed', False),
            created_date=data.get('created_date'),
            task_id=data.get('task_id')
        )
        task.completed_date = data.get('completed_date')
        return task
    
    def __str__(self) -> str:
        """String representation of the task."""
        status = "✓" if self.completed else "○"
        return f"{status} [{self.task_id}] {self.title} ({self.category})"


class TodoApp:
    """Main application class for managing tasks."""
    
    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        self.tasks: List[Task] = []
        self.next_id = 1
        self.categories = {"Work", "Personal", "Urgent", "General", "Health", "Learning"}
        self.load_tasks()
    
    def save_tasks(self) -> bool:
        """Save tasks to JSON file."""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                task_data = [task.to_dict() for task in self.tasks]
                json.dump({
                    'tasks': task_data,
                    'next_id': self.next_id
                }, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving tasks: {e}")
            return False
    
    def load_tasks(self) -> bool:
        """Load tasks from JSON file."""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(task_data) for task_data in data.get('tasks', [])]
                    self.next_id = data.get('next_id', 1)
                    
                    # Assign IDs to tasks that don't have them (backward compatibility)
                    for task in self.tasks:
                        if task.task_id is None:
                            task.task_id = self.next_id
                            self.next_id += 1
                    
                    return True
            return True
        except Exception as e:
            print(f"Error loading tasks: {e}")
            return False
    
    def add_task(self, title: str, description: str = "", category: str = "General") -> bool:
        """Add a new task."""
        if not title.strip():
            print("Task title cannot be empty!")
            return False
        
        task = Task(title.strip(), description.strip(), category, task_id=self.next_id)
        self.tasks.append(task)
        self.next_id += 1
        
        if category not in self.categories:
            self.categories.add(category)
        
        print(f"Task '{title}' added successfully!")
        return True
    
    def view_tasks(self, category_filter: Optional[str] = None, show_completed: bool = True) -> None:
        """Display all tasks or filtered tasks."""
        if not self.tasks:
            print("No tasks found!")
            return
        
        filtered_tasks = self.tasks
        
        if category_filter:
            filtered_tasks = [task for task in self.tasks if task.category.lower() == category_filter.lower()]
        
        if not show_completed:
            filtered_tasks = [task for task in filtered_tasks if not task.completed]
        
        if not filtered_tasks:
            print("No tasks match the filter criteria!")
            return
        
        print("\n" + "="*60)
        print("YOUR TASKS")
        print("="*60)
        
        # Group by category
        categories = {}
        for task in filtered_tasks:
            if task.category not in categories:
                categories[task.category] = []
            categories[task.category].append(task)
        
        for category, tasks in categories.items():
            print(f"\n📁 {category.upper()}")
            print("-" * 40)
            for task in sorted(tasks, key=lambda x: (x.completed, x.task_id)):
                print(f"  {task}")
                if task.description:
                    print(f"     Description: {task.description}")
                print(f"     Created: {task.created_date}")
                if task.completed and task.completed_date:
                    print(f"     Completed: {task.completed_date}")
                print()
    
    def mark_task_completed(self, task_id: int) -> bool:
        """Mark a task as completed."""
        task = self.find_task_by_id(task_id)
        if task:
            if task.completed:
                print(f"Task '{task.title}' is already completed!")
            else:
                task.mark_completed()
                print(f"Task '{task.title}' marked as completed!")
            return True
        else:
            print(f"Task with ID {task_id} not found!")
            return False
    
    def mark_task_incomplete(self, task_id: int) -> bool:
        """Mark a task as incomplete."""
        task = self.find_task_by_id(task_id)
        if task:
            if not task.completed:
                print(f"Task '{task.title}' is already incomplete!")
            else:
                task.mark_incomplete()
                print(f"Task '{task.title}' marked as incomplete!")
            return True
        else:
            print(f"Task with ID {task_id} not found!")
            return False
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID."""
        task = self.find_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            print(f"Task '{task.title}' deleted successfully!")
            return True
        else:
            print(f"Task with ID {task_id} not found!")
            return False
    
    def edit_task(self, task_id: int) -> bool:
        """Edit an existing task."""
        task = self.find_task_by_id(task_id)
        if not task:
            print(f"Task with ID {task_id} not found!")
            return False
        
        print(f"\nEditing task: {task.title}")
        print("Leave blank to keep current value.")
        
        new_title = input(f"Title [{task.title}]: ").strip()
        if new_title:
            task.title = new_title
        
        new_description = input(f"Description [{task.description}]: ").strip()
        if new_description or new_description == "":
            task.description = new_description
        
        new_category = input(f"Category [{task.category}]: ").strip()
        if new_category:
            task.category = new_category
            if new_category not in self.categories:
                self.categories.add(new_category)
        
        print(f"Task '{task.title}' updated successfully!")
        return True
    
    def find_task_by_id(self, task_id: int) -> Optional[Task]:
        """Find a task by its ID."""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None
    
    def search_tasks(self, query: str) -> List[Task]:
        """Search tasks by title or description."""
        query = query.lower().strip()
        matching_tasks = []
        
        for task in self.tasks:
            if (query in task.title.lower() or 
                query in task.description.lower() or 
                query in task.category.lower()):
                matching_tasks.append(task)
        
        return matching_tasks
    
    def get_task_statistics(self) -> dict:
        """Get statistics about tasks."""
        total_tasks = len(self.tasks)
        completed_tasks = len([task for task in self.tasks if task.completed])
        incomplete_tasks = total_tasks - completed_tasks
        
        categories_stats = {}
        for task in self.tasks:
            if task.category not in categories_stats:
                categories_stats[task.category] = {'total': 0, 'completed': 0}
            categories_stats[task.category]['total'] += 1
            if task.completed:
                categories_stats[task.category]['completed'] += 1
        
        return {
            'total': total_tasks,
            'completed': completed_tasks,
            'incomplete': incomplete_tasks,
            'categories': categories_stats
        }


def display_menu():
    """Display the main menu."""
    print("\n" + "="*50)
    print("📝 PERSONAL TO-DO LIST APPLICATION")
    print("="*50)
    print("1.  ➕ Add Task")
    print("2.  👁️  View All Tasks")
    print("3.  👁️  View Incomplete Tasks Only")
    print("4.  ✅ Mark Task as Completed")
    print("5.  ↩️  Mark Task as Incomplete")
    print("6.  ✏️  Edit Task")
    print("7.  🗑️  Delete Task")
    print("8.  🔍 Search Tasks")
    print("9.  📊 View Statistics")
    print("10. 📁 Filter by Category")
    print("11. 📋 List Categories")
    print("0.  🚪 Exit")
    print("="*50)


def get_user_input(prompt: str, input_type: type = str, allow_empty: bool = False):
    """Get validated input from user."""
    while True:
        try:
            value = input(prompt).strip()
            if not allow_empty and not value:
                print("Input cannot be empty. Please try again.")
                continue
            
            if input_type == int:
                return int(value)
            return value
        except ValueError:
            print(f"Please enter a valid {input_type.__name__}.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return None


def main():
    """Main application loop."""
    app = TodoApp()
    
    print("Welcome to your Personal To-Do List Application!")
    print("Your tasks are automatically saved to 'tasks.json'")
    
    while True:
        display_menu()
        
        choice = get_user_input("Choose an option (0-11): ")
        if choice is None:
            continue
        
        try:
            choice = int(choice)
        except ValueError:
            print("Please enter a valid number.")
            continue
        
        if choice == 1:
            # Add Task
            title = get_user_input("Enter task title: ")
            if title is None:
                continue
            
            description = get_user_input("Enter task description (optional): ", allow_empty=True)
            
            print(f"Available categories: {', '.join(sorted(app.categories))}")
            category = get_user_input("Enter category (or press Enter for 'General'): ", allow_empty=True)
            if not category:
                category = "General"
            
            app.add_task(title, description, category)
            app.save_tasks()
        
        elif choice == 2:
            # View All Tasks
            app.view_tasks()
        
        elif choice == 3:
            # View Incomplete Tasks Only
            app.view_tasks(show_completed=False)
        
        elif choice == 4:
            # Mark Task Completed
            app.view_tasks(show_completed=False)
            if app.tasks:
                task_id = get_user_input("Enter task ID to mark as completed: ", int)
                if task_id is not None:
                    app.mark_task_completed(task_id)
                    app.save_tasks()
        
        elif choice == 5:
            # Mark Task Incomplete
            completed_tasks = [task for task in app.tasks if task.completed]
            if not completed_tasks:
                print("No completed tasks found!")
            else:
                for task in completed_tasks:
                    print(f"  {task}")
                task_id = get_user_input("Enter task ID to mark as incomplete: ", int)
                if task_id is not None:
                    app.mark_task_incomplete(task_id)
                    app.save_tasks()
        
        elif choice == 6:
            # Edit Task
            app.view_tasks()
            if app.tasks:
                task_id = get_user_input("Enter task ID to edit: ", int)
                if task_id is not None:
                    app.edit_task(task_id)
                    app.save_tasks()
        
        elif choice == 7:
            # Delete Task
            app.view_tasks()
            if app.tasks:
                task_id = get_user_input("Enter task ID to delete: ", int)
                if task_id is not None:
                    confirm = get_user_input("Are you sure you want to delete this task? (y/N): ", allow_empty=True)
                    if confirm.lower() in ['y', 'yes']:
                        app.delete_task(task_id)
                        app.save_tasks()
                    else:
                        print("Delete operation cancelled.")
        
        elif choice == 8:
            # Search Tasks
            query = get_user_input("Enter search query: ")
            if query is None:
                continue
            
            matching_tasks = app.search_tasks(query)
            if matching_tasks:
                print(f"\nFound {len(matching_tasks)} matching task(s):")
                print("-" * 40)
                for task in matching_tasks:
                    print(f"  {task}")
                    if task.description:
                        print(f"     Description: {task.description}")
                    print()
            else:
                print("No tasks match your search query.")
        
        elif choice == 9:
            # View Statistics
            stats = app.get_task_statistics()
            print("\n📊 TASK STATISTICS")
            print("=" * 30)
            print(f"Total Tasks: {stats['total']}")
            print(f"Completed: {stats['completed']}")
            print(f"Incomplete: {stats['incomplete']}")
            
            if stats['total'] > 0:
                completion_rate = (stats['completed'] / stats['total']) * 100
                print(f"Completion Rate: {completion_rate:.1f}%")
            
            print("\nBy Category:")
            for category, cat_stats in stats['categories'].items():
                print(f"  {category}: {cat_stats['completed']}/{cat_stats['total']} completed")
        
        elif choice == 10:
            # Filter by Category
            print(f"Available categories: {', '.join(sorted(app.categories))}")
            category = get_user_input("Enter category to filter by: ")
            if category is None:
                continue
            app.view_tasks(category_filter=category)
        
        elif choice == 11:
            # List Categories
            print(f"\n📁 Available Categories: {', '.join(sorted(app.categories))}")
        
        elif choice == 0:
            # Exit
            if app.save_tasks():
                print("Tasks saved successfully!")
            print("Thank you for using the Personal To-Do List Application!")
            print("Goodbye! 👋")
            break
        
        else:
            print("Invalid choice. Please select a number between 0-11.")
        
        # Pause before showing menu again
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nApplication terminated by user. Goodbye! 👋")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("Please restart the application.")