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
from plyer import camera
from datetime import datetime

# Import data functions
from admin import load_seasons, load_users, load_projects


from android.permissions import check_permission, Permission, request_permissions
from android import activity
from plyer import camera


class Permission:
    CAMERA = "android.permission.CAMERA"
    ACCESS_FINE_LOCATION = "android.permission.ACCESS_FINE_LOCATION"
    ACCESS_COARSE_LOCATION = "android.permission.ACCESS_COARSE_LOCATION"
    READ_EXTERNAL_STORAGE = "android.permission.READ_EXTERNAL_STORAGE"
    WRITE_EXTERNAL_STORAGE = "android.permission.WRITE_EXTERNAL_STORAGE"
    INTERNET = "android.permission.INTERNET"
    ACCESS_NETWORK_STATE = "android.permission.ACCESS_NETWORK_STATE"


def check_permission(permission):
    """Stub - assume permissions granted on desktop"""
    return True


def request_permissions(permissions, callback):
    """Stub - immediately callback with success"""
    callback(permissions, [True] * len(permissions))


class activity:
    @staticmethod
    def getFilesDir():
        """Stub for desktop"""
        import tempfile
        return tempfile.gettempdir()

    @staticmethod
    def getCacheDir():
        """Stub for desktop"""
        import tempfile
        return tempfile.gettempdir()

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

    def scan_join_qr(self):
        """Scan QR code to join a project"""
        # Check if we're on Android with camera available
        if ANDROID_AVAILABLE and ANDROID_PERMISSIONS_AVAILABLE:
            from android.permissions import check_permission, Permission, request_permissions
            if not check_permission(Permission.CAMERA):
                request_permissions([Permission.CAMERA], self._camera_permission_for_qr)
                return

        # For desktop or if camera permission already granted
        self._start_qr_scan()

    def _camera_permission_for_qr(self, permissions, results):
        """Called after camera permission request for QR"""
        if all(results):
            self._start_qr_scan()
        else:
            self.show_qr_input_dialog()

    def _start_qr_scan(self):
        """Start the camera for QR scanning"""
        try:
            from plyer import camera
            # Check if camera is available (hasattr check)
            if not hasattr(camera, 'take_picture'):
                self.show_message("Camera not available on this device")
                self.show_qr_input_dialog()
                return

            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"qr_scan_{timestamp}.jpg"
            data_dir = self.get_data_dir()
            scans_dir = data_dir / "qr_scans"
            scans_dir.mkdir(parents=True, exist_ok=True)
            filepath = scans_dir / filename

            camera.take_picture(filename=str(filepath), on_complete=self.on_qr_captured)
            self.show_message("Scan the QR code...")
        except Exception as e:
            print(f"Camera error: {e}")
            self.show_qr_input_dialog()

    def on_qr_captured(self, filepath):
        """Handle captured QR code image"""
        # For now, fall back to manual input
        # Future: Add QR decoding with pyzbar
        self.show_qr_input_dialog()

    def show_qr_input_dialog(self):
        """Show dialog to enter QR code data"""
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.textfield import MDTextField
        from kivymd.uix.button import MDRaisedButton, MDFlatButton
        from kivy.uix.boxlayout import BoxLayout

        content = BoxLayout(orientation='vertical', spacing=10, padding=20, size_hint_y=None, height=200)

        self.qr_input_field = MDTextField(
            hint_text="Paste QR data here",
            mode="rectangle",
            multiline=True,
            size_hint_y=None,
            height=150
        )
        content.add_widget(self.qr_input_field)

        self.qr_dialog = MDDialog(
            title="Join Project",
            type="custom",
            content_cls=content,
            size_hint=(0.9, None),
            height=350,
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: self.qr_dialog.dismiss()),
                MDRaisedButton(text="JOIN", on_release=lambda x: self.process_join_qr(self.qr_input_field.text))
            ]
        )
        self.qr_dialog.open()

    def process_join_qr(self, qr_data):
        """Process scanned QR code and import project configuration"""
        import json
        from admin import load_users, save_users, load_projects, save_projects, load_seasons, save_seasons
        from kivymd.app import MDApp

        if hasattr(self, 'qr_dialog') and self.qr_dialog:
            self.qr_dialog.dismiss()

        try:
            config = json.loads(qr_data)

            if config.get('version') != '1.0':
                self.show_message("Unsupported QR code version")
                return

            project_id = config.get('project_id')
            project_name = config.get('project_name', 'Unnamed')
            season_id = config.get('season_id')
            users_data = config.get('users', {})

            # Load existing data
            users = load_users()
            projects = load_projects()
            seasons = load_seasons()

            # Check if season exists, if not, create it
            if season_id not in seasons:
                seasons[season_id] = {
                    "organization": "KFFS",
                    "year": season_id,
                    "status": "active",
                    "start_date": datetime.now().strftime("%Y-%m-%d"),
                    "end_date": f"{int(season_id) + 1}-12-31",
                    "projects": 0,
                    "created_at": datetime.now().isoformat(),
                    "created_by": "QR Import"
                }
                save_seasons(seasons)

            # Check if project exists, if not, create it
            if project_id not in projects:
                projects[project_id] = {
                    "project_id": project_id,
                    "name": project_name,
                    "description": f"Imported via QR on {datetime.now().strftime('%Y-%m-%d')}",
                    "season_id": season_id,
                    "status": "active",
                    "created_at": datetime.now().isoformat(),
                    "created_by": "QR Import"
                }
                save_projects(projects)

                # Update season project count
                if season_id in seasons:
                    seasons[season_id]['projects'] = seasons[season_id].get('projects', 0) + 1
                    save_seasons(seasons)

            # Import users
            imported_count = 0
            for user_id, user_data in users_data.items():
                if user_id not in users:
                    users[user_id] = {
                        "name": user_data.get('name', ''),
                        "first_name": user_data.get('first_name', ''),
                        "last_name": user_data.get('last_name', ''),
                        "user_type": user_data.get('user_type', 'seasonal'),
                        "season": season_id,
                        "projects": [project_id],
                        "status": "active",
                        "created_at": datetime.now().isoformat(),
                        "created_by": "QR Import"
                    }
                    imported_count += 1
                else:
                    # Add project to existing user if not already there
                    if 'projects' not in users[user_id]:
                        users[user_id]['projects'] = []
                    if project_id not in users[user_id]['projects']:
                        users[user_id]['projects'].append(project_id)

            save_users(users)

            # Auto-fill the login fields
            # Season ID is like "2025", extract last 2 digits "25", then add project
            season_short = season_id[2:] if len(season_id) == 4 else season_id
            self.ids.season_project_field.text = f"{season_short}{project_id}"

            self.show_message(
                f"Successfully joined project '{project_name}'\n\nImported {imported_count} users.\n\nEnter your User ID to login.")

        except json.JSONDecodeError:
            self.show_message("Invalid QR code data")
        except Exception as e:
            self.show_message(f"Error: {str(e)}")

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
        """Get app-private storage directory - NO PERMISSIONS NEEDED"""
        from pathlib import Path
        import sys

        if hasattr(sys, 'getandroidapilevel'):
            from android import activity
            data_dir = Path(activity.getFilesDir()) / "field_data"
        else:
            data_dir = Path.home() / "field_data"

        data_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Data directory: {data_dir}")
        return data_dir

    def open_menu(self):
        """Open dropdown menu from top-left icon"""
        if self.menu:
            self.menu.dismiss()

        menu_items = [
            {
                "text": "Join Project with QR",
                "leading_icon": "qrcode-scan",
                "on_release": lambda x="join_project": self.menu_callback("join_project"),
            },
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
            width_mult=4,
            position="auto",
        )
        self.menu.open()

    def menu_callback(self, item):
        """Handle menu item selection"""
        self.menu.dismiss()
        if item == "admin":
            self.go_to_admin()
        elif item == "settings":
            self.show_settings()
        elif item == "join_project":
            self.scan_join_qr()  # Call the QR join method

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
        from admin import load_seasons, load_users, load_projects

        seasons = load_seasons()
        users = load_users()
        projects = load_projects()

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

        # Check if project exists
        if project not in projects:
            self.show_message(f"Project {project} does not exist")
            return

        # Check project assignment
        user_projects = user.get('projects', [])

        if project not in user_projects:
            # Show confirmation dialog with user's full name
            self.show_project_confirmation(project, user, user_projects, season_id, year, user_id)
            return

        # Normal login
        self.complete_login(user, project, season_id, year, user_id)

    def show_project_confirmation(self, project, user, user_projects, season_id, year, user_id):
        """Ask user to confirm if they want to work on a different project"""
        from admin import load_projects
        projects = load_projects()

        # Format project with leading zeros for lookup (if needed)
        project_str = project if len(project) == 2 else f"{int(project):02d}"
        project_data = projects.get(project_str, {})
        project_name = project_data.get('name', 'Unknown')

        # Get user's full name
        user_name = user.get('name', user_id)
        first_name = user.get('first_name', '')
        last_name = user.get('last_name', '')
        full_name = f"{first_name} {last_name}".strip() or user_name

        # Format assigned projects list
        assigned_projects = []
        for p in user_projects:
            p_data = projects.get(p, {})
            p_name = p_data.get('name', '')
            assigned_projects.append(f"{p} ({p_name})" if p_name else p)

        assigned_text = ", ".join(assigned_projects) if assigned_projects else "none"

        self.confirm_dialog = MDDialog(
            title="Project Not Assigned",
            text=f"User {full_name} is not assigned to Project {project_str} ({project_name}).\n\n"
                 f"Assigned projects: {assigned_text}\n\n"
                 f"Work on this project anyway?",
            buttons=[
                MDFlatButton(
                    text="NO",
                    on_release=lambda x: self.confirm_dialog.dismiss()  # Just closes, stays on login
                ),
                MDRaisedButton(
                    text="YES, CONTINUE",
                    md_bg_color=(0.8, 0.5, 0.2, 1),
                    on_release=lambda x: [
                        self.confirm_dialog.dismiss(),
                        self.complete_login(user, project_str, season_id, year, user_id)
                    ]
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