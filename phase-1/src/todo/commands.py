"""Command handler functions for the CLI."""

import re
from datetime import date, datetime

import questionary
from questionary import Choice

from todo import display
from todo.models import Priority, Task
from todo.storage import InMemoryStorage


def add_task(storage: InMemoryStorage) -> None:
    """Add a new task through interactive prompts."""
    try:
        # Prompt for title with validation
        title = questionary.text(
            "Enter task title:",
            validate=lambda t: _validate_title(t),
        ).ask()

        if title is None:  # User pressed Ctrl+C
            display.show_info("Operation cancelled. Returning to main menu...")
            return

        # Normalize title
        title = _normalize_text(title.strip())

        # Prompt for description (optional)
        description = questionary.text(
            "Enter task description (optional, press Enter to skip):", default=""
        ).ask()

        if description is None:  # User pressed Ctrl+C
            display.show_info("Operation cancelled. Returning to main menu...")
            return

        # Normalize description
        description = _normalize_text(description.strip())

        # Prompt for due date (optional) - interactive selection
        due_date_obj = _prompt_due_date()
        if due_date_obj is False:  # User cancelled
            display.show_info("Operation cancelled. Returning to main menu...")
            return

        # Prompt for priority (Medium listed first as default)
        priority_choice = questionary.select(
            "Select priority:",
            choices=[
                Choice("🟡 Medium", value=Priority.MEDIUM),
                Choice("🔴 High", value=Priority.HIGH),
                Choice("🟢 Low", value=Priority.LOW),
            ],
        ).ask()

        if priority_choice is None:  # User pressed Ctrl+C
            display.show_info("Operation cancelled. Returning to main menu...")
            return

        # Create and save task
        task = Task(
            title=title, description=description, due_date=due_date_obj, priority=priority_choice
        )
        storage.add(task)

        # Display success message
        message = f"{task.title}\n"
        message += f"ID: {str(task.id)[:8]}\n"
        if task.due_date:
            message += f"Due Date: {task.due_date.strftime('%Y-%m-%d')}\n"
        message += f"Priority: {display.format_priority(task.priority)}\n"
        message += f"Status: {display.format_status(task.is_completed)}"

        display.show_success("Task Added", message)

    except KeyboardInterrupt:
        display.show_info("Operation cancelled. Returning to main menu...")
        return


def list_tasks(storage: InMemoryStorage) -> None:
    """Display all tasks in formatted table."""
    tasks = storage.get_all()

    if not tasks:
        display.show_empty_state()
        return

    counts = storage.count()
    display.show_task_table(tasks, counts)


def update_task(storage: InMemoryStorage) -> None:
    """Update an existing task's details."""
    tasks = storage.get_all()

    if not tasks:
        display.show_warning(
            "No tasks available to update\n\n💡 Tip: Create a task first using 'add'"
        )
        return

    try:
        # Select task to update
        task = _prompt_select_task(tasks, "Select task to update:")
        if task is None:
            display.show_info("Operation cancelled. Returning to main menu...")
            return

        # Select what to update
        update_choice = questionary.select(
            "What would you like to update?",
            choices=[
                Choice("Title", value="title"),
                Choice("Description", value="description"),
                Choice("Due Date", value="due_date"),
                Choice("Priority", value="priority"),
                Choice("All fields", value="all"),
            ],
        ).ask()

        if update_choice is None:
            display.show_info("Operation cancelled. Returning to main menu...")
            return

        # Store original values for comparison
        original_title = task.title
        original_description = task.description
        original_due_date = task.due_date
        original_priority = task.priority

        # Collect updates based on choice
        updates = {}

        if update_choice in ["title", "all"]:
            new_title = questionary.text(
                "Enter new title:", default=task.title, validate=lambda t: _validate_title(t)
            ).ask()
            if new_title is None:
                display.show_info("Operation cancelled. Returning to main menu...")
                return
            updates["title"] = _normalize_text(new_title.strip())

        if update_choice in ["description", "all"]:
            new_description = questionary.text(
                "Enter new description:", default=task.description
            ).ask()
            if new_description is None:
                display.show_info("Operation cancelled. Returning to main menu...")
                return
            updates["description"] = _normalize_text(new_description.strip())

        if update_choice in ["due_date", "all"]:
            # Interactive due date selection with current value
            new_due_date = _prompt_due_date(current_date=task.due_date)
            if new_due_date is False:  # User cancelled
                display.show_info("Operation cancelled. Returning to main menu...")
                return
            updates["due_date"] = new_due_date

        if update_choice in ["priority", "all"]:
            current_priority_idx = [Priority.HIGH, Priority.MEDIUM, Priority.LOW].index(
                task.priority
            )
            choices = [
                Choice("🔴 High", value=Priority.HIGH),
                Choice("🟡 Medium", value=Priority.MEDIUM),
                Choice("🟢 Low", value=Priority.LOW),
            ]
            new_priority = questionary.select(
                "Select new priority:", choices=choices, default=choices[current_priority_idx]
            ).ask()
            if new_priority is None:
                display.show_info("Operation cancelled. Returning to main menu...")
                return
            updates["priority"] = new_priority

        # Apply updates
        storage.update(task.id, **updates)

        # Show before/after comparison
        message = ""
        if "title" in updates and updates["title"] != original_title:
            message += f"Title: {original_title} → {updates['title']}\n"
        if "description" in updates and updates["description"] != original_description:
            message += f"Description: {original_description or '(none)'} → {updates['description'] or '(none)'}\n"
        if "due_date" in updates and updates["due_date"] != original_due_date:
            original_str = original_due_date.strftime("%Y-%m-%d") if original_due_date else "(none)"
            new_str = updates["due_date"].strftime("%Y-%m-%d") if updates["due_date"] else "(none)"
            message += f"Due Date: {original_str} → {new_str}\n"
        if "priority" in updates and updates["priority"] != original_priority:
            message += f"Priority: {display.format_priority(original_priority)} → {display.format_priority(updates['priority'])}"

        if not message:
            message = "No changes made (all fields kept the same)"

        display.show_success("Task Updated", message.strip())

    except KeyboardInterrupt:
        display.show_info("Operation cancelled. Returning to main menu...")
        return


def delete_task(storage: InMemoryStorage) -> None:
    """Delete a task with confirmation."""
    tasks = storage.get_all()

    if not tasks:
        display.show_warning("No tasks available\n\n💡 Tip: Add tasks first using 'add'")
        return

    try:
        # Select task to delete
        task = _prompt_select_task(tasks, "Select task to delete:")
        if task is None:
            display.show_info("Operation cancelled. Returning to main menu...")
            return

        # Show task details for confirmation
        display.show_task_details(task)

        # Confirm deletion
        confirm = questionary.select(
            f"Are you sure you want to delete '{task.title}'?",
            choices=[Choice("Yes, delete it", value=True), Choice("No, keep it", value=False)],
        ).ask()

        if confirm is None or not confirm:
            display.show_info("Deletion cancelled. Task was not removed.")
            return

        # Delete task
        storage.delete(task.id)
        display.show_success("Task Deleted", f"'{task.title}' has been removed")

    except KeyboardInterrupt:
        display.show_info("Operation cancelled. Returning to main menu...")
        return


def mark_complete(storage: InMemoryStorage) -> None:
    """Mark an incomplete task as complete."""
    pending = storage.get_pending()

    if not pending:
        all_tasks = storage.get_all()
        if all_tasks:
            display.show_info(
                "All tasks are already complete!\n\n💡 Tip: Add new tasks or mark some incomplete"
            )
        else:
            display.show_warning("No tasks available\n\n💡 Tip: Add tasks first using 'add'")
        return

    try:
        # Select task from incomplete tasks
        task = _prompt_select_task(pending, "Select task to mark complete:")
        if task is None:
            display.show_info("Operation cancelled. Returning to main menu...")
            return

        # Mark as complete
        storage.update(task.id, is_completed=True, completed_at=datetime.now())

        message = f"{task.title}\n○ Pending → ✓ Complete"
        display.show_success("Task Completed", message)

    except KeyboardInterrupt:
        display.show_info("Operation cancelled. Returning to main menu...")
        return


def mark_incomplete(storage: InMemoryStorage) -> None:
    """Mark a complete task as incomplete."""
    completed = storage.get_completed()

    if not completed:
        display.show_info("No completed tasks to mark incomplete")
        return

    try:
        # Select task from completed tasks
        task = _prompt_select_task(completed, "Select task to mark incomplete:")
        if task is None:
            display.show_info("Operation cancelled. Returning to main menu...")
            return

        # Mark as incomplete
        storage.update(task.id, is_completed=False, completed_at=None)

        message = f"{task.title}\n✓ Complete → ○ Pending"
        display.show_success("Task Marked Incomplete", message)

    except KeyboardInterrupt:
        display.show_info("Operation cancelled. Returning to main menu...")
        return


def show_help() -> None:
    """Display help screen with command reference."""
    display.show_help_screen()


# Helper functions


def _validate_title(title: str) -> bool | str:
    """Validate task title."""
    title = title.strip()
    if len(title) == 0:
        return "Title is required - Please enter a title for your task (1-200 characters)"
    if len(title) > 200:
        return f"Title too long - Maximum 200 characters allowed. You entered {len(title)}"
    return True


def _normalize_text(text: str) -> str:
    """Normalize text by collapsing whitespace and stripping control characters."""
    # Strip control characters (except newlines and tabs)
    text = "".join(char for char in text if ord(char) >= 32 or char in "\n\t")
    # Collapse multiple spaces/newlines to single space
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _prompt_due_date(current_date: date | None = None) -> date | None | bool:
    """Prompt user to select a due date interactively.

    Args:
        current_date: Current due date (for updates), None for new tasks

    Returns:
        date object if selected, None if skipped/cleared, False if cancelled
    """
    from datetime import timedelta

    today = date.today()

    # Build quick selection options (future dates only)
    choices = []
    choices.append(Choice("No due date", value=None))
    choices.append(Choice(f"Today ({today.strftime('%Y-%m-%d')})", value=today))

    tomorrow = today + timedelta(days=1)
    choices.append(Choice(f"Tomorrow ({tomorrow.strftime('%Y-%m-%d')})", value=tomorrow))

    this_week_end = today + timedelta(days=(6 - today.weekday()))
    if this_week_end > tomorrow:
        choices.append(
            Choice(f"End of this week ({this_week_end.strftime('%Y-%m-%d')})", value=this_week_end)
        )

    next_week = today + timedelta(days=7)
    choices.append(Choice(f"Next week ({next_week.strftime('%Y-%m-%d')})", value=next_week))

    next_month = today + timedelta(days=30)
    choices.append(Choice(f"In 1 month ({next_month.strftime('%Y-%m-%d')})", value=next_month))

    choices.append(Choice("Custom date (enter manually)", value="custom"))

    # Show current date if updating
    message = "Select due date:"
    if current_date:
        message = f"Select due date (current: {current_date.strftime('%Y-%m-%d')}):"

    selection = questionary.select(message, choices=choices).ask()

    if selection is None:  # Ctrl+C
        return False

    if selection == "custom":
        # Manual entry for custom dates
        date_input = questionary.text(
            "Enter due date (YYYY-MM-DD):",
            default=current_date.strftime("%Y-%m-%d") if current_date else "",
        ).ask()

        if date_input is None:  # Ctrl+C
            return False

        if not date_input.strip():
            return None  # Clear due date

        # Validate custom date
        return _validate_due_date(date_input.strip())

    return selection  # Returns date object or None


def _validate_due_date(date_str: str) -> date | None:
    """Validate and parse due date string.

    Args:
        date_str: Date string in YYYY-MM-DD format

    Returns:
        date object if valid, None if invalid (error displayed)
    """
    try:
        # Parse YYYY-MM-DD format
        parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()

        # Check if date is in the past
        today = date.today()
        if parsed_date < today:
            display.show_error(
                f"Due date cannot be in the past",
                tip=f"Please enter today ({today.strftime('%Y-%m-%d')}) or a future date",
            )
            return None

        return parsed_date

    except ValueError:
        display.show_error(
            "Invalid date format", tip="Please use YYYY-MM-DD format (e.g., 2025-12-25)"
        )
        return None


def _prompt_select_task(tasks: list[Task], message: str) -> Task | None:
    """Prompt user to select a task from list."""
    if not tasks:
        return None

    choices = [Choice(display.format_task_choice(task), value=task) for task in tasks]

    return questionary.select(message, choices=choices).ask()
