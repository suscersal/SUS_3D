from ursina import *
from ursina.prefabs.slider import Slider

class ColorPicker(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=camera.ui)

        self.sliders = {}
        # Теперь используем каналы R, G, B, A
        labels = ('R', 'G', 'B', 'A')
        
        start_y = 0.1
        step_y = 0.05
        
        for i, name in enumerate(labels):
            Text(parent=self, text=name, position=(-0.2, start_y - (i * step_y)), scale=0.7)

            # Все слайдеры теперь от 0 до 255
            s = Slider(
                parent=self,
                min=0, max=255,
                default=255,
                dynamic=True,
                x=-0.14, y=start_y - (i * step_y)-0.01,
                on_value_changed=self._update_color
            )
            
            s.scale = 0.3
            s.knob.scale = 0.02
            s.knob.model = 'circle'
            s.label.text = ""
            
            # Текст значения
            s.val_text = Text(parent=self, text='255', position=(0.05, start_y - (i * step_y)), scale=0.7)
            self.sliders[name.lower()] = s

        # Превью цвета
        self.preview = Entity(
            parent=self, 
            model='quad', 
            scale=(0.2, 0.03), 
            y=0.01, x=0.11,
            color=color.white,
            rotation_z=90
            )

        self.on_value_changed = None
        
        # Применяем внешние параметры до первого обновления
        for key, value in kwargs.items():
            setattr(self, key, value)
            
        self._update_color()

    def _update_color(self):
        # Получаем значения 0-255
        r = self.sliders['r'].value
        g = self.sliders['g'].value
        b = self.sliders['b'].value
        a = self.sliders['a'].value

        # В Ursina color.rgba принимает значения от 0 до 1, 
        # поэтому делим на 255
        self.value = color.rgba(r/255, g/255, b/255, a/255)
        self.preview.color = self.value
        
        # Обновляем текст
        for key in self.sliders:
            self.sliders[key].val_text.text = str(int(self.sliders[key].value))

        # Цвет фона слайдеров для наглядности (чистые цвета каналов)
        self.sliders['r'].bg.color = color.rgba(r/255, 0, 0, 1)
        self.sliders['g'].bg.color = color.rgba(0, g/255, 0, 1)
        self.sliders['b'].bg.color = color.rgba(0, 0, b/255, 1)
        # Для альфы можно оставить серый или сделать градиент
        self.sliders['a'].bg.color = color.black

        if self.on_value_changed:
            self.on_value_changed()
    
    def return_color(self):
        return self.value

if __name__ == '__main__':
    app = Ursina()
    cp = ColorPicker(x=0.5, y=0.2)
    app.run()
