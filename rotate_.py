from ursina import *
from ursina.shaders import unlit_shader

class Rotate_Arrow(Button):
    def __init__(self, model='assets/main/models/rotate_arrow.glb', position=Vec3(1,0,0), 
                 rotation=Vec3(0,0,0), color_=color.green, parent=None, 
                 on_click=None, highlight_color=color.black):
        super().__init__(
            parent=parent,
            model=model,
            position=position,
            scale=(0.15,0.15,0.15),
            rotation=rotation,
            color=color_,
            on_click=on_click,
            highlight_color=highlight_color,
            shader=unlit_shader
        )



    def update(self):
        self.world_scale = (0.15,0.15,0.15)
        


class Rotate(Entity):
    def __init__(self, parent=scene):
        super().__init__(parent=parent)

        #X
        self.x_rotate_arrow_plus=Rotate_Arrow(position=Vec3(0,0,0), rotation=Vec3(0,0,0), color_=color.green, parent=self, on_click=Func(self.rotate, Vec3(0,0,45)))
        self.x_rotate_arrow_minus=Rotate_Arrow(position=Vec3(0,0,0), rotation=Vec3(0,180,0), color_=color.green, parent=self, on_click=Func(self.rotate, Vec3(0,0,-45)))

        #Y
        self.y_rotate_arrow_plus=Rotate_Arrow(position=Vec3(0,0,0), rotation=Vec3(90,0,180), color_=color.blue, parent=self, on_click=Func(self.rotate, Vec3(0,45,0)))
        self.y_rotate_arrow_minus=Rotate_Arrow(position=Vec3(0,0,0), rotation=Vec3(270,180,180), color_=color.blue, parent=self, on_click=Func(self.rotate, Vec3(0,-45,0)))

        #Z
        self.z_rotate_arrow_plus=Rotate_Arrow(position=Vec3(0,0,0), rotation=Vec3(0,90,180), color_=color.red, parent=self, on_click=Func(self.rotate, Vec3(-45,0,0)))
        self.z_rotate_arrow_minus=Rotate_Arrow(position=Vec3(0,0,0), rotation=Vec3(180,90,0), color_=color.red, parent=self, on_click=Func(self.rotate, Vec3(45,0,0)))


        self.size_dist = 0.5

    def rotate(self, vec):
        if self.parent:
            # Изменяем размер родительского объекта
            self.parent.rotation += (vec * self.size_dist)

if __name__ == "__main__":
    app = Ursina()
    # Тестовый объект
    target = Entity(model='cube', color=color.gray)
    EditorCamera()
    
    # Инициализация системы изменения размера
    Rotate(parent=target)
    
    app.run()
