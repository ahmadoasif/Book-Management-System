import json
import os

def changedirectory():
    try:
        script_path = __file__
        absolute_path = os.path.abspath(script_path)
        directory = os.path.dirname(absolute_path)
        os.chdir(directory)
    except NameError:
        print("This script is running interactively or in an environment where __file__ is not available.")
        directory = os.getcwd()  # Fallback to current working directory

def Menu():
    menu = {1: 'Add Book', 2: 'Search Books', 3: 'Remove Books', 4: 'List Books'}
    for i in menu:
        print(f"{i} : {menu[i]}")
    
    while True:
        raw_input = input("Select an Option: ")
        try:
            user_selection = int(raw_input)
            if user_selection in menu:
                redirect(user_selection)
            else:
                print("Invalid option")
        except ValueError:
            print("Invalid input")

def AddBook():
    class Dic_compilar:
        def __init__(self, book, author, date, inStock):
            self.book = book
            self.author = author
            self.date = date
            self.inStock = inStock
        
        def file_handel(self):
            book_detail = {
                "BookName": self.book,
                "Author": self.author,
                "Published": self.date,
                "Available": self.inStock
            }
            try:
                with open("book_list.json", 'r') as file:
                    content = file.read()
                    if content.strip() == "":
                        data = []
                    else:
                        data = json.loads(content)
            except FileNotFoundError:
                print("No File Found. Creating New File...")
                data = []
                
            data.append(book_detail)
            with open("book_list.json", 'w') as file:
                json.dump(data, file, indent=4)

    book_name = input("Enter Book Name: ").lower()
    book_author = input("Author: ").lower()
    book_published = int(input("Release Date: "))
    is_available = int(input("Available? Enter '1' for yes and '0' for no: "))
    new_book = Dic_compilar(book_name, book_author, book_published, is_available)
    new_book.file_handel()

def redirect(x):
    if x == 1:
        AddBook()
    elif x == 2:
        SearchBook()
    elif x == 3:
        RemoveBook()
    else:
        ListBook()

def SearchBook():
    def IsAvailable(content, keyword):
        found = []
        for item in content:
            if item["BookName"] == keyword or item["Author"] == keyword:
                found.append(item)
        return found

    try:
        with open("book_list.json", 'r') as file:
            content = json.load(file)
            if content:
                keyword = input("Enter Book Name or Search By Author Name: ").lower()
                books = IsAvailable(content, keyword)
                if books:
                    for item in books:
                        print(f"{item['BookName']} written by {item['Author']} on {item['Published']}")
                else:
                    print("No Book or Author Found")
            else:
                print("No Books Available right now")
    except FileNotFoundError:
        print("No data to search from")
        if input("Do you want to Add a new Book? Type 'y' for yes or any key to return: ") == "y":
            AddBook()
        else:
            print("Returning To Main Menu...")

def RemoveBook():
    book = input("Enter Book Name: ").lower()
    try:
        with open("book_list.json", 'r') as file:
            content = json.load(file)
        filtered_list = [item for item in content if item["BookName"] != book]
        
        if len(filtered_list) < len(content):
            print("Book removed successfully.")
            with open("book_list.json", 'w') as file:
                json.dump(filtered_list, file, indent=4)
        else:
            print("Book not found.")
    except FileNotFoundError:
        print("No data to remove from.")

def ListBook():
    try:
        with open("book_list.json", 'r') as file:
            for item in json.load(file):
                availability = "Currently Available" if item['Available'] else "Currently not Available"
                print(f"{item['BookName']} written by {item['Author']} published on {item['Published']} is {availability}")
    except FileNotFoundError:
        print("No books available to list.")

changedirectory()
if __name__ == "__main__":
    Menu()
