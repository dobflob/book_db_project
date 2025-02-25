from models import Base, session, Book, engine
import csv
import datetime
import time

# Clean Data: Date
def clean_date(date_str):
    MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    split_date = date_str.split(' ')
    # get integer values for month, day, and year
    try:
        month = int(MONTHS.index(split_date[0]) + 1)
        day = int(split_date[1].replace(',',''))
        year = int(split_date[2])
    except ValueError:
        print("""
** DATE ERROR **
The date format should include a valid Month Day, Year from the past.
Example: January 3, 2021
****************
""")
        return
    else:
        return datetime.date(year, month, day)

# Clean Data: Price
def clean_price(price_str):
    try:
        price_float = float(price_str)
    except ValueError:
        print("""
** PRICE ERROR **
The price format should include a valid number.
Example: 10.99
*****************
""")
        return
    else:
        return int(price_float * 100)

# Add CSV
def add_csv():
    with open('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            book_in_db = session.query(Book).filter(Book.title==row[0]).one_or_none()
            if book_in_db == None:
                title = row[0]
                author = row[1]
                date = clean_date(row[2])
                price = clean_price(row[3])
                new_book = Book(title=title, author=author, published_date=date, price=price)
                session.add(new_book)
        session.commit()

# Edit Check - make sure edited values are valid
def edit_check(field_str, current_value):
    if field_str == 'Published Date':
        current_value = current_value.strftime("%B %d, %Y")
    elif field_str == 'Price':
        current_value = current_value / 100

    print(f'\nCurrent {field_str}: {current_value}')
    updated_value = input(f'>> Updated {field_str}:  ')
    if field_str == 'Published Date':
        updated_value = clean_date(updated_value)
    elif field_str == 'Price':
        updated_value = clean_price(updated_value)
    return updated_value

# Add Book
def add_book():
    title = input('\nTitle:  ')
    author = input('\nAuthor:  ')
    date_error = True
    while date_error:
        date = input('\nPublished Date: (Example: October 12, 2024)  ')
        date = clean_date(date)
        if date:
            date_error = False
    price_error = True
    while price_error:
        price = input('\nPrice: (Example: 9.99)  ')
        price = clean_price(price)
        if price:
            price_error = False

    book_in_db = session.query(Book).filter(Book.title==title).one_or_none()
    if book_in_db == None:
        new_book = Book(title=title, author=author, published_date=date, price=price)
        session.add(new_book)
        session.commit()
        print('\nBook Added.\n')
        time.sleep(1.5)
    else:
        print('\nBook already exists.')
        return
    
def edit_book(book):
    updated_title = edit_check('Title', book.title)
    updated_author = edit_check('Author', book.author)

    date_error = True
    while date_error:
        updated_published_date = edit_check('Published Date', book.published_date)
        if updated_published_date:
            date_error = False

    price_error = True
    while price_error:
        updated_price = edit_check('Price', book.price )
        if updated_price:
            price_error = False

    book.title = updated_title
    book.author = updated_author
    book.published_date = updated_published_date
    book.price = updated_price
    
    session.commit()
    print('\n\nBook updated successfully.')
    time.sleep(1.5)
    return


def delete_book(book):
    session.delete(book)
    confirm_error = True

    while confirm_error:
        confirm = input(f'\n>> Are you sure you want to remove {book.title} from the database? (y/n)  ')
        if confirm == 'y':
            session.commit()
            print(f'\nBook successfully deleted.')
            confirm_error = False
            time.sleep(1.5)
        elif confirm == 'n':
            print(f'\n{book.title} was not deleted.')
            session.flush()
            print(session.dirty)
            confirm_error = False
            time.sleep(1.5)
        else:
            print("""
** CONFIRMATION ERROR **
Confirmation is required to delete a book.
Press 'y' to confirm the deletion or 'no' to cancel.
************************
""")

# Display all books
def display_books(books):
    # TODO: probably want to be able to sort the list
    for book in books:
        # TODO: Format how books are displayed!

        print(f"""
{book.id}. {book.title} by {book.author}
    * Published: {book.published_date.strftime("%B %d, %Y")}
    * Price: ${book.price/100}
""")
    
# Search for a book
def search_books(books):
    # it would be nice to be able to search by title, author, or id
    # perhaps that could be it's own menu after choosing 'search for a book' in the main menu?
    book_id_list = []
    for book in books:
        book_id_list.append(book.id)
    print(f'{book_id_list}')

    id_error = True
    while id_error:
        try:
            the_book_id = int(input('\nEnter a number to search for a book by Id:  '))
            
        except ValueError:
                    print(f"""
** ID ERROR **
Book id must be a number.
Select an option from the book id list:
{book_id_list}
****************
""")
        else:
            if the_book_id in book_id_list:
                the_book = session.query(Book).filter(Book.id==the_book_id).first()
                id_error = False
                print(f"""
{the_book.id}. {the_book.title} by {the_book.author}
    * Published: {the_book.published_date.strftime("%B %d, %Y")}
    * Price: ${the_book.price/100}
""")
                return the_book
            else:
                print(f"""
** ID ERROR **
Select an option from the book id list.
{book_id_list}
**************
""")

def analyze_books(books):
    oldest_book = books.order_by(Book.published_date).first()
    newest_book = books.order_by(Book.published_date.desc()).first()
    total_books = books.count()
    python_books = books.filter(Book.title.like('%Python%')).count()
    sql_books = books.filter(Book.title.like('%SQL%')).count()
    js_books = books.filter(Book.title.like('%JavaScript%')).count()

    print(F"""
PROGRAMMING BOOK ANALYSIS
-------------------------
Oldest Book: {oldest_book.title}
Newest Book: {newest_book.title}
Total Books: {total_books}  
Python Books: {python_books}
SQL Books: {sql_books}
JavaScript Books: {js_books}
""")
    
    time.sleep(1.5)
    

# Display the app menu and prompt the user to make a selection
def menu():
    while True:
        print("""
PROGRAMMING BOOKS
-----------------
1. Add book
2. View all books
3. Search for a book
4. Book analsis
5. Exit
""")
        
        choice = input('>> What would you like to do?  ')
        if choice in ['1', '2', '3', '4', '5']:
            return choice # return will always cancel out / stop a loop - so a valid choice is the only way out of the menu
        else:
            input('''
Please choose one of the options above (a number 1-5).
Press enter to try again.
''')
            
def book_menu():
    while True:
        print("""
BOOK OPTIONS:
-------------
1. Edit book
2. Delete book
3. Main Menu
""")
        choice = input('>> What would you like to do?  ')
        if choice in ['1', '2', '3']:
            return choice # return will always cancel out / stop a loop - so a valid choice is the only way out of the menu
        else:
            input('''
Please choose one of the options above (a number 1-3).
Press enter to try again.
''')
        
# Get user's menu choice and move to the next step until the user exits the program     
def app():
    app_running = True
    while app_running:
        choice = menu()
        book_list = session.query(Book)
        if choice == '1':
            # add book
            add_book()
        elif choice == '2':
            # view all books
            display_books(book_list)
            input('\n\nPress enter to return to the main menu...')
        elif choice == '3':
            # search books
            selected_book = search_books(book_list)
            if selected_book:
                choice = book_menu()
                if choice == '1':
                    edit_book(selected_book)
                elif choice == '2':
                    delete_book(selected_book)
                elif choice == '3':
                    continue
            input('\n\nPress enter to return to the main menu...')
        elif choice == '4':
            analyze_books(book_list)
            pass
        else:
            print('\nGoodbye\n')
            app_running = False

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # add_csv()
    app()