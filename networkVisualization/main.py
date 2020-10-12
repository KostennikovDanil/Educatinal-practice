from networkx import *
from pyvis.network import Network
from pyvis import network as net
import numpy as np

def pars():
    file=open('dataset.txt','r')
    lines = file.readlines()
    result = list()
    i = 0
    for line in lines:
        result.append(line.split("https://vk.com/id"))
        del result[i][0]
        i+=1

    file.close()
    return result


def visualization():
    print("f")
    ids = pars()
    print(ids)
    layout='test'
    G = Network(height='1500px', width= '1500px', directed=True,layout=None)
    i = 0
    while i < len(ids):
        G.add_node(ids[i][0], title = ids[i][0], color='red',)
        G.add_node(ids[i][1], title = ids[i][1],arrowStrikethrough=False)
        G.add_edge(ids[i][0],ids[i][1], physics = True, color='black')
        i+=1
    #G.show_buttons(filter_=['physics'])
    #G.barnes_hut()
    G.show("G.html")



if __name__ == '__main__':
    visualization()