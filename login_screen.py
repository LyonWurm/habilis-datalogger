from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from pathlib import Path
import json
from datetime import datetime

# Import data functions
from admin import load_seasons, load_users, load_projects

KV = '''
<LoginScreen>:
    MDBoxLayout:
        orientation: "vertical"
        size_hint: (1, 1)  
        pos_hint: {'x': 0, 'y': 0}


        
        MDTopAppBar:
            id: top_app_bar
            title: "Habilis Data Logger"
            elevation: 4
            left_action_items: [["menu", lambda x: root.open_menu()]]

        ScrollView:  # Add this wrapper
            MDBoxLayout:
                orientation: "vertical"
                spacing: "24dp"
                padding: "24dp"
                size_hint_y: None
                height: self.minimum_height

        MDBoxLayout:
            orientation: "vertical"
            spacing: "24dp"
            padding: "24dp"

        # Image:
        #     source: "assets/icon.png"
        #     size_hint_y: 0.3
        #     keep_ratio: True
        #     pos_hint: {"center_x": 0.5}

            MDCard:
                id: login_card
                orientation: "vertical"
                padding: "24dp"
                spacing: "20dp"
                size_hint: None, None
                size: "400dp", "350dp"
                pos_hint: {"center_x": 0.5}
                md_bg_color: self.theme_cls.bg_dark if self.theme_cls.theme_style == "Dark" else self.theme_cls.bg_light
               
               
                MDLabel:
                    text: "Field Login"
                    halign: "center"
                    theme_text_color: "Primary"
                    font_style: "H5"
                    size_hint_y: None
                    height: "30dp"

                MDTextField:
                    id: season_project_field
                    hint_text: "Season + Project"
                    helper_text: "YYPP format (e.g., 2401 = 2024, Project 01)"
                    helper_text_mode: "on_focus"
                    icon_right: "calendar"
                    mode: "rectangle"

                MDTextField:
                    id: user_field
                    hint_text: "User ID (01-99)"
                    helper_text: "Your 2-digit ID"
                    helper_text_mode: "on_focus"
                    icon_right: "account"
                    mode: "rectangle"

                MDRaisedButton:
                    text: "LOGIN"
                    size_hint: None, None
                    size: "200dp", "48dp"
                    pos_hint: {"center_x": 0.5}
                    on_release: root.do_login()
                
                
'''

class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu = None

    def test_dark_mode(self):
        """Simple test for dark mode"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()

        if app.theme_cls.theme_style == "Light":
            app.theme_cls.theme_style = "Dark"
            if hasattr(self, 'theme_switch'):
                self.theme_switch.active = True
        else:
            app.theme_cls.theme_style = "Light"
            if hasattr(self, 'theme_switch'):
                self.theme_switch.active = False

        # Save preference
        data_dir = self.get_data_dir()
        prefs_file = data_dir / "preferences.json"

        if prefs_file.exists():
            with open(prefs_file) as f:
                prefs = json.load(f)
        else:
            prefs = {}

        prefs['theme_style'] = app.theme_cls.theme_style
        with open(prefs_file, 'w') as f:
            json.dump(prefs, f, indent=2)

    def get_data_dir(self):
        from pathlib import Path
        data_dir = Path('field_data')
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir

    def open_menu(self):
        """Open dropdown menu from top-left icon"""
        if self.menu:
            self.menu.dismiss()

        menu_items = [
            {
                "text": "Admin Login",
                "leading_icon": "shield-account",
                "on_release": lambda x="admin": self.menu_callback("admin"),
            },
            {
                "text": "Settings",
                "leading_icon": "cog",
                "on_release": lambda x="settings": self.menu_callback("settings"),
            },
        ]

        self.menu = MDDropdownMenu(
            caller=self.ids.top_app_bar.ids.left_actions,
            items=menu_items,
            width_mult=3,
            position="auto",
        )
        self.menu.open()

    def menu_callback(self, item):
        """Handle menu item selection"""
        self.menu.dismiss()
        if item == "admin":
            self.go_to_admin()
        elif item == "settings":
            self.show_settings()  # Change this

    def go_to_admin(self):
        """Navigate to admin login screen"""
        self.manager.current = "admin_login"

    def show_settings(self):
        """Show settings dialog with Dark/Light mode toggle"""
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.label import MDLabel
        from kivymd.uix.button import MDRaisedButton
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.app import MDApp

        app = MDApp.get_running_app()

        current_theme = "ON" if app.theme_cls.theme_style == "Dark" else "OFF"

        content = MDBoxLayout(
            orientation='vertical',
            spacing=10,
            padding=20,
            size_hint_y=None,
            height=150
        )

        # Dark Mode row
        dark_row = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=50,
            spacing=10
        )

        # Dark Mode button on the left
        dark_btn = MDRaisedButton(
            text="Dark Mode",
            size_hint_x=0.6,
            height=40,
            on_release=lambda x: self.toggle_theme()
        )

        # Status on the right
        dark_status = MDLabel(
            text=current_theme,
            size_hint_x=0.4,
            halign="center",
            theme_text_color="Secondary"
        )

        dark_row.add_widget(dark_btn)
        dark_row.add_widget(dark_status)
        content.add_widget(dark_row)

        # Add more settings here in future rows
        # Example:
        # language_row = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        # ...

        self.settings_dialog = MDDialog(
            title="Settings",
            type="custom",
            content_cls=content,
            size_hint=(0.9, None),
            height=250,
            buttons=[
                MDRaisedButton(
                    text="CLOSE",
                    on_release=lambda x: self.settings_dialog.dismiss()
                )
            ]
        )
        self.settings_dialog.open()

    def toggle_theme(self):
        """Toggle between light and dark mode"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()

        if app.theme_cls.theme_style == "Light":
            app.theme_cls.theme_style = "Dark"
        else:
            app.theme_cls.theme_style = "Light"

        # Update the status label if the dialog is still open
        if hasattr(self, 'settings_dialog') and self.settings_dialog:
            current_theme = "ON" if app.theme_cls.theme_style == "Dark" else "OFF"
            for child in self.settings_dialog.content_cls.children:
                if isinstance(child, MDBoxLayout):
                    for subchild in child.children:
                        if isinstance(subchild, MDLabel) and subchild.text in ["ON", "OFF"]:
                            subchild.text = current_theme
                            break

        # Save preference - FIXED: use get_data_dir() with filename
        data_dir = self.get_data_dir()
        prefs_file = data_dir / "preferences.json"  # ← Added filename

        if prefs_file.exists():
            with open(prefs_file) as f:
                prefs = json.load(f)
        else:
            prefs = {}

        prefs['theme_style'] = app.theme_cls.theme_style
        with open(prefs_file, 'w') as f:
            json.dump(prefs, f, indent=2)

    def do_login(self):
        """Handle user login"""
        season_project = self.ids.season_project_field.text.strip()
        user_id = self.ids.user_field.text.strip()

        # Parse YYPP format
        if len(season_project) != 4 or not season_project.isdigit():
            self.show_message("Season+Project must be 4 digits (YYPP)")
            return

        season = season_project[:2]
        project = season_project[2:]

        # Convert to full year
        year = f"20{season}"

        if not user_id.isdigit() or len(user_id) != 2:
            self.show_message("User ID must be 2 digits (01-99)")
            return

        # Load local data
        from admin import load_seasons, load_users, load_projects  # Keep this

        seasons = load_seasons()
        users = load_users()
        projects = load_projects()  # Keep this - now we use it!

        # Find the season
        season_id = year
        season_data = seasons.get(season_id, {})

        if not season_data or season_data.get('status') != 'active':
            self.show_message(f"Season {year} is not active")
            return

        # Check user exists
        user = users.get(user_id, {})
        if not user:
            self.show_message(f"User {user_id} not found")
            return

        if user.get('status') != 'active':
            self.show_message("User account is inactive")
            return

        # Check if user is assigned to this season
        if user.get('season') != season_id:
            self.show_message(f"User {user_id} is not assigned to {season_id}")
            return

        # NEW: Check if project exists
        if project not in projects:
            self.show_message(f"Project {project} does not exist. Please check the project code.")
            return

        # Check project assignment
        user_projects = user.get('projects', [])

        if project not in user_projects:
            self.show_project_confirmation(project, user, user_projects, season_id, year, user_id)
            return

        # Normal login
        self.complete_login(user, project, season_id, year, user_id)

    def show_project_confirmation(self, project, user, user_projects, season_id, year, user_id):
        """Ask user to confirm if they want to work on a different project"""
        from admin import load_projects
        projects = load_projects()
        project_data = projects.get(project, {})
        project_name = project_data.get('name', 'Unknown')

        current_assignments = ", ".join(user_projects)

        self.confirm_dialog = MDDialog(
            title="Different Project",
            text=f"User {user.get('name')} is assigned to project(s): {current_assignments}\n\n"
                 f"You entered Project {project} ({project_name})\n\n"
                 f"Work on this project anyway?",
            buttons=[
                MDFlatButton(
                    text="NO",
                    on_release=lambda x: self.confirm_dialog.dismiss()
                ),
                MDRaisedButton(
                    text="YES, CONTINUE",
                    md_bg_color=(0.8, 0.5, 0.2, 1),
                    on_release=lambda x: self.complete_login(user, project, season_id, year, user_id)
                )
            ]
        )
        self.confirm_dialog.open()

    def complete_login(self, user, project, season_id, year, user_id):
        """Complete the login process"""
        from kivymd.app import MDApp

        # FIXED: Use get_data_dir() with filename
        data_dir = self.get_data_dir()
        cred_file = data_dir / "credentials.json"  # ← Added filename

        with open(cred_file, 'w') as f:
            json.dump({
                'season': season_id,
                'year': year,
                'project': project,
                'user_id': user_id,
                'user_name': user.get('name', user_id),
                'login_time': datetime.now().isoformat()
            }, f)

        # Store in app
        app = MDApp.get_running_app()
        app.current_user = {
            'user_id': user_id,
            'user_name': user.get('name', user_id),
            'season': season_id,
            'project': project,
            'year': year
        }

        self.manager.current = "collect"

    def show_message(self, message):
        """Show a simple message dialog"""
        dialog = MDDialog(
            text=message,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()


Builder.load_string(KV)