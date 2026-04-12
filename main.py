import sys
import json
from admin import AdminLoginScreen, AdminDashboardScreen,  BagTagManagementScreen, SeasonManagementScreen, ProjectManagementScreen, UserManagementScreen
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen  # Fixed import
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivy.core.window import Window
from pathlib import Path
from kivy.lang import Builder

import os
sys.path.insert(0, str(Path(__file__).parent.parent))

from login_screen import KV as login_kv
from collect_screen import KV as collect_kv

from sync_screen import KV as sync_kv
from admin import KV as admin_kv, AllProjectsScreen, AllUsersScreen

# Import your existing core
from core.infrastructure import FieldObservation
from login_screen import LoginScreen
from collect_screen import CollectScreen
from sync_screen import SyncScreen
from admin import (
    AdminLoginScreen,
    AdminDashboardScreen,
    SeasonManagementScreen,
    ProjectManagementScreen,
    UserManagementScreen
)


# Set a reasonable window size for desktop testing
Window.size = (400, 700)


class FieldApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage_path = Path.home() / "field_data"
        self.storage_path.mkdir(exist_ok=True)
        self.current_admin = None  # Track logged-in admin
        self.current_season = None  # Track currently selected season for project management
        self.current_user = None

    def build(self):
        Builder.load_string(login_kv)
        Builder.load_string(collect_kv)
        Builder.load_string(sync_kv)
        Builder.load_string(admin_kv)

        prefs_file = Path.home() / "field_data" / "preferences.json"
        if prefs_file.exists():
            with open(prefs_file) as f:
                prefs = json.load(f)
            theme = prefs.get('theme_style', 'Light')
            self.theme_cls.theme_style = theme
        else:
            self.theme_cls.theme_style = "Light"

        self.theme_cls.primary_palette = "Purple"


        # Load KV files if they exist
        for kv_file in ['login.kv', 'collect.kv', 'sync.kv']:
            if os.path.exists(kv_file):
                Builder.load_file(kv_file)

        # Screen manager
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(CollectScreen(name="collect"))
        sm.add_widget(SyncScreen(name="sync"))
        sm.add_widget(AdminLoginScreen(name="admin_login"))
        sm.add_widget(AdminDashboardScreen(name="admin_dashboard"))
        sm.add_widget(SeasonManagementScreen(name="season_management"))
        sm.add_widget(ProjectManagementScreen(name="project_management"))
        sm.add_widget(UserManagementScreen(name="user_management"))
        sm.add_widget(AllProjectsScreen(name="all_projects"))
        sm.add_widget(AllUsersScreen(name="all_users"))
        sm.add_widget(BagTagManagementScreen(name="bagtag_management"))

        return sm

    def on_start(self):
        """Check for saved credentials"""
        cred_file = self.storage_path / "credentials.json"
        if cred_file.exists():
            # Auto-login
            self.root.current = "collect"


if __name__ == "__main__":
    FieldApp().run()