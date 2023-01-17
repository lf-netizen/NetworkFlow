import numpy as np
import matplotlib.pyplot as plt
title_text = 'Loss by Disaster'
footer_text = 'June 24, 2020'
fig_background_color = 'skyblue'
fig_border = 'steelblue'
data =  [
            [         'Freeze', 'Wind', 'Flood', 'Quake', 'Hail'],
            [ '5 year',  66386, 174296,   75131,  577908,  32015],
            ['10 year',  58230, 381139,   78045,   99308, 160454],
            ['20 year',  89135,  80552,  152558,  497981, 603535],
            ['30 year',  78415,  81858,  150656,  193263,  69638],
            ['40 year', 139361, 331509,  343164,  781380,  52269],
        ]
# Pop the headers from the data array
column_headers = data.pop(0)
row_headers = [x.pop(0) for x in data]
# Table data needs to be non-numeric text. Format the data
# while I'm at it.
cell_text = []
for row in data:
    cell_text.append([f'{x/1000:1.1f}' for x in row])
# Get some lists of color specs for row and column headers
rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))
# Create the figure. Setting a small pad on tight_layout
# seems to better regulate white space. Sometimes experimenting
# with an explicit figsize here can produce better outcome.
plt.figure(linewidth=2,
           edgecolor=fig_border,
           facecolor=fig_background_color,
           tight_layout={'pad':1},
           #figsize=(5,3)
          )
# Add a table at the bottom of the axes
the_table = plt.table(cellText=cell_text,
                      rowLabels=row_headers,
                      rowColours=rcolors,
                      rowLoc='right',
                      colColours=ccolors,
                      colLabels=column_headers,
                      loc='center')
# Scaling is the only influence we have over top and bottom cell padding.
# Make the rows taller (i.e., make cell y scale larger).
the_table.scale(1, 1.5)
# Hide axes
ax = plt.gca()
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
# Hide axes border
plt.box(on=None)
# Add title
plt.suptitle(title_text)
# Add footer
plt.figtext(0.95, 0.05, footer_text, horizontalalignment='right', size=6, weight='light')
# Force the figure to update, so backends center objects correctly within the figure.
# Without plt.draw() here, the title will center on the axes and not the figure.
plt.draw()
# Create image. plt.savefig ignores figure edge and face colors, so map them.
fig = plt.gcf()
plt.show()
# plt.savefig('pyplot-table-demo.png',
#             #bbox='tight',
#             edgecolor=fig.get_edgecolor(),
#             facecolor=fig.get_facecolor(),
#             dpi=150
#             )



# import tkinter
# import customtkinter
# import os
# from PIL import Image
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
# customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


# class App(customtkinter.CTk):
#     def __init__(self):
#         super().__init__()

#         self.title("Network")
#         self.geometry(f"{1100}x{580}")

#         # set grid layout 1x2
#         self.grid_rowconfigure(0, weight=1)
#         self.grid_columnconfigure(1, weight=1)

#         # load images
#         self.load_images()

        
#         # create navigation frame
#         self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
#         self.navigation_frame.grid(row=0, column=0, sticky="nsew")
#         self.navigation_frame.grid_rowconfigure(4, weight=1)

#         self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Network", image=self.home_network_image,
#                                                              compound="left", font=customtkinter.CTkFont(size=18, weight="bold"))
#         self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

#         self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text=" Home",
#                                                    fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
#                                                    image=self.home_image, anchor="w", command=self.home_button_event, 
#                                                    font=customtkinter.CTkFont(size=15, weight="bold"))
#         self.home_button.grid(row=1, column=0, sticky="ew")

#         self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text=" Graph",
#                                                       fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
#                                                       image=self.graph_image, anchor="w", command=self.frame_2_button_event,
#                                                       font=customtkinter.CTkFont(size=15, weight="bold"))
#         self.frame_2_button.grid(row=2, column=0, sticky="ew")

#         self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text=" Chart",
#                                                       fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
#                                                       image=self.line_chart_image, anchor="w", command=self.frame_3_button_event,
#                                                       font=customtkinter.CTkFont(size=15, weight="bold"))
#         self.frame_3_button.grid(row=3, column=0, sticky="ew")

#         self.frame_4_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text=" Frame 4",
#                                                       fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
#                                                       image=self.add_user_image, anchor="w", command=self.frame_4_button_event,
#                                                       font=customtkinter.CTkFont(size=15, weight="bold"))
#         self.frame_4_button.grid(row=4, column=0, sticky="ew")

#     #     # self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
#     #     #                                                         command=self.change_appearance_mode_event)
#     #     # self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

#         # create home frame
#         self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
#     #     self.home_frame.grid_columnconfigure(0, weight=1)

#     #     self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.large_test_image)
#     #     self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

#     #     self.home_frame_button_1 = customtkinter.CTkButton(self.home_frame, text="", image=self.image_icon_image)
#     #     self.home_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
#     #     self.home_frame_button_2 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="right")
#     #     self.home_frame_button_2.grid(row=2, column=0, padx=20, pady=10)
#     #     self.home_frame_button_3 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="top")
#     #     self.home_frame_button_3.grid(row=3, column=0, padx=20, pady=10)
#     #     self.home_frame_button_4 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="top")
#     #     self.home_frame_button_4.grid(row=4, column=0, padx=20, pady=10)

#         # create second frame
#         self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="#dddddd")
#         # create radiobutton frame
#         self.second_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0))
#         self.radio_var = tkinter.IntVar(value=0)
#         self.label_radio_group = customtkinter.CTkLabel(master=self.second_frame, text="CTkRadioButton Group:")
#         self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
#         self.radio_button_1 = customtkinter.CTkRadioButton(master=self.second_frame, variable=self.radio_var, value=0)
#         self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
#         self.radio_button_2 = customtkinter.CTkRadioButton(master=self.second_frame, variable=self.radio_var, value=1)
#         self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
#         self.radio_button_3 = customtkinter.CTkRadioButton(master=self.second_frame, variable=self.radio_var, value=2)
#         self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

#     #     # # create checkbox and switch frame
#     #     # self.checkbox_slider_frame = customtkinter.CTkFrame(self)
#     #     # self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
#     #     # self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
#     #     # self.checkbox_1.grid(row=1, column=0, pady=(20, 10), padx=20, sticky="n")
#     #     # self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
#     #     # self.checkbox_2.grid(row=2, column=0, pady=10, padx=20, sticky="n")
#     #     # self.switch_1 = customtkinter.CTkSwitch(master=self.checkbox_slider_frame, command=lambda: print("switch 1 toggle"))
#     #     # self.switch_1.grid(row=3, column=0, pady=10, padx=20, sticky="n")
#     #     # self.switch_2 = customtkinter.CTkSwitch(master=self.checkbox_slider_frame)
#     #     # self.switch_2.grid(row=4, column=0, pady=(10, 20), padx=20, sticky="n")

#         # create third frame
#         self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="#444444")

#         # create fourth frame
#         self.fourth_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="#FF2222")

#         # select default frame
#         self.select_frame_by_name("home")

#     def select_frame_by_name(self, name):
#         # set button color for selected button
#         self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
#         self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
#         self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
#         self.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")

#         # show selected frame
#         if name == "home":
#             self.home_frame.grid(row=0, column=1, sticky="nsew")
#         else:
#             self.home_frame.grid_forget()
#         if name == "frame_2":
#             self.second_frame.grid(row=0, column=1, sticky="nsew")
#         else:
#             self.second_frame.grid_forget()
#         if name == "frame_3":
#             self.third_frame.grid(row=0, column=1, sticky="nsew")
#         else:
#             self.third_frame.grid_forget()
#         if name == "frame_4":
#             self.fourth_frame.grid(row=0, column=1, sticky="nsew")
#         else:
#             self.fourth_frame.grid_forget()

#     def home_button_event(self):
#         self.select_frame_by_name("home")

#     def frame_2_button_event(self):
#         self.select_frame_by_name("frame_2")

#     def frame_3_button_event(self):
#         self.select_frame_by_name("frame_3")

#     def frame_4_button_event(self):
#         self.select_frame_by_name("frame_4")
    
#     def load_images(self):
#         # load images with light and dark mode image
#         image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
#         self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
#         self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
#         self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
#         # self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
#         #                                          dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
#         # self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
#         #                                          dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
#         self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
#                                                         dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

#         my_image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "my_images")
#         self.home_network_image = customtkinter.CTkImage(Image.open(os.path.join(my_image_path, "networking.png")), size=(35, 35))
#         self.home_image = customtkinter.CTkImage(Image.open(os.path.join(my_image_path, "home-icon.png")), size=(28, 28))
#         self.graph_image = customtkinter.CTkImage(Image.open(os.path.join(my_image_path, "neural-network.png")), size=(30, 30))
#         self.line_chart_image = customtkinter.CTkImage(Image.open(os.path.join(my_image_path, "line-chart.png")), size=(30, 30))


# if __name__ == "__main__":
#     app = App()
#     app.mainloop()