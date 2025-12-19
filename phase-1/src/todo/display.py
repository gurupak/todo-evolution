"""Display and formatting functions using rich library."""

from datetime import datetime, timedelta

from pyfiglet import Figlet
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

from todo.models import Priority, Task

# Create singleton console with custom theme
theme = Theme(
    {
        "success": "green bold",
        "error": "red bold",
        "warning": "yellow bold",
        "info": "blue",
        "dim": "dim",
    }
)

console = Console(theme=theme)


def show_banner() -> None:
    """Display application banner with ASCII art."""
    f = Figlet(font="slant")
    ascii_art = f.renderText("TODO")

    content = Text()
    content.append(ascii_art.rstrip(), style="cyan bold")
    content.append("\n")
    content.append("─" * 40, style="dim")
    content.append("\n")
    content.append("Phase I: In-Memory Console App", style="dim italic")
    content.append("\n")
    content.append("Version 0.1.0", style="dim")

    panel = Panel(Align.center(content), border_style="cyan", padding=(0, 2))
    console.print(panel)
    console.print()


def show_success(title: str, message: str) -> None:
    """Display success message in green panel."""
    panel = Panel(
        Text(message, style="success"), title=f"✓ {title}", border_style="green", padding=(1, 2)
    )
    console.print(panel)


def show_error(message: str, tip: str | None = None) -> None:
    """Display error message in red panel with optional tip."""
    content = Text()
    content.append("✗ ", style="error")
    content.append(message, style="error")

    if tip:
        content.append("\n\n")
        content.append("💡 Tip: ", style="info")
        content.append(tip, style="dim")

    panel = Panel(content, border_style="red", padding=(1, 2))
    console.print(panel)


def show_warning(message: str) -> None:
    """Display warning message in yellow panel."""
    content = Text()
    content.append("⚠ ", style="warning")
    content.append(message, style="warning")

    panel = Panel(content, border_style="yellow", padding=(1, 2))
    console.print(panel)


def show_info(message: str) -> None:
    """Display info message in blue panel."""
    content = Text()
    content.append("ℹ ", style="info")
    content.append(message, style="info")

    panel = Panel(content, border_style="blue", padding=(1, 2))
    console.print(panel)


def show_task_table(tasks: list[Task], storage_count: dict[str, int]) -> None:
    """Display tasks in formatted table with statistics."""
    from datetime import date

    table = Table(title="📋 Your Tasks", header_style="bold cyan", border_style="dim")

    table.add_column("ID", width=10, style="dim")
    table.add_column("Title", min_width=20, max_width=40)
    table.add_column("Due Date", justify="center", width=14)
    table.add_column("Priority", justify="center", width=10)
    table.add_column("Status", justify="center", width=12)
    table.add_column("Created", width=14, style="dim")

    # Sort by created_at descending (newest first)
    sorted_tasks = sorted(tasks, key=lambda t: t.created_at, reverse=True)
    today = date.today()

    for task in sorted_tasks:
        # Format due date with overdue indicator
        due_date_display = "-"
        if task.due_date:
            due_date_str = task.due_date.strftime("%Y-%m-%d")
            if task.due_date < today and not task.is_completed:
                due_date_display = f"🔴 {due_date_str}"
            else:
                due_date_display = due_date_str

        table.add_row(
            str(task.id)[:8],
            truncate_title(task.title, 40),
            due_date_display,
            format_priority(task.priority),
            format_status(task.is_completed),
            format_created_date(task.created_at),
        )

    console.print(table)

    # Summary statistics
    summary = Text()
    summary.append("📊 Total: ", style="bold")
    summary.append(f"{storage_count['total']} tasks", style="cyan")
    summary.append(" │ ", style="dim")
    summary.append("✓ ", style="green")
    summary.append(f"{storage_count['completed']} complete", style="green")
    summary.append(" │ ", style="dim")
    summary.append("○ ", style="yellow")
    summary.append(f"{storage_count['pending']} pending", style="yellow")

    console.print(summary)


def show_empty_state() -> None:
    """Display empty state when no tasks exist."""
    content = Text()
    content.append("📭 No tasks yet!\n\n", style="info")
    content.append("Get started by adding your first task.", style="dim")

    panel = Panel(Align.center(content), border_style="blue", padding=(2, 4))
    console.print(panel)


def show_task_details(task: Task) -> None:
    """Display detailed task information panel."""
    from datetime import date

    content = Text()
    content.append(f"ID: {str(task.id)[:8]}\n")
    content.append(f"Title: {task.title}\n")
    content.append(f"Description: {task.description or '(none)'}\n")

    # Format due date with overdue indicator
    if task.due_date:
        due_date_str = task.due_date.strftime("%Y-%m-%d")
        if task.due_date < date.today() and not task.is_completed:
            content.append(f"Due Date: 🔴 {due_date_str} (OVERDUE)\n")
        else:
            content.append(f"Due Date: {due_date_str}\n")
    else:
        content.append("Due Date: (none)\n")

    content.append(f"Priority: {format_priority(task.priority)}\n")
    content.append(f"Status: {format_status(task.is_completed)}\n")
    content.append(f"Created: {format_created_date(task.created_at)}")

    panel = Panel(content, title="Task Details", border_style="cyan", padding=(1, 2))
    console.print(panel)


def show_help_screen() -> None:
    """Display help screen with command reference."""
    content = Text()
    content.append("COMMANDS\n", style="bold cyan")
    content.append("➕ add      - Add a new task\n")
    content.append("📋 list     - View all tasks\n")
    content.append("✏️  update   - Update a task\n")
    content.append("🗑️  delete   - Delete a task\n")
    content.append("✅ done     - Mark task complete\n")
    content.append("⬜ undone   - Mark task incomplete\n")
    content.append("❓ help     - Show this help\n")
    content.append("🚪 exit     - Exit application\n\n")

    content.append("NAVIGATION\n", style="bold cyan")
    content.append("• Use ↑↓ arrows to select options\n")
    content.append("• Type command shortcuts (e.g., 'add')\n")
    content.append("• Press Ctrl+C to cancel/go back\n\n")

    content.append("EXAMPLES\n", style="bold cyan")
    content.append("1. Type 'add' or select '➕ Add Task'\n")
    content.append("2. Enter task details when prompted\n")
    content.append("3. View tasks with 'list' command")

    panel = Panel(content, title="❓ Help", border_style="cyan", padding=(1, 2))
    console.print(panel)


def show_goodbye() -> None:
    """Display goodbye message on exit."""
    content = Text()
    content.append("Your tasks were stored in memory\n", style="dim")
    content.append("and will be lost.\n\n", style="dim")
    content.append("See you next time!", style="cyan bold")

    panel = Panel(Align.center(content), title="Goodbye!", border_style="cyan", padding=(1, 2))
    console.print(panel)


def format_priority(priority: Priority) -> str:
    """Format priority with emoji indicator."""
    match priority:
        case Priority.HIGH:
            return "🔴 High"
        case Priority.MEDIUM:
            return "🟡 Medium"
        case Priority.LOW:
            return "🟢 Low"


def format_status(is_completed: bool) -> str:
    """Format status with icon indicator."""
    return "✓ Complete" if is_completed else "○ Pending"


def format_task_choice(task: Task) -> str:
    """Format task for selection menu display."""
    return f"{str(task.id)[:8]} │ {task.title[:40]} │ {format_priority(task.priority)} │ {format_status(task.is_completed)}"


def format_created_date(dt: datetime) -> str:
    """Format created timestamp (relative <7 days, absolute >=7 days)."""
    now = datetime.now()
    delta = now - dt

    if delta < timedelta(days=7):
        # Relative format
        if delta < timedelta(hours=1):
            minutes = int(delta.total_seconds() / 60)
            return f"{minutes}m ago"
        elif delta < timedelta(days=1):
            hours = int(delta.total_seconds() / 3600)
            return f"{hours}h ago"
        else:
            days = delta.days
            return f"{days}d ago"
    else:
        # Absolute format (YYYY-MM-DD)
        return dt.strftime("%Y-%m-%d")


def truncate_title(title: str, max_width: int) -> str:
    """Smart truncate title with ellipsis."""
    if len(title) <= max_width:
        return title
    return title[: max_width - 3] + "..."
