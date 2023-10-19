import matplotlib.pyplot as plt
from matplotlib import image


def HeatMap(kills):
    data = image.imread('static/map.png') 
    for kill in kills:
        if kill['killer']>=6: color ="blue"
        else: color = "red"
        plt.plot((kill["position"]["x"]*512)/15000, (kill["position"]["y"]*512)/15000, marker="v", color=color)
    plt.imshow(data)
    plt.show() 
    
