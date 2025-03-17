from car import Car
from car import Book, Library

car1 = Car("Lamba")

car2 = Car("Merc")

car1.set_color("red")
car2.set_color("white")

print(car1.color, car2.color)

print("Finish")
________
book = "Граф монте-кристо"
book1 = Book('Граф монте-кристо', 'Дюма', " 1844", '1000')
book2 = Book('Женщина в песках', "Абе Кобо", '2006', '200')


Library1 = Library([book1, book2])

# Получилось удалить?
Library1.remove_book(book)

a = Library1.find_book_by_name(book)

if a is not None:
    print("Нашел")
else:
    print("не нашел")


def func(par1, par2):
    print(par1, par2)

func(1, 2)

