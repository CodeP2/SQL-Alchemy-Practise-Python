import books_holder
import datetime
from decimal import Decimal


def add_book(new_author, new_title, new_publish_time, new_price):
    date_conv, deci_conv = data_cleaning(new_publish_time, new_price)
    book = books_holder.Books(author=new_author, title=new_title, published=date_conv, price=deci_conv)
    books_holder.session.add(book)
    yes_or_no_menu()


def data_cleaning(to_date=None, to_decimal=None, option=1):
    if option == 1:
        date = datetime.datetime.strptime(to_date, '%B %d, %Y').date()
        decimal = Decimal(to_decimal)
        return date, decimal
    elif option == 2:
        date = datetime.datetime.strptime(to_date, '%B %d, %Y').date()
        return date
    elif option == 3:
        decimal = Decimal(to_decimal)
        return decimal


def show_all_books():
    entry_number = 1
    for entry in books_holder.session.query(books_holder.Books):
        print(f"Entry number: {entry_number}:\n{entry}")
        entry_number += 1


def search_book(index_number):
    for entry in books_holder.session.query(books_holder.Books).filter(books_holder.Books.id==index_number):
        return entry


def edit_or_delete_menu(entry):
    option = int(input("what would you like to do?\n\n1) Edit a book\n2) Delete a book\n3) Exit\n\n>  "))
    if option == 1:
        edit_book(entry)
    elif option == 2:
        delete_book(entry)


def edit_book(entry):
    print(f"Currently you are trying to edit:\n{entry}")
    option = int(input("What kind of entry would you like to change?\
                        \n1) Author\n2) Publish data\n3) Price\n\n>  "))
    if option == 1:
        new_author = input("Author: ")
        entry.author = new_author
    elif option == 2:
        new_publish = input("Published (Example: January 13, 2005): ")
        clean = data_cleaning(new_publish, None, 2)
        entry.published = clean
    elif option == 3:
        new_price = input("Price (Example: 12.22): ")
        clean = data_cleaning(None, new_price, 3)
        entry.price = clean
    yes_or_no_menu()


def delete_book(entry):
    confirm_to_delete = input("Are you sure you want to delete the book?(Y/N)\
                            \n(WARNING: This cannot be undone)\n\n>  ")
    if confirm_to_delete.lower() == "y":
        books_holder.session.delete(entry)
        books_holder.session.commit()
    else:
        pass


def yes_or_no_menu():
    question = input(f"Are you sure you want to add/edit this user?(Y/N):\n")
    while True:
        if question.lower() in ["y", "n"]:
            break
        else:
            question = input(f"That's inncorrect input please try again (Correct inputs are (Y/N)\
                            \nAre you sure you want to add/edit this user?(Y/N):\n")
    if question.lower() == "y":
        books_holder.session.commit()
        print("Book added!")
    else:
        pass


def book_analysis_menu():
    option = int(input("Analysis Menu\n1) Show the oldest book by publish date\n2) Show the newset book by publish date\
                       \n3) Show total number of the books\n4) Average price for all books\n>  "))
    if option == 1:
        print(oldest_book())
    elif option == 2:
        print(newest_book())
    elif option == 3:
        print(total_books())
    elif option == 4:
        print(avg_price())
    input("Press enter to continue...")


def oldest_book():
    return books_holder.session.query(books_holder.Books).order_by(books_holder.Books.published).first()


def newest_book():
    return books_holder.session.query(books_holder.Books).order_by(books_holder.desc(books_holder.Books.published)).first()


def total_books():
    return books_holder.session.query(books_holder.func.count()).select_from(books_holder.Books).scalar()


def avg_price():
    return books_holder.session.query(books_holder.func.avg(books_holder.Books.price)).scalar()


def main_menu():
    while True:
        print("PROGRAMING BOOKS\n1) Add Book\n2) View All Books\n3) Search for a book\
              \n4) Book Analysis\n5) Exit\n")
        decision = int(input("What Would you like to do?\n>  "))
        if decision == 1:
            author = input("Author: ")
            title = input("Title of the book: ")
            published = input("Published (Example: January 13, 2005): ")
            price = input("Price (Example: 12.22): ")
            add_book(author, title, published, price)
        elif decision == 2:
            show_all_books()
        elif decision == 3:
            print(f"Options: {[item[0] for item in books_holder.session.query(books_holder.Books.id)]}")
            index_num = int(input("What is the book's id? "))
            entry = search_book(index_num)
            edit_or_delete_menu(entry)
        elif decision == 4:
            print(book_analysis_menu())
        elif decision == 5:
            break


books_holder.Base.metadata.create_all(books_holder.engine)
main_menu()
