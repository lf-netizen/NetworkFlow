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
        
        self.neighbourhood_switch_1 = customtkinter.CTkSwitch(self.neighbourhood_frame, text="neighbourhood 1")
        self.neighbourhood_switch_1.grid(row=0, column=0, padx=20, pady=10)
        self.neighbourhood_switch_2 = customtkinter.CTkSwitch(self.neighbourhood_frame, text="neighbourhood 2")
        self.neighbourhood_switch_2.grid(row=1, column=0, padx=20, pady=10)
        self.neighbourhood_switch_3 = customtkinter.CTkSwitch(self.neighbourhood_frame, text="neighbourhood 3")
        self.neighbourhood_switch_3.grid(row=2, column=0, padx=20, pady=10)
        self.neighbourhood_switch_4 = customtkinter.CTkSwitch(self.neighbourhood_frame, text="neighbourhood 4")
        self.neighbourhood_switch_4.grid(row=3, column=0, padx=20, pady=10)
        self.neighbourhood_switch_5 = customtkinter.CTkSwitch(self.neighbourhood_frame, text="neighbourhood 5")
        self.neighbourhood_switch_5.grid(row=4, column=0, padx=20, pady=10)
        self.neighbourhood_switch_6 = customtkinter.CTkSwitch(self.neighbourhood_frame, text="neighbourhood 6")
        self.neighbourhood_switch_6.grid(row=5, column=0, padx=20, pady=10)
        self.neighbourhood_switch_7 = customtkinter.CTkSwitch(self.neighbourhood_frame, text="neighbourhood 7")
        self.neighbourhood_switch_7.grid(row=6, column=0, padx=20, pady=10)
        self.neighbourhood_switch_8 = customtkinter.CTkSwitch(self.neighbourhood_frame, text="neighbourhood 8")
        self.neighbourhood_switch_8.grid(row=7, column=0, padx=20, pady=10)


        self.start_graph_frame = customtkinter.CTkFrame(self)
        self.start_graph_frame.grid(row=0, column=0, padx=20, pady=20)

        self.start_graph_frame.grid_rowconfigure(4, weight=1)
        self.start_graph_frame.grid_columnconfigure(0, weight=1)

        self.radio_var = tkinter.IntVar(value=0)
        self.start_graph_radio_1 = customtkinter.CTkRadioButton(self.start_graph_frame, variable=self.radio_var, value=0, text="graph 1")
        self.start_graph_radio_1.grid(row=0, column=0, padx=20, pady=10)
        self.start_graph_radio_2 = customtkinter.CTkRadioButton(self.start_graph_frame, variable=self.radio_var, value=1, text="graph 2")
        self.start_graph_radio_2.grid(row=1, column=0, padx=20, pady=10)
        self.start_graph_radio_3 = customtkinter.CTkRadioButton(self.start_graph_frame, variable=self.radio_var, value=2, text="graph 3")
        self.start_graph_radio_3.grid(row=2, column=0, padx=20, pady=10)
        self.start_graph_radio_4 = customtkinter.CTkRadioButton(self.start_graph_frame, variable=self.radio_var, value=3, text="graph 4")
        self.start_graph_radio_4.grid(row=3, column=0, padx=20, pady=10)

        self.parameters_frame = customtkinter.CTkFrame(self)
        self.parameters_frame.grid(row=0, column=1, padx=20, pady=20)

        self.parameters_frame.grid_rowconfigure(4, weight=1)
        self.parameters_frame.grid_columnconfigure(0, weight=1)

        self.parameters_slider_t0 = customtkinter.CTkSlider(self.parameters_frame, from_=100_000, to=1_000_000, command=self.slider_t0_event)
        self.parameters_slider_t0.grid(row=0, column=0, padx=20, pady=20)
        #self.parameters_slider_1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.parameters_slider_t1 = customtkinter.CTkSlider(self.parameters_frame, from_=0.000_001, to=0.000_1, command=self.slider_t1_event)
        self.parameters_slider_t1.grid(row=1, column=0, padx=20, pady=20)
        self.parameters_slider_alpha = customtkinter.CTkSlider(self.parameters_frame, from_=0, to=1, command=self.slider_alpha_event)
        self.parameters_slider_alpha.grid(row=2, column=0, padx=20, pady=20)
        self.parameters_slider_epoch_size = customtkinter.CTkSlider(self.parameters_frame, from_=1, to=50, command=self.slider_epoch_size_event)
        self.parameters_slider_epoch_size.grid(row=3, column=0, padx=20, pady=20)
        #self.parameters_slider_2.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

    def slider_t0_event(self, val):
        self.textbox.insert('0.0', f't0 value set to: {val} \n')
    def slider_t1_event(self, val):
        self.textbox.insert('0.0', f't1 value set to: {val} \n')
    def slider_alpha_event(self, val):
        self.textbox.insert('0.0', f'alpha value set to: {val} \n')
    def slider_epoch_size_event(self, val):
        self.textbox.insert('0.0', f'epoch_size value set to: {val} \n')


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


        G = nx.complete_graph(4)
        self.is_running = False
        self.draw_graph(G)

    def draw_graph(self, G):
        if self.is_running:
            return
        self.is_running = True
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        
        nx.draw(G, ax=ax, with_labels=True, font_weight='bold')

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
        self.chart.plot_chart()


class ChartInFrame(customtkinter.CTkFrame):
    def __init__(self, *args, test_value=1, **kwargs):
        super().__init__(*args, **kwargs)

        self.canvas = tk.Canvas(self, width=500, height=500)
        self.canvas.pack()

        self.fig = Figure(figsize=(5, 5))
        self.figure_canvas = FigureCanvasTkAgg(self.fig, self.canvas)
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

        self.Model = self.load_model()
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

    def load_model(self):
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

        network = Network(arch)
        network.load_schedule(schedule)
        return OptimizationModel(network=network, adjmatrix=adjmatrix)


    def plot_chart(self, slider_t0=100000, slider_t1=0.00001, slider_alpha=0.95, slider_epoch_size=100):        
        if self.is_running:
            return
        self.is_running = True
        
        self.Model.network.reset_state(with_schedule=False)
        event = threading.Event()
        t1 = threading.Thread(daemon=True, target=self.Model.run_model, args=(slider_t0, slider_t1, slider_alpha, slider_epoch_size, event))
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