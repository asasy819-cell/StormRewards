from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle, Line, Ellipse
from kivy.clock import Clock
import random
from datetime import date

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username = "Player"
        self.total_balance = 50
        self.spin_count = 0
        self.history_list = ["First-time Login Bonus: $50"]
        self.last_claim_date = None
        
        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # Background color
        with main_layout.canvas.before:
            Color(0.25, 0.25, 0.27, 1) # #41212c equivalent dark tone
            self.bg_rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
        main_layout.bind(size=self._update_bg, pos=self._update_bg)

        # Top Info Layout (Balance & Daily Bonus)
        top_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        self.balance_label = Label(text=f"Balance: ${self.total_balance}", font_size=18, color=(1, 1, 1, 1))
        btn_daily = Button(text="Daily Bonus", background_color=(0.1, 0.6, 0.2, 1), font_size=14)
        btn_daily.bind(on_press=self.claim_daily_bonus)
        
        top_layout.add_widget(self.balance_label)
        top_layout.add_widget(btn_daily)
        main_layout.add_widget(top_layout)
        
        # Title
        title_label = Label(text="StormRewards", font_size=22, bold=True, size_hint_y=None, height=40, color=(0.9, 0.3, 0.5, 1))
        main_layout.add_widget(title_label)
        
        # Wheel / Status Display Area
        self.status_label = Label(text="Press the button to start", font_size=16, size_hint_y=None, height=40, color=(1, 1, 1, 1))
        main_layout.add_widget(self.status_label)
        
        # Play Button
        self.play_btn = Button(text="PLAY", background_color=(0.8, 0.2, 0.2, 1), font_size=20, size_hint_y=None, height=60)
        self.play_btn.bind(on_press=self.spin_wheel)
        main_layout.add_widget(self.play_btn)
        
        # Sub label / History info
        self.sub_label = Label(text="Click and win the prize", font_size=14, italic=True, size_hint_y=None, height=30, color=(0.7, 0.7, 0.7, 1))
        main_layout.add_widget(self.sub_label)
        
        # History section title
        main_layout.add_widget(Label(text="Recent Prizes:", font_size=14, size_hint_y=None, height=25, color=(0.8, 0.8, 0.8, 1)))
        
        # History Display Box
        self.history_label = Label(text=self.get_history_str(), font_size=13, size_hint_y=None, height=80, color=(0.9, 0.9, 0.9, 1))
        main_layout.add_widget(self.history_label)

        # Navigation Bar at bottom
        nav_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        btn_home = Button(text="Home", background_color=(0.3, 0.3, 0.5, 1))
        btn_profile = Button(text="Profile", background_color=(0.2, 0.2, 0.3, 1), on_press=self.go_to_profile)
        btn_settings = Button(text="Settings", background_color=(0.2, 0.2, 0.3, 1), on_press=self.go_to_settings)
        
        nav_layout.add_widget(btn_home)
        nav_layout.add_widget(btn_profile)
        nav_layout.add_widget(nav_settings)
        main_layout.add_widget(nav_layout)
        
        self.add_widget(main_layout)

    def _update_bg(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def get_history_str(self):
        return "\n".join(self.history_list[-3:])

    def claim_daily_bonus(self, instance):
        today = date.today()
        if self.last_claim_date == today:
            self.status_label.text = "You have already claimed your daily bonus today!"
        else:
            self.last_claim_date = today
            bonus_amount = 30
            self.total_balance += bonus_amount
            self.history_list.append(f"Daily Bonus: ${bonus_amount}")
            if len(self.history_list) > 3:
                self.history_list.pop(0)
            self.balance_label.text = f"Balance: ${self.total_balance}"
            self.history_label.text = self.get_history_str()
            self.status_label.text = f"Success! Received ${bonus_amount} Daily Bonus."

    def spin_wheel(self, instance):
        prizes = [
            {"text": "Premium Smartphone", "val": 150},
            {"text": "Cash Prize $50", "val": 50},
            {"text": "Diamond Pack $25", "val": 25},
            {"text": "Mystery Gift $10", "val": 10},
            {"text": "Grand Jackpot $100", "val": 100}
        ]
        won = random.choice(prizes)
        self.total_balance += won["val"]
        self.spin_count += 1
        self.history_list.append(won["text"])
        if len(self.history_list) > 3:
            self.history_list.pop(0)
            
        self.balance_label.text = f"Balance: ${self.total_balance}"
        self.history_label.text = self.get_history_str()
        self.status_label.text = f"Won: {won['text']}!"

    def go_to_profile(self, instance):
        self.manager.current = 'profile'

    def go_to_settings(self, instance):
        self.manager.current = 'settings'


class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        layout.add_widget(Label(text="User Profile", font_size=24, color=(0.9, 0.3, 0.5, 1), size_hint_y=None, height=50))
        
        self.user_info_lbl = Label(text="Username: Player", font_size=18, color=(1, 1, 1, 1), size_hint_y=None, height=40)
        layout.add_widget(self.user_info_lbl)
        
        btn_change_name = Button(text="Change Username", size_hint_y=None, height=50)
        btn_change_name.bind(on_press=self.change_username)
        layout.add_widget(btn_change_name)
        
        layout.add_widget(Label(text="Total Balance: $50", font_size=16, color=(1, 1, 1, 1), size_hint_y=None, height=40))
        
        btn_back = Button(text="Back to Home", size_hint_y=None, height=50, background_color=(0.3, 0.3, 0.5, 1))
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(btn_back)
        
        # Spacer
        layout.add_widget(Label())
        self.add_widget(layout)

    def change_username(self, instance):
        # Placeholder for changing name securely in Kivy
        self.user_info_lbl.text = "Username: ProPlayer"


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        layout.add_widget(Label(text="Settings - Version 1.5", font_size=24, color=(0.9, 0.3, 0.5, 1), size_hint_y=None, height=50))
        layout.add_widget(Label(text="App Name: StormRewards", font_size=16, color=(1, 1, 1, 1), size_hint_y=None, height=30))
        layout.add_widget(Label(text="Visual Effects: Enabled", font_size=16, color=(1, 1, 1, 1), size_hint_y=None, height=30))
        
        btn_reset = Button(text="Reset Data", background_color=(0.8, 0.2, 0.2, 1), size_hint_y=None, height=50)
        btn_reset.bind(on_press=self.reset_data)
        layout.add_widget(btn_reset)
        
        btn_back = Button(text="Back to Home", size_hint_y=None, height=50, background_color=(0.3, 0.3, 0.5, 1))
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(btn_back)
        
        layout.add_widget(Label())
        self.add_widget(layout)

    def reset_data(self, instance):
        print("Data Reset Successfully!")


class StormRewardsApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(ProfileScreen(name='profile'))
        sm.add_widget(SettingsScreen(name='settings'))
        return sm


if __name__ == '__main__':
    StormRewardsApp().run()

