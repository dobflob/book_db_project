from models import Base, session, Book, engine
import csv
import datetime

# Clean Date
def clean_date(date_str):
    MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    split_date = date_str.split(' ')
    # get integer values for month, day, and year
    month = int(MONTHS.index(split_date[0]) + 1)
    day = int(split_date[1].replace(',',''))
    year = int(split_date[2])
    return datetime.date(year, month, day)

# Clean Price
def clean_price(price_str):
    price_float = float(price_str)
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
            pass
        elif choice == '2':
            # view all books
            pass
        elif choice == '3':
            # search books
            pass
        elif choice == '4':
            # book analysis
            pass
        else:
            print('\nGoodbye\n')
            app_running = False

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    # app()

    for book in session.query(Book):
        print(book)