import pickle
from pyvis.network import Network
import sqlite3


db = sqlite3.connect('users.db')
sql = db.cursor()

def visualization():


    G = Network(height='1000px',
                width='1000px',
                # directed=True,
                heading='Social graph of friends',
                )
    createNodesAndEdges(G)
    G.show("G.html")

def createNodesAndEdges(G):
    for value in sql.execute("SELECT * FROM users").fetchall():
        size_ = 20
        if value[4]!= '': size_ = len(pickle.loads(value[4])) + 20
        if size_ > 100: size_ = 100

        color_ = "blue"
        if value[0] == 225273973:
            color_ = "red"
        G.add_node(value[0],
                   shape = "circularImage",
                   label = str(value[2]),
                   title = str(value[2]),
                   color = color_,
                   size = size_,
                   mas = size_,
                   image = value[3])
    for value in sql.execute("SELECT * FROM users").fetchall():
        if value[4]!= '':
            for edge in pickle.loads(value[4]):
                G.add_edge(value[0], edge,
                           physics=True,)

    G.show_buttons(filter_=['physics'])
    G.barnes_hut(
        gravity=-80000,
        central_gravity=2,
        spring_length=250,
        spring_strength=0.01,
        damping=0.09,
        overlap=0.1)

if __name__ == '__main__':
    visualization()