from models import Base, session, Book, engine
# import models file
# main menu - add, search, analysis, exit, view
# add books to the db
# edit books
# delete books
# search function
# data cleaning
# Loop running our program (i.e. while True)

if __name__ == '__main__':
    Base.metadata.create_all(engine)