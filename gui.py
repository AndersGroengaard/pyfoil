import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


#%matplotlib widget
import matplotlib.pyplot as plt


from mpl_interactions import ioff, panhandler, zoom_factory


from foils import NACA


def add_foil_plot(widget=None):
    """
    ---------------------------------------------------------------------------
    | Creates the base foil plot with layout and theme colors                 |
    | If a tkinter widget is supplied as input, it will be packed onto        |
    | that widget. If nothing is supplied it will plot as normally.           |
    ---------------------------------------------------------------------------
    """
    foil = NACA("7412")
    
    face_color = '#373737' 
    foil_color = '#08F7FE'
    
    fig = plt.Figure(#figsize=(3,3),
                     dpi=100, facecolor=face_color)
    ax = fig.add_subplot(111)
    ax.set_facecolor('#212946')
    
 
    
    if widget != None:
        figcanvas = FigureCanvasTkAgg(fig, widget)
        
        
    ax.fill(foil.pts[:,0], foil.pts[:,1], color=foil_color, alpha=0.25, zorder=1)  
    ax.set_aspect('equal', 'box')#.set_aspect('equal')#, adjustable='box')
    ax.set_adjustable("datalim")
 #   ax.patch.set_alpha(0.5)
 
    ax.grid(color='#2A3459', linestyle='solid') 
 
    for spine in ax.spines.values():
        spine.set_visible(False)
        
    ax.tick_params(colors='#DFE0E1', direction='out')
    for tick in ax.get_xticklabels():
        tick.set_color('#DFE0E1')
    for tick in ax.get_yticklabels():
        tick.set_color('#DFE0E1')    
        
 
    disconnect_zoom = zoom_factory(ax)
    display(fig.canvas)   
    
    pan_handler = panhandler(fig)
    display(fig.canvas)
   
    
    if widget == None:
        plt.show()
    else:
        return figcanvas, ax
    
    
  
 
# =============================================================================
#     fig = plt.figure(figsize=(7, 5), facecolor='#212946')
#     ax = fig.add_subplot(111)
#     ax.set_facecolor('#212946')
#     
#     if self.x is not None and self.yc is not None:
#         plot_glowing_line(ax, self.x, self.yc, 
#                           '#00ff9f',
#                         #  '#ea00d9', 
#                           linestyle='dashed', label="camber line")
# 
#     ax.fill(self.pts[:,0], self.pts[:,1], color=foil_color, alpha=0.25, zorder=1)      
#     plot_glowing_line(ax, self.pts[:,0], self.pts[:,1], foil_color, label="Foil Surface")
#    
#     ax.axis('equal')        
#     ax.set_title(self.name, color='#08F7FE')
#  
#     plt.grid(color='#2A3459', linestyle='solid')
#  
#     for spine in ax.spines.values():
#         spine.set_visible(False)
#  
#     ax.tick_params(colors='#DFE0E1', direction='out')
#     for tick in ax.get_xticklabels():
#         tick.set_color('#DFE0E1')
#     for tick in ax.get_yticklabels():
#         tick.set_color('#DFE0E1')
#         
#     ax.set_xlabel('X-axis',fontsize = 10, color='#08F7FE')                
#     ax.set_ylabel('Y-axis', fontsize = 10, color='#08F7FE')            
# =============================================================================

    
    
    
    
    
    
    
    
    

class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets onto the frame...
   #     self.label = customtkinter.CTkLabel(self)
  #      self.label.grid(row=0, column=0, padx=20)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("PyFoil - Multi Element Airfoil Maker")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="PyFoil", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
 
        # Create main plotting frame
        self.my_frame = MyFrame(master=self)
        self.my_frame.grid(row=0, column=1, rowspan=3, padx=20, pady=20, sticky="nsew")
   
        self.figcanvas, self.ax = add_foil_plot(self.my_frame)
        self.figcanvas.get_tk_widget().pack(fill='both', expand=True)#.grid(row=0, column=0, sticky=tkinter.E+tkinter.W+tkinter.N+tkinter.S)
    
        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self)#, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.main_button_1.configure(text="Export")


        # create scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Foils")
        self.scrollable_frame.grid(row=0, column=3, rowspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []
        for i in range(100):
            switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"CTkSwitch {i}")
            switch.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_frame_switches.append(switch)

 

        # set default values
        self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
 
        self.scrollable_frame_switches[0].select()
        self.scrollable_frame_switches[4].select()
 
    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()