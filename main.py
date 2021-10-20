import pygame,sys,math,time

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750

WHITE = (255, 255, 255)
ORANGE = (255, 127, 0)
BLACK = (0, 0, 0)
SCALE = 10e+13
G = 6.673 * 1e-10

pygame.init()
pygame.display.set_caption("GARGANTUA")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Math():
    @staticmethod
    def ParseToRadian(degree):
        return math.pi*degree/180
    
    @staticmethod
    def moveTo(x,y,delta,degree):
        return [
            x + math.cos(Math.ParseToRadian(degree))*delta,
            y + math.sin(Math.ParseToRadian(degree))*delta
        ]
    
    @staticmethod
    def moveToV(x,y,vector):
        return [
            x + math.cos(Math.ParseToRadian(vector.theta))*vector.k,
            y + math.sin(Math.ParseToRadian(vector.theta))*vector.k
        ]

    @staticmethod
    def moveToTheta(x,y,delta,theta):
        return [
            x + math.cos(theta)*delta,
            y + math.sin(theta)*delta
        ]
    
    @staticmethod
    def toVector(PVector):
        return Vector(math.atan2(PVector[1] , PVector[0]), math.sqrt(PVector[0]**2 + PVector[1]**2))

class Vector():
    def __init__(self,theta,k):
        self.theta = theta
        self.k = k
    
    def toPVector(self):
        return [
            math.cos(self.theta) * self.k,
            math.sin(self.theta) * self.k
        ]

class Gargantua():
    def __init__(self,x,y,weight=1.3923e+41) -> None:
        self.x = x
        self.y = y
        self.weight = weight
    
    def draw(self):
        pygame.draw.circle(screen, ORANGE, (self.x, self.y), 15)
        pygame.draw.circle(screen, BLACK, (self.x, self.y), 10)

class Ranger():
    def __init__(self,x,y,degree,weight = 10,speed = 0) -> None:
        self.img = pygame.image.load('ranger.jpg')
        self.img = pygame.transform.scale(self.img, (10, 10))
        self.img = pygame.transform.rotate(self.img, degree)
        self.x = x
        self.y = y
        self.weight = weight
        self.speed = Vector(-degree*math.pi/180, speed)
    
    def gravityCalculate(self,stars):
        v = self.speed
        for star in stars:
            P = v.toPVector()
            r = math.sqrt((star.x-self.x)**2+(star.y-self.y)**2)*SCALE
            F = G*(self.weight * star.weight) / (r**2)
            F = Vector(math.atan2(star.y-self.y,star.x-self.x)*180/math.pi,F)
            #print(F.k)
            #print(math.atan2(-star.y+self.y,star.x-self.x)*180/math.pi)
            print(F.toPVector())
            print(P)
            F = Math.moveToV(P[0],P[1],F)
            print(F)
            v = Math.toVector(F)
            v.theta *= 180/math.pi
        return v
        
    def move(self,stars):
        v = self.gravityCalculate(stars)
        self.x, self.y = Math.moveToV(self.x, self.y, v)
    
    def draw(self):
        screen.blit(self.img, (self.x, self.y))

clock = pygame.time.Clock()
stars = [Gargantua(500,500)]
ranger = Ranger(750,750,90,speed=1)
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(BLACK)
    print("=====")
    print(ranger.x,ranger.y)
    ranger.move(stars)
    print(ranger.x,ranger.y)
    print("=====")
    
    for star in stars : star.draw()
    ranger.draw()
    #time.sleep(1)
    pygame.display.update()