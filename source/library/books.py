from database.access_database import MongoDatabase

from rich.console import Console
from rich.table import Table
from rich import box

import smtplib

console = Console()


class Books:
    def __init__(self) -> None:
        self.db = MongoDatabase()
        self.db.connect_database("library_database")

    def list_all_books(self):
        self.db.access_collection("books")
        booksdata = self.db.collection.find({})

        table = Table(title="Books list", box=box.ROUNDED)
        table.add_column("No.")
        table.add_column("Title")
        table.add_column("Author")
        table.add_column("Available in stack")
        counter = 1
        for i in booksdata:
            table.add_row(str(counter), i["title"], i["author"], "yes" if i["available"] else "no")
            counter = counter + 1

        console.print(table, justify="center")

    def list_available_books(self):
        self.db.access_collection("books")
        booksdata = self.db.collection.find({"available": True})

        table = Table(title="Books available in stack", box=box.ROUNDED)
        table.add_column("No.")
        table.add_column("Title")
        table.add_column("Author")
        table.add_column("Language")
        table.add_column("Year")
        counter = 1
        for i in booksdata:
            table.add_row(str(counter), i["title"], i["author"], i["language"], str(i["year"]))
            counter = counter + 1

        console.print(table, justify="center")

    def search_book(self):
        keyword = input("\nKeyword: ")
        self.db.access_collection("books")
        results = list(self.db.collection.find({"title": {"$regex": keyword, "$options": "i"}}))

        counter = 1
        if results == None:
            console.print("\nNo matches found!", style="bold")

        else:
            table = Table(title="Books found", box=box.ROUNDED)
            table.add_column("No.")
            table.add_column("Title")
            table.add_column("Author")
            table.add_column("Available in stack")
            for i in results:
                table.add_row(
                    str(counter),
                    i["title"],
                    i["author"],
                    "yes" if i["available"] else "no",
                )
                counter = counter + 1

            console.print(table, justify="center")

    def request_book(self, username):
        self.db.access_collection("users")
        userdata = self.db.collection.find_one({"username": username})
        print("Write an E-mail to request a book.\n")

        APP_PASSWORD = ("https://github.com/sayanmondl/library-system/docs/create-app-password.md")
        console.print("Read the docs to create app-password", APP_PASSWORD, justify="center")

        if userdata["email_password"] == None:
            passwd = input("Add your e-mail password: ")
            self.db.collection.update_one(
                {"username": username}, {"$set": {"email_password": passwd}}
            )
            print("Password added to your library account.\n")

        email = userdata["email"]
        print(f"From: {email}")
        if (input("Your email-password is associated with another email? [y/n]: ") == "y"):
            email = input("Enter e-mail: ")

        admin = self.db.collection.find_one({"username": "sayan"})
        print(f"To:", admin["email"], "\n")
        print("Enter message, end with `ctrl-d` (Unix) or `ctrl-z` (Windows):")

        msg = ""
        while True:
            try:
                line = input()
            except EOFError:
                break
            if not line:
                break
            msg = msg + line

        try:
            server = smtplib.SMTP_SSL("smtp.gmail.com")
            server.ehlo()
            userdata = self.db.collection.find_one({"username": username})
            server.login(email, userdata["email_password"])
            server.sendmail(email, admin["email"], msg)
            server.close()
            print("\nEmail sent!\n")

        except Exception as e:
            print(f"Unable to send email due to {e}")

    def delete_book(self, book_id):
        try:
            self.db.access_collection("books")
            self.db.collection.delete_one({"_id": book_id})
        except:
            print("Book not found.\n")

    def add_book(self):
        console.print("Add a book.", style="bold")
        title = input("Title: ")
        author = input("Author: ")
        language = input("Language: ")
        country = input("Country: ")
        year = input("Year: ")
        pages = input("Pages: ")
        link = input("Link: ")

        table = Table(title="Book info", show_header=False, box=box.ROUNDED)
        table.add_row("Title", title)
        table.add_row("Author", author)
        table.add_row("Language", language)
        table.add_row("Country", country)
        table.add_row("Year", year)
        table.add_row("Pages", pages)
        table.add_row("Link", link)

        console.print(table, justify="center")

        if input("Confirm add? [y/n]: ") == "y":
            try:
                self.db.access_collection("books")
                self.db.collection.insert_one(
                    {
                        "author": author,
                        "country": country,
                        "language": language,
                        "link": link,
                        "pages": pages,
                        "title": title,
                        "year": year,
                        "available": True,
                    }
                )
                print("Book added to library.\n")
            except:
                print("There was a problem adding book.\n")
