from pyvis.network import Network
from pyvis import network as net
import numpy as np
from networkx import *
import re

def pars():
    print("Введите путь к файлу. Если файл уже в программе введите 0")
    path = input()
    if (path=='0'):
        file=open('dataset.txt','r')
    else:
        file=open(path,'r')
    lines = file.readlines()
    result = list()
    print("Выбирите формат датасет файла. 0 - id id, 1 - link\\id link\\id")
    dataset_format = int(input())
    if(dataset_format == 0):
        for line in lines:
            line = line.partition(' ')
            result.append([line[0],line[2]])
    if (dataset_format == 1):
        i = 0
        for line in lines:
            print(line)
            result.append(line.split("https://vk.com/id"))
            del result[i][0]
            result[i][0] = result[i][0].replace("\t", "")
            result[i][1] = result[i][1].replace("\n", "")
            i += 1

    file.close()
    number_of_appearence=get_number_of_appearence(result)
    for i in range(len(result)):
        for j in range(len(number_of_appearence)):
            if(result[i][0]==number_of_appearence[j][0]):
                result[i].append(number_of_appearence[j][1])
                break

    return result

def get_number_of_appearence(arr):
    wtf = [[1, 2]]
    number_of_appearence = list()
    number_of_appearence.append([])

    k=0

    number_of_appearence[k].append(arr[0][0])
    number_of_appearence[k].append(1)
    tmp = arr[0][0]
    unice_numbers = list()
    unice_numbers.append(arr[0][0])
    has = False
    i=0
    while i<len(arr):
        for j in unice_numbers:
            if(j==arr[i][0]):
                has = True
        if(has==False):
            unice_numbers.append(arr[i][0])
        i+=1
        has=False
    print(unice_numbers)
    i=1
    was = False
    p=0
    while i<len(arr):

        if(k>=1):
            tmp = arr[i][0]
            for j in range(len(number_of_appearence)):
                if (number_of_appearence[j][0] == tmp):
                    was=True
                    p=j
                    break
        if(was==True):
            number_of_appearence[p][1]+=1
            was=False
        else :
            tmp = arr[i-1][0]
            if(arr[i][0]==tmp):
                number_of_appearence[k][1] +=1
            else:
                k+=1
                number_of_appearence.append([])
                number_of_appearence[k].append(arr[i][0])
                number_of_appearence[k].append(1)
        tmp = arr[i][0]
        i+=1

    return number_of_appearence

def visualization():
    ids = pars()
    print(ids)
    layout='test'
    G = Network(height='1000px',
                width= '1000px',
                #directed=True,
                heading='Social graph of friends',
                )
    print("Введите количество связей(вершин) которые хотите нарисовать. Если хотите нарисовать все впишите 0")
    amount_of_printed_nodes = input()
    if(amount_of_printed_nodes == '0'):
        amount_of_printed_nodes =len(ids)
    i = 0
    while i < int(amount_of_printed_nodes):
        if (ids[i][2] > 100):
            size_ = 100
        else:
            size_ = ids[i][2]
        G.add_node(ids[i][0],
                   title = ids[i][0],
                   color = 'red',
                   size = size_,
                   mas = ids[i][2])
        G.add_node(ids[i][1],
                   title = ids[i][1],)
        G.add_edge(ids[i][0],ids[i][1],
                   physics = True,)
        G.add_edge(ids[i][1], ids[i][0],
                   physics=True,)
        i+=1
    G.show_buttons(filter_=['physics'])
    G.barnes_hut(
        gravity=-80000,
        central_gravity=2,
        spring_length=250,
        spring_strength= 0.01,
        damping=0.09,
        overlap=0.1)
    G.show("G.html")

def test():
    G = Network(height='1000px',
                width= '1000px',
                directed=True,
                heading= 'Test',
                )
    G.add_node(0)
    G.add_node(1)
    G.add_edge(0,1,arrowStrikethrough=True )
    G.add_edge(1,0,arrowStrikethrough=True)
    G.show("G.html")


if __name__ == '__main__':
    visualization()
    #test()