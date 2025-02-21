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
The price format should include a valie number.
Example: 10.99
****************
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
    
# Search for a book
def search_books():
    # it would be nice to be able to search by title, author, or id
    # perhaps that could be it's own menu after choosing 'search for a book' in the main menu?
    search_text = input('>> Book Title:  ')
   
    
# Display all books
def display_books():
    # TODO: probably want to be able to sort the list
    books = []
    for book in session.query(Book):
        # TODO: Format how books are displayed!
        print(f"""
{book.id}. {book.title} by {book.author}
    * Published: {book.published_date.strftime("%B %d, %Y")}
    * Price: ${book.price/100}
""")
        

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

# Get user's menu choice and move to the next step until the user exits the program     
def app():
    app_running = True
    while app_running:
        choice = menu()

        if choice == '1':
            # add book
            add_book()
        elif choice == '2':
            # view all books
            display_books()
            input('\n\nPress enter to return to the main menu...')
        elif choice == '3':
            # search books
            search_books()
            input('\n\nPress enter to return to the main menu...')
        elif choice == '4':
            # book analysis
            pass
        else:
            print('\nGoodbye\n')
            app_running = False

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # add_csv()
    app()