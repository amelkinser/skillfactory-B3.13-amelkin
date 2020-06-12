
##---------- B3.13 Домашнее задание ----------
##    12.06.2020 г.
##    Группа: PWS-21.
##    Амелькин С.Б.
##--------------------------------------------

class HTML: # Класс для вывода данных на экран или в файл
    def __init__(self, tag, filename=""):
        self.tag = tag
        self.children = []
        self.filename = filename

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.filename == "": #  Вывод на экран
            print("<%s>" % self.tag) 
            for child in self.children:  # в списке классы
                print(child)             # печать-> идет вызов метода __str__ класса child
            print("</%s>" % self.tag)
        else:                   # Вывод в файл
            f= open(self.filename, "w")
            print("<%s>" % self.tag, file=f)
            for child in self.children:  
                print(child, file=f) 
            print("</%s>" % self.tag, file=f)            
            f.flush()
            f.close()
            
    def __iadd__(self, other): # в список дочерних классов поместили очередной класс
        self.children.append(other)
        return(self)

##---------------------------------------------
class TopLevelTag : # класс "верхних" тегов ("head","body")
    
    def __init__(self, tag):
        self.tag = tag
        self.children = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass
    
    def __iadd__(self, other): # в список дочерних классов поместили очередной класс
        self.children.append(other)
        return(self)

    def __str__(self):
        internal=""
        opening = "<%s>\n" % self.tag
        for child in self.children:
            internal = internal+"%s\n" % child
        ending = "</%s>" % self.tag
        return opening + internal + ending

    
##---------------------------------------------
class Tag: # класс остальных тегов 
    def __init__(self, tag, is_single=False, attributes = {}):
        self.tag = tag
        self.text = ""
        self.attributes = attributes

        self.is_single = is_single
        self.children = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass
    
    def __iadd__(self, other):
        self.children.append(other) # в список дочерних классов поместили очередной класс
        return(self)

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append("%s=\"%s\"" % (attribute, value))
        attrs = " ".join(attrs)

        if self.children: # если есть дочерние классы 
            opening = "<%s %s>\n" % (self.tag, attrs)
            internal = "%s" % self.text
            for child in self.children:
                internal = internal+"%s\n" % child
            ending = "</%s>" % self.tag
            return opening + internal + ending
        else:             
            if self.is_single:
                return "<%s %s/>" % (self.tag, attrs)

            else:
                return "<%s %s>%s</%s>" % (self.tag, attrs, self.text, self.tag)    

##---------------------------------------------
            
def main(file_name=""): # Функция формирования конкретного html-текста
    with HTML("html",file_name) as html:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
            head += title
        html += head

        with TopLevelTag("body") as body:
            with Tag("h1", attributes = {"class": "main-text"}) as h1:
                h1.text = "Test"
            body += h1
            with Tag("div", attributes = {"class": "container container-fluid", "id": "lead"}) as div:
                with Tag("p") as p:
                    p.text = "another test"
                with Tag("img", is_single=True, attributes = {"src": "/icon.png", "data-image": "responsive"}) as img:
                    pass
            
                div += p            
                div += img       
            
            body += div    
        html += body
        
##---------------------------------------------
        
if __name__ == "__main__": # Основная программа       
    main()                      # вывод на печать
    main("test_file1.html")     # вывод в файл

    

































































































    











