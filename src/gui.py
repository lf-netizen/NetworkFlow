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
import my_model
import copy
from itertools import compress
from gui_custom_types import SliderBlock

from model import model_load, unpack_json, model1, model2, model3

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

# load required images
my_image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "my_images")

home_network_image = customtkinter.CTkImage(Image.open(os.path.join(my_image_path, "networking.png")), size=(35, 35))
home_image = customtkinter.CTkImage(Image.open(os.path.join(my_image_path, "home-icon.png")), size=(28, 28))
graph_image = customtkinter.CTkImage(Image.open(os.path.join(my_image_path, "neural-network.png")), size=(30, 30))
chart_image = customtkinter.CTkImage(Image.open(os.path.join(my_image_path, "line-chart.png")), size=(30, 30))
heat_map_image = customtkinter.CTkImage(Image.open(os.path.join(my_image_path, "color_map.png")), size=(30, 250))

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
    
    def load_network(self, loader: callable, model_name: str = None, *args) -> None:
        if self.model_name == model_name:
            return

        adjmatrix, arch, schedule = loader(*args)
        
        Network.reset_devices_ids()
        network = Network(arch)
        network.load_schedule(schedule)
        self.model =  OptimizationModel(network, adjmatrix)
        self.model_name = model_name
    
    def simulate(self, *args) -> None:
        nbhoods_fun = [self.model.change_solution, self.model.change_solution2, self.model.change_solution3, self.model.change_solution4, self.model.change_solution5, self.model.change_solution6]
        nbhoods = set(compress(nbhoods_fun, self.nbhoods))

        self.model.network.reset_state(with_schedule=False)
        self.model.run_model(self.t0, self.t1, self.alpha, self.epoch_size, nbhoods, *args)

class HomeFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._corner_radius = 0
        # self._fg_color="#0000FF"

        # create 2x2 grid system
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.neighbourhood_frame = customtkinter.CTkFrame(self)
        self.neighbourhood_frame.grid(row=1, column=0, padx=20, pady=(0, 20))
        self.neighbourhood_frame.grid(row=1, column=0, padx=20, pady=(0, 20))

        self.neighbourhood_frame.grid_rowconfigure(8, weight=1)
        self.neighbourhood_frame.grid_columnconfigure(1, weight=1)

        self.switch_var1 = customtkinter.StringVar(value="on")
        self.switch_var2 = customtkinter.StringVar(value="on")
        self.switch_var3 = customtkinter.StringVar(value="on")
        self.switch_var4 = customtkinter.StringVar(value="on")
        self.switch_var5 = customtkinter.StringVar(value="on")
        self.switch_var6 = customtkinter.StringVar(value="on")
        self.neighbourhood_switch_1 = customtkinter.CTkSwitch(self.neighbourhood_frame, text="neighbourhood 1",
                                                              command=self.switch1_event, variable=self.switch_var1)
        self.neighbourhood_switch_1.grid(row=0, column=0, padx=20, pady=10)
        self.neighbourhood_switch_2 = customtkinter.CTkSwitch(self.neighbourhood_frame, text="neighbourhood 2",
                                                              command=self.switch2_event, variable=self.switch_var2)
        self.neighbourhood_switch_2.grid(row=1, column=0, padx=20, pady=10)
        self.neighbourhood_switch_3 = customtkinter.CTkSwitch(self.neighbourhood_frame, text="neighbourhood 3",
                                                              command=self.switch3_event, variable=self.switch_var3)
        self.neighbourhood_switch_3.grid(row=2, column=0, padx=20, pady=10)
        self.neighbourhood_switch_4 = customtkinter.CTkSwitch(self.neighbourhood_frame, text="neighbourhood 4",
                                                              command=self.switch4_event, variable=self.switch_var4)
        self.neighbourhood_switch_4.grid(row=3, column=0, padx=20, pady=10)
        self.neighbourhood_switch_5 = customtkinter.CTkSwitch(self.neighbourhood_frame, text="neighbourhood 5",
                                                              command=self.switch5_event, variable=self.switch_var5)
        self.neighbourhood_switch_5.grid(row=4, column=0, padx=20, pady=10)
        self.neighbourhood_switch_6 = customtkinter.CTkSwitch(self.neighbourhood_frame, text="neighbourhood 6",
                                                              command=self.switch6_event, variable=self.switch_var6)
        self.neighbourhood_switch_6.grid(row=5, column=0, padx=20, pady=10)

        self.start_graph_frame = customtkinter.CTkFrame(self)
        self.start_graph_frame.grid(row=0, column=0, padx=20, pady=20)

        self.start_graph_frame.grid_rowconfigure(4, weight=1)
        self.start_graph_frame.grid_columnconfigure(0, weight=1)

        self.radio_graph_reload = tkinter.IntVar(value=0)
        self.start_graph_radio_1 = customtkinter.CTkRadioButton(self.start_graph_frame, command=self.graph_reload_event,
                                                                variable=self.radio_graph_reload, value=0, text="graph 1")
        self.start_graph_radio_1.grid(row=0, column=0, padx=20, pady=10)
        self.start_graph_radio_2 = customtkinter.CTkRadioButton(self.start_graph_frame, command=self.graph_reload_event,
                                                                variable=self.radio_graph_reload, value=1, text="graph 2")
        self.start_graph_radio_2.grid(row=1, column=0, padx=20, pady=10)
        self.start_graph_radio_3 = customtkinter.CTkRadioButton(self.start_graph_frame, command=self.graph_reload_event,
                                                                variable=self.radio_graph_reload, value=2, text="graph 3")
        self.start_graph_radio_3.grid(row=2, column=0, padx=20, pady=10)
        self.start_graph_radio_4 = customtkinter.CTkRadioButton(self.start_graph_frame, command=self.graph_reload_event,
                                                                variable=self.radio_graph_reload, value=3, text="my_model")
        self.start_graph_radio_4.grid(row=3, column=0, padx=20, pady=10)


        self.parameters_frame = customtkinter.CTkFrame(self)
        self.parameters_frame.grid(row=0, column=1, columnspan=2, padx=20, pady=20)
        self.parameters_frame.grid_rowconfigure(4, weight=1)
        self.parameters_frame.grid_columnconfigure(1, weight=1)


        self.parameters_slider_t0 = SliderBlock(self.parameters_frame, name='t0', slider_start=0, slider_end=8, steps=100_000, default_value=1_000_000, scale_fun=lambda x: np.log10(x), inverse_fun=lambda x: np.power(10, x), round_factor=0)
        self.parameters_slider_t0.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky='ew')
        # self.parameters_slider_t0.set(self.t0)
        # self.parameters_slider_1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.parameters_slider_t1 = SliderBlock(self.parameters_frame, name='t1', slider_start=-8, slider_end=0, steps=100_000, default_value=0.01, scale_fun=lambda x: np.log10(x), inverse_fun=lambda x: np.power(10, x), round_factor=8)
        self.parameters_slider_t1.grid(row=1, column=0, columnspan=2, padx=10, pady=0, sticky='ew')
        # self.parameters_slider_t1.set(np.log10(self.t1))

        self.parameters_slider_alpha = SliderBlock(self.parameters_frame, name='alpha', slider_start=0.001, slider_end=0.99, steps=1_000, default_value=0.95)
        self.parameters_slider_alpha.grid(row=2, column=0, columnspan=2, padx=10, pady=0, sticky='ew')
        # self.parameters_slider_alpha.set(self.alpha)

        self.parameters_slider_epoch_size = SliderBlock(self.parameters_frame, name='epoch_size', slider_start=10, slider_end=200, steps=190, default_value=50, round_factor=0)
        self.parameters_slider_epoch_size.grid(row=3, column=0, columnspan=2, padx=10, pady=0, sticky='ew')
        # self.parameters_slider_epoch_size.set(self.epoch_size)

        self.parameters_button_reset = customtkinter.CTkButton(master=self.parameters_frame,
                                                             width=120,
                                                             height=32,
                                                             border_width=0,
                                                             corner_radius=8,
                                                             text="RESET",
                                                             command=self.parameters_button_reset_event)
        self.parameters_button_reset.grid(row=4, column=0, padx=(40, 0), pady=(10, 10))

        self.parameters_button_set = customtkinter.CTkButton(master=self.parameters_frame,
                                                             width=120,
                                                             height=32,
                                                             border_width=0,
                                                             corner_radius=8,
                                                             text="SAVE",
                                                             command=self.parameters_button_set_event)
        self.parameters_button_set.grid(row=4, column=1, padx=(0, 40), pady=(10, 10), sticky='e')

        self.textbox = customtkinter.CTkTextbox(self, width=200)
        self.textbox.grid(row=1, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.upload_model_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10,
                                                           text=" Upload new model",
                                                           fg_color="transparent", text_color=("gray10", "gray90"),
                                                           hover_color=("gray70", "gray30"),
                                                           anchor="w", command=self.upload_model_button_event,
                                                           font=customtkinter.CTkFont(size=15, weight="bold"))
        self.upload_model_button.grid(row=1, column=2, sticky="ew")

    def parameters_button_set_event(self):
        # temp = float(self.parameters_slider_t0.get_textbox_content())


        self.parameters_slider_t0.set(float(self.parameters_slider_t0.get_textbox_content()))
        self.parameters_slider_t1.set(float(self.parameters_slider_t1.get_textbox_content()))
        self.parameters_slider_alpha.set(float(self.parameters_slider_alpha.get_textbox_content()))
        self.parameters_slider_epoch_size.set(float(self.parameters_slider_epoch_size.get_textbox_content()))

    def parameters_button_reset_event(self):
        self.parameters_slider_t0.reset()
        self.parameters_slider_t1.reset()
        self.parameters_slider_alpha.reset()
        self.parameters_slider_epoch_size.reset()

    def upload_model_button_event(self):
        text = self.textbox.get("0.0", "end")

        with open('src/my_model.py', 'w') as f:
            f.write(f'from custom_types import ID\nimport numpy as np\n{text}')

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

    def graph_reload_event(self):
        graph_id = self.radio_graph_reload.get()
        print(graph_id)

        if graph_id == 0:
            wrapper.load_network(model1, 'model1')
        elif graph_id == 1:
            wrapper.load_network(model2, 'model2')
        elif graph_id == 2:
            wrapper.load_network(model_load, 'predefined_dense', 'predefined_dense')
        elif graph_id == 3:
            wrapper.load_network(model_load, 'predefined_sparse', 'predefined_sparse')

        app.on_model_load()

    def update_params(self):
        wrapper.t0 = self.parameters_slider_t0.get_value()
        wrapper.t1 = self.parameters_slider_t1.get_value()
        wrapper.alpha = self.parameters_slider_alpha.get_value()
        wrapper.epoch_size = self.parameters_slider_epoch_size.get_value()



class GraphFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._corner_radius = 0
        # self._fg_color="#FF0000"
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.heat_map_button = customtkinter.CTkButton(self, corner_radius=0, height=400, border_spacing=10,
                                                       text=" Legend",
                                                       fg_color="transparent", text_color=("gray10", "gray90"),
                                                       hover_color=("#d9d9d9", "#d9d9d9"),
                                                       image=heat_map_image, anchor="w",
                                                       font=customtkinter.CTkFont(size=15, weight="bold"))
        self.heat_map_button.grid(row=0, column=1, padx=20, pady=(0, 20), sticky="ew")

        self.canvas = tk.Canvas(self, width=500, height=500)
        self.canvas.grid(row=0, column=0, padx=20, pady=(0, 20))
        # self.canvas.pack()

        self.fig = Figure(figsize=(8, 8))
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


class ChartFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._corner_radius = 0
        # self._fg_color="#00FF00"

        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10,
                                              text=" Generate Chart",
                                              fg_color="transparent", text_color=("gray10", "gray90"),
                                              hover_color=("gray70", "gray30"),
                                              image=home_image, anchor="w", command=self.plot_chart_button_event,
                                              font=customtkinter.CTkFont(size=15, weight="bold"))
        self.button.grid(row=0, column=0, sticky="ew")

        self.text_field = customtkinter.CTkTextbox(self, width=500, height=20, activate_scrollbars=False)
        self.text_field.grid(row=1, column=0, columnspan=2, padx=(20, 20), pady=(25, 14), sticky="nsew")

        self.chart = ChartInFrame(self)
        self.chart.grid(row=0, column=1)

    def plot_chart_button_event(self):
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

        self.fig = Figure(figsize=(5, 5))
        self.figure_canvas = FigureCanvasTkAgg(self.fig, self.canvas)
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

    def draw_graph(self, data):
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.plot(data)
        self.fig.canvas.draw()

    def process_queue(self, event):
        while True:
            data = wrapper.model.log_queue.get(block=True)
            if data is None:
                app.on_simulation_end()
                return
            wrapper.logs['min_value'] = min(data)
            wrapper.logs['max_value'] = max(data)
            wrapper.logs['num_improvements'] = sum(prev > next for prev, next in zip(data[:-1], data[1:]))

            self.draw_graph(data)
            event.set()


class NavigationFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.header_name = "NavigationFrame"
        self._corner_radius = 0
        self.fg_color = "gray85"

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
                                                    border_spacing=10, text=" Chart",
                                                    fg_color="transparent", text_color="gray10", hover_color="gray70",
                                                    image=chart_image, anchor="w", command=self.chart_button_event,
                                                    font=customtkinter.CTkFont(size=15, weight="bold"))
        self.chart_button.grid(row=3, column=0, sticky="ew")

    def home_button_event(self):
        self.highlight_selected_button(self.home_button)
        app.main_frame.select_frame_by_name("home")

    def graph_button_event(self):
        self.highlight_selected_button(self.graph_button)
        app.main_frame.select_frame_by_name("graph")

    def chart_button_event(self):
        self.highlight_selected_button(self.chart_button)
        app.main_frame.select_frame_by_name("chart")

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
        self.title("Test app")  # window title
        self.geometry(f"{1100}x{620}")  # default window size
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

    def on_simulation_begin(self):
        self.simulation_running = True
        # TA LINIJKA DO OSOBNEJ FUNKCJI W CHART FRAME
        app.main_frame.chart_frame.text_field.insert('0.0', 'simulation in progress...\n')

    def on_simulation_end(self):
        self.simulation_running = False

        self.main_frame.graph_frame.draw_graph_with_colors()
        # TA LINIJKA DO OSOBNEJ FUNKCJI W CHART FRAME
        app.main_frame.chart_frame.text_field.insert('0.0', f"min val: {wrapper.logs['min_value']:.3f}, max val: {wrapper.logs['max_value']:.3f}, num improvements: {wrapper.logs['num_improvements']:.0f}\n")


if __name__ == "__main__":
    wrapper = Wrapper()
    app = App()
    app.on_app_load()
    app.mainloop()
