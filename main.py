from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '700')
Config.set('graphics', 'resizable', '0')
Config.set('kivy', 'window_icon', 'images/mascot.jpeg') # <-- English

import copy
import random
import os
import math
from datetime import datetime
from kivy.app import App
from kivy.core.text import LabelBase
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.scrollview import ScrollView
from kivy.uix.carousel import Carousel
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle, RoundedRectangle, Line, StencilPush, StencilUse, StencilUnUse, StencilPop, SmoothLine
from kivy.animation import Animation
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.storage.jsonstore import JsonStore
from kivy.uix.image import Image

try:
    from plyer import notification, vibrator
except ImportError:
    notification = None
    vibrator = None

BG_COLOR = '#121212'
ACCENT_COLOR = '#FFD54F'
TEXT_COLOR = '#FAFAFA'
SUBTEXT_COLOR = '#9E9E9E'
CARD_BG = '#1E1E1E' 
STOP_COLOR = '#EF5350'
DISABLED_COLOR = '#424242'
SEPARATOR_COLOR = '#333333'
BLACK_BG = '#000000'

Window.clearcolor = get_color_from_hex(BG_COLOR)

DEFAULT_DATA = {
    'quail': {'default': [140, 180, 260]},
    'chicken': {
        'C3': [190, 250, 480],
        'C2': [220, 280, 520],
        'C1': [250, 310, 570],
        'C0': [270, 340, 620],
        'CB': [300, 370, 660]
    }
}
current_times = copy.deepcopy(DEFAULT_DATA)

# === ОБНОВЛЕННЫЕ ПУТИ К КАРТИНКАМ (ENGLISH) ===
EGG_PERSONAS = [
    {"name": "Сырое яйцо-интроверт", "desc": "Ты еще только прогреваешься.\nНе спеши, главное — не треснуть.", "img": "images/introvert.png"},
    {"name": "Всмятку яйцо-мечтатель", "desc": "Снаружи собрана,\nвнутри — лава идей.\nВажно не перевариться.", "img": "images/dreamer.jpeg"},
    {"name": "Подсоленное яйцо", "desc": "Ты сегодня в балансе:\nчуть сарказма,\nчуть заботы —\nидеальный вкус.", "img": "images/salted.jpeg"},
    {"name": "Золотое яйцо", "desc": "Тебя мало, но ты ценный.\nБереги энергию\nи выбирай, куда вариться.", "img": "images/golden.jpeg"},
    {"name": "Шоколадное яйцо", "desc": "Сладкое снаружи,\nс сюрпризом внутри.\nТебя варить не надо —\nты и так подарок.", "img": "images/chocolate.jpeg"},
    {"name": "Пасхальное яйцо", "desc": "Яркая натура, душа компании.\nТы слишком красив,\nчтобы тебя просто так съесть.", "img": "images/easter.jpeg"},
    {"name": "Яйцо Фаберже", "desc": "Шедевр искусства.\nТрогать можно только взглядом,\nа работать — по настроению.", "img": "images/faberge.jpeg"},
    {"name": "Крутое яйцо", "desc": "Ты — кремень.\nЖизнь тебя кипятила,\nно ты стал только крепче.", "img": "images/cool.jpeg"},
    {"name": "Драконье яйцо", "desc": "Внутри дремлет пламя.\nНе буди зверя,\nпока он сам не решит вылупиться.", "img": "images/dragon.jpeg"},
    {"name": "Цыпленок", "desc": "Кажется, ты перележал.\nПора вылупляться!", "img": "images/chick.jpeg"}
]

store = JsonStore('egg_data.json')

class RoundedButton(ButtonBehavior, Label):
    bg_color = ListProperty(get_color_from_hex(ACCENT_COLOR))
    radius = ListProperty([dp(15)])
    glare_alpha = NumericProperty(0) 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bold = True
        self.bind(pos=self.update_canvas, size=self.update_canvas, bg_color=self.update_canvas, glare_alpha=self.update_canvas)
        self.update_canvas()
    def update_canvas(self, *args):
        self.canvas.before.clear()
        self.canvas.after.clear()
        with self.canvas.before:
            Color(*self.bg_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)
        with self.canvas.after:
            Color(1, 1, 1, self.glare_alpha)
            RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)
    def on_press(self): Animation(glare_alpha=0.3, duration=0.1).start(self)
    def on_release(self): Animation(glare_alpha=0, duration=0.2).start(self)

class SettingsRow(ButtonBehavior, BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None   
        self.height = dp(60)
        self.padding = [dp(15), 0]
        self.spacing = dp(10)

class YellowSwitch(ButtonBehavior, Widget):
    active = BooleanProperty(False)
    anim_progress = NumericProperty(0)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(50), dp(28))
        self.bind(pos=self.update_canvas, size=self.update_canvas, anim_progress=self.update_canvas)
        self.update_canvas()
    def on_active(self, instance, value):
        target = 1.0 if value else 0.0
        Animation(anim_progress=target, duration=0.2, t='out_quad').start(self)
    def update_canvas(self, *args):
        self.canvas.clear()
        disabled_col = get_color_from_hex(DISABLED_COLOR)
        active_col = get_color_from_hex(ACCENT_COLOR)
        r = disabled_col[0] + (active_col[0] - disabled_col[0]) * self.anim_progress
        g = disabled_col[1] + (active_col[1] - disabled_col[1]) * self.anim_progress
        b = disabled_col[2] + (active_col[2] - disabled_col[2]) * self.anim_progress
        with self.canvas:
            Color(r, g, b, 1 if self.anim_progress == 0 else 0.5) 
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(14)])
            Color(1, 1, 1, 1)
            padding = dp(2)
            knob_size = self.height - padding * 2
            start_x = self.x + padding
            end_x = self.x + self.width - knob_size - padding
            current_x = start_x + (end_x - start_x) * self.anim_progress
            Ellipse(pos=(current_x, self.y + padding), size=(knob_size, knob_size))
    def on_press(self): self.active = not self.active

class ResetButton(ButtonBehavior, Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, 1)
        self.width = dp(50)
        self.source = 'images/PhArrowCounterClockwiseBold.png'
        self._img = Image(source=self.source, keep_ratio=True, allow_stretch=True)
        self._img.reload()
        self.bind(pos=self.update_canvas, size=self.update_canvas)
    def update_canvas(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        d = dp(36)
        with self.canvas:
            StencilPush()
            Ellipse(pos=(cx - d/2, cy - d/2), size=(d, d))
            StencilUse()
            Color(1, 1, 1, 1)
            if self._img.texture:
                Rectangle(texture=self._img.texture, pos=(cx - d/2, cy - d/2), size=(d, d))
            StencilUnUse()
            Ellipse(pos=(cx - d/2, cy - d/2), size=(d, d))
            StencilPop()

class BurgerButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0,0,0,0)
        self.background_normal = ''
        with self.canvas.after:
            Color(*get_color_from_hex(ACCENT_COLOR))
            self.lines = [Line(width=dp(2)), Line(width=dp(2)), Line(width=dp(2))]
        self.bind(pos=self.update_canvas, size=self.update_canvas)
    def update_canvas(self, *args):
        cx, cy = self.center_x, self.center_y
        w = dp(22)
        offset = dp(6)
        self.lines[0].points = [cx - w/2, cy + offset, cx + w/2, cy + offset]
        self.lines[1].points = [cx - w/2, cy, cx + w/2, cy]
        self.lines[2].points = [cx - w/2, cy - offset, cx + w/2, cy - offset]

class CircularAvatar(ButtonBehavior, Widget):
    source = StringProperty('')
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(40), dp(40))
        self._img = Image(size_hint=(1,1), pos_hint={'center_x':0.5, 'center_y':0.5})
        self.bind(source=self._update_src)
        self.bind(pos=self.update_canvas, size=self.update_canvas)
    def _update_src(self, instance, value):
        self._img.source = value
        self._img.reload()
        self.update_canvas()
    def update_canvas(self, *args):
        self.canvas.clear()
        if not self.source:
            with self.canvas:
                Color(*get_color_from_hex(ACCENT_COLOR))
                Line(circle=(self.center_x, self.center_y, self.width/2), width=dp(1.5))
            return
        with self.canvas:
            StencilPush()
            Ellipse(pos=self.pos, size=self.size)
            StencilUse()
            Color(1, 1, 1, 1)
            if self._img.texture:
                Rectangle(texture=self._img.texture, pos=self.pos, size=self.size)
            StencilUnUse()
            Ellipse(pos=self.pos, size=self.size)
            StencilPop()
            Color(*get_color_from_hex(ACCENT_COLOR))
            Line(circle=(self.center_x, self.center_y, self.width/2), width=dp(1.5))

class Firework(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.particles = []
        with self.canvas:
            for _ in range(30):
                color = random.choice([ACCENT_COLOR, '#FF5722', '#03A9F4', '#8BC34A', '#E91E63'])
                Color(*get_color_from_hex(color))
                size = random.randint(int(dp(6)), int(dp(14)))
                p = Ellipse(pos=self.center, size=(size, size))
                self.particles.append(p)
        self.start_explosion()
    def start_explosion(self):
        for p in self.particles:
            anim = Animation(
                pos=(self.center_x + random.randint(int(dp(-180)), int(dp(180))), 
                     self.center_y + random.randint(int(dp(-180)), int(dp(180)))), 
                size=(0, 0), duration=1.5, t='out_expo')
            anim.start(p)
        Clock.schedule_once(self.remove_self, 1.6)
    def remove_self(self, dt):
        if self.parent: self.parent.remove_widget(self)

class SmoothModeButton(ToggleButton):
    bg_rgba = ListProperty(get_color_from_hex(CARD_BG)) 
    glare_alpha = NumericProperty(0)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0,0,0,0) 
        self.bg_rgba = get_color_from_hex(CARD_BG)
        self.color = (1, 1, 1, 1) 
    def animate_to_state(self, is_active):
        if is_active:
            target_color = get_color_from_hex(ACCENT_COLOR)
            self.color = (0, 0, 0, 1)
        else:
            target_color = get_color_from_hex(CARD_BG)
            self.color = (1, 1, 1, 1)
        Animation(bg_rgba=target_color, duration=0.2).start(self)
    def on_bg_rgba(self, instance, value): self.update_canvas()
    def on_glare_alpha(self, instance, value): self.update_canvas()
    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg_rgba)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
            Color(1, 1, 1, self.glare_alpha)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
    def on_press(self): Animation(glare_alpha=0.3, duration=0.1).start(self)
    def on_release(self): Animation(glare_alpha=0, duration=0.2).start(self)
    def on_size(self, *args): self.update_canvas()
    def on_pos(self, *args): self.update_canvas()

class TimeSettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation='vertical')
        header = BoxLayout(size_hint=(1, None), height=dp(60), padding=[dp(10), 0], spacing=dp(10))
        with header.canvas.before:
            Color(*get_color_from_hex(BG_COLOR))
            self.header_bg = Rectangle(pos=header.pos, size=header.size)
        header.bind(pos=lambda i,v: setattr(self.header_bg, 'pos', i.pos),
                    size=lambda i,v: setattr(self.header_bg, 'size', i.size))
        
        btn_back = Button(text="<", font_size=sp(24), size_hint=(None, 1), width=dp(50),
                          background_color=(0,0,0,0), color=get_color_from_hex(TEXT_COLOR))
        btn_back.bind(on_press=self.go_back)
        
        title = Label(text="Время приготовления", font_size=sp(20), bold=True,
                      color=get_color_from_hex(TEXT_COLOR), halign='left', valign='middle')
        title.bind(size=title.setter('text_size'))
        
        btn_reset = ResetButton()
        btn_reset.bind(on_press=self.confirm_reset)
        
        header.add_widget(btn_back)
        header.add_widget(title)
        header.add_widget(btn_reset)
        self.scroll = ScrollView(size_hint=(1, 1))
        self.cards_container = GridLayout(cols=1, spacing=dp(20), size_hint_y=None, padding=[dp(15), dp(10), dp(15), dp(20)])
        self.cards_container.bind(minimum_height=self.cards_container.setter('height'))
        self.scroll.add_widget(self.cards_container)
        root.add_widget(header)
        root.add_widget(self.scroll)
        self.add_widget(root)
        
    def on_pre_enter(self, *args): self.build_cards()
    def build_cards(self):
        self.cards_container.clear_widgets()
        order = [('chicken', 'C3'), ('chicken', 'C2'), ('chicken', 'C1'), 
                 ('chicken', 'C0'), ('chicken', 'CB'), ('quail', 'default')]
        for species, size_key in order: self._add_card(species, size_key)
    def _add_card(self, species, size_key):
        total_h = dp(235)
        card = GridLayout(cols=1, size_hint_y=None, height=total_h, spacing=0)
        with card.canvas.before:
            Color(*get_color_from_hex(CARD_BG))
            bg_rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(12)])
        def update_bg(instance, value, r=bg_rect):
            r.pos = instance.pos
            r.size = instance.size
        card.bind(pos=update_bg, size=update_bg)
        display_name = f"{size_key}-размер" if species == 'chicken' else "Перепелиное"
        header_box = BoxLayout(size_hint_y=None, height=dp(50), padding=[dp(15), 0])
        lbl = Label(text=display_name, color=get_color_from_hex(ACCENT_COLOR), 
                    bold=True, font_size=sp(16), halign='left', valign='middle')
        lbl.bind(size=lbl.setter('text_size'))
        header_box.add_widget(lbl)
        card.add_widget(header_box)
        sep = Widget(size_hint_y=None, height=dp(1))
        with sep.canvas:
            Color(*get_color_from_hex(SEPARATOR_COLOR))
            Rectangle(pos=sep.pos, size=sep.size)
        def update_sep(inst, v, s=sep):
            s.canvas.clear()
            with s.canvas:
                Color(*get_color_from_hex(SEPARATOR_COLOR))
                Rectangle(pos=inst.pos, size=inst.size)
        sep.bind(pos=update_sep, size=update_sep)
        card.add_widget(sep)
        times = current_times[species][size_key]
        modes = ["всмятку", "в мешочек", "вкрутую"]
        for i, mode_name in enumerate(modes):
            row = SettingsRow()
            row.bind(on_press=lambda x, sp=species, sk=size_key, idx=i: self.open_edit_popup(sp, sk, idx))
            text_box = BoxLayout(orientation='vertical', spacing=0, padding=[0, dp(12)])
            l1 = Label(text=mode_name, font_size=sp(16), color=get_color_from_hex(TEXT_COLOR),
                       halign='left', valign='middle', size_hint=(1, 0.6))
            l1.bind(size=l1.setter('text_size'))
            m, s = divmod(times[i], 60)
            l2 = Label(text=f"{m:02}:{s:02}", font_size=sp(13), color=get_color_from_hex(SUBTEXT_COLOR),
                       halign='left', valign='middle', size_hint=(1, 0.4))
            l2.bind(size=l2.setter('text_size'))
            text_box.add_widget(l1)
            text_box.add_widget(l2)
            arrow = Label(text=">", font_size=sp(18), color=get_color_from_hex(SUBTEXT_COLOR),
                          size_hint=(None, 1), width=dp(30))
            row.add_widget(text_box)
            row.add_widget(arrow)
            card.add_widget(row)
            if i < len(modes) - 1:
                s_line = Widget(size_hint_y=None, height=dp(1))
                with s_line.canvas:
                    Color(*get_color_from_hex(SEPARATOR_COLOR))
                    Rectangle(pos=s_line.pos, size=s_line.size)
                def upd_s(inst, val, w=s_line):
                    w.canvas.clear()
                    with w.canvas:
                        Color(*get_color_from_hex(SEPARATOR_COLOR))
                        Rectangle(pos=inst.pos, size=inst.size)
                s_line.bind(pos=upd_s, size=upd_s)
                card.add_widget(s_line)
        self.cards_container.add_widget(card)
        
    def open_edit_popup(self, species, size_key, mode_idx):
        current_sec = current_times[species][size_key][mode_idx]
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        controls = BoxLayout(spacing=dp(20), size_hint=(1, None), height=dp(100))
        lbl_val = Label(text=f"{current_sec}", font_size=sp(40), bold=True, color=get_color_from_hex(ACCENT_COLOR))
        def change_time(delta):
            new_val = int(lbl_val.text) + delta
            if new_val < 10: new_val = 10
            lbl_val.text = str(new_val)
        btn_minus = RoundedButton(text="- 10s", on_press=lambda x: change_time(-10), bg_color=get_color_from_hex('#333333'), color=(1,1,1,1))
        btn_plus = RoundedButton(text="+ 10s", on_press=lambda x: change_time(10), bg_color=get_color_from_hex('#333333'), color=(1,1,1,1))
        controls.add_widget(btn_minus)
        controls.add_widget(lbl_val)
        controls.add_widget(btn_plus)
        btn_save = RoundedButton(text="СОХРАНИТЬ", size_hint=(1, None), height=dp(50),
                          bg_color=get_color_from_hex(ACCENT_COLOR), color=(0,0,0,1))
        popup = Popup(title='Изменить время (сек)', content=content, size_hint=(0.8, 0.4), 
                      separator_color=get_color_from_hex(ACCENT_COLOR))
        def save_and_close(instance):
            current_times[species][size_key][mode_idx] = int(lbl_val.text)
            self.build_cards()
            popup.dismiss()
            if App.get_running_app().root:
                main = App.get_running_app().root.get_screen('main')
                if main: main.recalc_time()
        btn_save.bind(on_press=save_and_close)
        content.add_widget(controls)
        content.add_widget(btn_save)
        popup.open()
        
    def confirm_reset(self, instance):
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        lbl = Label(text="Сбросить все настройки?", halign='center', font_size=sp(16))
        btns = BoxLayout(spacing=dp(20), size_hint=(1, None), height=dp(50))
        btn_no = Button(text="ОТМЕНА", background_color=(0,0,0,0), color=get_color_from_hex(ACCENT_COLOR))
        btn_yes = Button(text="СБРОСИТЬ", background_color=(0,0,0,0), color=get_color_from_hex(ACCENT_COLOR), bold=True)
        popup = Popup(title='', content=content, size_hint=(0.85, 0.3), separator_height=0, 
                      background_color=get_color_from_hex('#222222'))
        def do_reset(x):
            global current_times
            current_times = copy.deepcopy(DEFAULT_DATA)
            self.build_cards()
            if App.get_running_app().root:
                main = App.get_running_app().root.get_screen('main')
                if main: main.recalc_time()
            popup.dismiss()
        btn_no.bind(on_press=popup.dismiss)
        btn_yes.bind(on_press=do_reset)
        btns.add_widget(btn_no)
        btns.add_widget(btn_yes)
        content.add_widget(lbl)
        content.add_widget(btns)
        popup.open()
        
    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'main'

class SideMenu(FloatLayout):
    x_pos = NumericProperty(-dp(300))
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu_width = dp(280)
        self.bg = Widget(pos_hint={'x':0, 'y':0}, size_hint=(None, None), size=(0,0))
        with self.bg.canvas:
            self.bg_color = Color(0, 0, 0, 0)
            self.bg_rect = Rectangle(pos=self.bg.pos, size=self.bg.size)
        self.bg.bind(pos=self.update_bg_rect, size=self.update_bg_rect)
        self.add_widget(self.bg)
        self.panel = BoxLayout(orientation='vertical', size_hint=(None, 1), width=self.menu_width, 
                              x=self.x_pos, padding=dp(20), spacing=dp(10))
        with self.panel.canvas.before:
            Color(*get_color_from_hex(CARD_BG))
            self.rect = Rectangle(pos=self.panel.pos, size=self.panel.size)
        self.panel.bind(pos=lambda inst, val: setattr(self.rect, 'pos', inst.pos), 
                       size=lambda inst, val: setattr(self.rect, 'size', inst.size))
        header = Label(text="Яичко-тян\nТаймер варки", font_size=sp(22), bold=True,
                       color=get_color_from_hex(ACCENT_COLOR), size_hint=(1, 0.2), halign='left')
        header.bind(size=header.setter('text_size'))
        
        btn_persona = Button(text="Какое яйцо ты сегодня?", size_hint=(1, None), height=dp(50),
                             background_normal='', background_color=(0,0,0,0), 
                             color=get_color_from_hex(TEXT_COLOR), halign='left', font_size=sp(16))
        btn_persona.bind(size=btn_persona.setter('text_size'))
        btn_persona.bind(on_press=self.open_persona_direct)
        
        btn_settings = Button(text="Время приготовления", size_hint=(1, None), height=dp(50),
                              background_normal='', background_color=(0,0,0,0), 
                              color=get_color_from_hex(TEXT_COLOR), halign='left', font_size=sp(16))
        btn_settings.bind(size=btn_settings.setter('text_size'))
        btn_settings.bind(on_press=self.go_to_settings)
        
        btn_instr = Button(text="Инструкция", size_hint=(1, None), height=dp(50),
                           background_normal='', background_color=(0,0,0,0), 
                           color=get_color_from_hex(TEXT_COLOR), halign='left', font_size=sp(16))
        btn_instr.bind(size=btn_instr.setter('text_size'))
        btn_instr.bind(on_press=self.open_instr_direct)
        
        self.panel.add_widget(header)
        self.panel.add_widget(btn_persona)
        self.panel.add_widget(btn_settings)
        self.panel.add_widget(btn_instr)
        self.panel.add_widget(Widget())
        self.add_widget(self.panel)
        self.bind(x_pos=self.update_pos)
        
    def open_persona_direct(self, instance):
        self.close_menu()
        App.get_running_app().root.get_screen('main').open_daily_egg()
    def open_instr_direct(self, instance):
        self.close_menu()
        App.get_running_app().root.get_screen('main').show_instruction()
    def update_bg_rect(self, *args):
        self.bg_rect.pos = self.bg.pos
        self.bg_rect.size = self.bg.size
    def update_pos(self, *args): self.panel.x = self.x_pos
    def on_touch_down(self, touch):
        if self.x_pos > -self.menu_width + dp(10):
            if self.bg.collide_point(*touch.pos) and not self.panel.collide_point(*touch.pos):
                self.close_menu()
                return True
        return super().on_touch_down(touch)
    def go_to_settings(self, instance):
        self.close_menu()
        app = App.get_running_app()
        app.root.transition = SlideTransition(direction="left")
        app.root.current = 'settings'
    def open_menu(self):
        self.bg.size_hint = (1, 1)
        Animation(a=0.6, duration=0.2).start(self.bg_color)
        Animation(x_pos=0, duration=0.3, t='out_cubic').start(self)
    def close_menu(self, *args):
        Animation(a=0, duration=0.2).start(self.bg_color)
        anim = Animation(x_pos=-self.menu_width, duration=0.3, t='in_cubic')
        anim.bind(on_complete=lambda x,y: setattr(self.bg, 'size_hint', (None, None)))
        anim.start(self)

class BottomSheet(FloatLayout):
    sheet_y = NumericProperty(0)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.HIDDEN_Y = dp(-440)
        self.OPEN_Y = 0
        self.sheet_y = self.HIDDEN_Y
        self.overlay = Button(background_color=(0,0,0,0), size_hint=(None, None), size=(0,0), pos_hint={'x':0, 'y':0})
        self.overlay.bind(on_press=self.check_close_touch)
        self.add_widget(self.overlay)
        self.sheet_container = BoxLayout(orientation='vertical', size_hint=(1, None), height=dp(500),
                                        padding=dp(15), spacing=dp(12))
        with self.sheet_container.canvas.before:
            Color(*get_color_from_hex(CARD_BG))
            self.bg_rect = RoundedRectangle(pos=self.sheet_container.pos, size=self.sheet_container.size, 
                                            radius=[dp(25), dp(25), 0, 0])
        self.sheet_container.bind(pos=lambda inst, val: setattr(self.bg_rect, 'pos', inst.pos), 
                                 size=lambda inst, val: setattr(self.bg_rect, 'size', inst.size))
        swipe_area = BoxLayout(orientation='vertical', size_hint=(1, None), height=dp(60))
        hint = Label(text="Смахните для настройки", font_size=sp(14),
                     color=get_color_from_hex(SUBTEXT_COLOR), size_hint=(1, 0.6))
        
        self.mini_timer_label = Label(text="04:00", font_size=sp(18), color=get_color_from_hex(ACCENT_COLOR),
                                      size_hint=(1, 0.4), bold=True, opacity=0)
        swipe_area.add_widget(hint)
        swipe_area.add_widget(self.mini_timer_label)
        
        scroll = ScrollView(size_hint=(1, 1))
        settings_content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(20), padding=[0, dp(10)])
        settings_content.bind(minimum_height=settings_content.setter('height'))
        cool_box = BoxLayout(size_hint=(1, None), height=dp(40), padding=[0, 0, dp(20), 0])
        cool_label = Label(text="Охлаждённый", halign='left', color=get_color_from_hex(TEXT_COLOR), 
                           size_hint_x=0.7, text_size=(dp(200), None))
        cool_box.add_widget(cool_label)
        switch_container = AnchorLayout(anchor_x='right', anchor_y='center', size_hint_x=0.3)
        self.cooling_switch = YellowSwitch()
        switch_container.add_widget(self.cooling_switch)
        cool_box.add_widget(switch_container)
        settings_content.add_widget(cool_box)
        settings_content.add_widget(self.make_section("Тип яйца"))
        type_btns = BoxLayout(size_hint=(1, None), height=dp(45), spacing=dp(10))
        self.btn_chicken = RoundedButton(text="Куриное", bg_color=get_color_from_hex(ACCENT_COLOR), color=(0,0,0,1))
        self.btn_quail = RoundedButton(text="Перепелиное", bg_color=get_color_from_hex(DISABLED_COLOR), color=(1,1,1,1))
        type_btns.add_widget(self.btn_chicken)
        type_btns.add_widget(self.btn_quail)
        settings_content.add_widget(type_btns)
        settings_content.add_widget(self.make_section("Размер"))
        size_btns = BoxLayout(size_hint=(1, None), height=dp(45), spacing=dp(10))
        self.size_btns = {}
        for name in ['C3', 'C2', 'C1', 'C0', 'CB']:
            btn = RoundedButton(text=name, 
                          bg_color=get_color_from_hex(ACCENT_COLOR if name == 'C1' else DISABLED_COLOR), 
                          color=(0,0,0,1) if name == 'C1' else (1,1,1,1))
            self.size_btns[name] = btn
            size_btns.add_widget(btn)
        settings_content.add_widget(size_btns)
        settings_content.add_widget(self.make_section("Количество яиц"))
        count_box = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(20))
        self.btn_minus = RoundedButton(text="-", size_hint=(None, 1), width=dp(60),
                                      bg_color=get_color_from_hex(DISABLED_COLOR))
        self.lbl_count = Label(text="1", font_size=sp(20), bold=True, color=get_color_from_hex(TEXT_COLOR))
        self.btn_plus = RoundedButton(text="+", size_hint=(None, 1), width=dp(60),
                                      bg_color=get_color_from_hex(DISABLED_COLOR))
        count_box.add_widget(Widget())
        count_box.add_widget(self.btn_minus)
        count_box.add_widget(self.lbl_count)
        count_box.add_widget(self.btn_plus)
        count_box.add_widget(Widget())
        settings_content.add_widget(count_box)
        scroll.add_widget(settings_content)
        self.sheet_container.add_widget(swipe_area)
        self.sheet_container.add_widget(scroll)
        self.add_widget(self.sheet_container)
        self.bind(sheet_y=self.update_sheet_pos)
        self.update_sheet_pos()
        swipe_area.bind(on_touch_down=self.on_touch_down_handle)
        swipe_area.bind(on_touch_move=self.on_touch_move_handle)
        swipe_area.bind(on_touch_up=self.on_touch_up_handle)
        
    def check_close_touch(self, instance):
        if self.sheet_y > self.HIDDEN_Y + dp(100):
            self.close_sheet()
    def make_section(self, title):
        lbl = Label(text=title, size_hint=(1, None), height=dp(30), font_size=sp(14), bold=True,
                    color=get_color_from_hex(TEXT_COLOR), halign='left')
        lbl.bind(size=lbl.setter('text_size'))
        return lbl
    def update_sheet_pos(self, *args): 
        self.sheet_container.pos = (0, self.sheet_y)
        dist_from_bottom = self.sheet_y - self.HIDDEN_Y
        if dist_from_bottom < dp(20):
            self.mini_timer_label.opacity = 0
        elif dist_from_bottom > dp(150):
            self.mini_timer_label.opacity = 1
        else:
            self.mini_timer_label.opacity = (dist_from_bottom - dp(20)) / dp(130)

        if self.sheet_y > self.HIDDEN_Y + dp(50):
            self.overlay.size_hint = (1, 1)
        else:
            self.overlay.size_hint = (None, None)
            self.overlay.size = (0, 0)
            
    def on_touch_down_handle(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.touch_start_y = touch.y
            self.initial_sheet_y = self.sheet_y
            touch.grab(self)
            return True
    def on_touch_move_handle(self, instance, touch):
        if touch.grab_current is self:
            self.sheet_y = max(self.HIDDEN_Y, min(self.OPEN_Y, self.initial_sheet_y + (touch.y - self.touch_start_y)))
            app = App.get_running_app()
            if app and app.root and app.root.get_screen('main'):
                progress = (self.sheet_y - self.HIDDEN_Y) / abs(self.HIDDEN_Y)
                offset = progress * dp(420)
                app.root.get_screen('main').move_content(offset)
                app.root.get_screen('main').update_opacity_on_swipe(progress)
            return True
    def on_touch_up_handle(self, instance, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            self.open_sheet() if self.sheet_y > (self.HIDDEN_Y + self.OPEN_Y) / 2 else self.close_sheet()
            return True
    def open_sheet(self):
        anim = Animation(sheet_y=self.OPEN_Y, duration=0.3, t='out_cubic')
        anim.start(self)
        App.get_running_app().root.get_screen('main').animate_content_up()
    def close_sheet(self):
        anim = Animation(sheet_y=self.HIDDEN_Y, duration=0.3, t='out_cubic')
        anim.start(self)
        App.get_running_app().root.get_screen('main').animate_content_down()

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timer_event = None
        self.current_mode_idx = 0
        self.time_left = 0
        self.is_running = False
        self.is_finished = False
        self.egg_type, self.egg_size, self.is_cooled = 'chicken', 'C1', False
        self.egg_count = 1
        self.timer_label = Label(text="04:00", font_size=sp(70), bold=True, color=get_color_from_hex(TEXT_COLOR))
        
        self.mode_buttons = []
        for i, name in enumerate(["Всмятку", "В мешочек", "Вкрутую"]):
            btn = SmoothModeButton(text=name, group='mode', font_size=sp(13))
            if i == 0:
                btn.bg_rgba = get_color_from_hex(ACCENT_COLOR)
                btn.color = (0,0,0,1)
            else:
                btn.bg_rgba = get_color_from_hex(CARD_BG)
                btn.color = (1,1,1,1)
            btn.bind(on_press=lambda x, idx=i: self.on_mode_change_click(idx))
            self.mode_buttons.append(btn)

        self.carousel = Carousel(direction='right', loop=True, size_hint=(1, 1))
        self.carousel.bind(current_slide=self.on_slide_change)
        
        # === ENGLISH PATHS HERE TOO ===
        mode_images = ['images/soft.png', 'images/bag.png', 'images/hard.png']
        for img_name in mode_images:
            slide = AnchorLayout(anchor_x='center', anchor_y='center')
            egg_img = Image(source=img_name, size_hint=(None, None), size=(dp(180), dp(220)))
            slide.add_widget(egg_img)
            self.carousel.add_widget(slide)
        
        self.root_layout = FloatLayout()
        
        self.content_layout = BoxLayout(orientation='vertical', padding=[0, dp(10), 0, 0], spacing=dp(10), pos_hint={'x': 0, 'top': 1})
        
        top_bar = BoxLayout(size_hint=(1, None), height=dp(60), padding=[dp(15), 0])
        menu_container = AnchorLayout(anchor_x='left', anchor_y='center', size_hint=(None, 1), width=dp(60))
        menu_btn = BurgerButton(size_hint=(None, 1), width=dp(50))
        menu_btn.bind(on_press=self.open_side_menu)
        menu_container.add_widget(menu_btn)
        title_label = Label(text="Яичко-тян", font_size=sp(18), bold=True, color=get_color_from_hex(ACCENT_COLOR))
        persona_container = AnchorLayout(anchor_x='right', anchor_y='center', size_hint=(None, 1), width=dp(60))
        self.persona_btn = CircularAvatar()
        self.persona_btn.bind(on_press=self.open_daily_egg_direct)
        persona_container.add_widget(self.persona_btn)
        self.update_corner_icon()
        top_bar.add_widget(menu_container)
        top_bar.add_widget(title_label)
        top_bar.add_widget(persona_container)
        
        modes_bar = BoxLayout(size_hint=(1, None), height=dp(60), padding=[dp(20), dp(10)], spacing=dp(15))
        for btn in self.mode_buttons: modes_bar.add_widget(btn)
        
        self.timer_box = BoxLayout(size_hint=(1, None), height=dp(120))
        self.timer_box.add_widget(self.timer_label)

        btn_container = BoxLayout(size_hint=(1, None), height=dp(80), padding=[dp(50), dp(10)])
        self.action_btn = RoundedButton(text="СТАРТ", bg_color=get_color_from_hex(ACCENT_COLOR), 
                                     color=(0,0,0,1), font_size=sp(22), bold=True,
                                     size_hint=(1, None), height=dp(60))
        self.action_btn.bind(on_press=self.toggle_timer)
        btn_container.add_widget(self.action_btn)
        
        spacer_for_sheet = Widget(size_hint=(1, None), height=dp(60))

        self.content_layout.add_widget(top_bar)
        self.content_layout.add_widget(modes_bar)
        self.content_layout.add_widget(self.carousel) 
        self.content_layout.add_widget(self.timer_box)
        self.content_layout.add_widget(btn_container)
        self.content_layout.add_widget(spacer_for_sheet)
        
        self.root_layout.add_widget(self.content_layout)

        self.bottom_sheet = BottomSheet(size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        self.root_layout.add_widget(self.bottom_sheet)
        
        self.side_menu = SideMenu(size_hint=(1, 1))
        self.root_layout.add_widget(self.side_menu)
        
        self.bottom_sheet.btn_chicken.bind(on_press=lambda x: self.change_egg_type('chicken'))
        self.bottom_sheet.btn_quail.bind(on_press=lambda x: self.change_egg_type('quail'))
        for name, btn in self.bottom_sheet.size_btns.items(): 
            btn.bind(on_press=lambda x, n=name: self.change_size(n))
        self.bottom_sheet.cooling_switch.bind(active=self.on_cooling_change)
        self.bottom_sheet.btn_minus.bind(on_press=lambda x: self.change_count(-1))
        self.bottom_sheet.btn_plus.bind(on_press=lambda x: self.change_count(1))
        
        self.add_widget(self.root_layout)
        self.recalc_time()

    def on_pause(self):
        if self.is_running and notification:
             try: notification.notify(title='Яичко-тян', message='Таймер запущен. Я сообщу, когда яйца будут готовы!', timeout=10)
             except: pass
        return True
    def on_resume(self): pass
    def open_daily_egg_direct(self, instance): self.open_daily_egg()
    def update_opacity_on_swipe(self, progress):
        alpha = 1.0 - (progress * 3.0)
        if alpha < 0: alpha = 0
        self.action_btn.opacity = alpha
        self.carousel.opacity = 1.0 - progress
    def animate_content_up(self): 
        Animation(y=dp(420), duration=0.3, t='out_cubic').start(self.content_layout)
        Animation(opacity=0, duration=0.1).start(self.action_btn)
        Animation(opacity=0, duration=0.2).start(self.carousel)
    def animate_content_down(self): 
        Animation(y=0, duration=0.3, t='out_cubic').start(self.content_layout)
        Animation(opacity=1, duration=0.3).start(self.action_btn)
        Animation(opacity=1, duration=0.3).start(self.carousel)
    def move_content(self, offset): self.content_layout.y = offset
    def open_side_menu(self, instance): self.side_menu.open_menu()
    def on_slide_change(self, carousel, slide):
        idx = carousel.index
        self.current_mode_idx = idx
        self.animate_mode_buttons(idx)
        self.recalc_time()
    def on_mode_change_click(self, idx):
        self.carousel.load_slide(self.carousel.slides[idx])
    def animate_mode_buttons(self, active_idx):
        for i, btn in enumerate(self.mode_buttons):
            if i == active_idx: btn.animate_to_state(True)
            else: btn.animate_to_state(False)
    def change_egg_type(self, etype):
        self.egg_type = etype
        self.bottom_sheet.btn_chicken.bg_color = get_color_from_hex(ACCENT_COLOR if etype=='chicken' else DISABLED_COLOR)
        self.bottom_sheet.btn_chicken.color = (0,0,0,1) if etype=='chicken' else (1,1,1,1)
        self.bottom_sheet.btn_quail.bg_color = get_color_from_hex(ACCENT_COLOR if etype=='quail' else DISABLED_COLOR)
        self.bottom_sheet.btn_quail.color = (0,0,0,1) if etype=='quail' else (1,1,1,1)
        for name, btn in self.bottom_sheet.size_btns.items():
            if etype == 'quail':
                btn.disabled = True
                btn.bg_color = get_color_from_hex(DISABLED_COLOR)
                btn.opacity = 0.5
            else:
                btn.disabled = False
                btn.opacity = 1
                btn.bg_color = get_color_from_hex(ACCENT_COLOR if name == self.egg_size else DISABLED_COLOR)
                btn.color = (0,0,0,1) if name == self.egg_size else (1,1,1,1)
        self.recalc_time()
    def change_size(self, size_name):
        if self.egg_type == 'quail': return
        self.egg_size = size_name
        for name, btn in self.bottom_sheet.size_btns.items():
            btn.bg_color = get_color_from_hex(ACCENT_COLOR if name == size_name else DISABLED_COLOR)
            btn.color = (0,0,0,1) if name == size_name else (1,1,1,1)
        self.recalc_time()
    def change_count(self, delta):
        new_count = self.egg_count + delta
        if new_count < 1: new_count = 1
        self.egg_count = new_count
        self.bottom_sheet.lbl_count.text = str(new_count)
        self.recalc_time()
    def on_cooling_change(self, instance, value):
        self.is_cooled = value
        self.recalc_time()
    def recalc_time(self):
        if self.is_running: return
        if self.egg_type == 'quail': size_key = 'default'
        else: size_key = self.egg_size
        base_seconds = current_times[self.egg_type][size_key][self.current_mode_idx]
        if self.is_cooled: base_seconds += 95
        base_seconds += (self.egg_count - 1) * 15
        self.time_left = max(10, base_seconds)
        self.update_label()
    def update_label(self):
        m, s = divmod(self.time_left, 60)
        time_str = f"{m:02}:{s:02}"
        self.timer_label.text = time_str
        if hasattr(self, 'bottom_sheet') and self.bottom_sheet:
            self.bottom_sheet.mini_timer_label.text = time_str
            
    def toggle_timer(self, instance):
        if self.is_finished:
            self.reset_timer_state()
        elif self.is_running:
            self.stop_timer()
        else:
            self.start_timer_logic()
            
    def start_timer_logic(self):
        self.is_running = True
        self.is_finished = False
        self.action_btn.text = "СТОП"
        self.action_btn.bg_color = get_color_from_hex(STOP_COLOR)
        self.bottom_sheet.close_sheet()
        self.timer_event = Clock.schedule_interval(self.tick, 1)
        
    def stop_timer(self):
        self.is_running = False
        if self.timer_event: self.timer_event.cancel()
        self.action_btn.text = "СТАРТ"
        self.action_btn.bg_color = get_color_from_hex(ACCENT_COLOR)
        self.recalc_time()
        
    def reset_timer_state(self):
        self.is_finished = False
        self.is_running = False
        self.action_btn.text = "СТАРТ"
        self.action_btn.bg_color = get_color_from_hex(ACCENT_COLOR)
        self.timer_label.text = "00:00"
        self.recalc_time()

    def tick(self, dt):
        self.time_left -= 1
        self.update_label()
        if self.time_left <= 0:
            self.finish_timer()

    def finish_timer(self):
        self.is_running = False
        self.is_finished = True
        if self.timer_event: self.timer_event.cancel()
        self.timer_label.text = "ГОТОВО!"
        if vibrator:
            try: vibrator.vibrate(1) 
            except: pass
        if notification:
            try: notification.notify(title='Яичко-тян', message='Яйца готовы! Скорее доставайте их!', timeout=10)
            except: pass
        self.action_btn.text = "ПРОДОЛЖИТЬ"
        self.action_btn.bg_color = get_color_from_hex(ACCENT_COLOR)

    def show_instruction(self, instance=None):
        content = AnchorLayout(anchor_x='center', anchor_y='center')
        box = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20), size_hint=(None, None), size=(dp(280), dp(250)))
        with box.canvas.before:
            Color(*get_color_from_hex(CARD_BG)) 
            self.instr_bg_rect = RoundedRectangle(pos=box.pos, size=box.size, radius=[dp(20)])
            Color(*get_color_from_hex(ACCENT_COLOR))
            self.instr_line_rect = Line(rounded_rectangle=(box.x, box.y, box.width, box.height, dp(20)), width=dp(2))
        def update_box(inst, val):
            if hasattr(self, 'instr_bg_rect'):
                self.instr_bg_rect.pos = inst.pos
                self.instr_bg_rect.size = inst.size
            if hasattr(self, 'instr_line_rect'):
                self.instr_line_rect.rounded_rectangle = (inst.x, inst.y, inst.width, inst.height, dp(20))
        box.bind(pos=update_box, size=update_box)
        lbl = Label(text="[b]Инструкция[/b]\n\n1. Вскипятите воду\n2. Посолите\n3. Опустите яйцо\n4. Нажмите СТАРТ", 
                    markup=True, halign='center', font_size=sp(16))
        btn = RoundedButton(text="ПОНЯТНО", size_hint=(1, 0.3), bg_color=get_color_from_hex(ACCENT_COLOR), 
                     color=(0,0,0,1), bold=True)
        box.add_widget(lbl)
        box.add_widget(btn)
        content.add_widget(box)
        popup = Popup(title='', content=content, size_hint=(1, 1), separator_height=0, 
                      background_color=(0,0,0,0.8)) 
        btn.bind(on_press=popup.dismiss)
        popup.open()

    def update_corner_icon(self):
        today = datetime.now().strftime('%Y-%m-%d')
        if store.exists('daily_egg') and store.get('daily_egg')['date'] == today:
            idx = store.get('daily_egg')['persona_idx']
            self.persona_btn.source = EGG_PERSONAS[idx]['img']
        else:
            self.persona_btn.source = 'images/mascot.jpeg' # <-- English
            
    def open_daily_egg(self, instance=None):
        today = datetime.now().strftime('%Y-%m-%d')
        if store.exists('daily_egg') and store.get('daily_egg')['date'] == today:
             self.show_egg_result(store.get('daily_egg')['persona_idx'])
        else:
             self.show_egg_reveal_dialog()
             
    def _create_popup_frame(self, bg_color_hex):
        content = AnchorLayout(anchor_x='center', anchor_y='center')
        box = BoxLayout(orientation='vertical', padding=[dp(20), dp(20), dp(20), dp(20)], spacing=dp(10), size_hint=(None, None), size=(dp(320), dp(480)))
        with box.canvas.before:
            Color(*get_color_from_hex(bg_color_hex)) 
            bg_rect = RoundedRectangle(pos=box.pos, size=box.size, radius=[dp(20)])
            Color(*get_color_from_hex(ACCENT_COLOR))
            line_rect = Line(rounded_rectangle=(box.x, box.y, box.width, box.height, dp(20)), width=dp(2))
        def update_box(inst, val, bg=bg_rect, ln=line_rect):
            bg.pos = inst.pos
            bg.size = inst.size
            ln.rounded_rectangle = (inst.x, inst.y, inst.width, inst.height, dp(20))
        box.bind(pos=update_box, size=update_box)
        return content, box

    def show_egg_reveal_dialog(self):
        content, box = self._create_popup_frame(BLACK_BG)
        
        lbl = Label(text="[b]Какое яйцо ты сегодня?[/b]", markup=True, halign='center', font_size=sp(18),
                    size_hint=(1, None), height=dp(50))
        
        egg_container = AnchorLayout(size_hint=(1, 1))
        egg_img = Image(source="images/mascot.jpeg", size_hint=(None, None), size=(dp(180), dp(240))) # <-- English
        egg_container.add_widget(egg_img)
        
        btn = RoundedButton(text="УЗНАТЬ", size_hint=(1, None), height=dp(50), bg_color=get_color_from_hex(ACCENT_COLOR),
                     color=(0,0,0,1), bold=True)
        
        popup = Popup(title='', content=content, size_hint=(1, 1), separator_height=0, 
                      background_color=(0,0,0,0.8))
        def reveal(x):
            popup.dismiss()
            self._reveal_logic()
        btn.bind(on_press=reveal)
        
        box.add_widget(lbl)
        box.add_widget(egg_container)
        box.add_widget(btn)
        content.add_widget(box)
        popup.open()

    def _reveal_logic(self):
        idx = random.randint(0, len(EGG_PERSONAS) - 1)
        store.put('daily_egg', date=datetime.now().strftime('%Y-%m-%d'), persona_idx=idx)
        self.show_egg_result(idx, animate=True)
        self.persona_btn.source = EGG_PERSONAS[idx]['img']

    def show_egg_result(self, idx, animate=False):
        persona = EGG_PERSONAS[idx]
        content, box = self._create_popup_frame(BLACK_BG)
        if animate:
            fw = Firework(pos_hint={'center_x': 0.5, 'center_y': 0.5})
            content.add_widget(fw)
        
        img_box = AnchorLayout(size_hint=(1, None), height=dp(180))
        egg_img = Image(source=persona['img'], size_hint=(None, None), size=(dp(150), dp(150)))
        img_box.add_widget(egg_img)
        
        lbl_title = Label(text=f"[b][size={int(sp(20))}]{persona['name']}[/size][/b]", markup=True,
                    halign='center', valign='middle', size_hint=(1, None), height=dp(40))
        
        lbl_desc = Label(text=persona['desc'], halign='center', valign='top', font_size=sp(15),
                         size_hint=(1, None), height=dp(80))
        lbl_desc.bind(size=lbl_desc.setter('text_size'))
        
        spacer = Widget(size_hint=(1, 1))
        
        lbl_hint = Label(text="Следующая попытка наступит завтра!!", 
                         font_size=sp(11), color=get_color_from_hex(SUBTEXT_COLOR),
                         size_hint=(1, None), height=dp(20))
        
        btn = RoundedButton(text="ПОНЯТНО!", size_hint=(1, None), height=dp(50),
                     bg_color=get_color_from_hex(ACCENT_COLOR), color=(0,0,0,1))
        
        popup = Popup(title='', separator_height=0, content=content, size_hint=(1, 1), 
                      background_color=(0,0,0,0.9))
        btn.bind(on_press=popup.dismiss)
        
        box.add_widget(img_box)
        box.add_widget(lbl_title)
        box.add_widget(lbl_desc)
        box.add_widget(spacer)
        box.add_widget(lbl_hint)
        box.add_widget(btn)
        
        content.add_widget(box)
        popup.open()

class EggChanApp(App):
    def build(self):
        self.title = "Яичко-тян"
        self.icon = 'images/mascot.jpeg' # <-- English
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(TimeSettingsScreen(name='settings'))
        return sm
    def on_pause(self): return self.root.get_screen('main').on_pause()
    def on_resume(self): return self.root.get_screen('main').on_resume()

if __name__ == '__main__':
    EggChanApp().run()
