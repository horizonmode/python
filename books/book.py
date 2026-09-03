class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year
        self.on_loan = False

    def get_descriptive_name(self):
        return f"{self.title} by {self.author}, published in {self.year}"

    def borrow(self):
        if not self.on_loan:
            self.on_loan = True
            return f"You have borrowed '{self.title}' by {self.author}."
        else:
            return f"'{self.title}' by {self.author} is already on loan."

    def return_book(self):
        if self.on_loan:
            self.on_loan = False
            return f"You have returned '{self.title}' by {self.author}."
        else:
            return f"'{self.title}' by {self.author} was not on loan."

    def __str__(self) -> str:
        return f"'{self.title}' by {self.author}, published in {self.year}. On loan: {self.on_loan}"
