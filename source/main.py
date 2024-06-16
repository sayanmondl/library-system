from login.login import Account
from library.books import Books
from library.issues import (
    list_issues,
    list_issues_not_returned,
    issue_book,
    return_book,
)
from database.access_database import MongoDatabase

from rich.markdown import Markdown
from rich.console import Console
from rich.table import Table
from rich import box

import os

# Header
HEADER = """
## Library System
"""
console = Console()
md = Markdown(HEADER)
console.print(md)
db = MongoDatabase()
db.connect_database("library_database")
books = Books()

# Instructions
console.print("- [bold][italic]Press `ctrl+c` to force quit the appication!\n")


def admin_privileges():
    if input("\nAdmin Password: ") != os.environ.get("ADMIN_PASSWD"):
        print("Wrong password.\n")
        return
    else:
        while True:
            table = Table(title="Admin Options", box=box.SIMPLE)
            table.add_column("Index")
            table.add_column("Option")
            table.add_column("What it does", width=50)

            table.add_row("1", "Remove User", "Remove a user from database")
            table.add_row("2", "List Issues", "List all issues")
            table.add_row("3", "Books Not Returned", "List all not-returned books")
            table.add_row("4", "Add Book", "Add a book to library")
            table.add_row("5", "Remove Book", "Remove a book from database")
            table.add_row("6", "Clear Issue-list", "Clear `issues` database")
            table.add_row("7", "Exit Admin", "Exit from admin")

            console.print(table, justify="center")

            opt = input(">>> ")
            match opt:
                case "1":
                    username = input("\nUsername: ")
                    db.delete_user(username)
                    print("User", username, "removed from database\n")

                case "2":
                    list_issues()

                case "3":
                    list_issues_not_returned()

                case "4":
                    books.add_book()

                case "5":
                    book_id = input("\nBook ID: ")
                    books.delete_book(book_id)

                case "6":
                    db.clear_issues()
                    print("Issues cleard.\n")

                case "7":
                    break

                case _:
                    print("Invalid option.\n")


def main():
    try:
        # Login
        account = Account()
        username = account.prompt()

        # User options
        while True:
            table = Table(title="Options", box=box.SIMPLE)
            table.add_column("Index")
            table.add_column("Option")
            table.add_column("What it does", width=50)

            table.add_row("1", "Admin access", "Login as administrator")
            table.add_row("2", "Search Book", "Search and list books")
            table.add_row("3", "Issue Book", "Search a book and issue")
            table.add_row("4", "Return Book", "Return a book to stack")
            table.add_row("5", "List Books", "List all books in the stack")
            table.add_row("6", "List Available Books", "List all available books in the stack")
            table.add_row("7", "Request Book", "Request a new book to add (through e-mail)")
            table.add_row("8", "Display Data", "Diplay user's data")
            table.add_row("9", "Log-out", "Log out from current account")
            table.add_row("10", "Exit", "Exit program")

            console.print(table, justify="center")

            opt = input(">>> ")
            match opt:
                case "1":
                    admin_privileges()

                case "2":
                    books.search_book()

                case "3":
                    issue_book(username)

                case "4":
                    return_book(username)

                case "5":
                    books.list_all_books()

                case "6":
                    books.list_available_books()

                case "7":
                    books.request_book()

                case "8":
                    account.display_user_data(username)

                case "9":
                    print("Logged out.\n")
                    username = account.prompt()

                case "10":
                    print("\n\nExiting...")
                    exit()

                case _:
                    print("Invalid option.\n")

    except KeyboardInterrupt:
        print("\n\nExiting...")


if __name__ == "__main__":
    main()
