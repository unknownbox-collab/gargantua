import pygame,sys,math,time,copy
import numpy as np

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

WHITE = (255, 255, 255)
ORANGE = (255, 127, 0)
BLACK = (0, 0, 0)
G = 6.673 * 1e-10
camSize = 1

pygame.init()
pygame.display.set_caption("GARGANTUA")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def add_h(arg):
    h = 1e-6
    return int(arg/(camSize+h))
def addTwoVector(v1,v2):
    one = np.array((math.cos(math.radians(v1[0]))*v1[1],math.sin(math.radians(v1[0]))*v1[1]))
    two = np.array((math.cos(math.radians(v2[0]))*v2[1],math.sin(math.radians(v2[0]))*v2[1]))
    return one + two

def posToVector(v):
    return np.array((math.atan2(v[1],v[0])*180/math.pi, math.sqrt(v[0]**2+v[1]**2)))

class Gargantua():
    def __init__(self,x,y,weight=1.3923e+41) -> None:
        self.x = x
        self.y = y
        self.weight = weight
    
    def draw(self):
        pygame.draw.circle(screen, ORANGE, (SCREEN_WIDTH/2+add_h(self.x), SCREEN_HEIGHT/2+add_h(self.y)), add_h(55))
        pygame.draw.circle(screen, BLACK, (SCREEN_WIDTH/2+add_h(self.x), SCREEN_HEIGHT/2+add_h(self.y)), add_h(40))

class Ranger():
    def __init__(self,x,y,degree,weight = 10,initForce = 0,constantForce = (-90,0)) -> None:
        self.img = pygame.image.load('ranger.jpg')
        self.img = pygame.transform.scale(self.img, (add_h(10), add_h(10)))
        self.img = pygame.transform.rotate(self.img, degree)
        self.x = x
        self.y = y
        self.weight = weight
        self.degree = degree
        self.speed = 0
        self.forceDegree = degree
        self.forceValue = initForce
        self.constantForceDegree = constantForce[0]
        self.constantForceValue = constantForce[1]
    
    def gravityCalculate(self,blackhole):
        r = math.sqrt((blackhole.x - self.x)**2 + (blackhole.y - self.y)**2)*camSize
        degree = math.atan2(self.y-blackhole.y,self.x-blackhole.x)*180/math.pi
        speed = - G * self.weight * blackhole.weight /(r**2)

        gravity = np.array((math.cos(degree)*speed,math.sin(degree)*speed))
        result = addTwoVector((degree,speed),(self.forceDegree,self.forceValue))
        result = addTwoVector(posToVector(result),posToVector(addTwoVector((0,0),(self.constantForceDegree,self.constantForceValue))))
        self.forceDegree = posToVector(result)[0]
        self.forceValue = posToVector(result)[1]
    
    def move(self,blackhole):
        self.gravityCalculate(blackhole)
        d = addTwoVector((self.forceDegree,self.forceValue),(self.degree,self.speed))
        self.x += d[0]
        self.y += d[1]
        
        d = posToVector(d)
        self.degree, self.speed = d
        #print(self.speed)
    
    def draw(self):
        x = add_h(self.x)+SCREEN_WIDTH/2
        y = add_h(self.y)+SCREEN_HEIGHT/2
        dx = add_h(math.cos(math.radians(self.degree)) * 15)
        dy = add_h(math.sin(math.radians(self.degree)) * 15)
        dx2 = add_h(math.cos(math.radians(self.degree+120)) * 10)
        dy2 = add_h(math.sin(math.radians(self.degree+120)) * 10)
        dx3 = add_h(math.cos(math.radians(self.degree-120)) * 10)
        dy3 = add_h(math.sin(math.radians(self.degree-120)) * 10)
        dx = int(math.cos(math.radians(self.degree)) * 15)
        dy = int(math.sin(math.radians(self.degree)) * 15)
        dx2 = int(math.cos(math.radians(self.degree+120)) * 10)
        dy2 = int(math.sin(math.radians(self.degree+120)) * 10)
        dx3 = int(math.cos(math.radians(self.degree-120)) * 10)
        dy3 = int(math.sin(math.radians(self.degree-120)) * 10)
        #pygame.draw.polygon(surface=screen, color=WHITE, points=[(x+dx,y+dy), (x+dx2,y+dy2), (x+dx3,y+dy3)])
        pygame.draw.polygon(surface=screen, color=WHITE, points=[(x+dx,y+dy), (x+dx2,y+dy2), (x+dx3,y+dy3)])
        #screen.blit(self.img, (add_h(self.x)+SCREEN_WIDTH/2, add_h(self.y)+SCREEN_HEIGHT/2))

clock = pygame.time.Clock()
gargantua = Gargantua(0,0,10000000000)
initRanger = Ranger(200,200,-90,initForce=0,constantForce=(-90,0.00005))
ranger = copy.copy(initRanger)
while True:
    clock.tick(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(BLACK)
    #print("=====")
    #print(ranger.x,ranger.y)
    ranger.move(gargantua)
    #print(ranger.x,ranger.y)
    if math.sqrt((ranger.x - gargantua.x)**2 + (ranger.y - gargantua.y)**2)*camSize <= 120:# or math.sqrt((ranger.x - gargantua.x)**2 + (ranger.y - gargantua.y)**2)*camSize >= 5550:
        print(ranger.x,ranger.y)
        ranger = copy.copy(initRanger)
    print(ranger.forceValue)
    #print(ranger.x,ranger.y)
    #print("=====")
    
    pygame.draw.line(screen,WHITE,(0,250),(500,250))
    pygame.draw.line(screen,WHITE,(250,0),(250,500))
    gargantua.draw()
    ranger.draw()
    #print("D : ",math.sqrt((ranger.x - gargantua.x)**2 + (ranger.y - gargantua.y)**2))
    #print(ranger.x,ranger.y)
    camSize = max(math.sqrt((ranger.x - gargantua.x)**2 + (ranger.y - gargantua.y)**2)/(120*math.sqrt(2)),3)
    #print("C : ",camSize)
    #time.sleep(1)
    pygame.display.update()