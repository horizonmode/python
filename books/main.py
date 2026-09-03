from book import Book
from library import Library

library = Library()

library.add_book(Book("1984", "George Orwell", 1985))
library.add_book(Book("Dune", "Frank Herbert", 1965))

library.borrow_book("dune")
library.list_books()

print(Library.get_library_count())
