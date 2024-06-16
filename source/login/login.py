from database.access_database import MongoDatabase
from login.sign_up import sign_up

from rich.table import Table
from rich.console import Console
from rich import box

console = Console()


class Account:
    def __init__(self) -> None:
        self.db = MongoDatabase()
        self.db.connect_database("library_database")

    def prompt(self):
        table = Table(title="Login options", show_header=False, box=box.ROUNDED)
        table.add_row("1", "Log In", "Login to your account")
        table.add_row("2", "Sign Up", "Create a new account")
        console.print(table, justify="center")

        if input(">>> ") == "2":
            sign_up()

        is_successful = self.login()
        while is_successful == "_":
            is_successful = self.login()

        print("Login successful.\n")
        return is_successful

    def login(self) -> str:
        username = input("\nUsername: ")
        self.db.access_collection("users")

        while self.db.collection.find_one({"username": username}) == None:
            print("\nUsername does not exist.\nTry again!\n")
            username = input("Username: ")

        userdata = self.db.collection.find_one({"username": username})
        passwd = input("Password: ")

        while userdata["password"] != passwd:
            print("\nWrong password.\nTry again!\n")
            if input("Reset password? [y/n]: ") == "y":
                self.reset_passwd(userdata)
                return "_"
            else:
                passwd = input("\nPassword: ")

        return username

    def reset_passwd(self, userdata):
        email = input("\nVerify E-mail: ")

        counter = 5
        while userdata["email"] != email:
            if counter == 0:
                print(f"\nWrong E-mail ({counter} tries left)!\nExiting...")
                exit()
            print(f"\nWrong E-mail.\nTry again ({counter} tries left)!\n")
            counter = counter - 1
            email = input("E-mail: ")

        passwd = input("New password: ")

        query_filter = {"username": userdata["username"]}
        update_operation = {"$set": {"password": passwd}}

        self.db.collection.update_one(query_filter, update_operation)
        print("Password changed.\n")

    def display_user_data(self, username):
        self.db.access_collection("users")
        userdata = self.db.collection.find_one({"username": username})

        table = Table(f"{username}'s data", box=box.ROUNDED, show_header=False)
        table.add_row("Username", userdata["username"])
        table.add_row("E-Mail", userdata["email"])
        table.add_row("Total books issued", str(userdata["total_books_issued"]))

        book_ids = list(userdata["currently_issued"])
        self.db.access_collection("books")
        books = []
        for i in book_ids:
            book = self.db.collection.find_one({"_id": i})
            books.append(book["title"])

        table.add_row("Currently issued", str(books))

        console.print(table, justify="center")
        print("\n")
