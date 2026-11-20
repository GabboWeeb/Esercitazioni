'''Design a simple class that represents a book that has the following attributes
- title
- author
- pages of pages
that has the following methods:
- info : returns a string with information about the book
use format()->print(....)'''

class book:
    
    def __init__(self , title='No title',author='No author',pages=0):
        self.title=title
        self.author=author
        self.pages=pages
    
    def info(self):
        return "Author: {}, Title: {} , Pages: {} " .format(self.author,self.title,self.pages)

b1=book(title='Promessi Sposi',author='Alessandro Manzoni', pages=500)
print(b1.info())
b2=book()
print(b2.info())