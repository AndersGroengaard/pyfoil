import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib.patches import Polygon
#%matplotlib widget
import matplotlib.pyplot as plt


from mpl_interactions import ioff, panhandler, zoom_factory
import numpy as np

from foils import NACA


class ZoomPan:
    """
    From Seadoodude's answer at:
        https://stackoverflow.com/questions/11551049/matplotlib-plot-zooming-with-scroll-wheel
    """
    def __init__(self):
        self.press = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None


    def zoom_factory(self, ax, base_scale = 2.):
        def zoom(event):
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()

            xdata = event.xdata # get event x location
            ydata = event.ydata # get event y location

            if event.button == 'down':
                # deal with zoom in
                scale_factor = 1 / base_scale
            elif event.button == 'up':
                # deal with zoom out
                scale_factor = base_scale
            else:
                # deal with something that should never happen
                scale_factor = 1
           
            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

            relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])

            ax.set_xlim([xdata - new_width * (1-relx), xdata + new_width * (relx)])
            ax.set_ylim([ydata - new_height * (1-rely), ydata + new_height * (rely)])
            ax.figure.canvas.draw()

        fig = ax.get_figure() # get the figure of interest
        fig.canvas.mpl_connect('scroll_event', zoom)

        return zoom

    def pan_factory(self, ax):
        def onPress(event):
            if event.inaxes != ax: return
            self.cur_xlim = ax.get_xlim()
            self.cur_ylim = ax.get_ylim()
            self.press = self.x0, self.y0, event.xdata, event.ydata
            self.x0, self.y0, self.xpress, self.ypress = self.press

        def onRelease(event):
            self.press = None
            ax.figure.canvas.draw()

        def onMotion(event):
            if self.press is None: return
            if event.inaxes != ax: return
            dx = event.xdata - self.xpress
            dy = event.ydata - self.ypress
            self.cur_xlim -= dx
            self.cur_ylim -= dy
            ax.set_xlim(self.cur_xlim)
            ax.set_ylim(self.cur_ylim)

            ax.figure.canvas.draw()

        fig = ax.get_figure() # get the figure of interest

        # attach the call back
        fig.canvas.mpl_connect('button_press_event',onPress)
        fig.canvas.mpl_connect('button_release_event',onRelease)
        fig.canvas.mpl_connect('motion_notify_event',onMotion)

        #return the function
        return onMotion


# =============================================================================
# 
# =============================================================================




  
 
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

    
class DraggableFoil:
    def __init__(self, rect):
        self.rect = rect
        self.press = None

    def connect(self):
        """Connect to all the events we need."""
        self.cidpress = self.rect.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.rect.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.rect.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):
        """Check whether mouse is over us; if so, store some data."""
        if event.inaxes != self.rect.axes:
            return
        contains, attrd = self.rect.contains(event)
        if not contains:
            return
        print('event contains', self.rect.xy)
        self.press = self.rect.xy, (event.xdata, event.ydata)

    def on_motion(self, event):
        """Move the rectangle if the mouse is over us."""
        if self.press is None or event.inaxes != self.rect.axes:
            return
        (x0, y0), (xpress, ypress) = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        # print(f'x0={x0}, xpress={xpress}, event.xdata={event.xdata}, '
        #       f'dx={dx}, x0+dx={x0+dx}')
        self.rect.set_x(x0+dx)
        self.rect.set_y(y0+dy)

        self.rect.figure.canvas.draw()

    def on_release(self, event):
        """Clear button press information."""
        self.press = None
        self.rect.figure.canvas.draw()

    def disconnect(self):
        """Disconnect all callbacks."""
        self.rect.figure.canvas.mpl_disconnect(self.cidpress)
        self.rect.figure.canvas.mpl_disconnect(self.cidrelease)
        self.rect.figure.canvas.mpl_disconnect(self.cidmotion)
    
    
    
    
    
    
    

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
        self.scrollable_frame.grid(row=0, column=3, rowspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
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

        face_color = '#373737' 
        foil_color = '#08F7FE'
        
        fig = plt.Figure(dpi=100, facecolor=face_color)
        self.ax = fig.add_subplot(111)
        self.ax.set_facecolor(face_color)
        
        if widget != None:
            self.figcanvas = FigureCanvasTkAgg(fig, widget)
 
        self.ax.set_aspect('equal', 'box') 
        self.ax.set_adjustable("datalim")

        self.ax.grid(color='#4E4E4E', linestyle='solid') 
     
        for spine in self.ax.spines.values():
            spine.set_visible(False)
            
        self.ax.tick_params(colors='#DFE0E1', direction='out')
        for tick in self.ax.get_xticklabels():
            tick.set_color('#DFE0E1')
        for tick in self.ax.get_yticklabels():
            tick.set_color('#DFE0E1')    
        
        self.ax.set_xlim(-3, 3)
        
        self.draggable_foils = []     # Initializing the foils list variable
   #     scale = 1.1
      #  zp = ZoomPan()
      #  figZoom = zp.zoom_factory(ax, base_scale = scale)
      #  figPan = zp.pan_factory(ax)
        fig.tight_layout()
 
  
 
        self.press = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None
        self.clicked_foil = None
        dragging_foil = False
        
        def onPress(event):
            
            global dragging_foil
            
            dragging_foil = False
            
            if event.inaxes == self.ax:
                self.clicked_on_any_foil=False
                for f in self.draggable_foils:
                    if f.contains(event)[0]:
                        dragging_foil = True      
                 #       print("clicked on foil")
                        self.clicked_on_any_foil = True
                    #    print('event contains', f.xy)
                        self.press = f.xy, (event.xdata, event.ydata)
                        self.clicked_foil = f
                        self.foil_xy = self.clicked_foil.get_xy()
   
                     
                if dragging_foil == False:
              #     print("Clicked on axes")
         
                    self.cur_xlim = self.ax.get_xlim()
                    self.cur_ylim = self.ax.get_ylim()
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
                self.ax.set_xlim(self.cur_xlim)
                self.ax.set_ylim(self.cur_ylim)
        
            self.ax.figure.canvas.draw()     
       
  
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

        base_scale = 1.1
        
        fig.canvas.mpl_connect('button_press_event', onPress)
        fig.canvas.mpl_connect('motion_notify_event', onMotion)
        fig.canvas.mpl_connect('button_release_event', onRelease)
        fig.canvas.mpl_connect('scroll_event', zoom)

      
      
    def add_foil(self):
        
        #face_color = '#373737' 
        foil_color = '#08F7FE'
        foil = NACA("7412", n_pts=100)
        
        new_foil = self.ax.fill(foil.pts[:,0], foil.pts[:,1], color=foil_color, alpha=0.25, zorder=1)  
# =============================================================================
#         
#         new_foil = plt.Polygon(foil.pts[:,:2], closed=True, fill=True, linewidth=3, color='#F97306')
#         self.ax.add_patch(new_foil)
#     
#       #  df = DraggableFoil(new_foil)
#       #  df.connect()
        for n in new_foil:
            self.draggable_foils.append(n)
# =============================================================================
# =============================================================================
#         import numpy as np
#         rects = self.ax.bar(range(10), 20*np.random.rand(10))
#   
#         for rect in rects:
#             dr = DraggableFoil(rect)
#             dr.connect()
#             self.draggable_foils.append(dr)
# 
# =============================================================================
        
        
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