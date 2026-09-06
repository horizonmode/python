# Books and Library

This is the introductory object-oriented scenario. A `Library` coordinates a
collection of `Book` objects and delegates borrowing behavior to each book.

## Concepts demonstrated

### Classes and instances

`Book` defines the data and behavior shared by every book. Each constructed book
is a separate instance with its own title, author, year, and loan state.

### Encapsulation of behavior

Borrowing and returning are implemented by `Book.borrow()` and
`Book.return_book()`. The library asks a book to change itself instead of
changing `book.on_loan` directly.

### Object collaboration

`Library` stores `Book` objects and finds the correct object before forwarding a
borrow or return request.

### Class variables and class methods

`Library.library_count` belongs to the class and is shared across all library
instances. `Library.get_library_count()` accesses it through `cls`.

### String representation

`Book.__str__()` controls how a book appears when passed to `print()` or `str()`.

## Files

- `book.py` — the book entity and its loan behavior
- `library.py` — collection management and library-level operations
- `main.py` — constructs objects and demonstrates their collaboration

## Run

```bash
cd /Users/sebsmith/python/books
python3 main.py
```

## Things to investigate

- Make title searches case-insensitive with `casefold()`.
- Validate that only `Book` objects can be added.
- Replace public attributes with read-only properties.
- Prevent duplicate books.
- Add an `EBook` subclass and override `__str__()`.

This scenario is intentionally simple. Its purpose is to make object ownership
and method calls clear before introducing abstraction and concurrency.
