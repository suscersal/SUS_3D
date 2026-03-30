from ursina import *
from ursina.shaders import unlit_shader

class Move_Arrow(Button):
    def __init__(self, model='assets/main/models/vector_arrow.glb', position=Vec3(1,0,0), scale=(0.5,0.1,0.05), rotation=Vec3(0,0,0), color=color.green, parent=None, on_click=None, highlight_color=color.black):
        super().__init__(
            parent=parent,
            model=model,
            position=position,
            scale=scale,
            rotation=rotation,
            color=color,
            on_click=on_click,
            highlight_color=highlight_color,
            shader=unlit_shader
        )

    def input(self, key):
        if key == 'left mouse down':
            if self.hovered:
                self.parent.parent.choices = True
                self.parent.parent.choice = True
                self.parent.parent.tap_arrow = True
                self.parent.parent.start_time = time.time()
    
    def update(self):
        self.world_scale=(0.5,0.1,0.05)

class Move(Empty):
    def __init__(self, parent=scene):
        super().__init__(parent=parent)
        
        self.x_arrow_up = Move_Arrow(
            position=Vec3(1,0,0), rotation=Vec3(0,0,0), color=color.green, 
            parent=parent, on_click=Func(self.move, Vec3(1,0,0)), highlight_color=color.black
        )
        self.x_arrow_down = Move_Arrow(
            position=Vec3(-1,0,0), rotation=Vec3(0,0,-180), color=color.green, 
            parent=parent, on_click=Func(self.move, Vec3(-1,0,0)), highlight_color=color.black
        )

        self.y_arrow_up = Move_Arrow(
            position=Vec3(0,1,0), rotation=Vec3(0,0,-90), color=color.blue, 
            parent=parent, on_click=Func(self.move, Vec3(0,1,0)), highlight_color=color.black
        )
        self.y_arrow_down = Move_Arrow(
            position=Vec3(0,-1,0), rotation=Vec3(0,0,90), color=color.blue, 
            parent=parent, on_click=Func(self.move, Vec3(0,-1,0)), highlight_color=color.black
        )

        self.z_arrow_up = Move_Arrow(
            position=Vec3(0,0,1), rotation=Vec3(0,-90,0), color=color.red, 
            parent=parent, on_click=Func(self.move, Vec3(0,0,1)), highlight_color=color.black
        )
        self.z_arrow_down = Move_Arrow(
            position=Vec3(0,0,-1), rotation=Vec3(0,90,0), color=color.red, 
            parent=parent, on_click=Func(self.move, Vec3(0,0,-1)), highlight_color=color.black
        )

        self.move_dist=0


    def move(self, vec):
        # print('move')
        self.parent.position += vec * self.move_dist