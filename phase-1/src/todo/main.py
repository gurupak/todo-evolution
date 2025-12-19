"""Main entry point for the todo CLI application."""

import questionary
from questionary import Choice, Separator

from todo import commands, display
from todo.storage import InMemoryStorage


def main() -> None:
    """Application entry point."""
    storage = InMemoryStorage()

    display.show_banner()

    while True:
        try:
            choice = _prompt_main_menu()

            if choice is None:  # User pressed Ctrl+C
                continue

            match choice:
                case "add":
                    commands.add_task(storage)
                case "list":
                    commands.list_tasks(storage)
                case "update":
                    commands.update_task(storage)
                case "delete":
                    commands.delete_task(storage)
                case "done":
                    commands.mark_complete(storage)
                case "undone":
                    commands.mark_incomplete(storage)
                case "help":
                    commands.show_help()
                case "exit":
                    if _prompt_confirm_exit():
                        display.show_goodbye()
                        break
                case _:
                    display.show_error("Unknown command")

        except KeyboardInterrupt:
            display.show_info("Operation cancelled.")
            continue
        except Exception as e:
            display.show_error(
                f"An unexpected error occurred: {str(e)}",
                "Please try again or report this issue if it persists",
            )
            continue


def _prompt_main_menu() -> str | None:
    """Display main menu and return selected command."""
    choices = [
        Choice("➕ Add Task", value="add"),
        Choice("📋 List Tasks", value="list"),
        Choice("✏️  Update Task", value="update"),
        Choice("🗑️  Delete Task", value="delete"),
        Choice("✅ Mark Complete", value="done"),
        Choice("⬜ Mark Incomplete", value="undone"),
        Separator(),
        Choice("❓ Help", value="help"),
        Choice("🚪 Exit", value="exit"),
    ]

    return questionary.select(
        "What would you like to do?",
        choices=choices,
        instruction="(Use ↑↓ arrows or type command shortcut)",
    ).ask()


def _prompt_confirm_exit() -> bool:
    """Prompt for exit confirmation."""
    choices = [Choice("Yes, exit", value=True), Choice("No, stay", value=False)]

    result = questionary.select("Are you sure you want to exit?", choices=choices).ask()

    return result if result is not None else False


if __name__ == "__main__":
    main()
