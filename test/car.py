from typing import Optional

print("Car imported")

class Car:
    def __init__(self):
        self.name = name
        self.color = "black"

    def set_color(self, color: str):
        self.color = color


"""
Нужны название, автор, год и количнство страниц 
"""
class Book:
    def __init__(self, name: str, author: str, year: int, pages: int):
        self.name = name
        self.author = author
        self.year = year
        self.pages = pages
        pass
    

class Library:
    def __init__(self, books: list[Book]):
        self.books = books
        passВернуть книги, год которых лежит в переданном диапозоне.
        Передаются два числа - год начала и год конца.
        Нужно найти книги написанные между этими датами

    def add_book(self, book: Book ):
        # Проверку на уникальность книги
        self.books.append(book)
        pass
    

    def remove_book(self, name ):
        # Не понятно - удалили ли мы книгу или мы не нашли ее
        for i in range(len(self.books)):
            delete_book = self.books[i].name
            if name == delete_book:
                del self.books[i]
                return
        pass

    def find_book_by_name(self, name) -> Optional[Book]:
        for i in range(len(self.books)):
            my_book = self.books[i]
            if name == my_book.name:
                return my_book
            
        return None
        pass

    def find_books_by_author(...) -> ...:
        """
        Вернуть список книг данного автора
        """
        pass

    def find_books_in_range(...) -> ...:
        """
        Вернуть книги, год которых лежит в переданном диапозоне.
        Передаются два числа - год начала и год конца.
        Нужно найти книги написанные между этими датами
        """
        pass
