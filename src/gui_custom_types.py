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


class SliderBlock(customtkinter.CTkFrame):
    def __init__(self, *args, value=1_000, name='t0', slider_start=0, slider_end=8, min_value=1, max_value=1_000_000,
                 scale_fun=lambda x: x, inverse_fun=lambda x: x, default_value=1_000, steps=100_000, round_factor=2, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = default_value
        self.name = name
        self.slider_start = slider_start
        self.slider_end = slider_end
        self.min_value = min_value
        self.max_value = max_value
        self.default_value = default_value
        self.steps = steps
        self.scale_fun = scale_fun
        self.round_factor = round_factor
        self.inverse_fun = inverse_fun

        self._corner_radius = 0
        print(self.scale_fun(1_000))

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(5, weight=1)
        self.slider = customtkinter.CTkSlider(self, from_=slider_start, to=slider_end, command=self.slider_event, number_of_steps=steps, corner_radius=0)
        self.slider.grid(row=0, column=1, columnspan=4, padx=(20, 20), pady=7, sticky='ew')
        self.slider.set(self.default_value)

        self.value_textbox = customtkinter.CTkTextbox(self, width=90, height=20, activate_scrollbars=False, border_spacing=0)
        self.value_textbox.grid(row=0, column=5, padx=(20, 20), pady=7, sticky="nsew")
        # self.value_textbox.configure(state="normal")
        self.value_textbox.insert("0.0", f'{self.default_value}')
        # self.value_textbox.configure(state="disabled")


        self.name_textbox = customtkinter.CTkTextbox(self, width=90, height=20, activate_scrollbars=False)
        self.name_textbox.insert("0.0", name)
        self.name_textbox.configure(state="disabled")
        self.name_textbox.grid(row=0, column=0, padx=(20, 20), pady=7, sticky="nsew")


    def slider_event(self, val):
        self.value = self.inverse_fun(val)
        # self.value_textbox.configure(state="normal")
        self.value_textbox.delete('0.0', 'end')
        self.value_textbox.insert("0.0", f'{self.value:.{self.round_factor}f}')
        # self.value_textbox.configure(state="disable")

    def set(self, val):
        self.slider.set(self.scale_fun(val))

    def get_value(self):
        return self.value

    def reset(self):
        self.value = self.default_value
        self.slider.set(self.scale_fun(self.default_value))
        self.value_textbox.delete('0.0', 'end')
        self.value_textbox.insert("0.0", f'{self.value:.{self.round_factor}f}')

    def get_textbox_content(self):
        return self.value_textbox.get('0.0', 'end')



        # self.value = self.scale_fun(self.default_value)
        # self.slider.set(self.value)
        # self.slider_event(self.default_value)
#
# class MainFrame(customtkinter.CTkFrame):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         # create 1x2 grid system
#         self.grid_rowconfigure(3, weight=1)
#         self.grid_columnconfigure(1, weight=1)
#
#         # self.slider = customtkinter.CTkSlider(self, from_=0, to=10, number_of_steps=100)
#         self.slider = SliderBlock()
#         self.slider.grid(row=0, column=1, padx=(20, 20), pady=0, sticky='nsew')
#         self.slider2 = SliderBlock(name='slider')
#         self.slider2.grid(row=1, column=1, padx=(20, 20), pady=0, sticky='nsew')
#         self.slider3 = SliderBlock(name='test')
#         self.slider3.grid(row=2, column=1, padx=(20, 20), pady=0, sticky='nsew')
#
#
# class App(customtkinter.CTk):
#     def __init__(self):
#         super().__init__()
#
#         # window properties
#         self.title("Test app")  # window title
#         self.geometry(f"{1100}x{620}")  # default window size
#         self.minsize(500, 400)  # minimum window size
#
#         # create 1x1 grid system
#         self.grid_rowconfigure(0, weight=1)
#         self.grid_columnconfigure(0, weight=1)
#
#         # display
#         self.main_frame = MainFrame(self)
#         self.main_frame.grid(row=0, column=0, sticky="nsew")
#
#
# if __name__ == "__main__":
#     app = App()
#     app.mainloop()
