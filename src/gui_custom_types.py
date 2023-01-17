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


class OptionMenuWithName(customtkinter.CTkFrame):
    def __init__(self, *args, options=[1, 2], name='name', command=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.options = []
        self.name = name

        for it, val in enumerate(options):
            self.options.append(str(val))

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.option_menu = customtkinter.CTkOptionMenu(self, values=self.options, width=100, height=20, command=command)
        self.option_menu.grid(row=0, column=1, padx=(0, 0), pady=0, sticky='ew')

        self.name = customtkinter.CTkButton(self, corner_radius=0, width=90, height=20, border_spacing=10,
                                                   text=f'{name}:',
                                                   fg_color="transparent", text_color="gray10", hover=False,
                                                   anchor="e",
                                                   font=customtkinter.CTkFont(size=15, weight="bold"))
        self.name.grid(row=0, column=0, padx=(0, 0), pady=0, sticky='ew')

    def option_menu_callback(self, id):
        return id

    def reload(self, options):
        self.options = []
        for _, val in enumerate(options):
            self.options.append(str(val))

        self.option_menu.configure(values=self.options)
        self.option_menu.set(self.options[0])



class TextboxWithName(customtkinter.CTkFrame):
    def __init__(self, *args, value=5, name='name', set_precision=2, use_precision=True,
                 v_witdth=60, v_height=20, v_activate_scrollbars=False, v_border_spacing=0, state='disabled',
                 m_witdth=70, m_height=20, m_font_size=15, m_font_weight='bold', **kwargs):
        super().__init__(*args, **kwargs)

        self.value = value
        self.name = name
        self.set_precision = set_precision
        self.use_precision = use_precision
        self.state = state
        self.m_font_size = m_font_size
        self.m_font_weight = m_font_weight

        self._bg_color = '#e5e5e5'
        self._fg_color = '#e5e5e5'

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.value_textbox = customtkinter.CTkTextbox(self, width=v_witdth, height=v_height, bg_color='#e5e5e5', activate_scrollbars=v_activate_scrollbars, border_spacing=v_border_spacing, state=self.state)
        self.value_textbox.grid(row=0, column=1, padx=(0, 0), pady=0, sticky='ew')

        self.name = customtkinter.CTkButton(self, corner_radius=0, width=m_witdth, height=m_height, border_spacing=6,
                                                   text=f'{name}:',
                                                   fg_color="transparent", text_color="gray10", hover=False,
                                                   anchor="e",
                                                   font=customtkinter.CTkFont(size=self.m_font_size, weight=self.m_font_weight))
        self.name.grid(row=0, column=0, padx=(0, 0), pady=0, sticky='ew')

    def change_value(self, val):
        if self.state == 'disabled':
            self.value_textbox.configure(state="normal")
            self.value_textbox.delete('0.0', 'end')
            if self.use_precision:
                self.value_textbox.insert("0.0", f'{val:.{self.set_precision}}')
            else:
                self.value_textbox.insert("0.0", f'{val}')
            self.value_textbox.configure(state="disabled")
        elif self.state == 'normal':
            self.value_textbox.delete('0.0', 'end')
            if self.use_precision:
                self.value_textbox.insert("0.0", f'{val:.{self.set_precision}}')
            else:
                self.value_textbox.insert("0.0", f'{val}')
    
    def reset_value(self):
        if self.state == 'disabled':
            self.value_textbox.configure(state="normal")
            self.value_textbox.delete('0.0', 'end')
            self.value_textbox.configure(state="disabled")     
        elif self.state == 'normal':
            self.value_textbox.delete('0.0', 'end')
    
    def get_value(self):
        if self.state == 'disabled':
            self.value_textbox.configure(state="normal")
            val = self.value_textbox.get('0.0', 'end')
            self.value_textbox.configure(state="disabled")     
            return val
        elif self.state == 'normal':
            return self.value_textbox.get('0.0', 'end')


class RandomGraphParams(customtkinter.CTkFrame):
    def __init__(self, *args, command=None, routers_val=10, PCs_val=5, packages_val=100, prob_val=0.5, time_val=5, **kwargs):
        super().__init__(*args, **kwargs)

        self.callback = command
        self.routers_val = routers_val
        self.PCs_val = PCs_val
        self.packages_val = packages_val
        self.prob_val = prob_val
        self.time_val = time_val

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(6, weight=1)

        self.label = customtkinter.CTkButton(self, corner_radius=0, height=20, border_spacing=10,
                                                       text="Random network params",
                                                       fg_color="transparent", text_color=("gray10", "gray90"),
                                                       hover=False,
                                                       anchor="n",
                                                       font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label.grid(row=0, column=0)

        self.number_of_routers = TextboxWithName(self, name='number of routers', state='normal', use_precision=False, m_font_size=None, m_font_weight='normal')
        self.number_of_routers.change_value(self.routers_val)
        self.number_of_routers.grid(row=1, column=0, pady=5, sticky='e')
        self.number_of_PCs = TextboxWithName(self, name='number of PCs', state='normal', use_precision=False, m_font_size=None, m_font_weight='normal')
        self.number_of_PCs.change_value(self.PCs_val)
        self.number_of_PCs.grid(row=2, column=0, pady=5, sticky='e')
        self.number_of_packages = TextboxWithName(self, name='number of packages', state='normal', use_precision=False, m_font_size=None, m_font_weight='normal')
        self.number_of_packages.change_value(self.packages_val)
        self.number_of_packages.grid(row=3, column=0, pady=5, sticky='e')
        self.connection_probability = TextboxWithName(self, name='connection probability', state='normal', use_precision=False, m_font_size=None, m_font_weight='normal')
        self.connection_probability.change_value(self.prob_val)
        self.connection_probability.grid(row=4, column=0, pady=5, sticky='e')
        self.timespan = TextboxWithName(self, name='timespan', state='normal', use_precision=False, m_font_size=12, m_font_weight='normal')
        self.timespan.change_value(self.time_val)
        self.timespan.grid(row=5, column=0, pady=5, sticky='e')

        self.save_button = customtkinter.CTkButton(self,
                                            width=50,
                                            height=20, border_spacing=10,
                                            border_width=0,
                                            corner_radius=8,
                                            text="RELOAD",
                                            command=self.button_event, 
                                            font=customtkinter.CTkFont(size=12, weight="bold"))
        self.save_button.grid(row=6, column=0, pady=10)
    
    def button_event(self):
        self.callback()
  


class EssentialsTextField(customtkinter.CTkFrame):
    def __init__(self, *args, min_value=5, max_value=8, improvements=20, iterations=10, deteriations=10, **kwargs):
        super().__init__(*args, **kwargs)

        self.min_value = min_value
        self.max_value = max_value
        self.improvements = improvements
        self.iterations = iterations
        self.deteriations = deteriations

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(4, weight=1)

        self.min_textbox = TextboxWithName(self, value=10, name='MIN')
        self.min_textbox.grid(row=0, column=0, padx=0, pady=10, sticky='ew')

        self.max_textbox = TextboxWithName(self, value=10, name='MAX')
        self.max_textbox.grid(row=0, column=1, padx=0, pady=10, sticky='ew')

        self.improvements_textbox = TextboxWithName(self, value=10, name='IMPROVEMENTS', use_precision=False)
        self.improvements_textbox.grid(row=0, column=2, padx=8, pady=10, sticky='ew')

        self.iterations_textbox = TextboxWithName(self, value=10, name='ITERATIONS', use_precision=False)
        self.iterations_textbox.grid(row=0, column=3, padx=8, pady=10, sticky='ew')

        self.deteriorations_textbox = TextboxWithName(self, value=10, name='DETERIORATIONS', use_precision=False)
        self.deteriorations_textbox.grid(row=0, column=4, padx=(8, 20), pady=10, sticky='ew')

    def set_values(self, min_val, max_val, improvements, iterations, deteriorations):
        self.min_textbox.change_value(min_val)
        self.max_textbox.change_value(max_val)
        self.improvements_textbox.change_value(improvements)
        self.iterations_textbox.change_value(iterations)
        self.deteriorations_textbox.change_value(deteriorations)

    def clean_values(self):
        self.min_textbox.reset_value()
        self.max_textbox.reset_value()
        self.improvements_textbox.reset_value()
        self.iterations_textbox.reset_value()
        self.deteriorations_textbox.reset_value()



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

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(5, weight=1)
        self.slider = customtkinter.CTkSlider(self, from_=slider_start, to=slider_end, command=self.slider_event, number_of_steps=steps, corner_radius=0)
        self.slider.grid(row=0, column=1, columnspan=4, padx=(20, 20), pady=7, sticky='ew')
        self.slider.set(self.scale_fun(self.default_value))

        self.value_textbox = customtkinter.CTkTextbox(self, width=90, height=20, activate_scrollbars=False, border_spacing=0)
        self.value_textbox.grid(row=0, column=5, padx=(20, 20), pady=7, sticky="nsew")
        # self.value_textbox.configure(state="normal")
        self.value_textbox.insert("0.0", f'{self.default_value:.{self.round_factor}f}')
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
