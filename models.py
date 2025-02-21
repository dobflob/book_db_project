from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker

# Create a database
# name it: books.db
# Create a model including: title, author, date published, and price
engine = create_engine('sqlite:///books.db', echo=False)
Session = sessionmaker(engine)
session = Session()
Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column('Title', String)
    author = Column('Author', String)
    published_date = Column('Published', Date)
    price = Column('Price', Integer)

    def __repr__(self):
        return f'Title: {self.title}, Author: {self.author}, Published: {self.published_date}, Price: {self.price}'