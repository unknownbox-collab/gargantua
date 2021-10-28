import pygame,sys,math,time,copy,datetime,json
import numpy as np

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

WHITE = (255, 255, 255)
ORANGE = (255, 127, 0)
BLACK = (0, 0, 0)
G = 6.673 * 1e-11
M_SUN = 1.98892e+30
M_EARTH = 5.9722e+24
camSize = 1

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
    def __init__(self,x,y,weight=4.7e+6 * M_SUN) -> None:
        self.x = x
        self.y = y
        self.weight = weight
    
    def draw(self):
        #pygame.draw.circle(screen, ORANGE, (SCREEN_WIDTH/2+add_h(self.x), SCREEN_HEIGHT/2+add_h(self.y)), int(55))
        #pygame.draw.circle(screen, BLACK, (SCREEN_WIDTH/2+add_h(self.x), SCREEN_HEIGHT/2+add_h(self.y)), int(50))
        pygame.draw.circle(screen, ORANGE, (SCREEN_WIDTH/2+add_h(self.x), SCREEN_HEIGHT/2+add_h(self.y)), add_h(55))
        pygame.draw.circle(screen, BLACK, (SCREEN_WIDTH/2+add_h(self.x), SCREEN_HEIGHT/2+add_h(self.y)), add_h(50))

class Ranger():
    def __init__(self,x,y,degree,weight = 10,initSpeed = 0,initForce = 0,constantForce = (-90,0)) -> None:
        #self.img = pygame.image.load('ranger.jpg')
        #self.img = pygame.transform.scale(self.img, (add_h(10), add_h(10)))
        #self.img = pygame.transform.rotate(self.img, degree)
        self.x = x
        self.y = y
        self.weight = weight
        self.degree = degree
        self.speed = initSpeed
        self.forceDegree = degree
        self.forceValue = initForce
        self.constantForceDegree = constantForce[0]
        self.constantForceValue = constantForce[1]
    
    def gravityCalculate(self,blackhole):
        r = math.sqrt((blackhole.x - self.x)**2 + (blackhole.y - self.y)**2)
        degree = math.atan2(self.y-blackhole.y,self.x-blackhole.x)*180/math.pi
        speed = - G * blackhole.weight /(r**2)

        result = addTwoVector((degree,speed),(self.forceDegree,self.forceValue))
        result = addTwoVector(posToVector(result),posToVector(addTwoVector((0,0),(self.constantForceDegree,self.constantForceValue))))
        self.forceDegree = posToVector(result)[0]
        self.forceValue = posToVector(result)[1]
    
    def move(self,blackhole):
        self.gravityCalculate(blackhole)
        d = addTwoVector((self.forceDegree,self.forceValue/self.weight),(self.degree,self.speed))
        self.x += d[0]
        self.y += d[1]
        
        d = posToVector(d)
        self.degree, self.speed = d
        #print(self.speed)
    
    def draw(self):
        x = add_h(self.x)+SCREEN_WIDTH/2
        y = add_h(self.y)+SCREEN_HEIGHT/2
        dx = int(math.cos(math.radians(self.degree)) * 15)
        dy = int(math.sin(math.radians(self.degree)) * 15)
        dx2 = int(math.cos(math.radians(self.degree+120)) * 10)
        dy2 = int(math.sin(math.radians(self.degree+120)) * 10)
        dx3 = int(math.cos(math.radians(self.degree-120)) * 10)
        dy3 = int(math.sin(math.radians(self.degree-120)) * 10)
        dx = add_h(math.cos(math.radians(self.degree)) * 15)
        dy = add_h(math.sin(math.radians(self.degree)) * 15)
        dx2 = add_h(math.cos(math.radians(self.degree+120)) * 10)
        dy2 = add_h(math.sin(math.radians(self.degree+120)) * 10)
        dx3 = add_h(math.cos(math.radians(self.degree-120)) * 10)
        dy3 = add_h(math.sin(math.radians(self.degree-120)) * 10)
        pygame.draw.polygon(surface=screen, color=WHITE, points=[(x+dx,y+dy), (x+dx2,y+dy2), (x+dx3,y+dy3)])    
gargantua = Gargantua(0,0,3e+10)
if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("GARGANTUA")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    gene = [
            6273,
            214,
            5916,
            7418,
            5794,
            824,
            2,
            335
        ]
    initRanger = Ranger(gene[0]-5000,gene[1]-5000,gene[2]/5000*180,initSpeed=gene[3]/1000000,initForce=gene[4]/1000000,constantForce=(gene[5]/5000*180,gene[6]/10000000),weight=gene[7]/100)
    #initRanger = Ranger(100,100,-90,initForce=1,constantForce=(-90,0.0),weight=10)
    ranger = copy.copy(initRanger)
    data = {"forceValue":[],
            "distance":[],
            "speed":[],
            "deltaForceValue":[],
            "pos":[],
            "deltaPos":[]}
    startTime = time.time()
    while True:
        clock.tick(1000000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        #m**2=(gargantua.x * m - m*ranger.x + ranger.y - gargantua.y)**2/(50**2) - 1

        screen.fill(BLACK)
        #print("=====")
        #print(ranger.x,ranger.y)
        ranger.move(gargantua)
        #print(ranger.x,ranger.y)
        print(ranger.forceValue,ranger.speed,ranger.degree)
        data["pos"].append([ranger.x,ranger.y])
        if len(data["pos"])>=2 : data["deltaPos"].append(math.sqrt(np.sum((np.array((ranger.x,ranger.y))-np.array(data["pos"][-2]))**2)))
        data["forceValue"].append(ranger.forceValue)
        data["distance"].append(math.sqrt((ranger.x - gargantua.x)**2 + (ranger.y - gargantua.y)**2))
        if len(data["forceValue"])>=2 : data["deltaForceValue"].append(ranger.forceValue-data["forceValue"][-2])
        data["speed"].append(ranger.speed)
        if math.sqrt((ranger.x - gargantua.x)**2 + (ranger.y - gargantua.y)**2) <= 50 or math.sqrt((ranger.x - gargantua.x)**2 + (ranger.y - gargantua.y)**2) > 1e+6:
            print(ranger.x,ranger.y)
            break
            #if time.time()-startTime>10:break
            #ranger = copy.copy(initRanger)
        #print(ranger.forceValue)
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
    now = datetime.datetime.now()

    file = open(f'./result/{now.year}.{now.month}.{now.day}.{now.hour}.{now.minute}.{now.second}.{now.microsecond}.json','w')
    print(sum(data["deltaPos"]))
    file.write(json.dumps(data,indent=4))
    file.close()
    print(f"결과가 저장되었습니다!\n{now.year}.{now.month}.{now.day}.{now.hour}.{now.minute}.{now.second}.{now.microsecond}.json")

def get_fitness(gene,gargantuaInfo):
    gargantua = Gargantua(gargantuaInfo[0],gargantuaInfo[1],gargantuaInfo[2])
    data = {"forceValue":[],
            "distance":[],
            "speed":[],
            "deltaForceValue":[],
            "pos":[],
            "deltaPos":[]}
    ranger = Ranger(gene[0]-5000,gene[1]-5000,gene[2]/5000*180,initSpeed=gene[3]/1000000,initForce=gene[4]/1000000,constantForce=(gene[5]/5000*180,gene[6]/10000000),weight=gene[7]/100)
    startTime = time.time()
    while True:
        ranger.move(gargantua)
        data["forceValue"].append(ranger.forceValue)
        data["pos"].append([ranger.x,ranger.y])
        if len(data["pos"])>=2 : data["deltaPos"].append(math.sqrt(np.sum((np.array((ranger.x,ranger.y))-np.array(data["pos"][-2]))**2)))
        data["distance"].append(math.sqrt((ranger.x - gargantua.x)**2 + (ranger.y - gargantua.y)**2))
        if len(data["forceValue"])>=2 : data["deltaForceValue"].append(ranger.forceValue-data["forceValue"][-2])
        data["speed"].append(ranger.speed)
        if math.sqrt((ranger.x - gargantua.x)**2 + (ranger.y - gargantua.y)**2) <= 50 or math.sqrt((ranger.x - gargantua.x)**2 + (ranger.y - gargantua.y)**2) > 1e+6: # or time.time() - startTime > 1:
            break
    return sum(data['deltaPos'])