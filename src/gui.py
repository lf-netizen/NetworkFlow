import tkinter
import customtkinter
import os
import sys
import pandas as pd
from PIL import Image
# graph
import matplotlib.pyplot as plt
import networkx as nx
import simulated_annealing
from simulated_annealing import OptimizationModel
from network import Network
from custom_types import ID
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import queue
import tkinter as tk
import time
import threading
import model

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

# load required images

# load images with light and dark mode image
image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
# self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
#                                          dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
# self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
#                                          dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

my_image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "my_images")
home_network_image = customtkinter.CTkImage(Image.open(os.path.join(my_image_path, "networking.png")), size=(35, 35))
home_image = customtkinter.CTkImage(Image.open(os.path.join(my_image_path, "home-icon.png")), size=(28, 28))
graph_image = customtkinter.CTkImage(Image.open(os.path.join(my_image_path, "neural-network.png")), size=(30, 30))
chart_image = customtkinter.CTkImage(Image.open(os.path.join(my_image_path, "line-chart.png")), size=(30, 30))

global_radio_var = 0
graph_select = 0
def load_model():
    adjmatrix = np.array([[0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0],
                        [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0],
                        [1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0],
                        [1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1],
                        [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0],
                        [0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0],
                        [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0],
                        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]],dtype=object)
    arch = {
        'routers': [
            {'id': 0, 'transmission_capacity':  5},
            {'id': 1, 'transmission_capacity': 10},
            {'id': 2, 'transmission_capacity': 10},
            {'id': 3, 'transmission_capacity': 5},
            {'id': 4, 'transmission_capacity': 10},
            {'id': 5, 'transmission_capacity': 10},
            {'id': 6, 'transmission_capacity': 5}
        ],
        'endpoints': [
            {'id': 7, 'gate_id': 0},
            {'id': 8, 'gate_id': 1},
            {'id': 9, 'gate_id': 2},
            {'id': 10, 'gate_id': 3}
        ]
    }
    schedule = {
        7: [
            {'destination_id': 8,      'request_time': 2, 'priority': 2},
            {'destination_id': [9, 10], 'request_time': 4, 'priority': 2},
            {'destination_id': 9,      'request_time': 3, 'priority': 1}
        ],
        8: [
            {'destination_id': 7,      'request_time': 1, 'priority': 2},
            {'destination_id': 9, 'request_time': 2, 'priority': 2},
            {'destination_id': 10,      'request_time': 3, 'priority': 1}
        ],
        9: [
            {'destination_id': 7, 'request_time': 5, 'priority': 2},
            {'destination_id': 8, 'request_time': 3, 'priority': 1}
        ],
        10: [
            {'destination_id': 7, 'request_time': 4, 'priority': 2},
            {'destination_id': 8, 'request_time': 6, 'priority': 2},
            {'destination_id': 9, 'request_time': 3, 'priority': 1}
        ]
    }

    # example pipeline
    return adjmatrix, arch, schedule
    # network = Network(arch)
    # network.load_schedule(schedule)
    # return OptimizationModel(network=network, adjmatrix=adjmatrix)


adjmatrix, arch, schedule = load_model()
global_network = Network(arch)
global_network.load_schedule(schedule)
global_model = OptimizationModel(global_network, adjmatrix)
prev_radio_var = 0

t0 = 100
t1 = 0.1
alpha = 0.8
epoch_size = 100
nbhood = [0, 0, 0, 0, 0, 0]

class HomeFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._corner_radius=0
        # self._fg_color="#0000FF"

        # create 2x2 grid system
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)


        self.neighbourhood_frame = customtkinter.CTkFrame(self)
        self.neighbourhood_frame.grid(row=1, column=0, padx=20, pady=(0, 20))

        self.neighbourhood_frame.grid_rowconfigure(8, weight=1)
        self.neighbourhood_frame.grid_columnconfigure(1, weight=1)
        
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
        # self.neighbourhood_switch_7 = customtkinter.CTkSwitch(self.neighbourhood_frame, text="neighbourhood 7")
        # self.neighbourhood_switch_7.grid(row=6, column=0, padx=20, pady=10)
        # self.neighbourhood_switch_8 = customtkinter.CTkSwitch(self.neighbourhood_frame, text="neighbourhood 8")
        # self.neighbourhood_switch_8.grid(row=7, column=0, padx=20, pady=10)


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
        self.start_graph_radio_4 = customtkinter.CTkRadioButton(self.start_graph_frame, command=self.radio_event, variable=self.radio_var, value=3, text="graph 4")
        self.start_graph_radio_4.grid(row=3, column=0, padx=20, pady=10)
        

        self.parameters_frame = customtkinter.CTkFrame(self)
        self.parameters_frame.grid(row=0, column=1, padx=20, pady=20)

        self.parameters_frame.grid_rowconfigure(4, weight=1)
        self.parameters_frame.grid_columnconfigure(0, weight=1)

        self.parameters_slider_t0 = customtkinter.CTkSlider(self.parameters_frame, from_=10, to=500, command=self.slider_t0_event, number_of_steps=490)
        self.parameters_slider_t0.grid(row=0, column=0, padx=20, pady=20)
        #self.parameters_slider_1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.parameters_slider_t1 = customtkinter.CTkSlider(self.parameters_frame, from_=0.01, to=0.1, command=self.slider_t1_event, number_of_steps=99)
        self.parameters_slider_t1.grid(row=1, column=0, padx=20, pady=20)
        self.parameters_slider_alpha = customtkinter.CTkSlider(self.parameters_frame, from_=0, to=1, command=self.slider_alpha_event, number_of_steps=100)
        self.parameters_slider_alpha.grid(row=2, column=0, padx=20, pady=20)
        self.parameters_slider_epoch_size = customtkinter.CTkSlider(self.parameters_frame, from_=20, to=200, command=self.slider_epoch_size_event, number_of_steps=180)
        self.parameters_slider_epoch_size.grid(row=3, column=0, padx=20, pady=20)
        #self.parameters_slider_2.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
    
    
    def switch1_event(self):
        global nbhood
        print(f'sw1 {self.switch_var1.get()}')
        if self.switch_var1.get():
            print('1')
            nbhood[0] = 1
        else:
            nbhood[0] = 0
    def switch2_event(self):
        global nbhood
        if self.switch_var2.get():
            nbhood[1] = 1
        else:
            nbhood[1] = 0
    def switch3_event(self):
        global nbhood
        if self.switch_var3.get():
            nbhood[2] = 1
        else:
            nbhood[2] = 0
    def switch4_event(self):
        global nbhood
        if self.switch_var4.get():
            nbhood[3] = 1
        else:
            nbhood[3] = 0
    def switch5_event(self):
        global nbhood
        if self.switch_var5.get():
            nbhood[4] = 1
        else:
            nbhood[4] = 0
    def switch6_event(self):
        global nbhood
        if self.switch_var6.get():
            nbhood[5] = 1
        else:
            nbhood[5] = 0



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
                adjmatrix, arch, schedule = model.model2()
            elif global_radio_var == 2:
                adjmatrix, arch, schedule = model.model3()
            else:
                adjmatrix, arch, schedule = model.model1()
            global_network = Network(arch)
            global_network.load_schedule(schedule)
            global_model = OptimizationModel(global_network, adjmatrix)
            #GraphFrame.temp()
        else:
            graph_select = 0
        print("radiobutton toggled, current value:", self.radio_var.get())

    def slider_t0_event(self, val):
        self.textbox.insert('0.0', f't0 value set to: {val} \n')
        global t0
        t0 = val
    def slider_t1_event(self, val):
        self.textbox.insert('0.0', f't1 value set to: {val} \n')
        global t1
        t1 = val
    def slider_alpha_event(self, val):
        self.textbox.insert('0.0', f'alpha value set to: {val} \n')
        global alpha
        alpha = val
    def slider_epoch_size_event(self, val):
        self.textbox.insert('0.0', f'epoch_size value set to: {val} \n')
        global epoch_size
        epoch_size = val


class GraphFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._corner_radius=0
        # self._fg_color="#FF0000" 


        self.canvas = tk.Canvas(self, width=500, height=500)
        self.canvas.pack()

        self.fig = Figure(figsize=(5, 5))
        self.figure_canvas = FigureCanvasTkAgg(self.fig, self.canvas)
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

        #global_model.adjmatrix
        self.G = nx.Graph()
        self.is_running = False
        self.change_model()

        
        self.draw_graph()


    
    def temp(self):
        global graph_select
        if graph_select == 1:
            print('graph')
            self.is_running = False
            self.change_model()
            self.draw_graph()

    def change_model(self):
        if self.is_running:
            return
        global global_model
        self.G = nx.Graph()
        for i in range(0, len(global_model.adjmatrix)):
            self.G.add_node(i)
        
        for i in range(0, len(global_model.adjmatrix)):
            for j in range(0, len(global_model.adjmatrix)):
                if global_model.adjmatrix[i, j] == 1:
                    self.G.add_edge(i, j)

    def draw_graph(self):
        if self.is_running:
            return
        self.is_running = True
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        
        nx.draw(self.G, ax=ax, with_labels=True, font_weight='bold')

        self.fig.canvas.draw()



class ChartFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._corner_radius=0
        # self._fg_color="#00FF00"

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text=" Generate Chart",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=home_image, anchor="w", command=self.plot_chart_event, 
                                                   font=customtkinter.CTkFont(size=15, weight="bold"))
        self.button.grid(row=0, column=0, sticky="ew")

        self.chart = ChartInFrame(self)
        self.chart.grid(row=0, column=1)
        # self.chart.after(0, self.chart.process_queue)
        # self.chart.after(1000, self.chart.add_to_queue)  # schedule the add_to_queue method to be called after 1 second

    def plot_chart_event(self):
        # global prev_radio_var
        # global global_radio_var
        # if prev_radio_var != global_radio_var:
        #     self.graph_frame.temp()
        #     prev_radio_var = global_radio_var

        global t0
        global t1
        global alpha
        global epoch_size
        global nbhood
        print(nbhood)
        print(f'{t0},  {t1},  {alpha},   {epoch_size}')
        self.chart.reload()
        self.chart.plot_chart(t0, t1, alpha, epoch_size, nbhood)


class ChartInFrame(customtkinter.CTkFrame):
    def __init__(self, *args, test_value=1, **kwargs):
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

        self.is_running = False

    def draw_graph(self, data):
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.plot(data)
        self.fig.canvas.draw()

    def process_queue(self, event):
        while True:
            data = self.q.get(block=True)
            if data is None:
                print('returning - end of simulation')
                self.is_running = False
                return
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




    def plot_chart(self, slider_t0=100000, slider_t1=0.00001, slider_alpha=0.95, slider_epoch_size=100, nbhood=[1, 0, 0, 0, 0, 0]):        
        if self.is_running:
            return
        self.is_running = True
        
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

        if len(neighbourhood) == 0:
            neighbourhood.add(self.Model.change_solution)
            neighbourhood.add(self.Model.change_solution2)
            neighbourhood.add(self.Model.change_solution3)
            neighbourhood.add(self.Model.change_solution4)
            neighbourhood.add(self.Model.change_solution5)
            neighbourhood.add(self.Model.change_solution6)
        
        print(neighbourhood)

        event = threading.Event()
        self.is_running = True
        # t0: float = 100, t1: float = 0.01, alpha: float = 0.95, epoch_size: int = 100,neighbourhoods_active:set = {}, event=None
        t1 = threading.Thread(daemon=True, target=self.Model.run_model, args=(slider_t0, slider_t1, slider_alpha, slider_epoch_size, neighbourhood, event))
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
        if prev_radio_var != global_radio_var:
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

        # global radio_var
        # print(radio_var)

# adjmatrix, arch, schedule = load_model()
# global_network.reset_state(True, True)
# global_network = Network(arch)
# global_network.load_schedule(schedule)
# global_model = OptimizationModel(global_network, adjmatrix)




if __name__ == "__main__":
    app = App()
    app.mainloop()