from PIL import Image, ImageTk, ImageDraw
import customtkinter as ctk
import math

class EiffelTower:
    def __init__(self, master):
        self.master = master
        master.title("Eiffel Tower 2.5D Drawing")
        master.resizable(False, False)

        self.width = 1280   # ancho de la ventana
        self.height = 720   # alto de la ventana
        
        self.pillow_image = Image.new('RGB', (self.width, self.height), 'white')    # lienzo para el dibujo
        self.drawer = ImageDraw.Draw(self.pillow_image) # objeto para dibujar 
        
        self.canvas = ctk.CTkCanvas(master, width= self.width, height= self.height, bg= "#F0F0F0")  # donde se encapsulara pillow_image 
        self.canvas.pack()
        
        self.ctk_image = None   # para almazenar la figura
        self.canvas_image_item = None
        
        self.angle_x = 0.5  # angulos de rotacion
        self.angle_y = 0.5
        self.angle_z = 0
        self.scale = 1.0
        
        self.is_dragging = False    # ultima ubicacion del mouse en pantalla
        self.last_x = 0
        self.last_y = 0
        
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)    # lectura de las entradas del mouse
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)
        self.canvas.bind("<MouseWheel>",self.update_scale)
   
        self.vertices_base = [] # coordenadas de todos los vertices
        self.edges = [] # indice de conexiones
        
        self.load_model("models/torre_pisa.txt")
        self.draw_model()
        
    def on_mouse_press(self, event):    # funcion de sostener click
        self.is_dragging = True
        self.last_x = event.x
        self.last_y = event.y

    def on_mouse_drag(self, event):     # funcion de arratrado
        if self.is_dragging:
            delta_x = event.x - self.last_x
            delta_y = event.y - self.last_y
            
            self.angle_y += delta_x * 0.01  # mide la distancia recorrida del mouse
            self.angle_x += delta_y * 0.01 
            
            self.last_x = event.x
            self.last_y = event.y
            self.draw_model()

    def on_mouse_release(self):  # funcion de soltar click
        self.is_dragging = False   
     
    def update_scale(self, event):    # funcion de escalado
        if event.num == 4 or event.delta > 0:  
            if self.scale >= 0.2:
                self.scale += -0.1 
                self.draw_model()
        elif event.num == 5 or event.delta < 0:  
            self.scale += 0.1
            self.draw_model()
 
        
    def rotate_point_3d(self, x, y, z): # funcion de rotacion
        y_temp = y * math.cos(self.angle_x) - z * math.sin(self.angle_x)    # rotacion en X
        z_temp = y * math.sin(self.angle_x) + z * math.cos(self.angle_x)
        x_rot_x, y_rot_x, z_rot_x = x, y_temp, z_temp
        
        x_temp = x_rot_x * math.cos(self.angle_y) + z_rot_x * math.sin(self.angle_y)    # rotacion en Y
        z_temp = -x_rot_x * math.sin(self.angle_y) + z_rot_x * math.cos(self.angle_y)
        x_rot_y, y_rot_y, z_rot_y = x_temp, y_rot_x, z_temp

        x_final = x_rot_y * math.cos(self.angle_z) - y_rot_y * math.sin(self.angle_z)   # rotacion en Z
        y_final = x_rot_y * math.sin(self.angle_z) + y_rot_y * math.cos(self.angle_z)
        
        return x_final, y_final, z_rot_y
        
    def load_model(self, filename):
        self.vertices_base = []
        self.edges = []

        try:
            with open(filename, "r") as f:
                for line in f:
                    parts = line.strip().split()
                    if not parts or parts[0].startswith("#"):
                        continue

                    if parts[0] == "v": # separar vertices
                        x, y, z = map(float, parts[1:])
                        self.vertices_base.append((x, y, z))

                    elif parts[0] == "e":   # separar aristas
                        a, b = map(int, parts[1:])
                        self.edges.append((a - 1, b - 1))

        except FileNotFoundError:
            print("File not found")
        
    def draw_model(self):
       
        self.drawer.rectangle([0, 0, self.width, self.height], fill="#F0F0F0")  # base blanca
        vertices_rotados = [self.rotate_point_3d(x, y, z) for x, y, z in self.vertices_base]
        
        offset_x = self.width // 2  # centra la figura en la ventana
        offset_y = self.height * .8  
        
        vertices_2d_projected = []  # dibuja las aristas
        for x, y, z in vertices_rotados:
            x_proj = x * self.scale + offset_x
            y_proj = -y * self.scale + offset_y 
            vertices_2d_projected.append((x_proj, y_proj, z)) 
        
        aristas_ordenadas = []  # dibuja las aristas (conexiones entre los vertices)
        for i, j in self.edges:
            p_i = vertices_2d_projected[i]
            p_j = vertices_2d_projected[j]           
            z_promedio = (p_i[2] + p_j[2]) / 2
            aristas_ordenadas.append((z_promedio, p_i, p_j))
        
        aristas_ordenadas.sort(key=lambda x: x[0]) 
        
        for z_promedio, p_i, p_j in aristas_ordenadas:
            x_i, y_i, z_i = p_i
            x_j, y_j, z_j = p_j
            
            line_color = "black" # color y gruesor de las lineas
            line_width = 1

            self.drawer.line([(x_i, y_i), (x_j, y_j)], fill=line_color, width=line_width)

        self.ctk_image = ImageTk.PhotoImage(self.pillow_image)  # transforma la figura en una imagen compatible con customtkinter
        if self.canvas_image_item:
            self.canvas.itemconfig(self.canvas_image_item, image= self.ctk_image)
        else:
            self.canvas_image_item = self.canvas.create_image(0, 0, anchor= "nw", image=self.ctk_image)
                
root = ctk.CTk()        
app = EiffelTower(root) 
root.mainloop()
       