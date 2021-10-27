import math,random,datetime,main,json,copy

from numpy.core.fromnumeric import reshape
import numpy as np

GENE_SET = 10000
OBJECT_NUM = 10
GENE_NUM = 7
BEST_NUM = 2

def mCopy(arg):
    return list(map(copy.copy,arg))
def makeParents():
    result = [np.random.choice(GENE_SET, GENE_NUM, replace=False) for i in range(OBJECT_NUM)]
    return result[:]

def selection(gene,fitness):
    result = [[],[]]
    copyGene = mCopy(gene)
    copyFitness = mCopy(fitness)
    for i in range(BEST_NUM):
        best = np.argmax(copyFitness)
        result[0].append(copyGene[best])
        result[1].append(copyFitness[best])
        del copyGene[best]
        del copyFitness[best]
    return mCopy(result)

def crossOver(gene):
    result = mCopy(gene)
    random.shuffle(result)
    for i in range(len(gene)//2):
        first = result[i]
        second = result[i+1]
        a = random.randint(0,GENE_NUM-2)
        b = random.randint(a,GENE_NUM)
        temp = first[a:b]
        first[a:b] = second[a:b]
        second[a:b] = temp
        result[i] = copy.copy(first)
        result[i+1] = copy.copy(second)
    return  mCopy(result)

def simulation(gene,nowCycle = None,printMod = False) -> list:
    result = []
    copyGene = mCopy(gene)
    for i in range(len(gene)):
        result.append(main.get_fitness(copyGene[i]))
        if printMod:
            if nowCycle is None:
                print(f'{round((i+1)/len(gene)*100,3)}%')
            else:
                print(f'Generation {nowCycle+1}...{round((i+1)/len(gene)*100,3)}%')
    return result[:]

def mutation(gene,percent = 10) -> list:
    copyGene = mCopy(gene)
    result = copyGene
    for i in range(len(gene)):
        for j in range(GENE_NUM):
            if random.random() < percent/100:
                result[i][j] = random.randint(0,GENE_SET)
    return mCopy(result)

def oneCycle(gene,generation = 0,printMod = False):
    if printMod : print(f"/////GENERATION {generation+1}/////")
    fitness = simulation(mCopy(gene),generation,printMod)[:]
    print("///////////////")
    print(np.max(fitness))
    bestGene = selection(mCopy(gene),fitness[:])[0]
    S = sum([selection(mCopy(gene),fitness[:])[0] for i in range(OBJECT_NUM//BEST_NUM-1)] ,[])
    G2 = mCopy(crossOver(S))
    G2 = mCopy(mutation(G2,20))
    final = bestGene
    final.extend(mCopy(G2))
    return mCopy(final),fitness[:]

def GA(generation,file = False,printMod = False):
    try:
        gene = [makeParents(),np.zeros(OBJECT_NUM)]
        now = datetime.datetime.now()
        if file:
            print("초기 데이터 설정중..")
            fitness = simulation(gene[0],printMod = True)
            data = {"gene" : [list(map(list,mCopy(gene)[0]))],
                    "fitness" : [fitness[:]],
                    "bestGene" : [list(mCopy(gene)[0][np.argmax(fitness[:])])],
                    "bestFitness" : [np.max(fitness[:])]
                }
            print("초기데이터 설정 완료!")
        for i in range(generation):
            gene = oneCycle(mCopy(gene)[0],i,printMod)[:]
            #print(chromosomes[np.argmax(map(getFitness,fitness[:]))])
            if file:
                data["gene"].append(list(map(list,mCopy(gene)[0])))
                data["fitness"].append(mCopy(gene)[1])
                data["bestGene"].append(list(mCopy(gene)[0][np.argmax(mCopy(gene)[1])]))
                data["bestFitness"].append(np.max(mCopy(gene)[1]))
        if file:
            openFile = open(f'./result/GA_{now.year}.{now.month}.{now.day}.{now.hour}.{now.minute}.{now.second}.{now.microsecond}.json','w')
            data["fitness"].pop(1)
            data = eval(str(data))
            openFile.write(json.dumps(data,indent=4))
            openFile.close()
    except KeyboardInterrupt:
        if file:
            now = datetime.datetime.now()
            openFile = open(f'./result/GA_{now.year}.{now.month}.{now.day}.{now.hour}.{now.minute}.{now.second}.{now.microsecond}.json','w')
            data = eval(str(data))
            openFile.write(json.dumps(data,indent=4))
            openFile.close()

GA(30,True,True)