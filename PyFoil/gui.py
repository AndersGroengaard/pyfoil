# /*##########################################################################
#
# Copyright (c) 2023  
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/









import tkinter as tk
#import tkinter.messagebox
import customtkinter
#import types
import math

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
#customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("./pyfoil_theme.json")




import matplotlib as mpl
#mpl.use('Qt5Agg')
#mpl.use('TkAgg')
#mpl.use('Agg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


import matplotlib.pyplot as plt
from matplotlib import backend_bases

#from mpl_interactions import ioff, panhandler, zoom_factory
import numpy as np
#import mplcursors
from foils import NACA

import AUlibrary as au
    
class FoilFrame(customtkinter.CTkFrame):
    def __init__(self, master, name, foil_id, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color=au.RGBtoHex(au.AUlightblue))
        # add widgets onto the frame...
        self.id = foil_id
        self.name = name
        self.label = customtkinter.CTkLabel(self)
        self.label.configure(text=self.name)
        self.label.grid(row=0, column=0, padx=0)


class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
 


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.draggable_foils = []                                              # Initializing the foils list variable
        self.foil_objs = {}                                                    # Initializing the foils obj dict variable
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
        self.scrollable_frame_foils = []

        self.add_foil_button = customtkinter.CTkButton(self.scrollable_frame, command=self.add_foil)
        self.add_foil_button.configure(text="Add Foil")
        self.add_foil_button.pack()
        
        

      
     

    
    def add_foil_plot(self, widget=None):
        """
        -----------------------------------------------------------------------
        | Creates the base foil plot with layout and theme colors             |
        | If a tkinter widget is supplied as input, it will be packed onto    |
        | that widget. If nothing is supplied it will plot as normally.       |
        -----------------------------------------------------------------------
        """
        import matplotlib.style as mplstyle
        
        
        #from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
      #  from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
        
        mplstyle.use('fast')
        
        
        
        
        backend_bases.NavigationToolbar2.toolitems = (
                ('Home', 'Reset original view', 'home', 'home'),
                ('Back', 'Back to  previous view', 'back', 'back'),
                ('Forward', 'Forward to next view', 'forward', 'forward'),
                (None, None, None, None),
                ('Save', 'Save the figure', 'filesave', 'save_figure'),
            )
                    
                    
        
        
        
        face_color = '#373737' 
 
        self.selected_color = '#96FEF9'  
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
 
        self.ax.tick_params(axis='both', colors='#9E9E9E')
        
        self.ax.axhline(color='#D2686E', lw=0.5)
        self.ax.axvline(color='#92B780', lw=0.5)
 
        self.ax.spines['left'].set_position(('data', 0.0))
        self.ax.spines['bottom'].set_position(('data', 0.0))

        self.ax.set_xlim(-3, 3)
  
 
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
        self.theta_old = None
        self.scaling_distance_old = None
        self.transform_state = "Normal"
        
        def blit_foil():
            fcanvas = self.clicked_foil.figure.canvas
            faxes = self.clicked_foil.axes
            fcanvas.restore_region(self.fbackground)                           # restore the background region      
            faxes.draw_artist(self.clicked_foil)                               # redraw just the current rectangle
            fcanvas.blit(faxes.bbox)                                           # blit just the redrawn area
 
        
        def onPress(event):
 
            self.transform_state = "Normal"
 
            if event.key == 'ctrl':
                self._ctrl_press = True
            
            
            if event.inaxes == self.ax:
                self.clicked_on_any_foil=False

                for _id, v in self.foil_objs.items():
                    f = v["foil_plot"]
    
                    if f.contains(event)[0]:
     
                        self.transform_state = "Dragging foil"
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
                        
                        # Blitting
   
                        fcanvas = f.figure.canvas
                        faxes = f.axes
                        f.set_animated(True)
                        fcanvas.draw()
                        self.fbackground = fcanvas.copy_from_bbox(f.axes.bbox)
                        faxes.draw_artist(f)
                        fcanvas.blit(faxes.bbox)
                        
 
                if self.transform_state == "Normal":
                    print("Clicked on axes")
         
                    self.cur_xlim = self.ax.get_xlim()
                    self.cur_ylim = self.ax.get_ylim()
                   
                    for f in self._selected_geometry.values():
                        if f != None:
                            f.set_color(self.unselected_color)
                          
                            f.set_animated(True)
                            blit_foil()
                            f.set_animated(False)
    
                    self._selected_geometry.clear()
           
                self.press = self.x0, self.y0, event.xdata, event.ydata
                self.x0, self.y0, self.xpress, self.ypress = self.press
 
 
                if self.transform_state == "Normal": 
                    x, y = event.x, event.y
                    self.ax.start_pan(x, y, event.button)
                
        def onRelease(event):

            self.transform_state = "Normal"
            self.press = None
            for f in self._selected_geometry.values():
                f.set_animated(False)
                
        def onMotion(event):
 
            if self.press is None: 
                if self.transform_state == "Rotation":    
      
                    theta = math.atan2((event.ydata - self.rotOy) , (event.xdata - self.rotOx))   
                    if self.theta_old != None:
 
                        d_alpha = self.theta_old - theta
                        new_xy = self.rotate_around_point_highperf(self.rotxy, d_alpha, self.rotOx, self.rotOy)
                        self.clicked_foil.set_xy(new_xy)
                        blit_foil()
 
                    self.theta_old = theta
          
            
                elif self.transform_state == "Scaling":  
                    scaling_distance = math.sqrt( (abs(event.xdata - self.scaleOx))**2 + (abs(event.ydata - self.scaleOy))**2)
                        
                    if self.scaling_distance_old != None:
           
                        s = scaling_distance/self.scaling_distance_old
                        new_xy = self.scalexy.copy()
                        new_xy[:,0] = new_xy[:,0] - self.scaleOx
                        new_xy[:,1] = new_xy[:,1] - self.scaleOy
                        new_xy = new_xy * s
                        new_xy[:,0] = new_xy[:,0] + self.scaleOx
                        new_xy[:,1] = new_xy[:,1] + self.scaleOy
     
                        self.clicked_foil.set_xy(new_xy) 
                        blit_foil()
                        
               #     self.scaling_distance_old = scaling_distance
                    
                   
                else:        
                    return
                 
            if event.inaxes != self.ax: 
                return
            
 
            if self.transform_state == "Dragging foil":
                dx = event.xdata - self.xpress
                dy = event.ydata - self.ypress
                new_xy = self.foil_xy.copy()
 
                new_xy[:,0] += dx
                new_xy[:,1] += dy
                
                self.clicked_foil.set_xy(new_xy)
                               
                fcanvas = self.clicked_foil.figure.canvas
                faxes = self.clicked_foil.axes
      
                fcanvas.restore_region(self.fbackground)                       # restore the background region      
                faxes.draw_artist(self.clicked_foil)                           # redraw just the current rectangle
                fcanvas.blit(faxes.bbox)                                       # blit just the redrawn area
         
            elif self.transform_state == "Normal":
                dx = event.xdata - self.xpress
                dy = event.ydata - self.ypress
                self.cur_xlim -= dx
                self.cur_ylim -= dy
                 
                self.ax.drag_pan(1, event.key, event.x, event.y)
                fig.canvas.draw_idle()
 
  
        def zoom(event):
            cur_xlim = self.ax.get_xlim()
            cur_ylim = self.ax.get_ylim()

            xdata = event.xdata # get event x location
            ydata = event.ydata # get event y location

            if event.button == 'up':                                  # deal with zoom out
                scale_factor = 1 / base_scale
            elif event.button == 'down':                              # deal with zoom in
                scale_factor = base_scale
            else:                                                     # deal with something that should never happen                
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
            if event.key == "p":
                self.p1.toolbar.pan()
            if event.key == "f":
                print("Flipping foil")
                self.transform_state = "Flip"
                for _id, v in self._selected_geometry.items():
    
                    xy = v.get_xy()
                    Ox = (min(xy[:,0]) + max(xy[:,0]))/2
                    Oy = (min(xy[:,1]) + max(xy[:,1]))/2
                    
            if event.key == "r":
                print("rotating airfoil")
                self.transform_state = "Rotation"
                for _id, v in self._selected_geometry.items():
 
                    self.rotxy = v.get_xy()
                    self.rotOx = (min(self.rotxy[:,0]) + max(self.rotxy[:,0]))/2
                    self.rotOy = (min(self.rotxy[:,1]) + max(self.rotxy[:,1]))/2

            if event.key == "s":
                self.transform_state = "Scaling"
                for _id, v in self._selected_geometry.items():
 
                    self.scalexy = v.get_xy()
       
                    self.scaleOx = (min(self.scalexy[:,0]) + max(self.scalexy[:,0]))/2
                    self.scaleOy = (min(self.scalexy[:,1]) + max(self.scalexy[:,1]))/2
                    self.scaling_distance_old  = math.sqrt( (abs(event.xdata - self.scaleOx))**2 + (abs(event.ydata - self.scaleOy))**2)
         
                print("scaling airfoil")
                    
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
    
      #  mplcursors.cursor(self.ax)
    
    def delete_selected_foils(self):    
        for _id, v in self._selected_geometry.items():
       #     print("deleting foil with id: "+str(_id))
            v.remove()
            del self.foil_objs[_id] 
            self.ax.figure.canvas.draw()
            self.clicked_foil = None
        self._selected_geometry.clear()
            
    def add_foil(self):
        
        name = "NACA7412"
        
        foil = NACA("7412", n_pts=100)
        foil_plot = self.ax.fill(foil.pts[:,0], foil.pts[:,1], color=self.unselected_color, alpha=0.25, zorder=3)    
        
        self.foil_objs[foil.id] = {"foil":foil , "foil_plot": foil_plot[0]}
 
        self.ax.figure.canvas.draw()
        
        fframe = FoilFrame(self.scrollable_frame, name, foil.id)
        fframe.pack(#anchor=tk.N, 
                    fill=tk.BOTH, 
                    expand=True, 
                    pady=(5, 0),
                    padx=(25, 0)
                  #  side=tk.LEFT
                    )
 
    
 
    def rotate_around_point_highperf(self, xy, radians, o_x, o_y):
       """
       ------------------------------------------------------------------------
       | Rotate an array of points, xy, around a specific point (o_x, o_y)    |
       | by theta (radians)                                                   |
       ------------------------------------------------------------------------
       |  INPUT:                                                              |
       |     xy (array) : Array of points to be rotated, with x coordinates   |
       |                  in column 0 and y-coordinates in column 1           |
       |     radians (float) : The amount of radians that the points xy       |
       |                       should be rotated.                             |
       |     o_x (float) : x-coordinate for the offset point                  |
       |     o_y (float) : y-coordinate for the offset point                  |
       |______________________________________________________________________|
       """
     #  x, y = xy
   
       adjusted_x = (xy[:,0] - o_x)
       adjusted_y = (xy[:,1] - o_y)
       cos_rad = math.cos(radians)
       sin_rad = math.sin(radians)
       xy[:,0] = o_x + cos_rad * adjusted_x + sin_rad * adjusted_y
       xy[:,1] = o_y + -sin_rad * adjusted_x + cos_rad * adjusted_y
   
       return xy

        
        
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

    tracemalloc.start()    # starting the monitoring
     
    app = App()
    app.mainloop()

    print(tracemalloc.get_traced_memory()) # displaying the memory
     # 10-02-2023 21:36  -> (2767038, 2852662)
    # stopping the library
    tracemalloc.stop()
        
    
    
    