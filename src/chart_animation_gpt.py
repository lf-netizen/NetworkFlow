import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import queue

class CTkFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.canvas = tk.Canvas(self, width=500, height=500)
        self.canvas.pack()

        self.fig = plt.figure(figsize=(5, 5))
        self.figure_canvas = FigureCanvasTkAgg(self.fig, self.canvas)
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

        self.q = queue.Queue()

    def draw_graph(self, G):
        self.fig.clear()
        nx.draw(G, with_labels=True, font_weight='bold')
        self.fig.canvas.draw()

    def process_queue(self):
        while True:
            try:
                G = self.q.get(block=False)
                self.draw_graph(G)
            except queue.Empty:
                self.after(100, self.process_queue)  # schedule the process_queue method to be called again after 100 milliseconds
                break

    def add_to_queue(self):
        # create some example graphs
        G1 = nx.Graph()
        G1.add_nodes_from([1, 2, 3])
        G1.add_edges_from([(1, 2), (2, 3)])
        G2 = nx.Graph()
        G2.add_nodes_from([1, 2, 3, 4])
        G2.add_edges_from([(1, 2), (2, 3), (3, 4)])
        G3 = nx.Graph()
        G3.add_nodes_from([1, 2, 3, 4, 5])
        G3.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 5)])

        # add the first graph to the queue
        self.q.put(G1)

        # schedule the second and third graphs to be added to the queue after 2 seconds and 4 seconds respectively
        self.after(2000, lambda: self.q.put(G2))
        self.after(4000, lambda: self.q.put(G3))

if __name__ == '__main__':
    root = tk.Tk()
    frame = CTkFrame(root)
    frame.pack()
    frame.after(0, frame.process_queue)
    frame.after(1000, frame.add_to_queue)  # schedule the add_to_queue method to be called after 1 second
    root.mainloop()
