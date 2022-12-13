# import tkinter as tk
# import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import matplotlib.pyplot as plt
# import networkx as nx

# data1 = {'country': ['A', 'B', 'C', 'D', 'E'],
#          'gdp_per_capita': [45000, 42000, 52000, 49000, 47000]
#          }
# df1 = pd.DataFrame(data1)


# root = tk.Tk()

# figure1 = plt.Figure(figsize=(6, 5), dpi=100)
# ax1 = figure1.add_subplot(111)
# bar1 = FigureCanvasTkAgg(figure1, root)
# bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
# df1 = df1[['country', 'gdp_per_capita']].groupby('country').sum()
# df1.plot(kind='bar', legend=True, ax=ax1)
# ax1.set_title('Country Vs. GDP Per Capita')

# figure = plt.Figure(figsize=(5, 5), dpi=100)
# G = nx.petersen_graph()
# subax1 = figure.subplot(121)
# nx.draw(G, with_labels=True, font_weight='bold')
# subax2 = figure.subplot(122)
# bar1 = FigureCanvasTkAgg(figure, root)
# bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
# nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')

# plt.show()

# root.mainloop()

from tkinter import *
import networkx as nx
from pandas import DataFrame
from digraph import ford_fulkerson
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
window = Tk()
window.title("Graphs")

graph = nx.DiGraph()
graph.add_nodes_from('ABCDEFGH')
graph.add_edges_from([
    ('A', 'B', {'capacity': 4, 'flow': 0}),
    ('A', 'C', {'capacity': 5, 'flow': 0}),
    ('A', 'D', {'capacity': 7, 'flow': 0}),
    ('B', 'E', {'capacity': 7, 'flow': 0}),
    ('C', 'E', {'capacity': 6, 'flow': 0}),
    ('C', 'F', {'capacity': 4, 'flow': 0}),
    ('C', 'G', {'capacity': 1, 'flow': 0}),
    ('D', 'F', {'capacity': 8, 'flow': 0}),
    ('D', 'G', {'capacity': 1, 'flow': 0}),
    ('E', 'H', {'capacity': 7, 'flow': 0}),
    ('F', 'H', {'capacity': 6, 'flow': 0}),
    ('G', 'H', {'capacity': 4, 'flow': 0}),

])

layout = {
    'A': [0, 1], 'B': [1, 2], 'C': [1, 1], 'D': [1, 0],
    'E': [2, 2], 'F': [2, 1], 'G': [2, 0], 'H': [3, 1],
}

def draw_graph():
    f = plt.Figure(figsize=(5, 5), dpi=100)
    a = f.add_subplot(111)
    a.plot()
    a.draw_networkx_nodes(graph, layout, node_color='steelblue', node_size=600)
    a.draw_networkx_edges(graph, layout, edge_color='gray')
    a.draw_networkx_labels(graph, layout, font_color='white')

    for u, v, e in graph.edges(data=True):
        label = '{}/{}'.format(e['flow'], e['capacity'])
        color = 'green' if e['flow'] < e['capacity'] else 'red'
        x = layout[u][0] * .6 + layout[v][0] * .4
        y = layout[u][1] * .6 + layout[v][1] * .4
        t = plt.text(x, y, label, size=16, color=color,
                     horizontalalignment='center', verticalalignment='center')

    plt.show()

def flow_debug(graph, path, reserve, flow):
    print('flow increased by', reserve,
          'at path', path,
          '; current flow', flow)
    draw_graph()

def plot_max_flow():
    ford_fulkerson(graph, 'A', 'H', flow_debug)


VertexData = Entry(window)
VertexData.grid(row = 0, column = 0)
Button(window, text = "Insert Vertex").grid(sticky = W, row = 0, column = 1, padx = 4)
Button(window, text = "Delete Vertex").grid(sticky = W, row = 0, column = 2, padx = 4)
Button(window, text = "MaxFlow").grid(sticky = W, row = 0, column = 3, padx = 4, command = ford_fulkerson(graph, 'A', 'H', flow_debug))
df3 = DataFrame()


window.mainloop()