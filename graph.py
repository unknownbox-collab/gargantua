import matplotlib.pyplot as plt
import numpy as np
import os,json

class Result():
    def __init__(self,fileName = None) -> None:
        if fileName is None:
            dirs = os.listdir('./result')
            fileSelect = input("===CHOOSE FILE===\n"+'\n'.join([f"[{i}] {dirs[i]}" for i in range(len(dirs))])+"\n>>> ")
            self.fileName = dirs[int(fileSelect)]            
        else:
            self.fileName = fileName
    
    def dump(self,ratioMod = False):
        with open("./result/"+self.fileName, "r") as file:
            result = json.load(file)
        if ratioMod:
            for i in result.keys():
                maxValue = np.max(result[i])
                minValue = np.min(result[i])
                if abs(maxValue) <= abs(minValue): maxValue = abs(minValue)
                result[i] /= maxValue
        return result

    def drawGraph(self,value = None,ratioMod = None):
        if value is None:
            OPTIONS = ["forceValue","distance","speed","deltaForceValue","pos","deltaPos"]
            optionSelect = input("===CHOOSE VALUES===\n"+'\n'.join([f"[{i}] {OPTIONS[i]}" for i in range(len(OPTIONS))])+"\n>>> ").split(",")
            value = [OPTIONS[int(i)] for i in optionSelect]
        if ratioMod is None:
            ratioMod = bool(int(input("===RATIO MOD?===\n[0] No\n[1] Yes\n>>> ")))
        data = [self.dump(ratioMod = ratioMod)[i] for i in value]
        for i in range(len(data)) : plt.plot(list(range(len(data[i]))),data[i],label = value[i])
        plt.legend()
        plt.show()
Result().drawGraph()