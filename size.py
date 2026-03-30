from ursina import *
from ursina.shaders import unlit_shader

class Size_Arrow(Button):
    def __init__(self, model='assets/main/models/size_arrow.glb', position=Vec3(1,0,0), scale=(0.5,0.1,0.1), 
                 rotation=Vec3(0,0,0), color_=color.green, parent=None, 
                 on_click=None, highlight_color=color.black, label=''):
        super().__init__(
            parent=parent,
            model=model,
            position=position,
            scale=scale,
            rotation=rotation,
            color=color_,
            on_click=on_click,
            highlight_color=highlight_color,
            shader=unlit_shader
        )
        
        if label:
            self.text_label = Text(
                text=label,
                parent=self,
                color=color.white,
                origin=(0, 0),
                # Смещаем текст на кончик стрелки (вдоль оси модели)
                position=(2.5, 0, 0), 
                scale=3,
                billboard=True
            )

    def update(self):
        # Ограничиваем масштаб самой модели стрелки
        self.world_scale = (0.5, 0.1, 0.1)
        
        if hasattr(self, 'text_label'):
            # Убираем деформацию текста и делаем его крупным
            self.text_label.world_scale = 5
            self.text_label.shader = None 

class Size(Entity):
    def __init__(self, parent=scene):
        super().__init__(parent=parent)
        
        # Дистанция стрелок от центра объекта
        dist = 1.5

        # X Axis (Зеленые)
        self.x_size_up = Size_Arrow(label='+', position=Vec3(dist,0,0), rotation=Vec3(0,0,0), color_=color.green, parent=self, on_click=Func(self.size, Vec3(1,0,0)))
        self.x_size_down = Size_Arrow(label='-', position=Vec3(-dist,0,0), rotation=Vec3(0,0,180), color_=color.green, parent=self, on_click=Func(self.size, Vec3(-1,0,0)))

        # Y Axis (Синие)
        self.y_size_up = Size_Arrow(label='+', position=Vec3(0,dist,0), rotation=Vec3(0,0,-90), color_=color.blue, parent=self, on_click=Func(self.size, Vec3(0,1,0)))
        self.y_size_down = Size_Arrow(label='-', position=Vec3(0,-dist,0), rotation=Vec3(0,0,90), color_=color.blue, parent=self, on_click=Func(self.size, Vec3(0,-1,0)))

        # Z Axis (Красные)
        self.z_size_up = Size_Arrow(label='+', position=Vec3(0,0,dist), rotation=Vec3(0,-90,0), color_=color.red, parent=self, on_click=Func(self.size, Vec3(0,0,1)))
        self.z_size_down = Size_Arrow(label='-', position=Vec3(0,0,-dist), rotation=Vec3(0,90,0), color_=color.red, parent=self, on_click=Func(self.size, Vec3(0,0,-1)))

        self.size_dist = 0.5

    def size(self, vec):
        if self.parent:
            # Изменяем размер родительского объекта
            self.parent.scale += (vec * self.size_dist) / 2

if __name__ == "__main__":
    app = Ursina()
    # Тестовый объект
    target = Entity(model='cube', color=color.gray)
    EditorCamera()
    
    # Инициализация системы изменения размера
    Size(parent=target)
    
    app.run()
