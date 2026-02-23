
from abc import ABC, abstractmethod

class Iterator(ABC):
    
    @abstractmethod
    def hasNext(self): pass

    @abstractmethod
    def next(self): pass


class Book:
    name = None

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return self.name


class BookRepo:
    books = []

    def add(self, book):
        self.books.append(book)



class BookIterator(Iterator):
    idx = 0
    book_repo = None

    def __init__(self, book_repo):
        self.book_repo = book_repo
    
    def hasNext(self):
        if self.idx < len(self.book_repo.books):
            return True
        return False
    
    def next(self):
        ans = self.book_repo.books[self.idx]
        self.idx += 1
        return ans

    


book1 = Book("coding")
book2 = Book("algo")
book3 = Book("dsa")

book_store = BookRepo()
book_store.add(book1)
book_store.add(book2)
book_store.add(book3)



book_itr = BookIterator(book_repo=book_store)

while book_itr.hasNext():
    print(book_itr.next())
