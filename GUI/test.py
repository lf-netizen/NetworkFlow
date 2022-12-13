import tkinter
import customtkinter
import os
import sys
from PIL import Image
# graph
import matplotlib.pyplot as plt
import networkx as nx
# sys.path.append( '\src' )
# from simulated_annealing import OptimizationModel
# from network import Network
# from custom_types import ID
import numpy as np

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
        self.neighbourhood_frame.grid(row=0, column=1, padx=20, pady=20)

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


class GraphFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._corner_radius=0
        # self._fg_color="#FF0000"



        # G = nx.petersen_graph()
        # subax1 = plt.subplot(121)
        # nx.draw(G, with_labels=True, font_weight='bold')
        # subax2 = plt.subplot(122)
        # nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
        # plt.show()



class ChartFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._corner_radius=0
        # self._fg_color="#00FF00"

        



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
        self.geometry(f"{1100}x{580}")  # default window size
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



#     class RadioButtonFrame(customtkinter.CTkFrame):
#     def __init__(self, *args, header_name="RadioButtonFrame", **kwargs):
#         super().__init__(*args, **kwargs)
        
#         self.header_name = header_name

#         self.header = customtkinter.CTkLabel(self, text=self.header_name)
#         self.header.grid(row=0, column=0, padx=10, pady=10)

#         self.radio_button_var = customtkinter.StringVar(value="")

#         self.radio_button_1 = customtkinter.CTkRadioButton(self, text="Option 1", value="Option 1", variable=self.radio_button_var)
#         self.radio_button_1.grid(row=1, column=0, padx=10, pady=10)
#         self.radio_button_2 = customtkinter.CTkRadioButton(self, text="Option 2", value="Option 2", variable=self.radio_button_var)
#         self.radio_button_2.grid(row=2, column=0, padx=10, pady=10)
#         self.radio_button_3 = customtkinter.CTkRadioButton(self, text="Option 3", value="Option 3", variable=self.radio_button_var)
#         self.radio_button_3.grid(row=3, column=0, padx=10, pady=(10, 20))

#     def get_value(self):
#         """ returns selected value as a string, returns an empty string if nothing selected """
#         return self.radio_button_var.get()

#     def set_value(self, selection):
#         """ selects the corresponding radio button, selects nothing if no corresponding radio button """
#         self.radio_button_var.set(selection)


# class ThreeButtons(customtkinter.CTkFrame):
#     def __init__(self, *args, header_name="ThreeButtonsFrame", **kwargs):
#         super().__init__(*args, **kwargs)
        
#         self.header_name = header_name

#         self.header = customtkinter.CTkLabel(self, text=self.header_name)
#         self.header.grid(row=0, column=0, padx=10, pady=10)

#         self.button1 = customtkinter.CTkButton(self, text="button 1")
#         self.button1.grid(row=1, column=0, padx=20, pady=10)
#         self.button2 = customtkinter.CTkButton(self, text="button 2")
#         self.button2.grid(row=2, column=0, padx=20, pady=10)
#         self.button3 = customtkinter.CTkButton(self, text="button 3")
#         self.button3.grid(row=3, column=0, padx=20, pady=10)


# class ParentFrame(customtkinter.CTkFrame):
#     def __init__(self, *args, header_name="ThreeButtonsFrame", **kwargs):
#         super().__init__(*args, **kwargs)
        
#         self.header_name = header_name

#         self.header = customtkinter.CTkLabel(self, text=self.header_name)
#         self.header.grid(row=0, column=0, padx=10, pady=10)


#         self.radio_button_frame_1 = RadioButtonFrame(self, header_name="RadioButtonFrame 1")
#         self.radio_button_frame_1.grid(row=0, column=0, padx=20, pady=20)

        
#         self.buttons_frame = ThreeButtons(self, header_name="ThreeButtonsFrame")
#         self.buttons_frame.grid(row=0, column=1, padx=20, pady=20)