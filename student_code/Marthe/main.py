from kivy.app import App
from kivy.clock import Clock
from kivy.core.image import Image
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, ListProperty, NumericProperty
from kivy.properties import AliasProperty
from kivy.core.window import Window, Keyboard
from kivy.uix.image import Image as ImageWidget

import random


class BaseWidget(Widget):
    def load_tileable(self, name):
        t = Image('images/{}.png'.format(name)).texture
        t.wrap = 'repeat'
        setattr(self, 'tx_{}'.format(name), t)


class Background(BaseWidget):
    tx_background = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Background, self).__init__(**kwargs)
        self.load_tileable('background')

    def set_background_size(self, tx):
        tx.uvsize = (self.width / tx.width, -1)

    def on_size(self, *args):
        self.set_background_size(self.tx_background)

    def update(self, nap):
        self.set_background_uv('tx_background', 2 * nap)

    def set_background_uv(self, name, val):
        t = getattr(self, name)
        t.uvpos = ((t.uvpos[0] + val) % self.width, t.uvpos[1])
        self.property(name).dispatch(self)


class Pipe(BaseWidget):
    FLOOR = 112
    PTOP_HEIGHT = 26
    PIPE_GAP = 150

    tx_pipe = ObjectProperty(None)
    tx_ptop = ObjectProperty(None)

    ratio = NumericProperty(0.5)
    lower_len = NumericProperty(0)
    lower_coords = ListProperty((0, 0, 1, 0, 1, 1, 0, 1))
    upper_len = NumericProperty(0)
    upper_coords = ListProperty((0, 0, 1, 0, 1, 1, 0, 1))

    upper_y = AliasProperty(
            lambda self: self.height - self.upper_len,
            None, bind=['height', 'upper_len'])

    def __init__(self, **kwargs):
        super(Pipe, self).__init__(**kwargs)

        for name in ('pipe', 'ptop'):
            self.load_tileable(name)

    def set_coords(self, coords, len):
        len /= 16
        coords[5:] = (len, 0, len)

    def on_size(self, *args):
        pipes_length = self.height - (
                Pipe.FLOOR + Pipe.PIPE_GAP + 2 * Pipe.PTOP_HEIGHT)
        self.lower_len = self.ratio * pipes_length
        self.upper_len = pipes_length - self.lower_len
        self.set_coords(self.lower_coords, self.lower_len)
        self.set_coords(self.upper_coords, self.upper_len)
        self.bind(ratio=self.on_size)

class Fish(ImageWidget):

    def update(self, nap):
        self.MOVELENGTH = 2
        print self
        if (random.randint(1,20) <= 19):
            if (random.randint(1,2) == 1) and (self.y<= 540): #random.randint(1,2) == 1    ||   self.y>= 100
                self.y += self.MOVELENGTH
            else:
                if self.y >= 100:
                    self.y -= self.MOVELENGTH
        else:
            if self.y < 270:
                self.y += self.MOVELENGTH
            else:
                self.y -= self.MOVELENGTH

class Bullets(ImageWidget):

    bullets = []

    def update(self, nap):
        self.x -= 10


class Bird(ImageWidget):

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
#        self.x = touch.x
            self.center = touch.pos

#    ACCEL_FALL = 0 #0.25
#    ACCEL_JUMP = 5

#    speed = NumericProperty(0)
#    angle = AliasProperty(
#            lambda self: 5 * self.speed,
#            None, bind=['speed'])

#    def gravity_on(self, height):

#        self.pos_hint.pop('center_y', None)
#        self.center_y = 0.6 * height

    def update(self, nap):
#        self.speed -= Bird.ACCEL_FALL
#        self.y += self.speed
#        self.y += 5
        pass

#    def bump(self):
#        self.speed = Bird.ACCEL_JUMP


class KivyBirdApp(App):
    pipes = []
    playing = False
    gameover_switch = False
    highscore = 0

    def on_start(self):
        self.spacing = 0.5 * self.root.width
        self.background = self.root.ids.background
        self.score_label = self.root.ids.score_label
        self.bird = self.root.ids.bird
        self.fish = self.root.ids.fish
        self.highscore_label = self.root.ids.highscore_label
        self.bullets = Bullets(source="images/5.png", size=(102,39),
            size_hint=(None, None), pos=self.fish.pos)
        self.gameover_label = self.root.ids.gameover_label
        self.root.add_widget(self.bullets)
        self.highscore_label.text = "Highscore: " + str(self.highscore)
        self.score = 0
        Clock.schedule_interval(self.update, 1.0/500.0)
        Window.bind(on_key_down=self.on_key_down)
#        Window.bind(on_touch_move=Bird.on_touch_move)
        self.background.on_touch_down = self.user_action
#        self.score_label = Label(center_x=self.center_x,
#            top=self.top - 30, text="0")

    def on_key_down(self, window, key, *args):
        if key == Keyboard.keycodes['spacebar']:
            self.user_action()

    def user_action(self, *args):
        self.gameover_switch = True
        if not self.playing:
#            self.bird.gravity_on(self.root.height)
            self.spawn_pipes()
            self.playing = True
#        self.bird.bump()
        self.bird.on_touch_move

    def update(self, nap):
        if self.bullets.x <= -250:
            self.bullets.pos = self.fish.pos
        self.background.update(nap)
        self.gameover_label.text = ""
        if not self.playing:
            if self.gameover_switch == True:
                self.gameover_label.text = "Game Over!"
            else:
                self.gameover_label.text = "Press to play"
            self.score = 0
#            self.score_label.text = "Touch to start"
            return
        self.score_label.text = str(self.score)
        self.fish.update(nap)
        self.bird.update(nap)
        self.bullets.update(nap)

        for p in self.pipes:
            p.x -= 500 * nap #96
            if p.x <= -64:
                self.score += 1
                p.x += 4 * self.spacing
                p.ratio = random.uniform(0.25, 0.75)

        if self.test_game_over():
            if self.score > self.highscore:
                self.highscore = self.score
            self.highscore_label.text = "Highscore: " + str(self.highscore)
            self.playing = False

    def test_game_over(self):

        screen_height = self.root.height

        if self.bird.y < 90 or self.bird.y > screen_height - 50:
            return True

        if self.bullets.collide_widget(self.bird):
            self.bullets.x = -200
            return True

        for p in self.pipes:
            if not p.collide_widget(self.bird):
                continue

            if (self.bird.y < p.lower_len + 116 or
                    self.bird.y > screen_height - (p.upper_len + 75)):
                return True
        return False

    def spawn_pipes(self):
        for p in self.pipes:
            self.root.remove_widget(p)

        self.pipes = []

        for i in range(4):
            p = Pipe(x=self.root.width + (self.spacing * i))
            p.ratio = random.uniform(0.25, 0.75)
            self.root.add_widget(p)
            self.pipes.append(p)


if __name__ == "__main__":
    KivyBirdApp().run()
