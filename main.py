import sys
from pathlib import Path
import json
from admin import get_data_dir
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

# Import permission manager
try:
    from permissions import PermissionManager, ANDROID_AVAILABLE
except ImportError:
    ANDROID_AVAILABLE = False


    class PermissionManager:
        def check_permissions(self): return True

        def request_all_permissions(self, cb=None):
            if cb: cb(True)
            return True

from admin import AdminLoginScreen, AdminDashboardScreen, BagTagManagementScreen, SeasonManagementScreen, \
    ProjectManagementScreen, UserManagementScreen
from login_screen import LoginScreen
from collect_screen import CollectScreen
from sync_screen import SyncScreen
from admin import AllProjectsScreen, AllUsersScreen

# Set window size for desktop
#Window.size = (400, 700) only used for testing on desktop


class FieldApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage_path = get_data_dir()
        self.current_admin = None
        self.current_season = None
        self.current_user = None
        self.permission_manager = PermissionManager()
        self.permissions_granted = False

    def build(self):
        # Load KV strings
        from login_screen import KV as login_kv
        from collect_screen import KV as collect_kv
        from sync_screen import KV as sync_kv
        from admin import KV as admin_kv

        Window.softinput_mode = "below_target"

        Builder.load_string(login_kv)
        Builder.load_string(collect_kv)
        Builder.load_string(sync_kv)
        Builder.load_string(admin_kv)

        # Load theme preference
        prefs_file = get_data_dir() / "preferences.json"  # ← Added filename
        if prefs_file.exists():
            with open(prefs_file) as f:
                prefs = json.load(f)
            theme = prefs.get('theme_style', 'Light')
            self.theme_cls.theme_style = theme
        else:
            self.theme_cls.theme_style = "Light"

        self.theme_cls.primary_palette = "Purple"

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
        """Check permissions when app starts"""
        if ANDROID_AVAILABLE:
            # Request permissions on Android
            self.permission_manager.request_all_permissions(self._on_permissions_result)
        else:
            # Desktop: proceed normally
            self._check_saved_credentials()

    def _on_permissions_result(self, granted):
        """Called after permission request completes"""
        self.permissions_granted = granted
        if granted:
            self._check_saved_credentials()
        else:
            # Show message and exit? Or keep trying?
            from kivymd.uix.dialog import MDDialog
            from kivymd.uix.button import MDRaisedButton

            dialog = MDDialog(
                title="Permissions Required",
                text="This app cannot function without camera, GPS, and storage permissions.\n\nLimited Functionality",
                buttons=[
                    MDRaisedButton(
                        text="Ok",
                        on_release=lambda x: [dialog.dismiss(), self._check_saved_credentials()]                    ),

                ]
            )
            dialog.open()

    def _check_saved_credentials(self):
        """Check for saved login credentials"""
        # FIXED: Use get_data_dir() with filename
        cred_file = self.storage_path / "credentials.json"  # storage_path is already get_data_dir()
        if cred_file.exists():
            self.root.current = "collect"

if __name__ == "__main__":
    FieldApp().run()
