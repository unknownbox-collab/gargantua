import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import os,json
import matplotlib.pyplot as plt

class Result():
    def __init__(self,fileName = None) -> None:
        if fileName is None:
            dirs = os.listdir('./result')
            fileSelect = input("===CHOOSE FILE===\n"+'\n'.join([f"[{i}] {dirs[i]}" for i in range(len(dirs))])+"\n>>> ")
            self.fileName = dirs[int(fileSelect)]            
        else:
            self.fileName = fileName
    
    def dump(self):
        with open("./result/"+self.fileName, "r") as file:
            result = json.load(file)
        return result

    def drawGraph(self,value = None):
        if value is None:
            OPTIONS = ["forceValue","distance","speed","deltaForceValue"]
            optionSelect = input("===CHOOSE VALUES===\n"+'\n'.join([f"[{i}] {OPTIONS[i]}" for i in range(len(OPTIONS))])+"\n>>> ")
            value = OPTIONS[int(optionSelect)]
        data = self.dump()[value]
        plt.plot(list(range(int(len(data)))),data)
        plt.show()
Result().drawGraph()