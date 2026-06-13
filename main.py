import os
import sys

# Must be before ANY kivy import
os.environ['KIVY_NO_ENV_CONFIG'] = '1'
os.environ['KIVY_GL_BACKEND'] = 'sdl2'
os.environ['KCFG_GRAPHICS_MULTISAMPLES'] = '0'
os.environ['KCFG_GRAPHICS_MAXFPS'] = '60'

from kivy.config import Config
Config.set('graphics', 'multisamples', '0')
Config.set('graphics', 'maxfps', '60')

from pathlib import Path
import json
from admin import get_data_dir
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
# Android permission handling - built directly into main.py
try:
    from android.permissions import request_permissions, check_permission, Permission
    from android import activity

    ANDROID_AVAILABLE = True

    # Set FileProvider authority for camera
    try:
        import plyer.camera
        from jnius import autoclass

        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        package_name = PythonActivity.mActivity.getPackageName()
        plyer.camera.FILEPROVIDER_AUTHORITY = f'{package_name}.fileprovider'
        print(f"FileProvider authority set to: {plyer.camera.FILEPROVIDER_AUTHORITY}")
    except Exception as e:
        print(f"Could not set FileProvider: {e}")

except ImportError:
    ANDROID_AVAILABLE = False


    # Dummy for desktop
    class Permission:
        CAMERA = "android.permission.CAMERA"
        ACCESS_FINE_LOCATION = "android.permission.ACCESS_FINE_LOCATION"
        ACCESS_COARSE_LOCATION = "android.permission.ACCESS_COARSE_LOCATION"
        READ_EXTERNAL_STORAGE = "android.permission.READ_EXTERNAL_STORAGE"
        WRITE_EXTERNAL_STORAGE = "android.permission.WRITE_EXTERNAL_STORAGE"
        INTERNET = "android.permission.INTERNET"
        ACCESS_NETWORK_STATE = "android.permission.ACCESS_NETWORK_STATE"


    def check_permission(p):
        return True


    def request_permissions(p, cb):
        if cb:
            cb([], [])
        return True


class PermissionManager:
    """Simple permission manager built into main.py"""

    def __init__(self):
        self.granted = False

    def check_permissions(self):
        if not ANDROID_AVAILABLE:
            return True
        required = [
            Permission.CAMERA,
            Permission.ACCESS_FINE_LOCATION,
            Permission.ACCESS_COARSE_LOCATION,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
        ]
        for p in required:
            if not check_permission(p):
                return False
        return True

    def request_all_permissions(self, callback=None):
        if not ANDROID_AVAILABLE:
            if callback:
                callback(True)
            return True

        if self.check_permissions():
            if callback:
                callback(True)
            return True

        required = [
            Permission.CAMERA,
            Permission.ACCESS_FINE_LOCATION,
            Permission.ACCESS_COARSE_LOCATION,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
        ]

        def on_permissions_result(permissions, results):
            granted = all(results)
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: callback(granted) if callback else None, 0)

        request_permissions(required, on_permissions_result)
        return False

from admin import AdminLoginScreen, AdminDashboardScreen, BagTagManagementScreen, SeasonManagementScreen, \
    ProjectManagementScreen, UserManagementScreen
from login_screen import LoginScreen
from collect_screen import CollectScreen
from sync_screen import SyncScreen
from admin import AllProjectsScreen, AllUsersScreen




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
        sm.size_hint = (1, 1)
        sm.pos_hint = {'x': 0, 'y': 0}
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
        if ANDROID_AVAILABLE:
            self.permission_manager.request_all_permissions(self._on_permissions_result)
        else:
            self._check_saved_credentials()

    def _on_permissions_result(self, granted):
        self.permissions_granted = granted
        self._check_saved_credentials()

    def _check_saved_credentials(self):
        """Check for saved login credentials"""
        # FIXED: Use get_data_dir() with filename
        cred_file = self.storage_path / "credentials.json"  # storage_path is already get_data_dir()
        if cred_file.exists():
            self.root.current = "collect"

if __name__ == "__main__":
    FieldApp().run()
