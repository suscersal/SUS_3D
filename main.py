from import_helper import *
from load_config import load_cfg
from save_config import save_cfg
from color_sliders import ColorPicker
from ursina.shaders import unlit_shader
from file_browser import *
from file_browser_save import *
from ursina.prefabs.first_person_controller import FirstPersonController

from move import *
from size import *
from rotate_ import *


app=Ursina(title='SUS Engine',development_mode=False)

scene.light = AmbientLight(shadows=True)
AmbientLight(intensity=0.5)


global choice,choice_instrument, all_objects
all_objects=[]
choice=False
choice_instrument='move'





class Instruments_button(Button):
    def __init__(self,texture=None,position=Vec3(0,0,0)):
        super().__init__(
            parent=camera.ui,
            texture=texture,
            position=position,
            scale=(0.05,0.05),
            color=color.color(0,0,0.9),
            highlight_color=color.color(0,0,2)
        )

        self.choice=False
        self.Inst=None
        # print(self.texture)
        if str(self.texture)=='move.jpg':
            self.Inst='move'
        elif str(self.texture)=='size.jpg':
            self.Inst='size'
        elif str(self.texture)=='rotate.jpg':
            self.Inst='rotate'
        
        # self.start_time=time.time()
    

    def update(self):
        # if time.time() - self.start_time >= 5:
        if self.choice==True and choice_instrument==self.Inst:
            # print('true ' + self.Inst)
            self.color=color.color(0,0,0.25)
        else:
            # print('false ' + self.Inst)
            self.choice=False
            self.color=color.color(0,0,0.9)
        
        # self.start_time=time.time()
        

    
    def input(self,key):
        global choice_instrument
        if self.hovered:
            if key=='left mouse down':             
                self.choice=True
                choice_instrument=self.Inst
    




        
class Instruments(Empty):
    def __init__(self):
        super().__init__()

        self.move=Instruments_button(texture='assets/main/textures/move.jpg',position=(-0.775,0.35))
        self.move.choice=True
        self.scale=Instruments_button(texture='assets/main/textures/size.jpg',position=(-0.775,0.30))
        self.rotate=Instruments_button(texture='assets/main/textures/rotate.jpg',position=(-0.775,0.25))

    
    
        



class VectorArrows(Entity):
    def __init__(self):
        super().__init__(
            visible = True
                         )

        self.x_arrow = Entity(model='assets/main/models/vector_arrow.glb',scale=(0.5,0.1,0.05),rotation=Vec3(0,0,0),color=color.green,position=Vec3(0.7,0,0),shader=unlit_shader)
        self.y_arrow = Entity(model='assets/main/models/vector_arrow.glb',scale=(0.5,0.1,0.05),rotation=Vec3(0,0,-90),color=color.blue,position=Vec3(0,0.7,0),shader=unlit_shader)
        self.z_arrow = Entity(model='assets/main/models/vector_arrow.glb',scale=(0.5,0.1,0.05),rotation=Vec3(0,90,0),color=color.red,position=Vec3(0,0,-0.7),shader=unlit_shader)
        self.sphere = Entity(model='sphere',scale=(0.3,0.3,0.3))
        

        self.start_time=time.time()

    def update(self):
        if time.time()- self.start_time >= 5:       
            self.x_arrow.visible=self.visible
            self.y_arrow.visible=self.visible
            self.z_arrow.visible=self.visible
            self.sphere.visible=self.visible
            self.start_time=time.time()
            


class Move_dist():
    move_dist=load_cfg()

move_dist=Move_dist()
# print(move_dist)

move_dist_input = InputField(model='cube',parent=camera.ui,position=(-0.525,0.48),scale=(0.1,0.06),limit_content_to='0123456789',default_value=f'Move: {move_dist.move_dist}',active=False,color=color.gray,character_limit=5)





       


class Add_Entity(Button):
    def __init__(self,model='cube',position=Vec3(1,1,1),scale=1,color_=color.white):
        super().__init__(
            parent=scene,
            position=position,
            scale=scale,
            highlight_color=color.rgba(0,128,128,128),
            model=model,
            collider='cube',
            color=color_,
                         )
        
        self.choices=False
        self.tap_arrow=False
        self.move=Move(parent=self)  
        self.size=Size(parent=self) 
        self.Rotate=Rotate(parent=self)
        self.a=self.move.x_arrow_down.hovered or self.move.x_arrow_up.hovered or self.move.y_arrow_down.hovered or self.move.y_arrow_up.hovered or self.move.z_arrow_down.hovered or self.move.z_arrow_up.hovered
        self.start_time=time.time()
        self.properties=Properties(parent=camera.ui)
        self.bb=self.properties.color_sliders.sliders
        self.properties.color_sliders.sliders['r'].value = self.color.r * 255
        self.properties.color_sliders.sliders['g'].value = self.color.g * 255
        self.properties.color_sliders.sliders['b'].value = self.color.b * 255
        self.properties.color_sliders.sliders['a'].value = self.color.a * 255

    def input(self,key):
        global choice

        if key == 'left mouse down':
            # 1. Собираем все стрелки в один список для быстрой проверки
            arrows = [
                self.move.x_arrow_down, self.move.x_arrow_up,
                self.move.y_arrow_down, self.move.y_arrow_up,
                self.move.z_arrow_down, self.move.z_arrow_up,

                self.size.x_size_down, self.size.x_size_up,
                self.size.y_size_down, self.size.y_size_up,
                self.size.z_size_down, self.size.z_size_up,

                self.Rotate.x_rotate_arrow_plus, self.Rotate.x_rotate_arrow_minus,
                self.Rotate.y_rotate_arrow_plus, self.Rotate.y_rotate_arrow_minus,
                self.Rotate.z_rotate_arrow_plus, self.Rotate.z_rotate_arrow_minus,

                instruments.move,instruments.scale,instruments.rotate
            ]

            # 2. Проверяем, на что именно навели мышку в момент клика
            hover = mouse.hovered_entity

            # УСЛОВИЯ:
            # А. Если нажали на сам куб
            if hover == self:
                self.choices = True
                choice = True

            # Б. Если нажали на одну из стрелок
            elif hover in arrows:
                self.choices = True  # ПАНЕЛЬ ОСТАЕТСЯ
                choice = True        # ВЫДЕЛЕНИЕ НЕ СНИМАЕТСЯ

            # В. Если нажали на панель свойств или ползунки
            elif hover and (hover == self.properties or hover.has_ancestor(self.properties)):
                self.choices = True  # ПАНЕЛЬ ОСТАЕТСЯ

            # Г. Если кликнули в пустоту (не по кубу, не по стрелкам, не по UI)
            else:
                self.choices = False
                choice = False

        if key == 'escape':
            if self.choices:
                self.choices=False
                choice=False
        
        if key == 'delete' and self.choices:
            self.destroy_move()
            self.destroy_size()
            self.destroy_rotate()

            destroy(self.properties)
            destroy(self)


    def destroy_move(self):
        destroy(self.move.x_arrow_up)
        destroy(self.move.x_arrow_down)

        destroy(self.move.y_arrow_up)
        destroy(self.move.y_arrow_down)

        destroy(self.move.z_arrow_up)
        destroy(self.move.z_arrow_down)
    


    def destroy_size(self):
        destroy(self.size.x_size_up)
        destroy(self.size.x_size_down)

        destroy(self.size.y_size_up)
        destroy(self.size.y_size_down)

        destroy(self.size.z_size_up)
        destroy(self.size.z_size_down)

    def destroy_rotate(self):
        destroy(self.Rotate.x_rotate_arrow_plus)
        destroy(self.Rotate.x_rotate_arrow_minus)

        destroy(self.Rotate.y_rotate_arrow_plus)
        destroy(self.Rotate.y_rotate_arrow_minus)

        destroy(self.Rotate.z_rotate_arrow_plus)
        destroy(self.Rotate.z_rotate_arrow_minus)




    def update(self):
        if self.scale.x < 0.5:
            self.scale=(0.5,self.scale.y,self.scale.z)
        if self.scale.y < 0.5:
            self.scale=(self.scale.x,0.5,self.scale.z)
        if self.scale.z < 0.5:
            self.scale=(self.scale.x,self.scale.y,0.5)
        


        self.color=self.properties.color_sliders.return_color()
        # if time.time() - self.start_time > 0.5:
        #     self.tap_arrow=False

        self.properties.position_text.text=f'Position: ({self.position.x},{self.position.y},{self.position.z})'
        self.properties.size_text.text=f'Size: ({self.scale.x},{self.scale.y},{self.scale.z})'
        self.properties.rotate_text.text=f'Rotation: ({self.rotation.x},{self.rotation.y},{self.rotation.z})'

        # print(self.choices)
        if self.choices:
            self.color=color.yellow
            self.properties.enabled=True
        else:
            # self.color=color.rgba(0,220,220,220)
            self.properties.enabled=False
            try:
                self.destroy_move()
                self.destroy_size()
                self.destroy_rotate()
            except:
                pass
        

        if time.time() - self.start_time >= 0.1:

            self.destroy_move()
            self.destroy_size()
            self.destroy_rotate()
            if self.choices:
                if choice_instrument=='move':
                    self.move=Move(parent=self)
                    self.move.move_dist=move_dist.move_dist

                elif choice_instrument == 'size':
                    self.size=Size(parent=self)
                    self.size.size_dist=move_dist.move_dist
                
                elif choice_instrument == 'rotate':
                    self.Rotate=Rotate(parent=self)

            self.start_time=time.time()
                

            

        

        



class Properties(Entity):
    def __init__(self, parent=camera.ui): # Лучше явно указать camera.ui для UI
        super().__init__(parent=parent)

        # 1. collider=None — чтобы клики пролетали сквозь фон к ползункам
        # 2. z=0.1 — отодвигаем фон чуть назад (в UI чем больше Z, тем дальше объект)
        self.background = Sprite(
            parent=self, 
            position=(0.65, -0.3), 
            scale=(0.4, 0.4), 
            color=color.gray, 
            collider=None, # Исправлено
            z=0.1          # Исправлено
        )
        
        self.properties_text = Text(parent=self, text='Properties', color=color.black, position=(0.6, -0.1))
        
        # ColorPicker теперь будет на z=-0.1 или 0, то есть ПЕРЕД фоном
        self.color_sliders = ColorPicker(
            parent=self, 
            position=Vec2(0.7, -0.4), 
            z=0 
        )

        self.position_text=Text(parent=self,text=f'Position:',color=color.black,position=(0.5,-0.15),scale=(1.25,1.25))
        self.size_text=Text(parent=self,text=f'Size:',color=color.black,position=(0.5,-0.2),scale=(1.25,1.25))
        self.rotate_text=Text(parent=self,text=f'Rotation:',color=color.black,position=(0.5,-0.25),scale=(1.25,1.25))




def add_obj_mesh(model,color_,position,scale):
    global all_objects
    all_objects.append(Add_Entity(model=model,color_=color_,position=position,scale=scale))


class OpenButton(Button):
    def __init__(self, text='button',command=None,scale=(0,0),position=(0,0),text_size=1):
        super().__init__(
            scale=scale,
            position=position,
            text=text,
            parent=camera.ui,
            color=color.gray,
            model='cube',
            collider='mesh',
            text_size=text_size
                        )
        
        self.command=command
    
    def input(self, key):
        if self.hovered:
            if key=='left mouse down':
                self.command(model='cube',color_=color.white,position=Vec3(1,1,1),scale=1)





def export_model(filename='test.ply'):
    global all_objects
    blocks_data = []

    for b in all_objects:
        # Позиция
        pos = b.position
        # Масштаб (Vec3)
        s = b.scale
        # Поворот (Vec3)
        r_deg = b.rotation
        # Цвет
        r, g, bl, a = [int(x * 255) for x in b.color]

        # Строка: X Y Z R G B A ScaleX ScaleY ScaleZ RotX RotY RotZ
        line = f"{pos.x} {pos.y} {pos.z} {r} {g} {bl} {a} {s.x} {s.y} {s.z} {r_deg.x} {r_deg.y} {r_deg.z}"
        blocks_data.append(line)

    header = (
        "ply\n"
        "format ascii 1.0\n"
        f"element vertex {len(blocks_data)}\n"
        "property float x\n"
        "property float y\n"
        "property float z\n"
        "property uchar red\n"
        "property uchar green\n"
        "property uchar blue\n"
        "property uchar alpha\n"
        "property float scale_x\n"
        "property float scale_y\n"
        "property float scale_z\n"
        "property float rot_x\n"
        "property float rot_y\n"
        "property float rot_z\n"
        "end_header\n"
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(header)
        f.write("\n".join(blocks_data))
    
    print(f"Экспорт параметров завершен! Файлов: {len(blocks_data)}")


    mainMenuButton.menu.enabled = False

def clear_scene():
    global all_objects
    for i in all_objects:
        destroy(i)

def import_model(filename):
    clear_scene()

    if isinstance(filename, list): filename = filename[0]
    if not os.path.exists(filename): return

    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    header_end = 0
    for i, line in enumerate(lines):
        if 'end_header' in line:
            header_end = i + 1
            break

    # Читаем данные после заголовка
    for i in range(header_end, len(lines)):
        line = lines[i].strip()
        if not line: continue
        
        data = line.split()
        
        # 1. Позиция (0, 1, 2)
        pos = Vec3(float(data[0]), float(data[1]), float(data[2]))
        
        # 2. Цвет (3, 4, 5, 6)
        r, g, b, a = int(data[3]), int(data[4]), int(data[5]), int(data[6])
        
        # 3. Масштаб (7, 8, 9)
        sc = Vec3(float(data[7]), float(data[8]), float(data[9]))
        
        # 4. Поворот (10, 11, 12)
        rot = Vec3(float(data[10]), float(data[11]), float(data[12]))

        # Создаем объект через вашу функцию
        new_obj = add_obj_mesh(
            model='cube', 
            color_=color.rgba32(r, g, b, a), 
            position=pos, 
            scale=sc
        )
        
        # Дополнительно применяем поворот (так как в add_obj_mesh его нет в аргументах)
        # Если add_obj_mesh возвращает созданный объект:
        # new_obj.rotation = rot
        
        # Если add_obj_mesh не возвращает объект, можно обратиться к последнему в списке:
        all_objects[-1].rotation = rot

    print("Импорт завершен!")


    mainMenuButton.menu.enabled = False







        
class MainMenuButton(Button):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            scale=(0.05,0.05),
            model='cube',
            position=(-0.775,0.475),
            texture='assets/main/textures/icon.jpg',
            color=color.color(0,0,0.9),
            highlight_color=color.white,
        )

        def _export():
            self.menu.enabled = False
            # Создаем окно сохранения. 
            # file_types должен быть списком расширений через запятую (например, ['.ply'])
            fb = FileBrowserSave(
                file_types=['.ply'],
                enabled=True
            )
            # Когда пользователь нажмет "Save", вызовется наша функция экспорта
            fb.on_submit = lambda path: [setattr(self.menu, 'enabled', True), export_model(str(path))]
            fb.on_cancel  = lambda: setattr(self.menu, 'enabled', True)
            

        def _import():
            self.menu.enabled = False
            # Создаем окно выбора файла
            fb = FileBrowser(
                file_types=['.ply'],
                enabled=True
            )
            # Когда пользователь выберет файл, вызовется наша функция импорта
            fb.on_submit = lambda path: [setattr(self.menu, 'enabled', True), import_model(str(path[0]))]
            fb.on_cancel  = lambda: setattr(self.menu, 'enabled', True)



        self.menu = Entity(parent=camera.ui, enabled=False)

        Button(parent=self.menu, text='Импортировать ply', scale=(.3, .05), y=.1, on_click=_import,color=color.gray)
        Button(parent=self.menu, text='Экспортировать в ply', scale=(.3, .05), y=.04, on_click=_export,color=color.gray)
        Button(parent=self.menu, text='Выход из приложения', scale=(.3, .05), y=-.02, on_click=lambda: application.quit(),color=color.red)

        
    
    def input(self,key):
        if self.hovered:
            if key=='left mouse down':
                self.menu.enabled = not self.menu.enabled




class Add_Menu():
    def __init__(self):
        self.open_button=OpenButton(text='Добавить обьект',command=add_obj_mesh,scale=(0.15,0.06),position=(-0.675,0.48),text_size=0.5)





fps_text=Text(position=Vec2(0.7,0.5))
global start_time
start_time=time.time()
start_time_=time.time()

def update():
    global start_time,move_dist,start_time_,all_objects
    # if time.time() - start_time >= 0.5:
        
    #     # print(move_dist)
    #     fps = int(1//time.dt_unscaled)
    #     fps_text.text = "FPS: " + str(fps)
    #     if fps >= 50:
    #         fps_text.color=color.lime
    #     elif fps < 50 and fps > 25:
    #         fps_text.color=color.yellow
    #     else:
    #         fps_text.color=color.red
        
    #     start_time=time.time()
    # print(all_objects)
    if move_dist_input.text!='' and move_dist_input.text!=f'Move: {move_dist.move_dist}':
        move_dist.move_dist=int(move_dist_input.text)
        move_dist_input.text=f'Move: {move_dist}'
    
    if time.time() - start_time_ >= 1:
        start_time_=time.time()
        save_cfg(move_dist.move_dist)
        # print(choice_instrument)
        # game_()
        
        # print(scene.children)
    
    








global game
game=False

add_menu=Add_Menu()
mainMenuButton=MainMenuButton()
vector_arrows=VectorArrows()
grid=Entity(model=Grid(1000,1000), rotation_x=90, scale=1000, color=color.white33)
instruments = Instruments()

player=EditorCamera()
# player_=FirstPersonController(gravity=0)
# player_.enabled=False
player.look_at((0,0,0))

# def input(key):
#     global game
#     if key == 'tab':
#         game = not game
#         camera.position=Vec3(0,0,0)
        


def game_():
    global game,player
    if game == False:
        add_menu.open_button.enabled=True
        mainMenuButton.enabled=True

        vector_arrows.x_arrow.enabled=True
        vector_arrows.y_arrow.enabled=True
        vector_arrows.z_arrow.enabled=True
        vector_arrows.sphere.enabled=True

        grid.enabled=True
        move_dist_input.enabled=True

        instruments.move.enabled=True

        player.enabled=True
        # player_.enabled=False
        camera.parent=player
        clear_scene()
        
    else:
        add_menu.open_button.enabled=False
        mainMenuButton.enabled=False
        
        vector_arrows.x_arrow.enabled=False
        vector_arrows.y_arrow.enabled=False
        vector_arrows.z_arrow.enabled=False
        vector_arrows.sphere.enabled=False

        grid.enabled=False
        move_dist_input.enabled=False

        instruments.move.enabled=False

        player.enabled=False
        # player_.enabled=True
        # camera.parent=player_.camera_pivot

        import_model('test.ply')

        
        


app.run()