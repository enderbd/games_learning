class Cylinder(object):
    pi = 3.14

    def __init__(self, height=1, radius=1):
        self.r = radius
        self.h = height

    def volume(self):
        volume = Cylinder.pi * (self.r ** 2) * self.h
        print volume

    def area(self):
        area = 2 * Cylinder.pi * self.r * self.h + 2 * Cylinder.pi * (self.r ** 2)
        print area



