import random
import math

def setup():
    size(400,700)
    background(175,175,175)
    
def islegal(position, move):
    return(100<=position+move<=300)

class Image:
    def __init__(self,fname):
        self.speed = 1
        self.y = -50
        self.x = random.choice([35,375])
        self.fname = fname
        self.nextImage = random.randint(100,200)
    
    def move(self):
        self.y += self.speed
        self.img = loadImage(self.fname)
        
    def display(self):
        image(self.img,self.x,self.y,40,60)

class SinCurve:
    def __init__(self):
        self.c = 0
    
    def move(self):
        self.c+=math.pi/60

class Player:
    def __init__(self):
        self.points = 0
        self.speed = 5
        self.helper = False
        
    def addPoint(self):
        self.points += 1
        self.helper = True
       
        if (self.points)%5 == 0 and self.helper:
            self.speed += 0.1
            self.helper = False
        
class Obstacles: 
    def __init__(self,x):
        self.x = x
        self.y = -20
        self.ry = (p.speed)
        self.c = [0,0,0]
        self.duplicate = False
        self.duppoint = 0
        
    def move(self):
        self.y += self.ry
    
    def display(self):
        fill(self.c[0],self.c[1],self.c[2])
        return ellipse(self.x,self.y,20,20)
    
class Lines:
    def __init__(self,x,y=-50):
        self.x = x
        self.y = y
        self.ry = 1
        self.c = [255,255,0]
        self.duplicate = False
        
    def move(self):
        self.y += self.ry
    
    def display(self):
        fill(self.c[0],self.c[1],self.c[2])
        return rect(self.x,self.y,3,20)
    
class Sand:
    def __init__(self,x2,y=0):
        self.x1 = 0
        self.x2 = x2
        self.y = y
        
    def move(self):
        self.y += 1
    
    def display(self):
        stroke(255,252,141)
        line(self.x1,self.y,self.x2,self.y)
        line(400-self.x2,self.y,400,self.y)
        noStroke()

class RoadSand:
    def __init__(self,s,f,y=-1):
        self.x = random.randint(s,f)
        self.y = y
    
    def move(self):
        self.y += 1
    
    def display(self):
        stroke(255,252,141)
        point(self.x,self.y)
        noStroke()

class Car:
    def __init__(self):
        self.y = 650
        self.c = [0,0,0]
        self.position = 200
    
    def move(self,lr):
        if islegal(self.position,lr):
            self.position += lr
               
    def display(self):
        imageMode(CENTER)
        image(loadImage('car.png'),self.position,self.y,30,60)
             
s = SinCurve()
p = Player()
car = Car()

cars = [Obstacles(random.choice([100,200,300]))]
trees = []
palms = [Image('palm.png')]
lines = [Lines(150),Lines(250)]
sandLines = []
roadSand = []

for i in range(0,750,50): #creates road lines
    lines.append(Lines(150,700-i))
    lines.append(Lines(250,700-i))

for i in range(700):
    sandLines.append(Sand(sin(s.c)*4+65,700-i))
    s.move()
    for j in range(random.randint(5,10)):
        roadSand.append(RoadSand(50,350,i))
    
def draw():
    setup()
    
    sandLines.append(Sand(sin(s.c)*4+65))
    for l in sandLines:
        l.move()
        l.display()
        if l.y > 750:
            sandLines.pop(sandLines.index(l))
    
    for i in range(random.randint(5,10)):
        roadSand.append(RoadSand(50,350))
    
    for r in roadSand:
        r.move()
        r.display()
        if r.y > 750:
            roadSand.pop(roadSand.index(r))
    
    s.move() #increase sine function
    
    for i in palms:
       i.move()
       i.display()
       if i.y > 750:
           palms.pop(palms.index(i))
        
    car.display()
    a = False
    
    for i in cars:
        if i.y > 120 and i.duplicate == False:
            a = True
            i.duplicate = True
            
        if i.y > 750:
            cars.pop(cars.index(i))
    
    if a: #places obstacles at 120 pixel intervals
        c = random.choice([1,2]) #place one or two cars
        positions = [100,200,300]
        if c == 1:
            cars.append(Obstacles(positions.pop(random.randint(0,len(positions)-1))))
            print('Car appended')
        if c == 2:
            cars.append(Obstacles(positions.pop(random.randint(0,len(positions)-1))))
            print('Car appended')
            cars.append(Obstacles(positions.pop(random.randint(0,len(positions)-1))))
            print('Car appended')
            
    c = False
    oddCounter=0
    for i in lines: #places lines at 80 pixel intervals
        if i.y > 50 and i.duplicate == False and i.x==250:
            c = True
            i.duplicate = True
        if i.y > 750:
            lines.pop(lines.index(i))
        i.move()
        i.display()
        
    if c:
        lines.append(Lines(150))
        lines.append(Lines(250))
    
    if int(palms[len(palms)-1].y) == int(palms[len(palms)-1].nextImage):
        palms.append(Image('palm.png'))
    
    for i in cars: #ends game
        i.move()
        i.display()
        if i.y > 650 and i.duppoint == 0:
            p.addPoint()
            i.duppoint = 1
    
    noStroke()
    fill(255)
    rectMode(CENTER)
    rect(50,50,60,60)
    fill(0)
    textSize(32)
    textAlign(CENTER)
    text(p.points,50,63)
    
    for i in cars:    
        if i.x == car.position and i.y < 650 and i.y > 610:
            image(loadImage('gameover.jpg'),200,350,400,700)
            fill(255)
            stroke(0)
            textSize(60)
            textAlign(CENTER)
            text("GAME OVER\nScore: "+str(p.points),200,520)
            noLoop()
        
def keyPressed():
    if keyCode==LEFT:
            car.move(-100)
    if keyCode==RIGHT:
            car.move(100)


