import tkinter
import customtkinter
import os
from PIL import Image
import matplotlib.pyplot as plt
import networkx as nx
import simulated_annealing
from simulated_annealing import OptimizationModel
from network import Network
from custom_types import ID
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
import time
import threading
import model
import copy
from itertools import compress
from gui_custom_types import SliderBlock, EssentialsTextField, OptionMenuWithName, RandomGraphParams

from model import model_from_file, unpack_json, model1, model2, model3

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

# load required images
my_image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "my_images")

home_network_image = customtkinter.CTkImage(Image.open(os.path.join(my_image_path, "networking.png")), size=(35, 35))
home_image = customtkinter.CTkImage(Image.open(os.path.join(my_image_path, "home-icon.png")), size=(28, 28))
graph_image = customtkinter.CTkImage(Image.open(os.path.join(my_image_path, "neural-network.png")), size=(30, 30))
chart_image = customtkinter.CTkImage(Image.open(os.path.join(my_image_path, "line-chart.png")), size=(30, 30))
heat_map_image = customtkinter.CTkImage(Image.open(os.path.join(my_image_path, "color_map.png")), size=(30, 250))
white_play_image = customtkinter.CTkImage(Image.open(os.path.join(my_image_path, "white_play_button.png")), size=(30, 30))
green_play_image = customtkinter.CTkImage(Image.open(os.path.join(my_image_path, "green_play_button.png")), size=(30, 30))
gray_chart_image = customtkinter.CTkImage(Image.open(os.path.join(my_image_path, "neural-network-gray.png")), size=(30, 30))

class Wrapper:
    def __init__(self) -> None:
        self.model_name = None
        self.model = None
        self.logs = {}

        self.alpha = 0.95
        self.t0 = 100
        self.t1 = 1
        self.epoch_size = 10
        self.nbhoods = [1] * 6
    
    def load_network(self, loader: callable, model_name: str = None, *args, **kwargs) -> None:
        if self.model_name == model_name:
            return

        adjmatrix, arch, schedule = loader(*args, **kwargs)
        Network.reset_devices_ids()
        network = Network(arch)
        network.load_schedule(schedule)
        self.model =  OptimizationModel(network, adjmatrix)
        self.model_name = model_name
    
    def simulate(self, *args) -> None:
        nbhoods_fun = [self.model.change_solution, self.model.change_solution2, self.model.change_solution3, self.model.change_solution4, self.model.change_solution5, self.model.change_solution6]
        nbhoods = set(compress(nbhoods_fun, self.nbhoods))

        self.model.network.reset_state(with_schedule=False)
        _, _, data = self.model.run_model(self.t0, self.t1, self.alpha, self.epoch_size, nbhoods, *args)
        self.logs['min_value'] = min(data)
        self.logs['max_value'] = max(data)
        self.logs['iterations'] = len(data)
        self.logs['num_improvements'] = sum(prev < next for prev, next in zip(data[:-1], data[1:]))
        self.logs['num_deteriorations'] = sum(prev > next for prev, next in zip(data[:-1], data[1:]))


# pop-up window class
class PopUpWindow(customtkinter.CTkToplevel):
    def __init__(self, command_when_saved):
        super().__init__()
        self.title("Upload model")  # window title
        self.geometry(f"{500}x{500}")
        self.minsize(400, 400)
        self.command_when_saved = command_when_saved

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.textbox = customtkinter.CTkTextbox(self, width=300, height=300)
        self.textbox.grid(row=0, column=0)

        self.button = customtkinter.CTkButton(self,
                                            width=50,
                                            height=40, border_spacing=10,
                                            border_width=0,
                                            corner_radius=8,
                                            text="SAVE",
                                            command=self.button_event, font=customtkinter.CTkFont(size=15, weight="bold"))
        self.button.grid(row=1, column=0)

    def write_to_textbox(self, string):
        self.textbox.insert('0.0', string)

    def read_from_textbox(self) -> str:
        return self.textbox.get('0.0', 'end')

    def button_event(self) -> str:
        self.withdraw()
        with open("models/user_uploaded.json", "w") as f:
            f.write(self.read_from_textbox())
        try:
            wrapper.load_network(model_from_file('user_uploaded'), f'{time.perf_counter()}')
        except:
            print('Error: could not parse network.')
            return
        self.command_when_saved()
        app.on_model_load()

        


class ArrowGraph(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.option_menu = OptionMenuWithName(self, options=[], name='choose endpoint ID', command=self.option_menu_event)
        self.option_menu.grid(row=1, column=0, padx=(15), sticky='es')

        self.canvas = tk.Canvas(self, width=500, height=500)
        self.canvas.grid(row=0, column=0, columnspan=2, padx=20, pady=(0, 20), sticky='nw')

        self.fig = Figure(figsize=(10, 6))
        self.figure_canvas = FigureCanvasTkAgg(self.fig, self.canvas)
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().pack(side='top', fill='both', expand=1)


    def option_menu_event(self, id):
        self.draw_graph_solution(int(id))
        # app.main_frame.chart_frame.arrow_graph.update_graph()


    def draw_graph_solution(self, target_id=8):
        self.fig.clear()
        ax = self.fig.add_subplot(111)

        solution = wrapper.model.solution
        if solution is None:
            print('trying to draw solution graph with no solution')

        endpoints_gates = [(e.id, e.gate_id) for e in wrapper.model.network.e_it if e.id != target_id]
        routers_directions = [(src_id, dst_id) for src_id, routing_table in solution.items() for key, dst_id in
                              routing_table.items() if key == target_id]

        G = self.G.to_directed()
        G.remove_edges_from(list(G.edges))
        G.add_edges_from(endpoints_gates + routers_directions)

        nx.draw(G, pos=self.pos, ax=ax, with_labels=True, font_weight='bold')
        self.fig.canvas.draw()


    def update_graph(self):
        self.G = nx.Graph()
        for i in range(len(wrapper.model.adjmatrix)):
            self.G.add_node(i)
        for i in range(len(wrapper.model.adjmatrix)):
            for j in range(len(wrapper.model.adjmatrix)):
                if wrapper.model.adjmatrix[i, j] == 1:
                    self.G.add_edge(i, j)

        endpoints_ids = [e.id for e in wrapper.model.network.e_it]
        pos_endpoints = nx.circular_layout(self.G.subgraph(endpoints_ids), scale=2)
        pos = nx.spring_layout(self.G, pos=pos_endpoints, fixed=endpoints_ids, weight=None, seed=42)
        self.pos = pos

        self.draw_graph()

    def draw_graph(self):
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        nx.draw(self.G, pos=self.pos, ax=ax, with_labels=True, font_weight='bold')
        self.fig.canvas.draw()


class ColoredGraph(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.heat_map_button = customtkinter.CTkButton(self, corner_radius=0, height=400, border_spacing=10,
                                                       text=" Legend",
                                                       fg_color="transparent", text_color=("gray10", "gray90"),
                                                       hover=False,
                                                       image=heat_map_image, anchor="w",
                                                       font=customtkinter.CTkFont(size=15, weight="bold"))
        self.heat_map_button.grid(row=0, column=1, padx=20, pady=(0, 20), sticky="ew")

        self.canvas = tk.Canvas(self, width=500, height=500)
        self.canvas.grid(row=0, column=0, padx=20, pady=(0, 20))

        self.fig = Figure(figsize=(9, 6))
        self.figure_canvas = FigureCanvasTkAgg(self.fig, self.canvas)
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

    def update_graph(self):
        self.G = nx.Graph()
        for i in range(len(wrapper.model.adjmatrix)):
            self.G.add_node(i)
        for i in range(len(wrapper.model.adjmatrix)):
            for j in range(len(wrapper.model.adjmatrix)):
                if wrapper.model.adjmatrix[i, j] == 1:
                    self.G.add_edge(i, j)

        endpoints_ids = [e.id for e in wrapper.model.network.e_it]
        pos_endpoints = nx.circular_layout(self.G.subgraph(endpoints_ids), scale=2)
        pos = nx.spring_layout(self.G, pos=pos_endpoints, fixed=endpoints_ids, weight=None, seed=42)
        self.pos = pos

        self.draw_graph()

    def draw_graph(self):
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        nx.draw(self.G, pos=self.pos, ax=ax, with_labels=True, font_weight='bold')
        self.fig.canvas.draw()

    def draw_graph_with_colors(self):
        self.fig.clear()
        ax = self.fig.add_subplot(111)

        endpoints_ids = [e.id for e in wrapper.model.network.e_it]
        weights = wrapper.model.network.logs['edges_weight']

        for u, v, d in self.G.edges(data=True):
            if u in endpoints_ids or v in endpoints_ids:
                d['weight'] = 0
                continue
            try:
                w1 = weights[u][v]
            except:
                w1 = 0
            try:
                w2 = weights[v][u]
            except:
                w2 = 0
            d['weight'] = w1 + w2

        edges, weights = zip(*nx.get_edge_attributes(self.G, 'weight').items())
        nx.draw(self.G, pos=self.pos, node_color='b', edgelist=edges, edge_color=weights, width=5, edge_cmap=plt.cm.RdYlBu_r,
                ax=ax, with_labels=True)

        self.fig.canvas.draw()


class RoutingTable(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.grid_rowconfigure(0, weight=1)
        # self.grid_columnconfigure(0, weight=1)  

        # self.textbox = customtkinter.CTkTextbox(self, width=500, height=500, activate_scrollbars=False)
        # self.textbox.grid(row=0, column=0)

        self.canvas = tk.Canvas(self, width=500, height=500)
        self.canvas.grid(row=0, column=0, padx=20, pady=(0, 20))

        self.fig = Figure(figsize=(9, 6))
        self.figure_canvas = FigureCanvasTkAgg(self.fig, self.canvas)
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().pack(side='top', fill='both', expand=1)


    def write_to_textbox(self, string):
        self.textbox.delete('0.0', 'end')
        self.textbox.insert('0.0', string)
    
    def write_to_table(self, string):
        self.fig.clear()
        ax = self.fig.add_subplot(111)

        title_text = 'Routing tables'

        data =  [
                    [         'Freeze', 'Wind', 'Flood', 'Quake', 'Hail'],
                    [ '5 year',  66386, 174296,   75131,  577908,  32015],
                    ['10 year',  58230, 381139,   78045,   99308, 160454],
                    ['20 year',  89135,  80552,  152558,  497981, 603535],
                    ['30 year',  78415,  81858,  150656,  193263,  69638],
                    ['40 year', 139361, 331509,  343164,  781380,  52269],
                ]
        # column_headers = data.pop(0)
        # row_headers = [x.pop(0) for x in data]

        solution = wrapper.model.solution
        row_headers = list(solution.keys())
        column_headers = list(solution[row_headers[0]].keys())
        
        
        data = [[solution[r][c] for c in column_headers] for r in row_headers]

        print(data)
        print(row_headers)
        print(column_headers)
        print(solution)
        
        cell_text = []
        for row in data:
            cell_text.append([f'{x}' for x in row])
        # Get some lists of color specs for row and column headers
        rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
        ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))
        # Create the figure. Setting a small pad on tight_layout
        # seems to better regulate white space. Sometimes experimenting
        # with an explicit figsize here can produce better outcome.
        # plt.figure(linewidth=2,
        #         )
        # Add a table at the bottom of the axes
        
        ax.table(cellText=cell_text,
                            rowLabels=row_headers,
                            rowColours=rcolors,
                            rowLoc='right',
                            colColours=ccolors,
                            colLabels=column_headers,
                            loc='center')

        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        self.fig.suptitle(title_text)
      
        self.fig.canvas.draw()






class HomeFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._corner_radius = 0
        # self._fg_color="#0000FF"

        # create 2x2 grid system
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.neighbourhood_frame = customtkinter.CTkFrame(self)
        self.neighbourhood_frame.grid(row=0, column=0, rowspan=2, padx=20, pady=(20, 20), sticky='n')

        self.neighbourhood_frame.grid_rowconfigure(8, weight=1)
        self.neighbourhood_frame.grid_columnconfigure(1, weight=1)

        self.neighbourhood_frame_name = customtkinter.CTkButton(self.neighbourhood_frame, corner_radius=0, height=40, border_spacing=10,
                                                   text="Avaliable neighbourhoods",
                                                   fg_color="transparent", text_color="gray10", hover=False,
                                                   anchor="nesw",
                                                   font=customtkinter.CTkFont(size=16, weight="bold"))
        self.neighbourhood_frame_name.grid(row=0, column=0)

        self.switch_var1 = customtkinter.StringVar(value="on")
        self.switch_var2 = customtkinter.StringVar(value="on")
        self.switch_var3 = customtkinter.StringVar(value="on")
        self.switch_var4 = customtkinter.StringVar(value="on")
        self.switch_var5 = customtkinter.StringVar(value="on")
        self.switch_var6 = customtkinter.StringVar(value="on")
        self.neighbourhood_switch_1 = customtkinter.CTkSwitch(self.neighbourhood_frame, text="1. Random neighbourhood",
                                                              command=self.switch1_event, variable=self.switch_var1)
        self.neighbourhood_switch_1.grid(row=1, column=0, padx=20, pady=10, sticky='w')
        self.neighbourhood_switch_2 = customtkinter.CTkSwitch(self.neighbourhood_frame, text="2. Max number of datagrams in edge",
                                                              command=self.switch2_event, variable=self.switch_var2)
        self.neighbourhood_switch_2.grid(row=2, column=0, padx=20, pady=10, sticky='w')
        self.neighbourhood_switch_3 = customtkinter.CTkSwitch(self.neighbourhood_frame, text="3. Max number of datagrams in router",
                                                              command=self.switch3_event, variable=self.switch_var3)
        self.neighbourhood_switch_3.grid(row=3, column=0, padx=20, pady=10, sticky='w')
        self.neighbourhood_switch_4 = customtkinter.CTkSwitch(self.neighbourhood_frame, text="4. Max queue length in router",
                                                              command=self.switch4_event, variable=self.switch_var4)
        self.neighbourhood_switch_4.grid(row=4, column=0, padx=20, pady=10, sticky='w')
        self.neighbourhood_switch_5 = customtkinter.CTkSwitch(self.neighbourhood_frame, text="5. Max avg queue length in router",
                                                              command=self.switch5_event, variable=self.switch_var5)
        self.neighbourhood_switch_5.grid(row=5, column=0, padx=20, pady=10, sticky='w')
        self.neighbourhood_switch_6 = customtkinter.CTkSwitch(self.neighbourhood_frame, text="6. Max queue duration in a router",
                                                              command=self.switch6_event, variable=self.switch_var6)
        self.neighbourhood_switch_6.grid(row=6, column=0, padx=20, pady=10, sticky='w')


        self.parameters_frame = customtkinter.CTkFrame(self)
        self.parameters_frame.grid(row=0, column=1, columnspan=2, padx=20, pady=20)
        self.parameters_frame.grid_rowconfigure(5, weight=1)
        self.parameters_frame.grid_columnconfigure(1, weight=1)

        self.parameters_frame_label = customtkinter.CTkButton(self.parameters_frame, corner_radius=0, height=40, border_spacing=10,
                                                   text="Simulation parameters",
                                                   fg_color="transparent", text_color="gray10", hover=False,
                                                   anchor="ew",
                                                   font=customtkinter.CTkFont(size=16, weight="bold"))
        self.parameters_frame_label.grid(row=0, column=0, columnspan=2)

        self.parameters_slider_t0 = SliderBlock(self.parameters_frame, name='t0', slider_start=0, slider_end=8, steps=100_000, default_value=1_000_000, scale_fun=lambda x: np.log10(x), inverse_fun=lambda x: np.power(10, x), round_factor=0)
        self.parameters_slider_t0.grid(row=1, column=0, columnspan=2, padx=10, pady=(10, 0), sticky='ew')
        self.parameters_slider_t1 = SliderBlock(self.parameters_frame, name='t1', slider_start=-8, slider_end=0, steps=100_000, default_value=0.01, scale_fun=lambda x: np.log10(x), inverse_fun=lambda x: np.power(10, x), round_factor=8)
        self.parameters_slider_t1.grid(row=2, column=0, columnspan=2, padx=10, pady=0, sticky='ew')
        self.parameters_slider_alpha = SliderBlock(self.parameters_frame, name='alpha', slider_start=0.001, slider_end=0.99, steps=1_000, default_value=0.95)
        self.parameters_slider_alpha.grid(row=3, column=0, columnspan=2, padx=10, pady=0, sticky='ew')
        self.parameters_slider_epoch_size = SliderBlock(self.parameters_frame, name='epoch_size', slider_start=10, slider_end=200, steps=190, default_value=50, round_factor=0)
        self.parameters_slider_epoch_size.grid(row=4, column=0, columnspan=2, padx=10, pady=0, sticky='ew')

        self.parameters_button_reset = customtkinter.CTkButton(master=self.parameters_frame,
                                                             width=120,
                                                             height=32,
                                                             border_width=0,
                                                             corner_radius=8,
                                                             text="RESET",
                                                             command=self.parameters_button_reset_event)
        self.parameters_button_reset.grid(row=5, column=0, padx=(40, 0), pady=(10, 10))

        self.parameters_button_set = customtkinter.CTkButton(master=self.parameters_frame,
                                                             width=120,
                                                             height=32,
                                                             border_width=0,
                                                             corner_radius=8,
                                                             text="SAVE",
                                                             command=self.parameters_button_set_event)
        self.parameters_button_set.grid(row=5, column=1, padx=(0, 40), pady=(10, 10), sticky='e')

        # self.textbox = customtkinter.CTkTextbox(self, width=200)
        # self.textbox.grid(row=1, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # self.upload_model_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10,
        #                                                    text=" Upload new model",
        #                                                    fg_color="transparent", text_color=("gray10", "gray90"),
        #                                                    hover_color=("gray70", "gray30"),
        #                                                    anchor="w", command=self.upload_model_button_event,
        #                                                    font=customtkinter.CTkFont(size=15, weight="bold"))
        # self.upload_model_button.grid(row=1, column=2, sticky="ew")

    def parameters_button_set_event(self):
        self.parameters_slider_t0.set(float(self.parameters_slider_t0.get_textbox_content()))
        self.parameters_slider_t1.set(float(self.parameters_slider_t1.get_textbox_content()))
        self.parameters_slider_alpha.set(float(self.parameters_slider_alpha.get_textbox_content()))
        self.parameters_slider_epoch_size.set(float(self.parameters_slider_epoch_size.get_textbox_content()))

    def parameters_button_reset_event(self):
        self.parameters_slider_t0.reset()
        self.parameters_slider_t1.reset()
        self.parameters_slider_alpha.reset()
        self.parameters_slider_epoch_size.reset()

    def switch1_event(self):
        wrapper.nbhoods[0] = self.switch_var1.get()

    def switch2_event(self):
        wrapper.nbhoods[1] = self.switch_var1.get()

    def switch3_event(self):
        wrapper.nbhoods[2] = self.switch_var1.get()

    def switch4_event(self):
        wrapper.nbhoods[3] = self.switch_var1.get()

    def switch5_event(self):
        wrapper.nbhoods[4] = self.switch_var1.get()

    def switch6_event(self):
        wrapper.nbhoods[5] = self.switch_var1.get()

    def update_params(self):
        wrapper.t0 = self.parameters_slider_t0.get_value()
        wrapper.t1 = self.parameters_slider_t1.get_value()
        wrapper.alpha = self.parameters_slider_alpha.get_value()
        wrapper.epoch_size = self.parameters_slider_epoch_size.get_value()



class GraphFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._corner_radius = 0

        # params for random graph
        self.number_of_routers = 10
        self.number_of_PCs = 5
        self.number_of_packages = 100
        self.connection_probability = 0.5
        self.timespan = 5

        # self._fg_color="#FF0000"
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.model_selection_frame = customtkinter.CTkFrame(self)
        self.model_selection_frame.grid(row=0, column=1, padx=20, pady=20)

        self.model_selection_frame.grid_rowconfigure(5, weight=1)
        self.model_selection_frame.grid_columnconfigure(0, weight=1)

        self.network_label_button = customtkinter.CTkButton(self.model_selection_frame, corner_radius=0, height=20, border_spacing=10,
                                                       text="Network models",
                                                       fg_color="transparent", text_color=("gray10", "gray90"),
                                                       hover=False,
                                                       anchor="n",
                                                       font=customtkinter.CTkFont(size=15, weight="bold"))
        self.network_label_button.grid(row=0, column=0, padx=20, pady=(0, 0), sticky="ew")

        self.radio_graph_reload = tkinter.IntVar(value=0)
        self.radio_1 = customtkinter.CTkRadioButton(self.model_selection_frame, command=self.graph_reload_event,
                                                                variable=self.radio_graph_reload, value=0, text="network 1")
        self.radio_1.grid(row=1, column=0, padx=20, pady=10, sticky='w')
        self.radio_2 = customtkinter.CTkRadioButton(self.model_selection_frame, command=self.graph_reload_event,
                                                                variable=self.radio_graph_reload, value=1, text="network 2")
        self.radio_2.grid(row=2, column=0, padx=20, pady=10, sticky='w')
        self.radio_3 = customtkinter.CTkRadioButton(self.model_selection_frame, command=self.graph_reload_event,
                                                                variable=self.radio_graph_reload, value=2, text="network 3")
        self.radio_3.grid(row=3, column=0, padx=20, pady=10, sticky='w')
        self.radio_4 = customtkinter.CTkRadioButton(self.model_selection_frame, command=self.graph_reload_event,
                                                                variable=self.radio_graph_reload, value=3, text="random network")
        self.radio_4.grid(row=4, column=0, padx=20, pady=10, sticky='w')
        self.radio_5 = customtkinter.CTkRadioButton(self.model_selection_frame, command=self.graph_reload_event,
                                                                variable=self.radio_graph_reload, value=4, text="my network", state=tkinter.DISABLED)
        self.radio_5.grid(row=5, column=0, padx=20, pady=10, sticky='w')


        self.random_graph_frame = RandomGraphParams(self, command=self.save_random_network)
        self.random_graph_frame.grid(row=1, column=1, padx=20, pady=(0, 20), sticky="sew")


        self.import_model_button = customtkinter.CTkButton(self,
                                                             width=50,
                                                             height=40, border_spacing=10,
                                                             border_width=0,
                                                             corner_radius=8,
                                                             text="Upload model",
                                                             command=self.import_model_event, font=customtkinter.CTkFont(size=12, weight="bold"))
        self.import_model_button.grid(row=2, column=1, padx=20, pady=(0, 20), sticky="sew")
        

        self.canvas = tk.Canvas(self, width=500, height=500)
        self.canvas.grid(row=0, column=0, rowspan=3, padx=20, pady=(0, 20))

        self.fig = Figure(figsize=(8, 8))
        self.figure_canvas = FigureCanvasTkAgg(self.fig, self.canvas)
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().pack(side='top', fill='both', expand=1)


    def save_random_network(self):
        self.radio_graph_reload.set(3)

        try:
            self.number_of_routers = int(self.random_graph_frame.number_of_routers.get_value())
            self.number_of_PCs = int(self.random_graph_frame.number_of_PCs.get_value())
            self.number_of_packages = int(self.random_graph_frame.number_of_packages.get_value())
            self.connection_probability = float(self.random_graph_frame.connection_probability.get_value())
            self.timespan = int(self.random_graph_frame.timespan.get_value())
        except:
            self.random_graph_frame.number_of_routers.change_value(self.number_of_routers)
            self.random_graph_frame.number_of_PCs.change_value(self.number_of_PCs)
            self.random_graph_frame.number_of_packages.change_value(self.number_of_packages)
            self.random_graph_frame.connection_probability.change_value(self.connection_probability)
            self.random_graph_frame.timespan.change_value(self.timespan)

        wrapper.load_network(model.random_network_model, f'{time.perf_counter()}', 
                            number_of_routers=self.number_of_routers, 
                            number_of_PCs=self.number_of_PCs, 
                            number_of_packages=self.number_of_packages,
                            connection_probability=self.connection_probability,
                            timespan = self.timespan)

        app.on_model_load()


    def import_model_event(self):
        self.import_window = PopUpWindow(self.import_window_command)

    def import_window_command(self):
        self.radio_5.configure(state=tkinter.NORMAL)
        self.radio_5.select()
        

    def graph_reload_event(self):
        graph_id = self.radio_graph_reload.get()
        if graph_id == 0:
            wrapper.load_network(model1, 'model1')
        elif graph_id == 1:
            wrapper.load_network(model2, 'model2')
        elif graph_id == 2:
            wrapper.load_network(model_from_file('predefined_dense'), 'predefined_dense')
        elif graph_id == 3:          
            wrapper.load_network(model.random_network_model, f'{time.perf_counter()}', 
                                 number_of_routers=self.number_of_routers, 
                                 number_of_PCs=self.number_of_PCs, 
                                 number_of_packages=self.number_of_packages,
                                 connection_probability=self.connection_probability,
                                 timespan = self.timespan)
        elif graph_id == 4:
            wrapper.load_network(model_from_file('user_uploaded'), f'{time.perf_counter()}')

        app.on_model_load()

    def update_graph(self):
        self.G = nx.Graph()
        for i in range(len(wrapper.model.adjmatrix)):
            self.G.add_node(i)
        for i in range(len(wrapper.model.adjmatrix)):
            for j in range(len(wrapper.model.adjmatrix)):
                if wrapper.model.adjmatrix[i, j] == 1:
                    self.G.add_edge(i, j)

        endpoints_ids = [e.id for e in wrapper.model.network.e_it]
        pos_endpoints = nx.circular_layout(self.G.subgraph(endpoints_ids), scale=2)
        pos = nx.spring_layout(self.G, pos=pos_endpoints, fixed=endpoints_ids, weight=None, seed=42)
        self.pos = pos

        self.draw_graph()

    def draw_graph(self):
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        nx.draw(self.G, pos=self.pos, ax=ax, with_labels=True, font_weight='bold')
        self.fig.canvas.draw()



class ChartFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._corner_radius = 0
        # self._fg_color="#00FF00"

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.chart_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10,
                                                   text="Chart",
                                                   fg_color="transparent", text_color="gray10", hover_color="gray70",
                                                   anchor="ew", command=self.chart_button_event,
                                                   font=customtkinter.CTkFont(size=15, weight="bold"))
        self.chart_button.grid(row=0, column=0, sticky='e')

        self.colored_graph_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10,
                                                   text="Colored graph",
                                                   fg_color="transparent", text_color="gray10", hover_color="gray70",
                                                   anchor="ew", command=self.colored_graph_button_event,
                                                   font=customtkinter.CTkFont(size=15, weight="bold"))
        self.colored_graph_button.grid(row=0, column=1, sticky='e')

        self.arrow_graph_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10,
                                                   text="Arrow Graph",
                                                   fg_color="transparent", text_color="gray10", hover_color="gray70",
                                                   anchor="ew", command=self.arrow_graph_button_event,
                                                   font=customtkinter.CTkFont(size=15, weight="bold"))
        self.arrow_graph_button.grid(row=0, column=2, sticky='e')

        self.routing_table_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10,
                                                   text="Routing table",
                                                   fg_color="transparent", text_color="gray10", hover_color="gray70",
                                                   anchor="ew", command=self.routing_table_button_event,
                                                   font=customtkinter.CTkFont(size=15, weight="bold"))
        self.routing_table_button.grid(row=0, column=3, sticky='e')

        # self.text_field = customtkinter.CTkTextbox(self, width=500, height=20, activate_scrollbars=False)
        # self.text_field.grid(row=2, column=0, columnspan=4, padx=(20, 20), pady=(25, 14), sticky="nsew")

        self.colored_graph = ColoredGraph(self)
        self.colored_graph.grid(row=1, column=0, columnspan=4, sticky='nsew')

        self.arrow_graph = ArrowGraph(self)
        self.arrow_graph.grid(row=1, column=0, columnspan=4, sticky='nsew')

        self.chart = ChartInFrame(self)
        self.chart.grid(row=1, column=0, columnspan=4, sticky='nsew')

        self.routing_table = RoutingTable(self)
        self.routing_table.grid(row=1, column=0, columnspan=4, sticky='nsew')


        self.simulation_params = EssentialsTextField(self)

        self.simulation_in_progres_text = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10,
                                                   text="Simulation in progress.....",
                                                   fg_color="transparent", text_color="gray10", hover=False,
                                                   anchor="nesw",
                                                   font=customtkinter.CTkFont(size=20, weight="bold"))
        self.simulation_in_progres_text.grid(row=2, column=0, columnspan=4, sticky='sew')
        

    def routing_table_button_event(self):
        self.select_frame_by_button(self.routing_table_button)

        self.routing_table.write_to_table(wrapper.model.solution)
        # self.routing_table.plot_table()

    


    def chart_button_event(self):
        self.select_frame_by_button(self.chart_button)

    def colored_graph_button_event(self):
        self.select_frame_by_button(self.colored_graph_button)

    def arrow_graph_button_event(self):
        self.select_frame_by_button(self.arrow_graph_button)

    def select_frame_by_button(self, button):
        self.highlight_selected_button(button)

        # self.home_frame.update_params()
        if button == self.chart_button:
            self.chart.grid(row=1, column=0, columnspan=4, sticky='nsew')
        else:
            self.chart.grid_forget()
        if button == self.colored_graph_button:
            self.colored_graph.grid(row=1, column=0, columnspan=4, sticky='nsew')
        else:
            self.colored_graph.grid_forget()
        if button == self.arrow_graph_button:
            self.arrow_graph.grid(row=1, column=0, columnspan=4, sticky='nsew')
        else:
            self.arrow_graph.grid_forget()
        if button == self.routing_table_button:
            self.routing_table.grid(row=1, column=0, columnspan=4, sticky='nsew')
        else:
            self.routing_table.grid_forget()

    def highlight_selected_button(self, button):
        self.chart_button.configure(fg_color="transparent")
        self.colored_graph_button.configure(fg_color="transparent")
        self.arrow_graph_button.configure(fg_color="transparent")
        self.routing_table_button.configure(fg_color='transparent')

        # highlight selected button
        button.configure(fg_color=("gray75", "gray25"))


    def plot_chart(self):
        if app.simulation_running:
            return

        app.on_simulation_begin()
        
        event = threading.Event()
        t1 = threading.Thread(daemon=True, target=wrapper.simulate,
                              args=(event, ))
        t2 = threading.Thread(daemon=True, target=self.chart.process_queue, args=(event,))

        t1.start()
        t2.start()



class ChartInFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.canvas = tk.Canvas(self, width=500, height=500)
        self.canvas.pack()

        self.fig = Figure(figsize=(50, 6))
        self.figure_canvas = FigureCanvasTkAgg(self.fig, self.canvas)
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

    def draw_graph(self, data):
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.set_xlabel('iterations')
        ax.set_ylabel('loss')
        ax.set_title('loss function value during algorithm iterations')
        ax.plot(data)
        self.fig.canvas.draw()

    def process_queue(self, event):
        while True:
            data = wrapper.model.log_queue.get(block=True)
            if data is None:
                app.on_simulation_end()
                return

            self.draw_graph(data)
            event.set()


class NavigationFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.header_name = "NavigationFrame"
        self._corner_radius = 0
        self._bg_color = "green"

        self.grid_rowconfigure(4, weight=1)
        self.header = customtkinter.CTkLabel(self, text="  Network", image=home_network_image, compound="left",
                                             font=customtkinter.CTkFont(size=18, weight="bold"))
        self.header.grid(row=0, column=0, padx=20, pady=20)

        # navigation buttons
        self.home_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10,
                                                   text=" Home",
                                                   fg_color="transparent", text_color="gray10", hover_color="gray70",
                                                   image=home_image, anchor="w", command=self.home_button_event,
                                                   font=customtkinter.CTkFont(size=15, weight="bold"))
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.graph_button = customtkinter.CTkButton(self, corner_radius=0, height=40,
                                                    border_spacing=10, text=" Graph",
                                                    fg_color="transparent", text_color="gray10", hover_color="gray70",
                                                    image=graph_image, anchor="w", command=self.graph_button_event,
                                                    font=customtkinter.CTkFont(size=15, weight="bold"))
        self.graph_button.grid(row=2, column=0, sticky="ew")

        self.chart_button = customtkinter.CTkButton(self, corner_radius=0, height=40,
                                                    border_spacing=10, text=" Simulation", state='disabled',
                                                    fg_color="transparent", text_color="gray10", hover_color="gray70",
                                                    image=chart_image, anchor="w", command=self.chart_button_event,
                                                    font=customtkinter.CTkFont(size=15, weight="bold"))
        self.chart_button.grid(row=3, column=0, sticky="ew")

        self.run_button = customtkinter.CTkButton(self, corner_radius=0, height=40,
                                                    border_spacing=10, text=" RUN",
                                                    fg_color="#48a64c", text_color="white", hover_color="#368c39",
                                                    image=white_play_image, anchor="w", command=self.run_button_event,
                                                    font=customtkinter.CTkFont(size=15, weight="bold"))
        self.run_button.grid(row=4, column=0, sticky="ew")      

    def home_button_event(self):
        self.highlight_selected_button(self.home_button)
        app.main_frame.select_frame_by_name("home")

    def graph_button_event(self):
        self.highlight_selected_button(self.graph_button)
        app.main_frame.select_frame_by_name("graph")

    def chart_button_event(self):
        self.highlight_selected_button(self.chart_button)
        app.main_frame.select_frame_by_name("chart")
    
    def run_button_event(self):
        # open chart_frame
        self.highlight_selected_button(self.chart_button)
        app.main_frame.select_frame_by_name("chart")
        app.main_frame.chart_frame.select_frame_by_button(app.main_frame.chart_frame.chart_button)

        # run simulation
        app.main_frame.chart_frame.plot_chart()

    def block_simulation_button(self):
        self.chart_button.configure(state='disabled')
        self.chart_button.configure(image=gray_chart_image)
    
    def enable_simulation_button(self):
        self.chart_button.configure(state='normal')
        self.chart_button.configure(image=chart_image)


    def highlight_selected_button(self, button):
        self.home_button.configure(fg_color="transparent")
        self.graph_button.configure(fg_color="transparent")
        self.chart_button.configure(fg_color="transparent")

        # highlight selected button
        button.configure(fg_color=("gray75", "gray25"))


class MainFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create 1x2 grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # navigation frame
        self.navigation_frame = NavigationFrame(self)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")

        self.home_frame = HomeFrame(self)
        self.graph_frame = GraphFrame(self)
        self.chart_frame = ChartFrame(self)

        # select default frame
        self.select_frame_by_name("home")
        self.navigation_frame.highlight_selected_button(self.navigation_frame.home_button)

    def select_frame_by_name(self, name):
        self.home_frame.update_params()
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "graph":
            self.graph_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.graph_frame.grid_forget()
        if name == "chart":
            self.chart_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.chart_frame.grid_forget()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # window properties
        self.title("Network")  # window title
        self.geometry(f"{1100}x{650}")  # default window size
        self.minsize(500, 400)  # minimum window size

        # create 1x1 grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # display
        self.main_frame = MainFrame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.simulation_running = False

    def on_app_load(self):
        wrapper.load_network(model1, 'model1')
        self.on_model_load()

    def on_model_load(self):
        self.main_frame.graph_frame.update_graph()
        self.main_frame.chart_frame.colored_graph.update_graph()
        self.main_frame.chart_frame.arrow_graph.update_graph()
        self.main_frame.chart_frame.arrow_graph.option_menu.reload([e.id for e in wrapper.model.network.e_it])
        app.main_frame.navigation_frame.block_simulation_button()

    def on_simulation_begin(self):
        self.simulation_running = True
        # TA LINIJKA DO OSOBNEJ FUNKCJI W CHART FRAME
        app.main_frame.chart_frame.simulation_params.grid_forget()
        app.main_frame.chart_frame.simulation_in_progres_text.grid(row=2, column=0, columnspan=2, sticky='sew')
        app.main_frame.navigation_frame.enable_simulation_button()

    def on_simulation_end(self):
        self.simulation_running = False
        
        self.main_frame.chart_frame.arrow_graph.draw_graph_solution(int(self.main_frame.chart_frame.arrow_graph.option_menu.options[0]))
        self.main_frame.chart_frame.colored_graph.draw_graph_with_colors()
        # TA LINIJKA DO OSOBNEJ FUNKCJI W CHART FRAME
        app.main_frame.chart_frame.simulation_in_progres_text.grid_forget()
        app.main_frame.chart_frame.simulation_params.grid(row=2, column=0, columnspan=4, sticky='sw')
        app.main_frame.chart_frame.simulation_params.set_values(wrapper.logs['min_value'], wrapper.logs['max_value'], wrapper.logs['num_improvements'], wrapper.logs['iterations'], wrapper.logs['num_deteriorations'])


if __name__ == "__main__":
    wrapper = Wrapper()
    app = App()
    app.on_app_load()
    app.mainloop()
