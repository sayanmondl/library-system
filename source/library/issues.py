from database.access_database import MongoDatabase

from rich.console import Console
from rich.table import Table
from rich import box

import datetime

db = MongoDatabase()
console = Console()
db.connect_database("library_database")


def issue_book(username):
    userdata = db.get_user_data(username)
    db.access_collection("books")
    keyword = input("\nSearch for a book: ")
    results = list(db.collection.find({"title": {"$regex": keyword, "$options": "i"}}))

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

        n = input("\nPick a book by number [Press `n` to cancel]: ")
        if n == "n":
            return

        picked = results[int(n) - 1]

        if not picked["available"]:
            print("The book you picked is not abailable in the stack.\n")
            return

        print("You picked", picked["title"], "by", picked["author"], "\n")
        if input("Confirm issue? [y/n]: ") == "y":
            # Update user info
            db.access_collection("users")
            db.collection.update_one(
                {"username": userdata["username"]},
                {"$push": {"currently_issued": picked["_id"]}},
            )
            db.collection.update_one(
                {"username": userdata["username"]},
                {"$set": {"total_books_issued": userdata["total_books_issued"] + 1}},
            )

            # Update available to false
            db.access_collection("books")
            db.collection.update_one(
                {"_id": picked["_id"]}, {"$set": {"available": False}}
            )

            # Update issues
            db.access_collection("issues")
            db.collection.insert_one(
                {
                    "username": userdata["username"],
                    "date_issued": datetime.datetime.now(),
                    "book_id": picked["_id"],
                    "returned": False,
                    "date_returned": None,
                },
            )

            print("Book issued.\n")
            console.print("Full information at:", {picked["link"]}, justify="center")
            print("\n")
        else:
            return


def return_book(username):
    userdata = db.get_user_data(username)
    n_books = len(userdata["currently_issued"])
    print("\nYou have", n_books, "book issued.")

    if n_books == 0:
        console.print("Nothing to return.\n", style="bold")
        return

    table = Table(title="Books issued", box=box.ROUNDED)
    table.add_column("No.")
    table.add_column("Title")
    table.add_column("Author")
    table.add_column("Date issued")

    counter = 1
    db.access_collection("issues")
    user_issues = list(db.collection.find({"username": username, "returned": False}))

    db.access_collection("books")
    for i in user_issues:
        book = db.collection.find_one({"_id": i["book_id"]})
        table.add_row(str(counter), book["title"], book["author"], str(i["date_issued"]))
        counter = counter + 1

    console.print(table, justify="center")

    n = input("\nPick a book to return [Press `n` to cancel & `a` to return all]: ")
    if n == "n":
        print("\n")
        return

    # Return all
    if n == "a":
        if input("Return all? [y/n]: ") == "y":
            for i in user_issues:
                # Update books
                db.access_collection("books")
                book = db.collection.find_one({"_id": i["book_id"]})

                db.collection.update_one(
                    {"_id": book["_id"]}, {"$set": {"available": True}}
                )

                # Update issues
                db.access_collection("issues")
                db.collection.update_one(
                    {"book_id": i["book_id"]},
                    {"$set": {"date_returned": datetime.datetime.now(), "returned": True}}
                )

            # Update user info
            db.access_collection("users")
            db.collection.update_one(
                {"username": userdata["username"]},
                {"$set": {"currently_issued": []}},
            )
        else:
            return
        console.print(f"{n_books} books returned.\n", style="bold")
        return

    # Retunr one
    issue = user_issues[int(n) - 1]
    book = db.collection.find_one({"_id": issue["book_id"]})
    print("You picked", book["title"], "by", book["author"], "\n")

    if input("Confirm return? [y/n]: ") == "y":
        # Update user info
        db.access_collection("users")
        db.collection.update_one(
            {"username": userdata["username"]},
            {"$pull": {"currently_issued": book["_id"]}},
        )

        # Update available to true
        db.access_collection("books")
        db.collection.update_one({"_id": book["_id"]}, {"$set": {"available": True}})

        # Update issues
        db.access_collection("issues")
        db.collection.update_one(
            {"book_id": book["_id"]},
            {"$set": {"date_returned": datetime.datetime.now(), "returned": True}},
        )

        print("Book returned.\n")
    else:
        return


def list_issues():
    db.access_collection("issues")
    issues = db.collection.find({})

    table = Table(title="Issue list", box=box.ROUNDED)
    table.add_column("No.")
    table.add_column("Username")
    table.add_column("Title")
    table.add_column("Author")
    table.add_column("Date Issued")
    table.add_column("Returned")
    table.add_column("Date Returned")

    counter = 1
    db.access_collection("books")
    for i in issues:
        book = db.collection.find_one({"_id": i["book_id"]})
        table.add_row(
            str(counter),
            i["username"],
            book["title"],
            book["author"],
            str(i["date_issued"]),
            "yes" if i["returned"] else "no",
            str(i["date_returned"]) if not None else "",
        )
        counter = counter + 1

    console.print(table, justify="center")


def list_issues_not_returned():
    db.access_collection("issues")
    issues_not_returned = db.collection.find({"returned": False})

    table = Table(title="Issue list - not returned", box=box.ROUNDED)
    table.add_column("No.")
    table.add_column("Username")
    table.add_column("Title")
    table.add_column("Author")
    table.add_column("Date Issued")

    counter = 1
    db.access_collection("books")
    for i in issues_not_returned:
        book = db.collection.find_one({"_id": i["book_id"]})
        table.add_row(
            str(counter),
            i["username"],
            book["title"],
            book["author"],
            str(i["date_issued"]),
        )
        counter = counter + 1

    console.print(table, justify="center")
