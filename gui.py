import tkinter
import tkinter.messagebox
import customtkinter
import types

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib.patches import Polygon
#%matplotlib widget
import matplotlib.pyplot as plt


from mpl_interactions import ioff, panhandler, zoom_factory
import numpy as np

from foils import NACA


    

class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets onto the frame...
   #     self.label = customtkinter.CTkLabel(self)
  #      self.label.grid(row=0, column=0, padx=20)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.draggable_foils = []     # Initializing the foils list variable
        self.foil_objs = {}     # Initializing the foils obj dict variable
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
        self.my_frame.grid(row=0, column=1, rowspan=3, padx=5, pady=0, sticky="nsew")
   
        self.add_foil_plot(self.my_frame)
      #  self.figcanvas, self.ax = add_foil_plot(self.my_frame)
        self.figcanvas.get_tk_widget().pack(fill='both', expand=True)#.grid(row=0, column=0, sticky=tkinter.E+tkinter.W+tkinter.N+tkinter.S)
    
        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self)#, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.main_button_1.configure(text="Export")


        # create scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self)#, label_text="Foils")
        self.scrollable_frame.grid(row=0, column=3, rowspan=3, padx=(0, 0), pady=(5, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []
    #    for i in range(100):
     ##       switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"CTkSwitch {i}")
    #        switch.grid(row=i, column=0, padx=10, pady=(0, 20))
  #          self.scrollable_frame_switches.append(switch)

        self.add_foil_button = customtkinter.CTkButton(self.scrollable_frame, command=self.add_foil)
        self.add_foil_button.configure(text="Add Foil")
        self.add_foil_button.grid(row=0, column=0, padx=10, pady=(0, 20))
        
        
        # set default values
        #self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
 
      #  self.scrollable_frame_switches[0].select()
      #  self.scrollable_frame_switches[4].select()
      
      
     

    
    def add_foil_plot(self, widget=None):
        """
        ---------------------------------------------------------------------------
        | Creates the base foil plot with layout and theme colors                 |
        | If a tkinter widget is supplied as input, it will be packed onto        |
        | that widget. If nothing is supplied it will plot as normally.           |
        ---------------------------------------------------------------------------
        """
        import matplotlib.style as mplstyle
        mplstyle.use('fast')
        face_color = '#373737' 
    #    foil_color = '#08F7FE'
        self.selected_color = '#BCFFFF'  # '#00E0C7'
        self.unselected_color = '#08F7FE'
        
        fig = plt.Figure(dpi=100, facecolor=face_color)
  
        
        self.ax = fig.add_subplot(111)
        self.ax.set_position([0, 0, 1, 1])
        self.ax.set_facecolor(face_color)
        self.ax.margins(x=0)
        if widget != None:
            self.figcanvas = FigureCanvasTkAgg(fig, widget)
 
        self.ax.set_aspect('equal', 'box') 
        self.ax.set_adjustable("datalim")
 
        self.ax.grid(which='major', color='#4E4E4E', linestyle='-')
        self.ax.grid(which='minor', color='#454545', linestyle='--')   
        self.ax.minorticks_on()
        for spine in self.ax.spines.values():
            spine.set_visible(False)
            
# =============================================================================
#         self.ax.tick_params(colors='#DFE0E1', direction='out')
#         for tick in self.ax.get_xticklabels():
#             tick.set_color('#DFE0E1')
#         for tick in self.ax.get_yticklabels():
#             tick.set_color('#92B780')    
# =============================================================================
        self.ax.tick_params(axis='both', colors='#9E9E9E')
        
        self.ax.axhline(color='#D2686E', lw=0.5)
        self.ax.axvline(color='#92B780', lw=0.5)
        
       # self.ax.spines['bottom'].set_position('center') # spine for xaxis 
        #    - will pass through the center of the y-values (which is 0)
      #  self.ax.spines['left'].set_position('center')  # spine for yaxis 
        #    - will pass through the center of the x-values (which is 5)
# =============================================================================
        self.ax.spines['left'].set_position(('data', 0.0))
        self.ax.spines['bottom'].set_position(('data', 0.0))
#         self.ax.spines['right'].set_color('#08F7FE')
#         self.ax.spines['top'].set_color('#08F7FE')
# =============================================================================

        
        self.ax.set_xlim(-3, 3)
        
# =============================================================================
#         plt.gca().set_axis_off()
#         plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
#           hspace = 0, wspace = 0)
# =============================================================================
     
      #  fig.tight_layout()
      #  fig.tight_layout()
 
  
 
        self.press = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None
        self.clicked_foil = None
        self._selected_geometry = {}
        self._ctrl_press = False
        dragging_foil = False
        
        def onPress(event):
            
            global dragging_foil
            
            dragging_foil = False
            if event.key == 'ctrl':
                self._ctrl_press = True
            
            
            if event.inaxes == self.ax:
                self.clicked_on_any_foil=False

                for _id, v in self.foil_objs.items():
                    f = v["foil_plot"]
    
                    if f.contains(event)[0]:
                        dragging_foil = True      
                        print("clicked on foil with id: "+str(_id))
                        
                        if self._ctrl_press == False:
                            for v in self._selected_geometry.values():
                                v.set_color(self.unselected_color)
                            self._selected_geometry.clear()
                        
                        self.clicked_on_any_foil = True
               
                        self.press = f.xy, (event.xdata, event.ydata)
                        self.clicked_foil = f
                        self.foil_xy = self.clicked_foil.get_xy()
                   
                        f.set_color(self.selected_color)
 
                        self._selected_geometry[_id] = f
                        
                    self.ax.figure.canvas.draw()   
                    
                if dragging_foil == False:
                    print("Clicked on axes")
         
                    self.cur_xlim = self.ax.get_xlim()
                    self.cur_ylim = self.ax.get_ylim()
                    
                    
                    for v in self._selected_geometry.values():
                        v.set_color(self.unselected_color)
                    self._selected_geometry.clear()
                    
                    
                    self.ax.figure.canvas.draw()   
                    
                self.press = self.x0, self.y0, event.xdata, event.ydata
                self.x0, self.y0, self.xpress, self.ypress = self.press
        
        def onRelease(event):
                       
            global dragging_foil          
            dragging_foil = False
            self.press = None
 
        
        def onMotion(event):
            
            global dragging_foil
            
            if self.press is None: 
                return
            if event.inaxes != self.ax: 
                return
            
            if dragging_foil:   
          
                dx = event.xdata - self.xpress
                dy = event.ydata - self.ypress
                new_xy = self.foil_xy.copy()
 
                new_xy[:,0] += dx
                new_xy[:,1] += dy
                self.clicked_foil.set_xy(new_xy)
            else:
                dx = event.xdata - self.xpress
                dy = event.ydata - self.ypress
                self.cur_xlim -= dx
                self.cur_ylim -= dy
                 
                
                
# =============================================================================
#                 ax=event.inaxes
#                 ax._pan_start = types.SimpleNamespace(
#                         lim=ax.viewLim.frozen(),
#                         trans=ax.transData.frozen(),
#                         trans_inverse=ax.transData.inverted().frozen(),
#                         bbox=ax.bbox.frozen(),
#                         x=event.x,
#                         y=event.y)
#             
#                 ax.drag_pan(3, event.key, event.x+dx*100, event.y+dy*100)
#                 #fig=ax.get_figure()
#                 fig.canvas.draw_idle()
#                 
# =============================================================================
# =============================================================================
#                 self.ax.drag_pan(3, event.key, event.x+dx, event.y+dy)
#     
#               
#                 fig.canvas.draw_idle()
# =============================================================================

                self.ax.set_xlim(self.cur_xlim)
                self.ax.set_ylim(self.cur_ylim)
        
            self.ax.figure.canvas.draw()     
         #   self.ax.figure.canvas.flush_events()
  
        def zoom(event):
            cur_xlim = self.ax.get_xlim()
            cur_ylim = self.ax.get_ylim()

            xdata = event.xdata # get event x location
            ydata = event.ydata # get event y location

            if event.button == 'up':                               # deal with zoom out
                scale_factor = 1 / base_scale
            elif event.button == 'down':                              # deal with zoom in
                scale_factor = base_scale
            else:                                                   # deal with something that should never happen                
                scale_factor = 1
           
            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

            relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])

            self.ax.set_xlim([xdata - new_width * (1-relx), xdata + new_width * (relx)])
            self.ax.set_ylim([ydata - new_height * (1-rely), ydata + new_height * (rely)])
            self.ax.figure.canvas.draw()
 
        def on_key_press(event):
         #   print(event.key)
            if event.key == 'shift':
               self._shift_press = True
            if event.key == 'control':
                self._ctrl_press = True
            if event.key == 'delete':
                self.delete_selected_foils()
               
        def on_key_release(event):
       
           if event.key == 'shift':
               self._shift_press = False
           if event.key == 'control':
               self._ctrl_press = False
               
        base_scale = 1.1
        
        fig.canvas.mpl_connect('button_press_event', onPress)
        fig.canvas.mpl_connect('motion_notify_event', onMotion)
        fig.canvas.mpl_connect('button_release_event', onRelease)
        fig.canvas.mpl_connect('scroll_event', zoom)
        fig.canvas.mpl_connect('key_press_event', on_key_press)
        fig.canvas.mpl_connect('key_release_event', on_key_release)
    
    def delete_selected_foils(self):    
        for _id, v in self._selected_geometry.items():
            print("deleting foil with id: "+str(_id))
            v.remove()
            del self.foil_objs[_id] 
            self.ax.figure.canvas.draw()
            
            
    def add_foil(self):
        
        foil = NACA("7412", n_pts=100)

        foil_plot = self.ax.fill(foil.pts[:,0], foil.pts[:,1], color=self.unselected_color, alpha=0.25, zorder=3)  
        
        self.foil_objs[foil.id] = {"foil":foil , "foil_plot": foil_plot[0]}
 
        self.ax.figure.canvas.draw()
 
 
        
        
    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())


    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")


if __name__ == "__main__":
    
    
    import tracemalloc
 
 

    # starting the monitoring
    tracemalloc.start()
     
    
    
    
    app = App()
    app.mainloop()
    
    
    
    

 
     
    # displaying the memory
    print(tracemalloc.get_traced_memory()) #
     # 10-02-2023 21:36  -> (2767038, 2852662)
    # stopping the library
    tracemalloc.stop()
        
    
    
    