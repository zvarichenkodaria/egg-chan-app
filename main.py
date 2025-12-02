import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

# Цвета
BG_COLOR = '#FFF9C4'
TEXT_COLOR = '#5D4037'
BTN_COLOR = '#FFECB3'

Window.clearcolor = get_color_from_hex(BG_COLOR)

class EggChanApp(App):
    def build(self):
        self.time_left = 0
        self.timer_event = None
        
        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        # Заголовок
        self.title = Label(text="Яичко-тян", font_size='30sp', color=get_color_from_hex('#FBC02D'), size_hint=(1, 0.15))
        
        # Лицо
        self.face = Label(text="(・∀・)", font_size='60sp', color=get_color_from_hex(TEXT_COLOR), size_hint=(1, 0.3))
        
        # Таймер
        self.timer_display = Label(text="00:00", font_size='50sp', bold=True, color=get_color_from_hex(TEXT_COLOR), size_hint=(1, 0.15))
        
        # Кнопки
        self.btns_layout = BoxLayout(orientation='vertical', spacing=15, size_hint=(1, 0.4))
        self.btns_layout.add_widget(self.make_btn("Всмятку (4 мин)", 4))
        self.btns_layout.add_widget(self.make_btn("В мешочек (7 мин)", 7))
        self.btns_layout.add_widget(self.make_btn("Вкрутую (10 мин)", 10))
        
        self.stop_btn = Button(text="ОСТАНОВИТЬ", background_color=get_color_from_hex('#FF8A65'), background_normal='', font_size='20sp')
        self.stop_btn.bind(on_press=self.reset_timer)
        
        self.layout.add_widget(self.title)
        self.layout.add_widget(self.face)
        self.layout.add_widget(self.timer_display)
        self.layout.add_widget(self.btns_layout)
        
        return self.layout

    def make_btn(self, text, minutes):
        btn = Button(text=text, background_color=get_color_from_hex(BTN_COLOR), background_normal='', color=get_color_from_hex(TEXT_COLOR), font_size='18sp')
        btn.bind(on_press=lambda x: self.start_timer(minutes))
        return btn

    def start_timer(self, minutes):
        if self.timer_event: self.timer_event.cancel()
        self.time_left = minutes * 60
        self.face.text = "( >_< )"
        self.layout.remove_widget(self.btns_layout)
        self.layout.add_widget(self.stop_btn)
        self.update_display()
        self.timer_event = Clock.schedule_interval(self.tick, 1)

    def tick(self, dt):
        self.time_left -= 1
        self.update_display()
        if self.time_left <= 0:
            self.timer_event.cancel()
            self.face.text = "ГОТОВО!"
            self.timer_display.text = "00:00"

    def update_display(self):
        m, s = divmod(self.time_left, 60)
        self.timer_display.text = f"{m:02}:{s:02}"

    def reset_timer(self, instance):
        if self.timer_event: self.timer_event.cancel()
        self.face.text = "(・∀・)"
        self.timer_display.text = "00:00"
        self.layout.remove_widget(self.stop_btn)
        self.layout.add_widget(self.btns_layout)

if __name__ == '__main__':
    EggChanApp().run()
