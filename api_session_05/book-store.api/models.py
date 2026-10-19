from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.orm import mapped_column, relationship

db = SQLAlchemy()

book_authors = db.Table(
    "book_authors",
    db.Column("book_id", ForeignKey("books.id"), primary_key=True),
    db.Column("author_id", ForeignKey("authors.id"), primary_key=True)
)

class Book(db.Model):
    __tablename__ = "books"
    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String(200))
    isbn = mapped_column(String(13), unique=True)
    price_vnd = mapped_column(Integer)
    stock = mapped_column(Integer, default=0)
    category_id = mapped_column(ForeignKey("categories.id"))
    category = relationship("Category")
    authors = relationship("Author", secondary="book_authors")
    reviews = relationship("Review")

    def to_dict(self):
        return {"id": f"book_{self.id}", "title": self.title}


class Author(db.Model): # cần id primary key
    __tablename__ = "authors"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100))
    bio = mapped_column(Text)
    books = relationship("Book", secondary="book_authors")

class Category(db.Model):
    __tablename__ = "categories"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100))
    slug = mapped_column(String(100), unique=True)
    books = relationship("Book")

class Review(db.Model):
    __tablename__ = "reviews"
    id = mapped_column(Integer, primary_key=True)
    book_id = mapped_column(ForeignKey("books.id"))

    book = relationship("Book")

    user_id = mapped_column(ForeignKey("users.id"))

    user = relationship("User")

class User(db.Model):
    __tablename__ = "users"
    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(Text)
    display_name = mapped_column(String(100))

    orders = relationship("Order")

    reviews = relationship("Review")

class Order(db.Model):
    __tablename__ = "orders"
    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(ForeignKey("users.id"), nullable=False)

    user = relationship("User")