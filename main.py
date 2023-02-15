from kivy.app import App
from kivy.core.image import Texture
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from pipe import Pipe
from kivy.clock import Clock
from random import randint

class Background(Widget):
    clouds_texture = ObjectProperty(None)
    floor_texture = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #create textures
        self.clouds_texture = Image(source = "clouds.png").texture
        self.clouds_texture.wrap = 'repeat'
        self.clouds_texture.uvsize = (Window.width / self.clouds_texture.width, -1)

        self.floor_texture = Image(source = "floor.png").texture
        self.floor_texture.wrap = 'repeat'
        self.floor_texture.uvsize = (Window.width / self.floor_texture.width, -1)

    def scroll_textures(self, time_passed):
        #update the uvpos
        self.clouds_texture.uvpos = ((self.clouds_texture.uvpos[0] + time_passed/6.0)% Window.width , self.clouds_texture.uvpos[1])
        self.floor_texture.uvpos = ((self.floor_texture.uvpos[0] + time_passed)% Window.width , self.floor_texture.uvpos[1])
        #redraw
        texture = self.property('clouds_texture')
        texture.dispatch(self)
        
        texture = self.property('floor_texture')
        texture.dispatch(self)
    pass

class MainApp(App):
    pipes = []

    def on_start(self):
        Clock.schedule_interval(self.root.ids.background.scroll_textures, 1/60.)
    
    def start_game(self):
        num_pipes = 5
        distance_between_pipes = Window.width / (num_pipes - 1)
        for i in range(num_pipes):
            pipe = Pipe()
            pipe.pipe_center = randint(100 + 100, self.root.height - 100)
            pipe.size_hint = (None, None)
            pipe.pos = (Window.width + i * distance_between_pipes, 100)
            pipe.size = (64, self.root.height - 96)
            
            self.pipes.append(pipe)
            self.root.add_widget(pipe)


MainApp().run()