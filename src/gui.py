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

customtkinter.set_appearance_mode("Light")          # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

# load required images
my_image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "my_images")

home_network_image = customtkinter.CTkImage(Image.open(os.path.join(my_image_path, "networking.png")), size=(35, 35))
home_image = customtkinter.CTkImage(Image.open(os.path.join(my_image_path, "home-icon.png")), size=(28, 28))
graph_image = customtkinter.CTkImage(Image.open(os.path.join(my_image_path, "neural-network.png")), size=(30, 30))
chart_image = customtkinter.CTkImage(Image.open(os.path.join(my_image_path, "line-chart.png")), size=(30, 30))
heat_map_image = customtkinter.CTkImage(Image.open(os.path.join(my_image_path, "color_map.png")), size=(30, 250))


simulation_ended = False
global_radio_var = 0
graph_select = 0


adjmatrix, arch, schedule = model.model1()
global_network = Network(arch)
global_network.load_schedule(schedule)
global_model = OptimizationModel(global_network, adjmatrix)
prev_radio_var = 0

# results of simulation to display
min_value = None
max_value = None
num_improvements = None


class HomeFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._corner_radius=0
        # self._fg_color="#0000FF"

        # create 2x2 grid system
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)


        self.neighbourhood_frame = customtkinter.CTkFrame(self)
        self.neighbourhood_frame.grid(row=1, column=0, padx=20, pady=(0, 20))

        self.neighbourhood_frame.grid_rowconfigure(8, weight=1)
        self.neighbourhood_frame.grid_columnconfigure(1, weight=1)

        # define simulation parameters ##############
        self.t0 = 10e5      # =1_000_000
        self.t1 = 10e-3     # =0.01
        self.alpha = 0.95
        self.epoch_size = 50
        self.neighbourhoods = [0, 0, 0, 0, 0, 0]
        ###
        
        self.switch_var1 = customtkinter.StringVar(value="on")
        self.switch_var2 = customtkinter.StringVar(value="on")
        self.switch_var3 = customtkinter.StringVar(value="on")
        self.switch_var4 = customtkinter.StringVar(value="on")
        self.switch_var5 = customtkinter.StringVar(value="on")
        self.switch_var6 = customtkinter.StringVar(value="on")
        self.neighbourhood_switch_1 = customtkinter.CTkSwitch(self.neighbourhood_frame, text="neighbourhood 1", command=self.switch1_event, variable=self.switch_var1)
        self.neighbourhood_switch_1.grid(row=0, column=0, padx=20, pady=10)
        self.neighbourhood_switch_2 = customtkinter.CTkSwitch(self.neighbourhood_frame, text="neighbourhood 2", command=self.switch2_event, variable=self.switch_var2)
        self.neighbourhood_switch_2.grid(row=1, column=0, padx=20, pady=10)
        self.neighbourhood_switch_3 = customtkinter.CTkSwitch(self.neighbourhood_frame, text="neighbourhood 3", command=self.switch3_event, variable=self.switch_var3)
        self.neighbourhood_switch_3.grid(row=2, column=0, padx=20, pady=10)
        self.neighbourhood_switch_4 = customtkinter.CTkSwitch(self.neighbourhood_frame, text="neighbourhood 4", command=self.switch4_event, variable=self.switch_var4)
        self.neighbourhood_switch_4.grid(row=3, column=0, padx=20, pady=10)
        self.neighbourhood_switch_5 = customtkinter.CTkSwitch(self.neighbourhood_frame, text="neighbourhood 5", command=self.switch5_event, variable=self.switch_var5)
        self.neighbourhood_switch_5.grid(row=4, column=0, padx=20, pady=10)
        self.neighbourhood_switch_6 = customtkinter.CTkSwitch(self.neighbourhood_frame, text="neighbourhood 6", command=self.switch6_event, variable=self.switch_var6)
        self.neighbourhood_switch_6.grid(row=5, column=0, padx=20, pady=10)


        self.start_graph_frame = customtkinter.CTkFrame(self)
        self.start_graph_frame.grid(row=0, column=0, padx=20, pady=20)

        self.start_graph_frame.grid_rowconfigure(4, weight=1)
        self.start_graph_frame.grid_columnconfigure(0, weight=1)

        self.radio_var = tkinter.IntVar(value=0)
        self.start_graph_radio_1 = customtkinter.CTkRadioButton(self.start_graph_frame, command=self.radio_event, variable=self.radio_var, value=0, text="graph 1")
        self.start_graph_radio_1.grid(row=0, column=0, padx=20, pady=10)
        self.start_graph_radio_2 = customtkinter.CTkRadioButton(self.start_graph_frame, command=self.radio_event, variable=self.radio_var, value=1, text="graph 2")
        self.start_graph_radio_2.grid(row=1, column=0, padx=20, pady=10)
        self.start_graph_radio_3 = customtkinter.CTkRadioButton(self.start_graph_frame, command=self.radio_event, variable=self.radio_var, value=2, text="graph 3")
        self.start_graph_radio_3.grid(row=2, column=0, padx=20, pady=10)
        self.start_graph_radio_4 = customtkinter.CTkRadioButton(self.start_graph_frame, command=self.radio_event, variable=self.radio_var, value=3, text="my_model")
        self.start_graph_radio_4.grid(row=3, column=0, padx=20, pady=10)
        

        self.description_frame = customtkinter.CTkFrame(self)
        self.description_frame.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")

        self.description_frame.grid_rowconfigure(3, weight=1)
        self.description_frame.grid_columnconfigure(0, weight=1)

        self.description_textbox1 = customtkinter.CTkTextbox(self.description_frame, width=100, height=20, activate_scrollbars=False)
        self.description_textbox1.grid(row=0, column=0, padx=(20, 20), pady=(25, 14), sticky="nsew")
        self.description_textbox1.insert("0.0", f't0 value: 1000000 \n')
        self.description_textbox1.configure(state="disabled")
        self.description_textbox2 = customtkinter.CTkTextbox(self.description_frame, width=100, height=20, activate_scrollbars=False)
        self.description_textbox2.grid(row=1, column=0, padx=(20, 20), pady=(14, 14), sticky="nsew")
        self.description_textbox2.insert("0.0", f't1 value: 0.01 \n')
        self.description_textbox2.configure(state="disabled")
        self.description_textbox3 = customtkinter.CTkTextbox(self.description_frame, width=100, height=20, activate_scrollbars=False)
        self.description_textbox3.grid(row=2, column=0, padx=(20, 20), pady=(14, 14), sticky="nsew")
        self.description_textbox3.insert("0.0", f'alpha value: 0.95 \n')
        self.description_textbox3.configure(state="disabled")
        self.description_textbox4 = customtkinter.CTkTextbox(self.description_frame, width=100, height=20, activate_scrollbars=False)
        self.description_textbox4.grid(row=3, column=0, padx=(20, 20), pady=(14, 30), sticky="nsew")
        self.description_textbox4.insert("0.0", f'epoch_size value: 50 \n')
        self.description_textbox4.configure(state="disabled")

        self.parameters_frame = customtkinter.CTkFrame(self)
        self.parameters_frame.grid(row=0, column=2, padx=20, pady=20)

        self.parameters_frame.grid_rowconfigure(4, weight=1)
        self.parameters_frame.grid_columnconfigure(0, weight=1)

        self.parameters_slider_t0 = customtkinter.CTkSlider(self.parameters_frame, from_=0, to=8, command=self.slider_t0_event, number_of_steps=100_000)
        self.parameters_slider_t0.grid(row=0, column=0, padx=20, pady=20)
        self.parameters_slider_t0.set(np.log10(self.t0))
        #self.parameters_slider_1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.parameters_slider_t1 = customtkinter.CTkSlider(self.parameters_frame, from_=-8, to=0, command=self.slider_t1_event, number_of_steps=100_000)
        self.parameters_slider_t1.grid(row=1, column=0, padx=20, pady=20)
        self.parameters_slider_t1.set(np.log10(self.t1))
        self.parameters_slider_alpha = customtkinter.CTkSlider(self.parameters_frame, from_=0.001, to=0.99, command=self.slider_alpha_event, number_of_steps=1000)
        self.parameters_slider_alpha.grid(row=2, column=0, padx=20, pady=20)
        self.parameters_slider_alpha.set(self.alpha)
        self.parameters_slider_epoch_size = customtkinter.CTkSlider(self.parameters_frame, from_=10, to=200, command=self.slider_epoch_size_event, number_of_steps=190)
        self.parameters_slider_epoch_size.grid(row=3, column=0, padx=20, pady=20)
        self.parameters_slider_epoch_size.set(self.epoch_size)
        #self.parameters_slider_2.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.textbox = customtkinter.CTkTextbox(self, width=200)
        self.textbox.grid(row=1, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.upload_model_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text=" Upload new model",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.upload_model_button_event, 
                                                   font=customtkinter.CTkFont(size=15, weight="bold"))
        self.upload_model_button.grid(row=1, column=2, sticky="ew")

    def upload_model_button_event(self):
        text = self.textbox.get("0.0", "end")

        with open('src/my_model.py', 'w') as f:
            f.write(f'from custom_types import ID\nimport numpy as np\n{text}')

    
    def switch1_event(self):
        print(f'sw1 {self.switch_var1.get()}')
        self.neighbourhoods[0] = self.switch_var1.get()
    def switch2_event(self):
        self.neighbourhoods[1] = self.switch_var1.get()
    def switch3_event(self):
        self.neighbourhoods[2] = self.switch_var1.get()
    def switch4_event(self):
        self.neighbourhoods[3] = self.switch_var1.get()
    def switch5_event(self):
        self.neighbourhoods[4] = self.switch_var1.get()
    def switch6_event(self):
        self.neighbourhoods[5] = self.switch_var1.get()


    def radio_event(self):
        global prev_radio_var
        global global_network
        global global_model
        global graph_select
        global glabal_radio_var
        global_radio_var = self.radio_var.get()

        print(f'{prev_radio_var}  {global_radio_var}')
        if prev_radio_var != global_radio_var:
            prev_radio_var = global_radio_var
            graph_select = 1
            print('test')
            global_network.reset_state(True, True)
            if global_radio_var == 0:
                adjmatrix, arch, schedule = model.model1()
            elif global_radio_var == 1:
                print('dwa')
                adjmatrix, arch, schedule = model.model2()
            elif global_radio_var == 2:
                adjmatrix, arch, schedule = model.model3()
            else:
                adjmatrix, arch, schedule = my_model.model()
            global_network = Network(arch)
            global_network.load_schedule(schedule)
            global_model = OptimizationModel(global_network, adjmatrix)
        else:
            graph_select = 0
        print("radiobutton toggled, current value:", self.radio_var.get())

    def slider_t0_event(self, val):
        val = np.power(10, val)
        self.description_textbox1.configure(state="normal")
        self.description_textbox1.insert('0.0', f't0 value: {val:.1f} \n')
        self.description_textbox1.configure(state="disable")
        app.main_frame.home_frame.t0 = val
    def slider_t1_event(self, val):
        val = np.power(10, val)
        self.description_textbox2.configure(state="normal")
        self.description_textbox2.insert('0.0', f't1 value: {val:.10f} \n')
        self.description_textbox2.configure(state="disable")
        app.main_frame.home_frame.t1 = val
    def slider_alpha_event(self, val):
        self.description_textbox3.configure(state="normal")
        self.description_textbox3.insert('0.0', f'alpha value: {val:.2f} \n')
        self.description_textbox3.configure(state="disable")
        app.main_frame.home_frame.alpha = val
    def slider_epoch_size_event(self, val):
        self.description_textbox4.configure(state="normal")
        self.description_textbox4.insert('0.0', f'epoch_size value: {val:.0f} \n')
        self.description_textbox4.configure(state="disable")
        app.main_frame.home_frame.epoch_size = val


class GraphFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._corner_radius=0
        # self._fg_color="#FF0000"
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.heat_map_button = customtkinter.CTkButton(self, corner_radius=0, height=400, border_spacing=10, text=" Legend",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("#d9d9d9", "#d9d9d9"),
                                                   image=heat_map_image, anchor="w", 
                                                   font=customtkinter.CTkFont(size=15, weight="bold"))
        self.heat_map_button.grid(row=0, column=1, padx=20, pady=(0, 20), sticky="ew")

        self.canvas = tk.Canvas(self, width=500, height=500)
        self.canvas.grid(row=0, column=0, padx=20, pady=(0, 20))
        #self.canvas.pack()

        self.fig = Figure(figsize=(8, 8))
        self.figure_canvas = FigureCanvasTkAgg(self.fig, self.canvas)
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

        self.G = nx.Graph()
        self.is_running = False
        self.change_model()

        self.draw_graph()

    
    def temp(self):
        global graph_select

        if graph_select == 1:
            self.change_model()
            self.draw_graph()

    def change_model(self):

        global global_model
        self.G = nx.Graph()
        for i in range(0, len(global_model.adjmatrix)):
            self.G.add_node(i)
        
        for i in range(0, len(global_model.adjmatrix)):
            for j in range(0, len(global_model.adjmatrix)):
                if global_model.adjmatrix[i, j] == 1:
                    self.G.add_edge(i, j)

    def draw_graph(self):

        self.fig.clear()
        ax = self.fig.add_subplot(111)
        
        nx.draw(self.G, ax=ax, with_labels=True, font_weight='bold')

        self.fig.canvas.draw()
    
    def draw_graph_with_colors(self):
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        # pos = nx.spring_layout(self.G)

        weights = app.main_frame.chart_frame.chart.Model.network.logs['edges_weight']
        for u, v, d in self.G.edges(data=True):
            try:
                w1 = weights[u][v]
            except:
                w1 = 0
            try:
                w2 = weights[v][u]
            except:
                w2 = 0
            d['weight'] = w1 + w2

        pos = nx.spring_layout(self.G, scale=1)
        edges, weights = zip(*nx.get_edge_attributes(self.G,'weight').items())
        nx.draw(self.G, pos, node_color='b', edgelist=edges, edge_color=weights, width=5, edge_cmap=plt.cm.RdYlBu_r, ax=ax, with_labels=True)

        self.fig.canvas.draw()        



class ChartFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._corner_radius=0
        # self._fg_color="#00FF00"

        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text=" Generate Chart",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=home_image, anchor="w", command=self.plot_chart_button_event, 
                                                   font=customtkinter.CTkFont(size=15, weight="bold"))
        self.button.grid(row=0, column=0, sticky="ew")

        self.text_field = customtkinter.CTkTextbox(self, width=500, height=20, activate_scrollbars=False)
        self.text_field.grid(row=1, column=0, columnspan=2, padx=(20, 20), pady=(25, 14), sticky="nsew")

        self.chart = ChartInFrame(self)
        self.chart.grid(row=0, column=1)
        # self.chart.after(0, self.chart.process_queue)
        # self.chart.after(1000, self.chart.add_to_queue)  # schedule the add_to_queue method to be called after 1 second

    def plot_chart_button_event(self):
        self.plot_chart_event()
        global min_value
        global max_value
        global num_improvements

    def plot_chart_event(self):
        self.chart.reload()
        self.chart.plot_chart(app.main_frame.home_frame.t0, 
                              app.main_frame.home_frame.t1, 
                              app.main_frame.home_frame.alpha, 
                              app.main_frame.home_frame.epoch_size, 
                              app.main_frame.home_frame.neighbourhoods)



class ChartInFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.canvas = tk.Canvas(self, width=500, height=500)
        self.canvas.pack()

        self.fig = Figure(figsize=(5, 5))
        self.figure_canvas = FigureCanvasTkAgg(self.fig, self.canvas)
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

        global global_model
        self.Model = global_model
        self.q = self.Model.log_queue

        self.is_running = False

    def reload(self):
        global global_model
        self.Model = global_model
        self.q = self.Model.log_queue

    def draw_graph(self, data):
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.plot(data)
        self.fig.canvas.draw()

    def process_queue(self, event):
        global min_value, max_value, num_improvements, simulation_ended
        while True:
            data = self.q.get(block=True)
            if data is None:
                print('returning - end of simulation')
                print(min_value, max_value, num_improvements)
                app.main_frame.chart_frame.text_field.insert('0.0', f'min val: {min_value:.3f}, max val: {max_value:.3f}, num improvements: {num_improvements:.0f}\n')
                simulation_ended = True
                # app.main_frame.graph_frame.draw_graph_with_colors()
                self.is_running = False
                return
            min_value = min(data)
            max_value = max(data)
            num_improvements = sum(prev > next for prev, next in zip(data[:-1], data[1:]))
            
            self.draw_graph(data)
            event.set()

    def add_to_queue(self):
        # create some example data
        data1 = [1, 2, 3, 4]
        data2 = [5, 6, 7, 8]
        data3 = [9, 10, 11, 12]

        # add the first data to the queue
        self.q.put(data1)

        # schedule the second and third data to be added to the queue after 2 seconds and 4 seconds respectively
        self.after(2000, lambda: self.q.put(data2))
        self.after(4000, lambda: self.q.put(data3))


    def plot_chart(self, t0=10e5, t1=10e-3, alpha=0.95, epoch_size=50, nbhood=[0, 0, 0, 0, 0, 0]):        
        if self.is_running:
            return
        self.is_running = True
        app.main_frame.chart_frame.text_field.insert('0.0', 'simulation in progress...\n')
        
        self.Model.network.reset_state(with_schedule=False)

        neighbourhood = set()

        if nbhood[0]:
            neighbourhood.add(self.Model.change_solution)
        if nbhood[1]:
            neighbourhood.add(self.Model.change_solution2)
        if nbhood[2]:
            neighbourhood.add(self.Model.change_solution3)
        if nbhood[3]:
            neighbourhood.add(self.Model.change_solution4)
        if nbhood[4]:
            neighbourhood.add(self.Model.change_solution5)
        if nbhood[5]:
            neighbourhood.add(self.Model.change_solution6)
        print(neighbourhood)
        if len(neighbourhood) == 0:
            neighbourhood.add(self.Model.change_solution)
            neighbourhood.add(self.Model.change_solution2)
            neighbourhood.add(self.Model.change_solution3)
            neighbourhood.add(self.Model.change_solution4)
            neighbourhood.add(self.Model.change_solution5)
            neighbourhood.add(self.Model.change_solution6)
        
        event = threading.Event()
        self.is_running = True
        t1 = threading.Thread(daemon=True, target=self.Model.run_model, args=(t0, t1, alpha, epoch_size, neighbourhood, event))
        t2 = threading.Thread(daemon=True, target=self.process_queue, args=(event, ))
        
        t1.start()
        t2.start()


class NavigationFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.header_name = "NavigationFrame"
        self._corner_radius = 0
        self.header = customtkinter.CTkLabel(self, text="  Network", image=home_network_image, compound="left", 
                                             font=customtkinter.CTkFont(size=18, weight="bold"))
        self.header.grid(row=0, column=0, padx=15, pady=15)

        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        # navigation buttons
        self.home_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text=" Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=home_image, anchor="w", command=self.home_button_event, 
                                                   font=customtkinter.CTkFont(size=15, weight="bold"))
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.graph_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text=" Graph",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=graph_image, anchor="w", command=self.graph_button_event, 
                                                   font=customtkinter.CTkFont(size=15, weight="bold"))
        self.graph_button.grid(row=2, column=0, sticky="ew")

        self.chart_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text=" Chart",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=chart_image, anchor="w", command=self.chart_button_event, 
                                                   font=customtkinter.CTkFont(size=15, weight="bold"))
        self.chart_button.grid(row=3, column=0, sticky="ew")



class MainFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create 1x2 grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="gray85")
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Network", image=home_network_image,
                                                             compound="left", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text=" Home",
                                                   fg_color="transparent", text_color="gray10", hover_color="gray70",
                                                   image=home_image, anchor="w", command=self.home_button_event, 
                                                   font=customtkinter.CTkFont(size=15, weight="bold"))
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.graph_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text=" Graph",
                                                    fg_color="transparent", text_color="gray10", hover_color="gray70",
                                                    image=graph_image, anchor="w", command=self.graph_button_event,
                                                    font=customtkinter.CTkFont(size=15, weight="bold"))
        self.graph_button.grid(row=2, column=0, sticky="ew")

        self.chart_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text=" Chart",
                                                    fg_color="transparent", text_color="gray10", hover_color="gray70",
                                                    image=chart_image, anchor="w", command=self.chart_button_event,
                                                    font=customtkinter.CTkFont(size=15, weight="bold"))
        self.chart_button.grid(row=3, column=0, sticky="ew")


        self.home_frame = HomeFrame(self)
        self.graph_frame = GraphFrame(self)
        self.chart_frame = ChartFrame(self)

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.graph_button.configure(fg_color=("gray75", "gray25") if name == "graph" else "transparent")
        self.chart_button.configure(fg_color=("gray75", "gray25") if name == "chart" else "transparent")

        # show selected frame
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

    
    def home_button_event(self):
        self.select_frame_by_name("home")

    def graph_button_event(self):
        self.select_frame_by_name("graph")
        global prev_radio_var
        global global_radio_var
        global simulation_ended

        if simulation_ended:
            self.graph_frame.draw_graph_with_colors()
            simulation_ended = False
        elif prev_radio_var != global_radio_var:
            self.graph_frame.temp()
            prev_radio_var = global_radio_var
        

    def chart_button_event(self):
        self.select_frame_by_name("chart")



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


if __name__ == "__main__":
    app = App()
    app.mainloop()