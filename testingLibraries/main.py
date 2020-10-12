# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import matplotlib
import matplotlib.pyplot as plt
#import networkx.drawing

# Import packages for data cleaning
import numpy as np
import pandas as pd
import re # For finding specific strings in the text
# Import packages for data visualization
import plotly.offline as py
import plotly.graph_objects as go
import networkx as nx
import pylab
from networkx import *
import networkx.classes.function
import random
from pyvis.network import Network
from pyvis import network as net



from bokeh.io import show, output_file
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, TapTool, BoxSelectTool
from bokeh.models.graphs import from_networkx, NodesAndLinkedEdges, EdgesAndLinkedNodes
from bokeh.palettes import Spectral4

from networkx.drawing.nx_agraph import to_agraph


def just_test():

    J = nx.DiGraph()
    J.add_edges_from(
        [('A', 'B'), ('A', 'C')])

    val_map = {'A': 1.0,
               'B': 0.5714285714285714,
               'C': 2.0}
    values = [val_map.get(node, 0.25) for node in J.nodes()]
    # Specify the edges you want here
    red_edges = [('A', 'C')]
    edge_colours = ['black' if not edge in red_edges else 'red'
                    for edge in J.edges()]
    black_edges = [edge for edge in J.edges() if edge not in red_edges]

    # Need to create a layout when doing
    # separate calls to draw nodes and edges
    pos = nx.spring_layout(J)
    nx.draw_networkx_nodes(J, pos, cmap=plt.get_cmap('jet'),
                           node_color=values, node_size=500)
    nx.draw_networkx_labels(J, pos)
    nx.draw_networkx_edges(J, pos, edgelist=red_edges, edge_color='r', arrows=True)
    nx.draw_networkx_edges(J, pos, edgelist=black_edges, arrows=False)

    nx.draw(J)
    plt.savefig("path2.png")


def print_graph():
    G = nx.MultiDiGraph()
    G.add_node('A')
    G.add_node('B')
    G.add_edge('A','B',weight=0.3)
    G.add_edge('B','A',color='red',weight=0.9)
    G.add_edge('A','A',color='red',weight=0.9)
    elist = [('a', 'b', 5.0), ('b', 'c', 3.0), ('a', 'c', 1.0), ('c', 'd', 7.3), ('b','a', 0.7)]
    G.add_weighted_edges_from(elist)
    edge_labels = dict([((u, v,), d['weight'])
                        for u, v, d in G.edges(data=True)])

    val_map = {'A': 1.0,
               'D': 0.5714285714285714,
               'H': 0.0}

    values = [val_map.get(node, 0.45) for node in G.nodes()]


    red_edges = [('A','B')]
    #nx.draw(G)
    plt.subplot(121)
    pos = nx.spring_layout(G)
    #nx.draw_networkx_nodes(G,pos)
    nx.draw_networkx_labels(G,pos) #print lables (a,b, etc)
    #nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
    nx.draw(G,pos,node_color = values, node_size=1500,edge_cmap=plt.cm.Reds)

    #nx.draw(G, pos=nx.spectral_layout(G), nodecolor='r', edge_color='b')
    #plt.savefig("path.png")

    pylab.show()
    #nx.write_dot(G, 'my_graph.dot')
    #dot my_graph.dot - T png > output.png



def matplot_vis():
    G = nx.MultiDiGraph()
    file=open('dataset.txt','r')
    '''general_friend_list=[1,1,1,1,1,1,1,7,7,7]
    second_friend_list= [2,3,4,5,6,7,8,6,5,9]
    weight_list=[0.4,0.3,0.1,0.9,1,0.7,0.8,0.2,0.5,0.5]'''


    i=0
    lines = file.readlines()
    result = list()
    for line in lines:
        result.append(line.split("https://vk.com/id"))
    print(result)
    number_of_appearence = list()
    k=0
    number_of_appearence.append(result[0][1].split('\t'))
    number_of_appearence[k][1] = 1

    tmp = result[0][1]
    i=1
    while i<len(result):
        if(result[i][1]==tmp):
            number_of_appearence[k][1] +=1
        else:
            tmp = result[i][1]
            number_of_appearence.append(result[i][1].split('\t'))
            k+=1
            number_of_appearence[k][1]=1
        i+=1
    print(number_of_appearence)

    i=0
    while i < len(result):
        G.add_edges_from([
            (result[i][1],result[i][2])
        ])
        i += 1
    G.add_edges_from([
        (result[0][1], result[135][1])
    ])
    #nx.draw_circular(G)

    #edge_labels = dict([((u, v,), d['weight'])
     #                   for u, v, d in G.edges(data=True)])

    plt.figure(figsize=(15, 15))
    #plt.figure()
    node_size = [0.0005 * G.out_degree[v] for v in G]
    pos = nx.random_layout(G)
    nx.draw_random(G)
    #nx.draw_networkx(G,pos)
   # nx.draw_networkx_edge_labels(G, pos,label_pos= 0.5)
    #nx.draw_networkx_nodes(G,pos,node_color='red')
    #nx.draw_networkx_edges(G,pos,connectionstyle='arc3,rad=0.3')
    #nx.draw_networkx(G,pos, connectionstyle='arc3, rad=0.2',node_color='red',)

    #plt.show()

    nt = Network("1000px", "1000px")

    nt.from_nx(G)
    nt.show("nx.html")

def pyvis_vis():
    G = Network()
    file = open('dataset.txt', 'r')

    i = 0
    lines = file.readlines()
    result = list()
    for line in lines:
        result.append(line.split("https://vk.com/id"))
    print(result)



    i = 0
    while i < 10:
        G.add_node(result[i][1],title = result[i][1], size = 100)
        G.add_node(result[i][2])
        G.add_edge(result[i][1],result[i][2], weight = 10)
        i += 1
   # G.show_buttons(filter_=['physics'])
    G.show("nx.html")

def test_html(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')
    G = nx.karate_club_graph()
    plot = Plot(plot_width=400, plot_height=400,
                x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
    plot.title.text = "Graph Interaction Demonstration"

    plot.add_tools(HoverTool(tooltips=None), TapTool(), BoxSelectTool())

    graph_renderer = from_networkx(G, nx.circular_layout, scale=1, center=(0, 0))

    graph_renderer.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])
    graph_renderer.node_renderer.selection_glyph = Circle(size=15, fill_color=Spectral4[2])
    graph_renderer.node_renderer.hover_glyph = Circle(size=15, fill_color=Spectral4[1])

    graph_renderer.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=0.8, line_width=5)
    graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2], line_width=5)
    graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[1], line_width=5)

    graph_renderer.selection_policy = NodesAndLinkedEdges()
    graph_renderer.inspection_policy = EdgesAndLinkedNodes()

    plot.renderers.append(graph_renderer)

    output_file("interactive_graphs.html")
    show(plot)


if __name__ == '__main__':
    pyvis_vis()
