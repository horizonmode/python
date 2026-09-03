from book import Book


class Library:
    library_count = 0

    def __init__(self):
        self.books = []
        Library.library_count += 1

    def add_book(self, book):
        self.books.append(book)

    def list_books(self):
        for book in self.books:
            print(book)
            print(f"On loan: {book.on_loan}")

    def borrow_book(self, title):
        for book in self.books:
            if book.title == title:
                return book.borrow()
        return f"No book with the title '{title}' found."

    def return_book(self, title):
        for book in self.books:
            if book.title == title:
                return book.return_book()
        return f"No book with the title '{title}' found."

    @classmethod
    def get_library_count(cls):
        return cls.library_count
