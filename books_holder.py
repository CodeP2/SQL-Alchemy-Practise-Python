from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy import desc, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import Numeric


engine = create_engine("sqlite:///books.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Books(Base):
    __tablename__ = 'Books'

    id = Column(Integer ,primary_key=True)
    author = Column(String)
    title = Column(String)
    published = Column(Date)
    price = Column(Numeric(10, 2))
    
    def __repr__(self):
        return f'Author: {self.author}\nTitle: {self.title}\nPublished: {self.published}\nPrice: {self.price}\n'


if __name__ == "__main__":
    Base.metadata.create_all(engine)
