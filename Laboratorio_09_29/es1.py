class Book :

    def __init__(self,title="No title",author="Nobody",pages=0):
        self.title=title
        self.author=author
        self.pages=pages
        
        
    
    def info(self):
        print("Author: {}, Title: {}, Pages: {}.".format(self.author,self.title,self.pages))





b1= Book()

b1.info()

b2= Book(title="Tex Willer",author="Sergio Bonelli",pages=101)
b2.info()