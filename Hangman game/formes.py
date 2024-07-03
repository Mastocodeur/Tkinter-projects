from tkinter import Canvas


class Forme:
    def __init__(self, canevas, x, y):
        self.__canevas = canevas
        self._item = None
        self.x = x
        self.y = y
    
    def effacer(self):
        self.__canevas.delete(self._item)
    
    def deplacement(self, dx, dy):
        self.__canevas.move(self._item, dx, dy)
        self.x += dx
        self.y += dy
    
    def setState(self, s):
        self.__canevas.itemconfig(self._item, state=s)

    def setCouleur(self, couleur):
        # Change la couleur dans le canevas
        self.__canevas.itemconfig(self._item, fill = couleur)

class Rectangle(Forme):
    def __init__(self, canevas, x, y, l, h, couleur):
        Forme.__init__(self, canevas, x, y)
        self._item = canevas.create_rectangle(x, y, x+l, y+h, fill=couleur)
        canevas.itemconfig(self._item, state='hidden')
        self.__l = l
        self.__h = h
    
    def __str__(self):
        return f"Rectangle d'origine {self.x},{self.y} et de dimensions {self.__l}x{self.__h}"

    def get_dim(self):
        return self.__l, self.__h

    def set_dim(self, l, h):
        self.__l = l
        self.__h = h

    def contient_point(self, x, y):
        return self.x <= x <= self.x + self.__l and \
               self.y <= y <= self.y + self.__h

    def redimension_par_points(self, x0, y0, x1, y1):
        self.x = min(x0, x1)
        self.y = min(y0, y1)
        self.__l = abs(x0 - x1)
        self.__h = abs(y0 - y1)

class Ellipse(Forme):
    def __init__(self, canevas, x, y, rx, ry, couleur):
        Forme.__init__(self, canevas, x, y)
        self._item = canevas.create_oval(x-rx, y-ry, x+rx, y+ry, fill=couleur)
        canevas.itemconfig(self._item, state='hidden')
        self.__rx = rx
        self.__ry = ry

    def __str__(self):
        return f"Ellipse de centre {self.x},{self.y} et de rayons {self.__rx}x{self.__ry}"

    def get_dim(self):
        return self.__rx, self.__ry

    def set_dim(self, rx, ry):
        self.__rx = rx
        self.__ry = ry

    def contient_point(self, x, y):
        return ((x - self.x) / self.__rx) ** 2 + ((y - self.y) / self.__ry) ** 2 <= 1

    def redimension_par_points(self, x0, y0, x1, y1):
        self.x = (x0 + x1) // 2
        self.y = (y0 + y1) // 2
        self.__rx = abs(x0 - x1) / 2
        self.__ry = abs(y0 - y1) / 2
