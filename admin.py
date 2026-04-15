from kivymd.uix.screen import MDScreen
from typing import Dict, Any
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import Snackbar
from functools import partial
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivymd.uix.card import MDSeparator
from kivymd.uix.card import MDCard
from kivy.clock import Clock
from pathlib import Path
import json
import hashlib
import secrets
import string
from datetime import datetime
from kivymd.uix.spinner import MDSpinner  # If you use it

try:
    from fpdf import FPDF
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

# Simple "database" for now - will be replaced with actual DB
ADMINS_FILE = Path.home() / "field_data" / "admins.json"
SEASONS_FILE = Path.home() / "field_data" / "seasons.json"


def hash_password(password):
    """Simple password hashing"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_admins():
    if ADMINS_FILE.exists():
        with open(ADMINS_FILE) as f:
            return json.load(f)
    return {}

def save_admins(admins):
    ADMINS_FILE.parent.mkdir(exist_ok=True)
    with open(ADMINS_FILE, 'w') as f:
        json.dump(admins, f, indent=2)

SEASONS_FILE = Path.home() / "field_data" / "seasons.json"


def load_seasons():
    if SEASONS_FILE.exists():
        with open(SEASONS_FILE) as f:
            return json.load(f)
    return {}

def save_seasons(seasons):
    SEASONS_FILE.parent.mkdir(exist_ok=True)
    with open(SEASONS_FILE, 'w') as f:
        json.dump(seasons, f, indent=2)


def get_most_recent_season():
        """Get the most recent active season (by year)"""
        seasons = load_seasons()
        active_seasons = []

        for season_id, data in seasons.items():
            if data.get('status') == 'active':
                try:
                    year = int(data.get('year', season_id))
                    active_seasons.append((year, season_id, data.get('organization', 'KFFS')))
                except:
                    pass

        if not active_seasons:
            return None

        # Sort by year descending and get the most recent
        active_seasons.sort(reverse=True)
        return active_seasons[0]


PROJECTS_FILE = Path.home() / "field_data" / "projects.json"

def load_projects():
    if PROJECTS_FILE.exists():
        with open(PROJECTS_FILE) as f:
            return json.load(f)
    return {}

def save_projects(projects):
    PROJECTS_FILE.parent.mkdir(exist_ok=True)
    with open(PROJECTS_FILE, 'w') as f:
        json.dump(projects, f, indent=2)

def load_members():
    """Load members from database - placeholder until member system is built"""
    # This is a temporary function - replace with actual member loading later
    members_file = Path.home() / "field_data" / "members.json"
    if members_file.exists():
        with open(members_file) as f:
            return json.load(f)
    return {}

# User database functions
USERS_FILE = Path.home() / "field_data" / "users.json"

def load_users():
    """Load users from database"""
    if USERS_FILE.exists():
        with open(USERS_FILE) as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save users to database"""
    USERS_FILE.parent.mkdir(exist_ok=True)
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

# Add these functions near your other load/save functions
TAGS_FILE = Path.home() / "field_data" / "tags.json"

def load_tags():
    """Load tags from database"""
    if TAGS_FILE.exists():
        with open(TAGS_FILE) as f:
            return json.load(f)
    return {}

def save_tags(tags):
    """Save tags to database"""
    TAGS_FILE.parent.mkdir(exist_ok=True)
    with open(TAGS_FILE, 'w') as f:
        json.dump(tags, f, indent=2)

TAG_BATCHES_FILE = Path.home() / "field_data" / "tag_batches.json"

def load_tag_batches():
    """Load tag batches from database"""
    if TAG_BATCHES_FILE.exists():
        with open(TAG_BATCHES_FILE) as f:
            return json.load(f)
    return {}

def save_tag_batches(batches):
    """Save tag batches to database"""
    TAG_BATCHES_FILE.parent.mkdir(exist_ok=True)
    with open(TAG_BATCHES_FILE, 'w') as f:
        json.dump(batches, f, indent=2)

# Initialize with superadmin if no admins exist
def init_superadmin():
    admins = load_admins()
    if not admins:
        admins["KFFS"] = {
            "password_hash": hash_password("KNMER-1813"),
            "role": "superadmin",
            "created_at": datetime.now().isoformat(),
            "created_by": "system"
        }
        save_admins(admins)

init_superadmin()


KV = '''
<AdminLoginScreen>:
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Admin Access"
            elevation: 4
            left_action_items: [["arrow-left", lambda x: root.go_back()]]

        MDBoxLayout:
            orientation: "vertical"
            spacing: "24dp"
            padding: "24dp"

            MDCard:
                id: admin_login_card
                orientation: "vertical"
                padding: "24dp"
                spacing: "24dp"
                size_hint: None, None
                size: "400dp", "300dp"
                pos_hint: {"center_x": 0.5}
                md_bg_color: self.theme_cls.bg_dark if self.theme_cls.theme_style == "Dark" else self.theme_cls.bg_light

                MDTextField:
                    id: username_field
                    hint_text: "Username"
                    icon_right: "account"
                    mode: "rectangle"

                MDTextField:
                    id: password_field
                    hint_text: "Password"
                    icon_right: "lock"
                    password: True
                    mode: "rectangle"

                MDRaisedButton:
                    text: "LOGIN"
                    size_hint: None, None
                    size: "200dp", "48dp"
                    pos_hint: {"center_x": 0.5}
                    on_release: root.do_admin_login()

                MDLabel:
                    text: "Default: KFFS / KNMER-1813"
                    halign: "center"
                    theme_text_color: "Hint"
                    font_style: "Caption"

<AdminDashboardScreen>:
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            id: top_app_bar
            title: "Admin Dashboard"
            elevation: 4
            left_action_items: [["menu", lambda x: root.open_admin_menu()]]
            right_action_items: [["logout", lambda x: root.logout()]] 
            
        MDBoxLayout:
            orientation: "vertical"
            padding: "16dp"
            spacing: "16dp"

            MDLabel:
                id: welcome_label
                text: "Welcome"
                theme_text_color: "Primary"
                font_style: "H5"
                size_hint_y: None
                height: self.texture_size[1]

            MDLabel:
                id: role_label
                text: ""
                theme_text_color: "Secondary"
                font_style: "Body1"
                size_hint_y: None
                height: self.texture_size[1]

            MDSeparator:

            ScrollView:
                MDList:
                    id: admin_options_list

                    OneLineListItem:
                        text: "Manage Users"  # <-- ADD THIS
                        on_release: root.show_user_management()

                    OneLineListItem:
                        text: "Manage Seasons"
                        on_release: root.show_season_management()

                    OneLineListItem:
                        text: "Manage Projects"
                        on_release: root.show_project_management()

                    OneLineListItem:
                        text: "View All Projects"
                        on_release: root.view_all_projects()

                    OneLineListItem:
                        text: "View All Users"
                        on_release: root.view_all_users()

                
<SeasonManagementScreen>:
    MDBoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            title: "Manage Seasons"
            elevation: 4
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
            right_action_items: [["plus", lambda x: root.show_add_season_dialog()]]
        
        ScrollView:
            MDList:
                id: season_list  # ← This MUST be here
                spacing: "10dp"
                padding: "10dp"
                
<ProjectManagementScreen>:
    MDBoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            title: "Manage Projects"
            elevation: 4
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
            right_action_items: [["plus", lambda x: root.show_add_project_dialog()], ["calendar", lambda x: root.show_season_switch_dialog()]]
        
        MDBoxLayout:
            size_hint_y: None
            height: "15dp"
            
        MDLabel:
            id: season_label
            size_hint_y: None
            height: "45dp"
            padding: "10dp"
            theme_text_color: "Secondary"
        
        ScrollView:
            MDList:
                id: project_list
                spacing: "10dp"
                padding: "10dp"

<UserManagementScreen>:
    MDBoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            title: "Manage Users"
            elevation: 4
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
            right_action_items: [["plus", lambda x: root.show_add_user_dialog()]]
        
        MDBoxLayout:
            size_hint_y: None
            height: "80dp"
            padding: "16dp"
            spacing: "8dp"
            
            MDTextField:
                id: search_field
                hint_text: "Search users..."
                mode: "rectangle"
                on_text: root.filter_list(self.text)
        
        ScrollView:
            MDList:
                id: user_list
                spacing: "10dp"
                padding: "10dp"
                
<AllProjectsScreen>:
    MDBoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            title: "All Projects"
            elevation: 4
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
            right_action_items: [["refresh", lambda x: root.refresh_list()]]
        
        MDBoxLayout:
            size_hint_y: None
            height: "75dp"
            padding: "16dp"
            spacing: "8dp"
            
            MDTextField:
                id: search_field
                hint_text: "Search projects..."
                mode: "rectangle"
                on_text: root.filter_list(self.text)
            
            MDFlatButton:
                icon: "filter"
                on_release: root.show_filter_options()
        
        ScrollView:
            MDList:
                id: project_list
                spacing: "10dp"
                padding: "10dp"
                
<AllUsersScreen>:
    MDBoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            title: "All Users"
            elevation: 4
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
            right_action_items: [["refresh", lambda x: root.refresh_list()]]
        
        MDBoxLayout:
            size_hint_y: None
            height: "75dp"
            padding: "16dp"
            spacing: "8dp"
            
            MDTextField:
                id: search_field
                hint_text: "Search users..."
                mode: "rectangle"
                on_text: root.filter_list(self.text)
            
            MDFlatButton:
                icon: "filter"
                on_release: root.show_filter_options()
        
        ScrollView:
            MDList:
                id: user_list
                spacing: "10dp"
                padding: "10dp"
                
<BagTagManagementScreen>:
    MDBoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            title: "Bag Tag Manager"
            elevation: 4
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
        
        ScrollView:
            MDBoxLayout:
                id: main_layout
                orientation: "vertical"
                spacing: "15dp"
                padding: "15dp"
                size_hint_y: None
                height: self.minimum_height
'''


class AdminLoginScreen(MDScreen):
    def go_back(self):
        self.manager.current = "login"

    def do_admin_login(self):
        username = self.ids.username_field.text.strip()
        password = self.ids.password_field.text.strip()

        admins = load_admins()

        if username in admins:
            stored_hash = admins[username]["password_hash"]
            if hash_password(password) == stored_hash:
                app = MDApp.get_running_app()
                app.current_admin = {
                    "username": username,
                    "role": admins[username]["role"]
                }

                self.manager.current = "admin_dashboard"
                self.ids.username_field.text = ""
                self.ids.password_field.text = ""
                return

        # Failed login - use dialog instead of Snackbar
        self.ids.password_field.text = ""
        self.show_message("Invalid username or password")

    def show_message(self, message):
        """Show a simple message dialog"""
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDRaisedButton

        dialog = MDDialog(
            text=message,
            buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()

class AdminDashboardScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu = None

    def open_admin_menu(self):
        if self.menu:
            self.menu.dismiss()

        menu_items = [
            {
                "text": "Seasons",
                "leading_icon": "calendar",
                "on_release": lambda x="seasons": self.menu_callback("seasons"),
            },
            {
                "text": "Projects",
                "leading_icon": "account-group",
                "on_release": lambda x="projects": self.menu_callback("projects"),
            },
            {
                "text": "Users",
                "leading_icon": "account",
                "on_release": lambda x="users": self.menu_callback("users"),
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
        self.menu.dismiss()
        if item == "seasons":
            self.show_season_management()
        elif item == "projects":
            self.show_project_management()
        elif item == "users":
            self.show_user_management()
        elif item == "settings":
            self.show_settings()

    def on_enter(self):
        app = MDApp.get_running_app()
        username = app.current_admin.get("username", "Unknown")
        role = app.current_admin.get("role", "admin")

        # Set display text
        if role == "superadmin":
            display_role = "Super Admin"
        else:
            display_role = "Faculty Admin"

        self.ids.welcome_label.text = f"Welcome, {username}"
        self.ids.role_label.text = f"Role: {display_role}"

        # Update list items based on role
        self.update_list_items()

    def update_list_items(self):
        """Update the dashboard list based on user role"""
        list_widget = self.ids.admin_options_list
        list_widget.clear_widgets()

        app = MDApp.get_running_app()
        role = app.current_admin.get("role", "admin")

        # Common items for all admins
        common_items = [
            ("Manage Seasons", "show_season_management"),
            ("Manage Projects", "show_project_management"),
            ("Manage Users", "show_user_management"),
            ("View All Projects", "view_all_projects"),
            ("View All Users", "view_all_users"),
        ]

        # Add common items
        for text, method in common_items:
            item = OneLineListItem(
                text=text,
                on_release=lambda x, m=method: getattr(self, m)()
            )
            list_widget.add_widget(item)

    def show_settings(self):
        """Show settings dialog"""
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

        dark_btn = MDRaisedButton(
            text="Dark Mode",
            size_hint_x=0.6,
            height=40,
            on_release=lambda x: self.toggle_theme()
        )

        dark_status = MDLabel(
            text=current_theme,
            size_hint_x=0.4,
            halign="center",
            theme_text_color="Secondary"
        )

        dark_row.add_widget(dark_btn)
        dark_row.add_widget(dark_status)
        content.add_widget(dark_row)

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

        # Save preference
        prefs_file = Path.home() / "field_data" / "preferences.json"
        prefs_file.parent.mkdir(exist_ok=True)

        if prefs_file.exists():
            with open(prefs_file) as f:
                prefs = json.load(f)
        else:
            prefs = {}

        prefs['theme_style'] = app.theme_cls.theme_style
        with open(prefs_file, 'w') as f:
            json.dump(prefs, f, indent=2)

        # Update the status label if the dialog is still open
        if hasattr(self, 'settings_dialog') and self.settings_dialog:
            current_theme = "ON" if app.theme_cls.theme_style == "Dark" else "OFF"
            for child in self.settings_dialog.content_cls.children:
                if isinstance(child, MDBoxLayout):
                    for subchild in child.children:
                        if isinstance(subchild, MDLabel) and subchild.text in ["ON", "OFF"]:
                            subchild.text = current_theme
                            break


    def show_season_management(self):
        self.manager.current = "season_management"

    def show_project_management(self):
        self.manager.current = "project_management"

    def show_user_management(self):
        self.manager.current = "user_management"

    def view_all_projects(self):
        """Navigate to view all projects"""
        self.manager.current = "all_projects"

    def view_all_users(self):
        """Navigate to view all users"""
        self.manager.current = "all_users"

    def logout(self):
        app = MDApp.get_running_app()
        app.current_admin = None
        self.manager.current = "admin_login"

class ResetPasswordContent(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Builder.load_string('''
MDBoxLayout:
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "180dp"

    MDTextField:
        id: new_password_field
        hint_text: "New Password"
        mode: "rectangle"
        password: True

    MDTextField:
        id: confirm_field
        hint_text: "Confirm Password"
        mode: "rectangle"
        password: True
'''))

"""  def open_role_menu(self):
        # Only show superadmin option if current user is superadmin
        menu_items = [
            {"text": "Admin", "on_release": lambda x="admin": self.set_role("admin")},
        ]

        # Only add superadmin option for superadmins
        if self.current_role == "superadmin":
            menu_items.append(
                {"text": "Superadmin", "on_release": lambda x="superadmin": self.set_role("superadmin")}
            )

        self.role_menu = MDDropdownMenu(
            caller=self.ids.role_button,
            items=menu_items,
            width_mult=3,
        )
        self.role_menu.open()

    def set_role(self, role):
        display_text = "Superadmin" if role == "superadmin" else "Admin"
        self.ids.role_button.text = display_text
        self.selected_role = role
        if self.role_menu:
            self.role_menu.dismiss()

    def get_data(self):
        return {
            'username': self.ids.username_field.text.strip(),
            'password': self.ids.password_field.text.strip(),
            'confirm': self.ids.confirm_field.text.strip(),
            'role': self.selected_role
        }"""

# Load the KV string
Builder.load_string('''
<AddAdminContent>:
    MDBoxLayout:
        orientation: "vertical"
        spacing: "15dp"
        padding: "20dp"
        size_hint_y: None
        height: "320dp"
        width: "400dp"

        MDTextField:
            id: username_field
            hint_text: "Username"
            mode: "rectangle"
            size_hint_y: None
            height: "50dp"

        MDTextField:
            id: password_field
            hint_text: "Password"
            mode: "rectangle"
            password: True
            size_hint_y: None
            height: "50dp"

        MDTextField:
            id: confirm_field
            hint_text: "Confirm Password"
            mode: "rectangle"
            password: True
            size_hint_y: None
            height: "50dp"

        MDBoxLayout:
            orientation: "horizontal"
            spacing: "10dp"
            size_hint_y: None
            height: "50dp"
            pos_hint: {"center_x": 0.5}

            MDLabel:
                text: "Role:"
                size_hint_x: 0.3
                halign: "right"
                valign: "middle"
                theme_text_color: "Secondary"

            MDRaisedButton:
                id: role_button
                text: "Admin (default)"
                size_hint_x: 0.7
                size_hint_y: None
                height: "40dp"
                on_release: root.open_role_menu()
''')


class SeasonManagementScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.all_seasons = []
        self.filter_menu = None

    def on_enter(self):
        """Called when screen is shown"""
        self.refresh_list()
        self.check_auto_closeout()

    def check_auto_closeout(self):
        """Auto-close seasons that have passed their end date"""
        seasons = load_seasons()
        today = datetime.now().date()
        changed = False

        for season_id, data in seasons.items():
            # Skip if already closed
            if data.get('status') == 'closed':
                continue

            # Check if end date exists and is passed
            end_date_str = data.get('end_date')
            if end_date_str:
                try:
                    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
                    if end_date < today:
                        data['status'] = 'closed'
                        data['closed_at'] = today.isoformat()
                        data['closed_by'] = 'system'
                        changed = True
                except:
                    pass  # Invalid date format, skip

        if changed:
            save_seasons(seasons)
            self.refresh_list()

    def refresh_list(self):
        """Load and display all seasons"""
        self.ids.season_list.clear_widgets()
        seasons = load_seasons()
        self.all_seasons = list(seasons.items())

        for season_id, data in seasons.items():
            self.add_season_to_list(season_id, data)

    def add_season_to_list(self, season_id, data):
        """Add a single season item to the list UI"""
        card = MDCard(
            orientation="vertical",
            size_hint_y=None,
            height="140dp",  # Taller to accommodate more info
            padding="10dp",
            spacing="5dp",
            elevation=2
        )

        # Header with organization and year
        header = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height="30dp"
        )

        org = data.get('organization', 'KFFS')
        year = data.get('year', 'Unknown')
        status = data.get('status', 'active')

        # Status indicator
        status_color = (0.2, 0.8, 0.2, 1) if status == 'active' else (0.5, 0.5, 0.5, 1)
        status_text = "ACTIVE" if status == 'active' else "CLOSED"

        header.add_widget(
            MDLabel(
                text=f"{org} {year}",
                theme_text_color="Primary",
                font_style="H6",
                size_hint_x=0.5
            )
        )
        header.add_widget(
            MDLabel(
                text=status_text,
                theme_text_color="Custom",
                text_color=status_color,
                font_style="Subtitle1",
                size_hint_x=0.3,
                halign="center"
            )
        )

        # Project count
        projects = data.get('projects', 0)
        header.add_widget(
            MDLabel(
                text=f"Projects: {projects}",
                theme_text_color="Secondary",
                font_style="Subtitle1",
                size_hint_x=0.2,
                halign="right"
            )
        )
        card.add_widget(header)

        # Date range
        dates = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height="25dp",
            spacing="10dp"
        )

        start = data.get('start_date', 'Not set')
        end = data.get('end_date', 'Not set')

        dates.add_widget(
            MDLabel(
                text=f"Start: {start}",
                theme_text_color="Secondary",
                font_style="Caption",
                size_hint_x=0.5
            )
        )
        dates.add_widget(
            MDLabel(
                text=f"End: {end}",
                theme_text_color="Secondary",
                font_style="Caption",
                size_hint_x=0.5,
                halign="right"
            )
        )
        card.add_widget(dates)

        # Closed info (if closed)
        if status == 'closed' and 'closed_at' in data:
            closed_info = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height="20dp"
            )
            closed_info.add_widget(
                MDLabel(
                    text=f"Closed: {data['closed_at']} by {data.get('closed_by', 'unknown')}",
                    theme_text_color="Hint",
                    font_style="Caption"
                )
            )
            card.add_widget(closed_info)

        # Action buttons
        actions = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height="40dp",
            spacing="10dp"
        )

        # View projects button
        view_btn = MDRaisedButton(
            text="VIEW PROJECTS",
            size_hint=(None, None),
            size=("120dp", "35dp"),
            font_size="11sp",
            disabled=(status == 'closed'),  # Disable if season is closed
            on_release=lambda x, s=season_id: self.view_projects(s)
        )
        actions.add_widget(view_btn)

        # Close season button (only if active)
        if status == 'active':
            close_btn = MDRaisedButton(
                text="CLOSE",
                size_hint=(None, None),
                size=("70dp", "35dp"),
                font_size="11sp",
                md_bg_color=(0.8, 0.5, 0.2, 1),  # Orange
                on_release=lambda x, s=season_id: self.confirm_close_season(s)
            )
            actions.add_widget(close_btn)

        # Delete button (available to admins)
        delete_btn = MDRaisedButton(
            text="DELETE",
            size_hint=(None, None),
            size=("70dp", "35dp"),
            font_size="11sp",
            md_bg_color=(0.8, 0.2, 0.2, 1),
            on_release=lambda x, s=season_id: self.confirm_delete_season(s)
        )
        actions.add_widget(delete_btn)

        card.add_widget(actions)
        self.ids.season_list.add_widget(card)

    def show_add_season_dialog(self):
        """Show dialog to add a new season with dates"""
        content = MDBoxLayout(
            orientation="vertical",
            spacing="10dp",
            padding="20dp",
            size_hint_y=None,
            height="250dp"
        )

        # Organization field (defaults to KFFS but editable)
        self.season_org = MDTextField(
            hint_text="Organization",
            text="KFFS"
        )

        # Year field
        self.season_year = MDTextField(
            hint_text="Year (YYYY)",
            text=datetime.now().strftime("%Y")
        )

        # Start date field
        self.season_start = MDTextField(
            hint_text="Start Date (YYYY-MM-DD)",
            text=datetime.now().strftime("%Y-%m-%d")  # Default to today
        )

        # End date field (auto-calculate 1 year later as default)
        next_year = datetime.now().replace(year=datetime.now().year + 1)
        self.season_end = MDTextField(
            hint_text="End Date (YYYY-MM-DD)",
            text=next_year.strftime("%Y-%m-%d")
        )

        content.add_widget(self.season_org)
        content.add_widget(self.season_year)
        content.add_widget(self.season_start)
        content.add_widget(self.season_end)

        self.dialog = MDDialog(
            title="Add New Season",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text="CREATE", on_release=lambda x: self.create_season())
            ]
        )
        self.dialog.open()

    def create_season(self):
        """Create a new season"""
        org = self.season_org.text.strip() or "KFFS"
        year = self.season_year.text.strip()
        start = self.season_start.text.strip()
        end = self.season_end.text.strip()

        # Validation
        if not year or not year.isdigit() or len(year) != 4:
            self.show_message("Please enter a valid 4-digit year")
            return

        # Validate date format
        try:
            if start:
                datetime.strptime(start, "%Y-%m-%d")
            if end:
                datetime.strptime(end, "%Y-%m-%d")
        except ValueError:
            self.show_message("Dates must be in YYYY-MM-DD format")
            return

        # Load existing seasons
        seasons = load_seasons()

        # Season ID is just the year
        season_id = year

        # Check if this organization already has this year
        for existing_id, data in seasons.items():
            if existing_id == season_id and data.get('organization') == org:
                self.show_message(f"{org} {year} already exists")
                return

        # Create new season
        seasons[season_id] = {
            "organization": org,
            "year": year,
            "start_date": start,
            "end_date": end,
            "status": "active",
            "projects": 0,
            "created_at": datetime.now().isoformat(),
            "created_by": MDApp.get_running_app().current_admin.get("username")
        }

        save_seasons(seasons)

        self.dialog.dismiss()
        self.refresh_list()
        self.show_message(f"Season {org} {year} created")

    def confirm_close_season(self, season_id):
        """Confirm manual season closure"""
        seasons = load_seasons()
        season = seasons.get(season_id, {})
        org = season.get('organization', 'Unknown')
        year = season.get('year', 'Unknown')

        self.dialog = MDDialog(
            title="Close Season",
            text=f"Close {org} {year}?\n\nOnce closed, data can only be modified via desktop app.",
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(
                    text="CLOSE SEASON",
                    md_bg_color=(0.8, 0.5, 0.2, 1),
                    on_release=lambda x: self.close_season(season_id)
                )
            ]
        )
        self.dialog.open()

    def close_season(self, season_id):
        """Manually close a season"""
        seasons = load_seasons()
        if season_id in seasons:
            seasons[season_id]['status'] = 'closed'
            seasons[season_id]['closed_at'] = datetime.now().isoformat()
            seasons[season_id]['closed_by'] = MDApp.get_running_app().current_admin.get("username")
            save_seasons(seasons)
            self.dialog.dismiss()
            self.refresh_list()
            self.show_message("Season closed")

    def view_projects(self, season_id):
        """Navigate to projects for this season"""
        app = MDApp.get_running_app()
        app.current_season = season_id
        self.manager.current = "project_management"

    def confirm_delete_season(self, season_id):
        """Confirm season deletion"""
        seasons = load_seasons()
        season = seasons.get(season_id, {})
        org = season.get('organization', 'Unknown')
        year = season.get('year', 'Unknown')

        self.dialog = MDDialog(
            title="Delete Season",
            text=f"Delete {org} {year}?\n\nThis cannot be undone!",
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(
                    text="DELETE",
                    md_bg_color=(0.8, 0.2, 0.2, 1),
                    on_release=lambda x: self.delete_season(season_id)
                )
            ]
        )
        self.dialog.open()

    def delete_season(self, season_id):
        """Delete a season"""
        seasons = load_seasons()
        if season_id in seasons:
            del seasons[season_id]
            save_seasons(seasons)
            self.dialog.dismiss()
            self.refresh_list()
            self.show_message("Season deleted")

    def go_back(self):
        self.manager.current = "admin_dashboard"

    def show_message(self, message):
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDRaisedButton
        dialog = MDDialog(
            text=message,
            buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()


class ProjectManagementScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.all_projects = []
        self.filter_menu = None
        self.leader_menu = None
        self.reassign_menu = None
        self.contributor_menu = None
        self.selected_leader = None
        self.reassign_leader = None
        self.selected_contributor = None
        self.selected_contributor_name = None
        self.current_project_id = None
        self.current_project_name = None
        self.current_season_id = None
        self.current_season_display = None

    def on_enter(self):
        """Called when screen is shown - load most recent active season"""
        self.load_most_recent_season()

    def load_most_recent_season(self):
        """Find and load the most recent active season"""
        seasons = load_seasons()
        active_seasons = []

        for season_id, data in seasons.items():
            if data.get('status') == 'active':
                try:
                    year = int(data.get('year', season_id))
                    active_seasons.append((year, season_id, data))
                except:
                    pass

        if not active_seasons:
            self.show_no_seasons_message()
            return

        # Sort by year descending and get the most recent
        active_seasons.sort(reverse=True)
        year, season_id, data = active_seasons[0]

        org = data.get('organization', 'KFFS')
        self.current_season_id = season_id
        self.current_season_display = f"{org} {year}"

        # Update the label with season and switch button
        self.update_season_header()
        self.refresh_list()

    def update_season_header(self):
        """Update the top bar with season info and switch button"""
        # This will be handled in KV - we'll update the label
        self.ids.season_label.text = f"Season: {self.current_season_display}"

    def show_no_seasons_message(self):
        """Show message when no active seasons exist"""
        self.ids.project_list.clear_widgets()
        self.ids.season_label.text = "No active seasons"

        # Add a message card
        card = MDCard(
            orientation="vertical",
            size_hint_y=None,
            height="100dp",
            padding="20dp",
            spacing="10dp"
        )
        card.add_widget(
            MDLabel(
                text="No active seasons found.",
                halign="center",
                theme_text_color="Secondary"
            )
        )
        card.add_widget(
            MDLabel(
                text="Please create a season first in Season Management.",
                halign="center",
                theme_text_color="Hint",
                font_style="Caption"
            )
        )
        self.ids.project_list.add_widget(card)

    def show_message(self, message):
        """Show a simple message dialog"""
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDRaisedButton
        dialog = MDDialog(
            text=message,
            buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()

    def show_season_switch_dialog(self):
        """Show dialog to switch to a different active season"""
        seasons = load_seasons()
        active_seasons = []

        for season_id, data in seasons.items():
            if data.get('status') == 'active':
                try:
                    year = int(data.get('year', season_id))
                    active_seasons.append((year, season_id, data))
                except:
                    pass

        if not active_seasons:
            self.show_message("No other active seasons available")
            return

        # Sort by year descending
        active_seasons.sort(reverse=True)

        content = MDBoxLayout(
            orientation="vertical",
            spacing="10dp",
            padding="20dp",
            size_hint_y=None,
            height="300dp"
        )

        content.add_widget(
            MDLabel(
                text="Select Season:",
                theme_text_color="Primary",
                font_style="H6",
                size_hint_y=None,
                height="30dp"
            )
        )

        season_list = MDList(size_hint_y=None)
        season_list.bind(minimum_height=season_list.setter('height'))

        for year, season_id, data in active_seasons:
            org = data.get('organization', 'KFFS')
            display = f"{org} {year}"

            # Highlight the current season
            if season_id == self.current_season_id:
                display += " (current)"

            item = OneLineListItem(
                text=display,
                on_release=lambda x, s=season_id, d=display: self.switch_season(s, d)
            )
            season_list.add_widget(item)

        scroll = ScrollView(size_hint_y=None, height="250dp")
        scroll.add_widget(season_list)
        content.add_widget(scroll)

        self.season_switch_dialog = MDDialog(
            title="Switch Season",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda x: self.season_switch_dialog.dismiss()
                )
            ]
        )
        self.season_switch_dialog.open()

    def switch_season(self, season_id, display):
        """Switch to a different season"""
        self.current_season_id = season_id
        self.current_season_display = display
        self.update_season_header()
        self.refresh_list()
        self.season_switch_dialog.dismiss()
        self.show_message(f"Switched to {display}")

    def show_project_qr(self, project_id):
        import qrcode
        from io import BytesIO
        from kivy.core.image import Image as CoreImage
        from kivy.uix.image import Image
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDRaisedButton
        from kivy.uix.boxlayout import BoxLayout
        import json

        projects = load_projects()
        project = projects.get(project_id, {})
        users = load_users()

        project_users = {}
        for user_id, user_data in users.items():
            if project_id in user_data.get('projects', []):
                project_users[user_id] = {
                    "name": user_data.get('name', ''),
                    "first_name": user_data.get('first_name', ''),
                    "last_name": user_data.get('last_name', ''),
                    "user_type": user_data.get('user_type', 'seasonal'),
                    "season": user_data.get('season', '')
                }

        config_data = {
            "version": "1.0",
            "project_id": project_id,
            "project_name": project.get('name', 'Unnamed Project'),
            "project_leader": project.get('leader', ''),
            "season_id": self.current_season_id,
            "users": project_users
        }

        config_json = json.dumps(config_data)

        # Generate QR with qrcode (no Pillow needed — use pure python renderer)
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=8,
            border=4,
        )
        qr.add_data(config_json)
        qr.make(fit=True)

        # Use the pure-SVG or BytesIO PNG path
        # qrcode can render to PNG via its own image factory without Pillow
        # if we use the PilImage factory it needs Pillow, so we use StyledPilImage
        # alternative: use qrcode's SVG factory
        try:
            # Try PNG path (works if Pillow present, which it may be via kivy)
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer)
            buffer.seek(0)
            texture = CoreImage(buffer, ext='png').texture
        except Exception:
            # Fallback: SVG rendered as PNG via pure path
            import qrcode.image.svg as qr_svg
            factory = qr_svg.SvgPathImage
            img = qr.make_image(image_factory=factory)
            buffer = BytesIO()
            img.save(buffer)
            buffer.seek(0)
            # SVG can't go directly to CoreImage — show message instead
            self.show_message(
                f"QR data ready for project {project_id}.\n"
                f"Install Pillow to display QR visually."
            )
            return

        qr_widget = Image(
            texture=texture,
            size_hint=(None, None),
            size=(300, 300)
        )

        content = BoxLayout(
            orientation='vertical',
            spacing=10,
            padding=20,
            size_hint_y=None,
            height=450
        )
        from kivymd.uix.label import MDLabel
        content.add_widget(MDLabel(
            text=f"Project: {project.get('name', project_id)}",
            font_style="H6",
            halign="center",
            size_hint_y=None,
            height=30
        ))
        content.add_widget(qr_widget)
        content.add_widget(MDLabel(
            text=f"Users: {len(project_users)}",
            theme_text_color="Secondary",
            halign="center",
            size_hint_y=None,
            height=30
        ))
        content.add_widget(MDLabel(
            text="Scan from Field App → Join Project",
            theme_text_color="Hint",
            halign="center",
            font_style="Caption",
            size_hint_y=None,
            height=40
        ))

        self.qr_dialog = MDDialog(
            title="Project QR Code",
            type="custom",
            content_cls=content,
            size_hint=(0.9, None),
            height=550,
            buttons=[
                MDRaisedButton(
                    text="CLOSE",
                    on_release=lambda x: self.qr_dialog.dismiss()
                )
            ]
        )
        self.qr_dialog.open()

    def show_add_project_dialog(self):
        """Show dialog to add a new project"""
        content = MDBoxLayout(
            orientation="vertical",
            spacing="10dp",
            padding="20dp",
            size_hint_y=None,
            height="280dp"
        )

        self.project_name = MDTextField(
            hint_text="Project Name",
            mode="rectangle",
            size_hint_y=None,
            height="50dp"
        )

        self.project_desc = MDTextField(
            hint_text="Description (optional)",
            mode="rectangle",
            multiline=True,
            size_hint_y=None,
            height="70dp"
        )

        leader_label = MDLabel(
            text="Project Leader:",
            theme_text_color="Secondary",
            size_hint_y=None,
            height="20dp"
        )

        admins = load_admins()
        self.leader_names = []
        self.leader_usernames = []

        for username, data in admins.items():
            self.leader_names.append(f"{username} ({data['role']})")
            self.leader_usernames.append(username)

        self.leader_button = MDRaisedButton(
            text="Select Project Leader",
            size_hint_y=None,
            height="45dp",
            on_release=lambda x: self.open_leader_menu()
        )
        self.selected_leader = None

        content.add_widget(self.project_name)
        content.add_widget(self.project_desc)
        content.add_widget(leader_label)
        content.add_widget(self.leader_button)

        self.dialog = MDDialog(
            title="Add New Project",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text="CREATE", on_release=lambda x: self.create_project())
            ]
        )
        self.dialog.open()

    def add_project_to_list(self, project_id, data):
        """Add a single project item to the list UI"""
        card = MDCard(
            orientation="vertical",
            size_hint_y=None,
            height="235dp",
            padding="15dp",
            spacing="8dp",
            elevation=2,
            radius=[10, 10, 10, 10]
        )
        top_spacer = MDBoxLayout(
            size_hint_y=None,
            height="10dp"
        )
        card.add_widget(top_spacer)

        # Header with project ID and name
        header = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height="35dp",
            spacing="10dp"
        )

        project_name = data.get('name', 'Unnamed Project')
        status = data.get('status', 'active')

        status_color = (0.2, 0.8, 0.2, 1) if status == 'active' else (0.5, 0.5, 0.5, 1)
        status_text = "● ACTIVE" if status == 'active' else "● CLOSED"

        header.add_widget(
            MDLabel(
                text=f"Project {project_id}: {project_name}",
                theme_text_color="Primary",
                font_style="H6",
                size_hint_x=0.7
            )
        )

        status_label = MDLabel(
            text=status_text,
            theme_text_color="Custom",
            text_color=status_color,
            font_style="Subtitle1",
            size_hint_x=0.3,
            halign="right"
        )
        header.add_widget(status_label)
        card.add_widget(header)

        # Leader info
        leader_box = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height="25dp"
        )
        project_leader = data.get('leader_name', 'Unassigned')
        leader_box.add_widget(
            MDLabel(
                text=f"👤 Leader: {project_leader}",
                theme_text_color="Secondary",
                font_style="Subtitle2"
            )
        )
        card.add_widget(leader_box)

        # Contributors section
        contributors = data.get('contributors', [])
        contributor_names = data.get('contributor_names', [])

        if contributors:
            display_contributors = contributor_names[:3]
            remaining = len(contributors) - 3
            contrib_text = "👥 Contributors: " + ", ".join(display_contributors)
            if remaining > 0:
                contrib_text += f" +{remaining} more"
        else:
            contrib_text = "👥 No contributors assigned"

        contrib_label = MDLabel(
            text=contrib_text,
            theme_text_color="Hint",
            font_style="Caption",
            size_hint_y=None,
            height="20dp"
        )
        card.add_widget(contrib_label)

        # Collection count
        collections = data.get('collections', 0)
        collection_label = MDLabel(
            text=f"📊 Collections: {collections}",
            theme_text_color="Hint",
            font_style="Caption",
            size_hint_y=None,
            height="20dp"
        )
        card.add_widget(collection_label)

        # Action buttons
        actions = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height="45dp",
            spacing="8dp",
            padding=["0dp", "5dp", "0dp", "0dp"]
        )

        app = MDApp.get_running_app()
        current_user = app.current_admin.get("username")
        current_role = app.current_admin.get("role")
        project_leader_username = data.get('leader')
        status = data.get('status', 'active')

        button_height = "40dp"
        button_font_size = "11sp"
        contrib_color = (0.5, 0.3, 0.8, 1)
        close_color = (0.8, 0.5, 0.2, 1)
        delete_color = (0.8, 0.2, 0.2, 1)

        # Determine what the current user can do
        can_edit = (current_role == "superadmin" or current_user == project_leader_username)
        is_superadmin = (current_role == "superadmin")

        # Count how many buttons will be shown to calculate spacing
        button_count = 0
        if can_edit:
            button_count += 1
        if is_superadmin:
            button_count += 1
        if can_edit and status == 'active' and (
                current_role == "superadmin" or current_user == project_leader_username):
            button_count += 1

        # Calculate button width based on count (with 3 columns, each gets equal width)
        if button_count == 3:
            button_width = 0.33
        elif button_count == 2:
            button_width = 0.5
        else:
            button_width = 1.0

        # 1. CONTRIBUTORS button (only visible if user can edit the project)
        if can_edit:
            contrib_btn = MDRaisedButton(
                text="CONTRIBUTORS",
                size_hint=(button_width, None),
                height=button_height,
                font_size=button_font_size,
                md_bg_color=contrib_color,
                disabled=(status == 'closed'),
                on_release=lambda x, p=project_id: self.manage_contributors(p)
            )
            actions.add_widget(contrib_btn)

        if can_edit or is_superadmin:
            qr_btn = MDRaisedButton(
                text="QR CODE",
                size_hint=(0.2, None),
                height=button_height,
                font_size=button_font_size,
                md_bg_color=(0.3, 0.5, 0.7, 1),  # Blue
                on_release=lambda x, p=project_id: self.show_project_qr(p)
            )
            actions.add_widget(qr_btn)

        # 2. BAG TAGS button (only visible to superadmin)
        if is_superadmin:
            bagtag_btn = MDRaisedButton(
                text="BAG TAGS",
                size_hint=(button_width, None),
                height=button_height,
                font_size=button_font_size,
                md_bg_color=(0.6, 0.4, 0.2, 1),  # Brown
                on_release=lambda x, p=project_id: self.manage_bag_tags(p)
            )
            actions.add_widget(bagtag_btn)

        # 3. CLOSE button (leader or superadmin, and only if active)
        can_close = (current_role == "superadmin" or current_user == project_leader_username)
        if can_close and status == 'active':
            close_btn = MDRaisedButton(
                text="CLOSE",
                size_hint=(button_width, None),
                height=button_height,
                font_size=button_font_size,
                md_bg_color=close_color,
                on_release=lambda x, p=project_id: self.confirm_close_project(p)
            )
            actions.add_widget(close_btn)

        # Add spacers if needed to maintain layout
        if button_count == 1:
            # Add spacers on both sides to center the single button
            spacer = MDBoxLayout(size_hint_x=0.33)
            actions.add_widget(spacer, index=0)
            actions.add_widget(spacer)

        card.add_widget(actions)

        # Superadmin additional actions (reassign and delete)
        if is_superadmin:
            admin_actions = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height="35dp",
                spacing="8dp"
            )

            reassign_btn = MDRaisedButton(
                text="REASSIGN LEADER",
                size_hint=(0.5, None),
                height="30dp",
                font_size="10sp",
                md_bg_color=(0.3, 0.3, 0.3, 1),
                on_release=lambda x, p=project_id: self.show_reassign_dialog(p)
            )
            admin_actions.add_widget(reassign_btn)

            delete_btn = MDRaisedButton(
                text="DELETE",
                size_hint=(0.5, None),
                height="30dp",
                font_size="10sp",
                md_bg_color=delete_color,
                on_release=lambda x, p=project_id: self.confirm_delete_project(p)
            )
            admin_actions.add_widget(delete_btn)

            card.add_widget(admin_actions)

        self.ids.project_list.add_widget(card)

    def open_leader_menu(self):
        """Open dropdown menu to select project leader"""
        menu_items = []
        admins = load_admins()

        for username, data in admins.items():
            display = f"{username} ({data['role']})"
            menu_items.append({
                "text": display,
                "on_release": lambda x=username, d=display: self.set_leader(x, d)
            })

        self.leader_menu = MDDropdownMenu(
            caller=self.leader_button,
            items=menu_items,
            width_mult=4,
        )
        self.leader_menu.open()

    def set_leader(self, username, display):
        """Set the selected project leader"""
        self.selected_leader = username
        self.leader_button.text = display
        self.leader_menu.dismiss()

    # In create_project method
    def create_project(self):
        """Create a new project (independent of season)"""
        app = MDApp.get_running_app()
        name = self.project_name.text.strip()
        desc = self.project_desc.text.strip()

        if not name:
            self.show_message("Project name required")
            return

        if not self.selected_leader:
            self.show_message("Please select a project leader")
            return

        projects = load_projects()

        # Find next available project ID (not per season, global)
        existing_ids = []
        for pid in projects.keys():
            try:
                existing_ids.append(int(pid))
            except:
                pass

        next_id = 1
        if existing_ids:
            next_id = max(existing_ids) + 1

        project_id = f"{next_id:03d}"  # 3-digit project ID (001, 002, etc.)

        admins = load_admins()
        leader_data = admins.get(self.selected_leader, {})
        leader_name = f"{self.selected_leader} ({leader_data.get('role', 'admin')})"
        leader_user_id = leader_data.get("user_id")

        projects[project_id] = {
            "project_id": project_id,
            "name": name,
            "description": desc,
            "leader": self.selected_leader,
            "leader_name": leader_name,
            "leader_user_id": leader_user_id,
            "status": "active",  # Can be "active" or "closed"
            "created_at": datetime.now().isoformat(),
            "created_by": app.current_admin.get("username")
        }

        save_projects(projects)
        self.refresh_list()
        self.show_message(f"Project {project_id} created")

    def manage_contributors(self, project_id):
        """Open contributor management dialog"""
        projects = load_projects()
        project = projects.get(project_id, {})
        self.current_project_id = project_id
        self.current_project_name = project.get('name', 'Unknown')

        content = MDBoxLayout(
            orientation="vertical",
            spacing="10dp",
            padding="10dp",
            size_hint_y=None,
            height="400dp"
        )

        content.add_widget(
            MDLabel(
                text=f"Project {project_id}: {self.current_project_name}",
                theme_text_color="Primary",
                font_style="H6",
                size_hint_y=None,
                height="30dp"
            )
        )

        content.add_widget(
            MDLabel(
                text="Current Contributors:",
                theme_text_color="Secondary",
                font_style="Subtitle1",
                size_hint_y=None,
                height="25dp"
            )
        )

        self.contributors_list = MDList(size_hint_y=None)
        self.contributors_list.bind(minimum_height=self.contributors_list.setter('height'))

        contributors = project.get('contributors', [])
        contributor_names = project.get('contributor_names', [])

        for i, (username, name) in enumerate(zip(contributors, contributor_names)):
            item = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height="40dp",
                spacing="10dp"
            )

            item.add_widget(
                MDLabel(
                    text=name,
                    size_hint_x=0.7,
                    halign="left"
                )
            )

            remove_btn = MDRaisedButton(
                text="REMOVE",
                size_hint=(None, None),
                size=("70dp", "30dp"),
                font_size="10sp",
                md_bg_color=(0.8, 0.2, 0.2, 1),
                on_release=lambda x, u=username: self.remove_contributor(u)
            )
            item.add_widget(remove_btn)

            self.contributors_list.add_widget(item)

        scroll = ScrollView(size_hint_y=None, height="200dp")
        scroll.add_widget(self.contributors_list)
        content.add_widget(scroll)

        content.add_widget(
            MDLabel(
                text="Add New Contributor:",
                theme_text_color="Secondary",
                font_style="Subtitle1",
                size_hint_y=None,
                height="25dp"
            )
        )

        self.contributor_button = MDRaisedButton(
            text="SELECT USER",
            size_hint_y=None,
            height="45dp",
            on_release=lambda x: self.open_contributor_menu()
        )
        self.selected_contributor = None
        self.selected_contributor_name = None
        content.add_widget(self.contributor_button)

        self.contributor_dialog = MDDialog(
            title="Manage Contributors",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="DONE", on_release=lambda x: self.contributor_dialog.dismiss())
            ]
        )
        self.contributor_dialog.open()

    def open_contributor_menu(self):
        """Open dropdown to select a user to add as contributor"""
        menu_items = []
        users = load_users()
        current_season_id = self.current_season_id

        projects = load_projects()
        project = projects.get(self.current_project_id, {})
        existing_contributors = project.get('contributors', [])

        for user_id, data in users.items():
            if data.get('season') == current_season_id and user_id not in existing_contributors:
                display = f"{user_id}: {data.get('name', 'Unknown')}"
                menu_items.append({
                    "text": display,
                    "on_release": lambda x=user_id, d=display: self.confirm_add_contributor(x, d)
                })

        if not menu_items:
            self.show_message("No users available to add as contributors")
            return

        self.contributor_menu = MDDropdownMenu(
            caller=self.contributor_button,
            items=menu_items,
            width_mult=4,
        )
        self.contributor_menu.open()

    def confirm_add_contributor(self, user_id, display):
        """Show confirmation dialog before adding contributor"""
        self.confirm_user_id = user_id
        self.confirm_user_display = display

        # Close the dropdown first
        if self.contributor_menu:
            self.contributor_menu.dismiss()

        # Show confirmation dialog
        self.confirm_dialog = MDDialog(
            title="Add Contributor",
            text=f"Add {display} as a contributor to this project?",
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda x: self.confirm_dialog.dismiss()
                ),
                MDRaisedButton(
                    text="ADD",
                    md_bg_color=(0.2, 0.6, 0.2, 1),
                    on_release=lambda x: self.add_contributor_immediate(self.confirm_user_id, self.confirm_user_display)
                )
            ]
        )
        self.confirm_dialog.open()

    def add_contributor_immediate(self, user_id, display):
        """Add contributor after confirmation"""
        print(f"Adding contributor: user_id={user_id}, display={display}")

        # Close confirmation dialog
        if self.confirm_dialog:
            self.confirm_dialog.dismiss()

        projects = load_projects()
        users = load_users()

        if self.current_project_id in projects:
            project = projects[self.current_project_id]

            if 'contributors' not in project:
                project['contributors'] = []
            if 'contributor_names' not in project:
                project['contributor_names'] = []

            if user_id in project['contributors']:
                self.show_message("This user is already a contributor")
                return

            user_data = users.get(user_id, {})
            user_name = user_data.get('name', user_id)
            display_name = f"{user_id}: {user_name}"

            project['contributors'].append(user_id)
            project['contributor_names'].append(display_name)

            if user_id in users:
                if 'projects' not in users[user_id]:
                    users[user_id]['projects'] = []
                if self.current_project_id not in users[user_id]['projects']:
                    users[user_id]['projects'].append(self.current_project_id)

            save_projects(projects)
            save_users(users)

            # Refresh the contributor dialog
            self.contributor_dialog.dismiss()
            self.manage_contributors(self.current_project_id)
            self.show_message(f"Added {display} as contributor")

    def set_contributor(self, member_id, display):
        """Set the selected contributor"""
        self.selected_contributor = member_id
        self.selected_contributor_name = display
        self.contributor_button.text = display
        self.contributor_menu.dismiss()

    def add_contributor(self):
        """Add selected user as contributor to the project (and add project to user)"""
        if not self.selected_contributor:
            self.show_message("Please select a user to add")
            return

        projects = load_projects()
        users = load_users()

        if self.current_project_id in projects:
            project = projects[self.current_project_id]

            if 'contributors' not in project:
                project['contributors'] = []
            if 'contributor_names' not in project:
                project['contributor_names'] = []

            if self.selected_contributor in project['contributors']:
                self.show_message("This user is already a contributor")
                return

            # Get user's name
            user_data = users.get(self.selected_contributor, {})
            user_name = user_data.get('name', self.selected_contributor)
            # Create display name with user ID
            display_name = f"{self.selected_contributor}: {user_name}"

            # Add contributor to project
            project['contributors'].append(self.selected_contributor)
            project['contributor_names'].append(display_name)  # Store with ID

            # ALSO add project to user's projects list
            if self.selected_contributor in users:
                if 'projects' not in users[self.selected_contributor]:
                    users[self.selected_contributor]['projects'] = []

                if self.current_project_id not in users[self.selected_contributor]['projects']:
                    users[self.selected_contributor]['projects'].append(self.current_project_id)

            save_projects(projects)
            save_users(users)

            self.contributor_dialog.dismiss()
            self.manage_contributors(self.current_project_id)
            self.show_message(f"User {self.selected_contributor} added as contributor")

    def remove_contributor(self, user_id):
        """Show confirmation before removing a contributor"""
        # Find the contributor's name for the confirmation message
        projects = load_projects()
        project = projects.get(self.current_project_id, {})
        contributor_names = project.get('contributor_names', [])

        # Find the display name
        display_name = user_id
        for name in contributor_names:
            if name.startswith(f"{user_id}:"):
                display_name = name
                break

        self.confirm_remove_dialog = MDDialog(
            title="Remove Contributor",
            text=f"Remove {display_name} from this project?",
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda x: self.confirm_remove_dialog.dismiss()
                ),
                MDRaisedButton(
                    text="REMOVE",
                    md_bg_color=(0.8, 0.2, 0.2, 1),
                    on_release=lambda x: self.do_remove_contributor(user_id)
                )
            ]
        )
        self.confirm_remove_dialog.open()

    def do_remove_contributor(self, user_id):
        """Actually remove the contributor after confirmation"""
        projects = load_projects()
        users = load_users()

        if self.confirm_remove_dialog:
            self.confirm_remove_dialog.dismiss()

        if self.current_project_id in projects:
            project = projects[self.current_project_id]

            if 'contributors' in project and user_id in project['contributors']:
                idx = project['contributors'].index(user_id)

                project['contributors'].pop(idx)
                if 'contributor_names' in project and idx < len(project['contributor_names']):
                    project['contributor_names'].pop(idx)

                # Also remove project from user's projects list
                if user_id in users:
                    user = users[user_id]
                    if 'projects' in user and self.current_project_id in user['projects']:
                        user['projects'].remove(self.current_project_id)

                save_projects(projects)
                save_users(users)

                self.contributor_dialog.dismiss()
                self.manage_contributors(self.current_project_id)
                self.show_message("Contributor removed")

    def refresh_list(self):
        """Load and display all projects for current season"""
        self.ids.project_list.clear_widgets()

        if not self.current_season_id:
            self.load_most_recent_season()
            return

        projects = load_projects()
        season_projects = {k: v for k, v in projects.items() if v.get('season_id') == self.current_season_id}
        self.all_projects = list(season_projects.items())

        if not self.all_projects:
            # Show "no projects" message
            card = MDCard(
                orientation="vertical",
                size_hint_y=None,
                height="80dp",
                padding="20dp",
                spacing="10dp"
            )
            card.add_widget(
                MDLabel(
                    text="No projects found for this season.",
                    halign="center",
                    theme_text_color="Secondary"
                )
            )
            card.add_widget(
                MDLabel(
                    text="Click the + button to add a project.",
                    halign="center",
                    theme_text_color="Hint",
                    font_style="Caption"
                )
            )
            self.ids.project_list.add_widget(card)
        else:
            for project_id, data in season_projects.items():
                self.add_project_to_list(project_id, data)

    def manage_bag_tags(self, project_id):
        """Navigate to bag tag management for this project"""
        app = MDApp.get_running_app()
        app.current_bagtag_project = project_id
        self.manager.current = "bagtag_management"

    def confirm_close_project(self, project_id):
        """Confirm project closure"""
        projects = load_projects()
        project = projects.get(project_id, {})
        name = project.get('name', 'Unknown')

        self.close_dialog = MDDialog(
            title="Close Project",
            text=f"Close project {project_id}: {name}?\n\nNo further data can be added.",
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: self.close_dialog.dismiss()),
                MDRaisedButton(
                    text="CLOSE PROJECT",
                    md_bg_color=(0.8, 0.5, 0.2, 1),
                    on_release=lambda x: self.close_project(project_id)
                )
            ]
        )
        self.close_dialog.open()

    def close_project(self, project_id):
        """Close a project"""
        projects = load_projects()
        if project_id in projects:
            projects[project_id]['status'] = 'closed'
            projects[project_id]['closed_at'] = datetime.now().isoformat()
            projects[project_id]['closed_by'] = MDApp.get_running_app().current_admin.get("username")
            save_projects(projects)
            self.close_dialog.dismiss()
            self.refresh_list()
            self.show_message("Project closed")

    def confirm_delete_project(self, project_id):
        """Confirm project deletion"""
        projects = load_projects()
        project = projects.get(project_id, {})
        name = project.get('name', 'Unknown')

        self.delete_dialog = MDDialog(
            title="Delete Project",
            text=f"Delete project {project_id}: {name}?\n\nAll associated data will be lost!",
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: self.delete_dialog.dismiss()),
                MDRaisedButton(
                    text="DELETE",
                    md_bg_color=(0.8, 0.2, 0.2, 1),
                    on_release=lambda x: self.delete_project(project_id)
                )
            ]
        )
        self.delete_dialog.open()

    def delete_project(self, project_id):
        """Delete a project"""
        projects = load_projects()
        if project_id in projects:
            season_id = projects[project_id].get('season_id')
            del projects[project_id]
            save_projects(projects)

            if season_id:
                seasons = load_seasons()
                if season_id in seasons:
                    seasons[season_id]['projects'] = max(0, seasons[season_id].get('projects', 1) - 1)
                    save_seasons(seasons)

            self.delete_dialog.dismiss()
            self.refresh_list()
            self.show_message("Project deleted")


    def show_reassign_dialog(self, project_id):
        """Show dialog to reassign project leader"""
        projects = load_projects()
        project = projects.get(project_id, {})
        current_leader = project.get('leader_name', 'Unknown')

        content = MDBoxLayout(
            orientation="vertical",
            spacing="10dp",
            padding="20dp",
            size_hint_y=None,
            height="150dp"
        )

        self.reassign_project_id = project_id
        self.reassign_button = MDRaisedButton(
            text="Select New Leader",
            on_release=lambda x: self.open_reassign_menu()
        )
        self.reassign_leader = None

        content.add_widget(
            MDLabel(
                text=f"Current Leader: {current_leader}",
                theme_text_color="Secondary",
                size_hint_y=None,
                height="30dp"
            )
        )
        content.add_widget(self.reassign_button)

        self.reassign_dialog = MDDialog(
            title=f"Reassign Project {project_id}",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: self.reassign_dialog.dismiss()),
                MDRaisedButton(text="SAVE", on_release=lambda x: self.do_reassign())
            ]
        )
        self.reassign_dialog.open()

    def open_reassign_menu(self):
        """Open dropdown to select new leader"""
        menu_items = []
        admins = load_admins()

        for username, data in admins.items():
            display = f"{username} ({data['role']})"
            menu_items.append({
                "text": display,
                "on_release": lambda x=username, d=display: self.set_reassign_leader(x, d)
            })

        self.reassign_menu = MDDropdownMenu(
            caller=self.reassign_button,
            items=menu_items,
            width_mult=4,
        )
        self.reassign_menu.open()

    def set_reassign_leader(self, username, display):
        """Set the selected reassign leader"""
        self.reassign_leader = username
        self.reassign_button.text = display
        self.reassign_menu.dismiss()

    def do_reassign(self):
        """Perform leader reassignment"""
        if not self.reassign_leader:
            self.show_message("Please select a new leader")
            return

        projects = load_projects()
        admins = load_admins()
        users = load_users()

        if self.reassign_project_id in projects:
            project = projects[self.reassign_project_id]
            old_leader = project.get('leader')
            old_leader_user_id = project.get('leader_user_id')

            # Get new leader info
            new_leader_data = admins.get(self.reassign_leader, {})
            new_leader_user_id = new_leader_data.get("user_id")

            # Update project with new leader
            project['leader'] = self.reassign_leader
            project['leader_name'] = f"{self.reassign_leader} ({new_leader_data.get('role', 'admin')})"
            project['leader_user_id'] = new_leader_user_id

            # Remove old leader from contributors if they were there
            if old_leader_user_id and old_leader_user_id in project.get('contributors', []):
                idx = project['contributors'].index(old_leader_user_id)
                project['contributors'].pop(idx)
                if 'contributor_names' in project and idx < len(project['contributor_names']):
                    project['contributor_names'].pop(idx)

                # Also remove project from old leader's projects list
                if old_leader_user_id in users:
                    old_user = users[old_leader_user_id]
                    if self.reassign_project_id in old_user.get('projects', []):
                        old_user['projects'].remove(self.reassign_project_id)

            # Add new leader to contributors
            if new_leader_user_id and new_leader_user_id in users:
                new_user = users[new_leader_user_id]
                new_user_name = new_user.get('name', new_leader_user_id)

                if new_leader_user_id not in project.get('contributors', []):
                    if 'contributors' not in project:
                        project['contributors'] = []
                    if 'contributor_names' not in project:
                        project['contributor_names'] = []

                    project['contributors'].append(new_leader_user_id)
                    project['contributor_names'].append(f"{new_leader_user_id}: {new_user_name}")

                # Add project to new leader's projects list
                if 'projects' not in new_user:
                    new_user['projects'] = []
                if self.reassign_project_id not in new_user['projects']:
                    new_user['projects'].append(self.reassign_project_id)

            save_projects(projects)
            save_users(users)

            self.reassign_dialog.dismiss()
            self.refresh_list()
            self.show_message("Project leader updated")

    def go_back(self):
        """Return to admin dashboard"""
        self.manager.current = "admin_dashboard"

    # Add the switch button to the top app bar in your KV


class UserManagementScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.all_users = []
        self.filter_menu = None
        self.user_type = "seasonal"  # Default
        self.user_type_menu = None
        self.user_type_button = None
        self.faculty_id_container = None
        self.faculty_id = None
        self.user_name = None
        self.dialog = None

    def on_enter(self):
        """Called when screen is shown"""
        self.refresh_list()

    def refresh_list(self):
        """Load and display all users"""
        self.ids.user_list.clear_widgets()
        users = load_users()
        self.all_users = list(users.items())

        for user_id, data in users.items():
            self.add_user_to_list(user_id, data)


    def add_user_to_list(self, user_id, data):
        """Add a single user item to the list UI"""
        card = MDCard(
            orientation="vertical",
            size_hint_y=None,
            height="190dp",
            padding="15dp",
            spacing="5dp",
            elevation=2,
            radius=[10, 10, 10, 10]
        )

        # Header with user ID and name
        header = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height="25dp",
            spacing="10dp"
        )

        name = data.get('name', 'Unknown')
        status = data.get('status', 'active')
        user_type = data.get('user_type', 'seasonal')

        # Status indicator
        status_color = (0.2, 0.8, 0.2, 1) if status == 'active' else (0.5, 0.5, 0.5, 1)
        status_text = "●" if status == 'active' else "○"

        # User type badge
        type_color = (0.3, 0.3, 0.8, 1) if user_type == 'faculty' else (0.3, 0.8, 0.3, 1)
        type_text = "F" if user_type == 'faculty' else "S"

        header.add_widget(
            MDLabel(
                text=f"{user_id}: {name}",
                theme_text_color="Primary",
                font_style="H6",
                size_hint_x=0.6
            )
        )

        header.add_widget(
            MDLabel(
                text=type_text,
                theme_text_color="Custom",
                text_color=type_color,
                font_style="Subtitle1",
                size_hint_x=0.1,
                halign="center"
            )
        )

        header.add_widget(
            MDLabel(
                text=status_text,
                theme_text_color="Custom",
                text_color=status_color,
                font_style="Subtitle1",
                size_hint_x=0.1,
                halign="center"
            )
        )
        card.add_widget(header)

        # Season info
        season_id = data.get('season', 'Not assigned')
        if season_id != 'Not assigned':
            seasons = load_seasons()
            season_data = seasons.get(season_id, {})
            org = season_data.get('organization', 'KFFS')
            year = season_data.get('year', season_id)
            display_season = f"{org} {year}"
        else:
            display_season = "Not assigned"

        season_label = MDLabel(
            text=f"📅 Season: {display_season}",
            theme_text_color="Secondary",
            font_style="Caption",
            size_hint_y=None,
            height="20dp"
        )
        card.add_widget(season_label)

        # Projects section
        projects = data.get('projects', [])
        if projects:
            project_text = "📋 Projects: " + ", ".join(projects[:3])
            if len(projects) > 3:
                project_text += f" +{len(projects) - 3} more"
        else:
            project_text = "📋 No projects assigned"

        project_label = MDLabel(
            text=project_text,
            theme_text_color="Secondary",
            font_style="Caption",
            size_hint_y=None,
            height="25dp"
        )
        card.add_widget(project_label)

        # Action buttons
        actions = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height="40dp",
            spacing="10dp"
        )

        app = MDApp.get_running_app()
        current_role = app.current_admin.get("role")
        user_type = data.get('user_type', 'seasonal')

        # Superadmin sees additional actions for faculty users
        if current_role == "superadmin" and user_type == "faculty":
            # Add admin-specific buttons: Reset Password, Demote to Seasonal
            pass

        if current_role in ["admin", "superadmin"]:
            assign_btn = MDRaisedButton(
                text="ASSIGN PROJECTS",
                size_hint=(0.5, None),
                height="35dp",
                font_size="10sp",
                md_bg_color=(0.3, 0.5, 0.8, 1),
                on_release=lambda x, u=user_id: self.manage_user_projects(u)
            )
            actions.add_widget(assign_btn)

            if status == 'active':
                deactivate_btn = MDRaisedButton(
                    text="DEACTIVATE",
                    size_hint=(0.5, None),
                    height="35dp",
                    font_size="10sp",
                    md_bg_color=(0.8, 0.2, 0.2, 1),
                    on_release=lambda x, u=user_id: self.deactivate_user(u)
                )
                actions.add_widget(deactivate_btn)
            else:
                reactivate_btn = MDRaisedButton(
                    text="REACTIVATE",
                    size_hint=(0.5, None),
                    height="35dp",
                    font_size="10sp",
                    md_bg_color=(0.2, 0.6, 0.2, 1),
                    on_release=lambda x, u=user_id: self.reactivate_user(u)
                )
                actions.add_widget(reactivate_btn)

        card.add_widget(actions)

        # Delete button only for superadmin
        if current_role == "superadmin":
            delete_btn = MDRaisedButton(
                text="DELETE USER",
                size_hint_y=None,
                height="30dp",
                font_size="10sp",
                md_bg_color=(0.8, 0.2, 0.2, 1),
                on_release=lambda x, u=user_id: self.confirm_delete_user(u)
            )
            card.add_widget(delete_btn)

        self.ids.user_list.add_widget(card)

    def test_button(self):
        print("🔵🔵🔵 BUTTON WAS CLICKED! 🔵🔵🔵")
        self.open_user_type_menu()

    def show_add_user_dialog(self):
        """Show dialog to add a new user"""
        content = MDBoxLayout(
            orientation="vertical",
            spacing="10dp",
            padding="20dp",
            size_hint_y=None,
            height="320dp"  # Reduced height
        )

        # User type selector
        content.add_widget(
            MDLabel(
                text="User Type:",
                theme_text_color="Secondary",
                size_hint_y=None,
                height="20dp"
            )
        )

        self.user_type = "seasonal"
        self.user_type_button = MDFlatButton(
            text="Seasonal User",
            size_hint_y=None,
            height="45dp",
            on_release=lambda x: self.open_user_type_menu()
        )
        content.add_widget(self.user_type_button)

        # First and Last Name
        self.first_name_field = MDTextField(
            hint_text="First Name",
            mode="rectangle",
            size_hint_y=None,
            height="50dp"
        )
        content.add_widget(self.first_name_field)

        self.last_name_field = MDTextField(
            hint_text="Last Name",
            mode="rectangle",
            size_hint_y=None,
            height="50dp"
        )
        content.add_widget(self.last_name_field)

        self.dialog = MDDialog(
            title="Add New User",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text="CREATE", on_release=lambda x: self.create_user())
            ]
        )
        self.dialog.open()

    def open_user_type_menu(self):
        """Open dropdown to select user type"""
        print("🔵 open_user_type_menu CALLED")

        menu_items = [
            {
                "text": "Seasonal User",
                "on_release": lambda x="seasonal": self.set_user_type(x)
            },
            {
                "text": "Faculty (Admin Access)",
                "on_release": lambda x="faculty": self.set_user_type(x)
            },
        ]

        self.user_type_menu = MDDropdownMenu(
            caller=self.user_type_button,
            items=menu_items,
            width_mult=3,
            position="auto",
        )
        self.user_type_menu.open()

    def set_user_type(self, user_type):
        """Set user type and update UI accordingly"""
        self.user_type = user_type
        self.user_type_button.text = "Faculty (Admin Access)" if user_type == "faculty" else "Seasonal User"

        # No faculty ID field to show/hide anymore

        if self.user_type_menu:
            self.user_type_menu.dismiss()

    def add_contributor(self):
        """Add selected user as contributor to the project (and add project to user)"""
        if not self.selected_contributor:
            self.show_message("Please select a user to add")
            return

        projects = load_projects()
        users = load_users()

        if self.current_project_id in projects:
            project = projects[self.current_project_id]

            if 'contributors' not in project:
                project['contributors'] = []
            if 'contributor_names' not in project:
                project['contributor_names'] = []

            if self.selected_contributor in project['contributors']:
                self.show_message("This user is already a contributor")
                return

            # Get user's name
            user_data = users.get(self.selected_contributor, {})
            user_name = user_data.get('name', self.selected_contributor)
            # Create display name with user ID
            display_name = f"{self.selected_contributor}: {user_name}"

            # Add contributor to project
            project['contributors'].append(self.selected_contributor)
            project['contributor_names'].append(display_name)

            # ALSO add project to user's projects list
            if self.selected_contributor in users:
                if 'projects' not in users[self.selected_contributor]:
                    users[self.selected_contributor]['projects'] = []

                if self.current_project_id not in users[self.selected_contributor]['projects']:
                    users[self.selected_contributor]['projects'].append(self.current_project_id)

            save_projects(projects)
            save_users(users)

            self.contributor_dialog.dismiss()
            self.manage_contributors(self.current_project_id)
            self.show_message(
                f"User {self.selected_contributor} added as contributor")  # Use selected_contributor, not user_name

    def create_user(self):
        """Create a new user (handles both seasonal and faculty)"""
        first_name = self.first_name_field.text.strip()
        last_name = self.last_name_field.text.strip()
        user_type = self.user_type

        if not first_name or not last_name:
            self.show_message("First and last name required")
            return

        full_name = f"{first_name} {last_name}"

        users = load_users()
        admins = load_admins()

        # Auto-assign user ID for everyone (no faculty ID field)
        user_id = self.get_next_user_id()

        # Check if user ID already exists
        if user_id in users:
            self.show_message(f"User ID {user_id} already exists")
            return

        # Get most recent season
        recent_season = get_most_recent_season()
        season_id = recent_season[1] if recent_season else "2024"

        # Create user record
        users[user_id] = {
            "first_name": first_name,
            "last_name": last_name,
            "name": full_name,
            "user_type": user_type,
            "role": "user",
            "status": "active",
            "season": season_id,
            "projects": [],
            "created_at": datetime.now().isoformat(),
            "created_by": MDApp.get_running_app().current_admin.get("username")
        }

        # If faculty, also create admin account
        if user_type == "faculty":
            # Generate a default password
            default_password = f"field{user_id}"

            # Generate admin username: first initial + last name
            # e.g., John Smith -> jsmith
            first_initial = first_name[0].lower() if first_name else ""
            last_name_lower = last_name.lower()
            admin_username = f"{first_initial}{last_name_lower}"

            # Handle potential duplicates
            base_username = admin_username
            counter = 1
            while admin_username in admins:
                admin_username = f"{base_username}{counter}"
                counter += 1

            # Also store the user_id for reference
            admins[admin_username] = {
                "password_hash": hash_password(default_password),
                "role": "admin",
                "user_id": user_id,
                "first_name": first_name,
                "last_name": last_name,
                "created_at": datetime.now().isoformat(),
                "created_by": MDApp.get_running_app().current_admin.get("username")
            }
            save_admins(admins)

            admin_msg = f"\n\nAdmin login: {admin_username}\nDefault password: {default_password}"
        else:
            admin_msg = ""

        save_users(users)

        self.dialog.dismiss()
        self.refresh_list()
        self.show_message(f"User {user_id} ({full_name}) created as {user_type}{admin_msg}")

    def get_next_user_id(self):
        """Get the next available user ID starting from 11"""
        users = load_users()
        admins = load_admins()

        used_ids = set()
        for uid in users.keys():
            used_ids.add(int(uid))
        for admin_data in admins.values():
            if admin_data.get('user_id'):
                used_ids.add(int(admin_data['user_id']))

        next_id = 11
        while next_id in used_ids:
            next_id += 1

        return f"{next_id:02d}"

    def manage_user_projects(self, user_id):
        """Open dialog to manage user's project assignments"""
        users = load_users()
        user = users.get(user_id, {})

        content = MDBoxLayout(
            orientation="vertical",
            spacing="10dp",
            padding="20dp",
            size_hint_y=None,
            height="300dp"
        )

        content.add_widget(
            MDLabel(
                text=f"Projects for {user_id}: {user.get('name')}",
                theme_text_color="Primary",
                font_style="H6",
                size_hint_y=None,
                height="30dp"
            )
        )

        projects = user.get('projects', [])

        if projects:
            for i, project_id in enumerate(projects):
                project_box = MDBoxLayout(
                    orientation="horizontal",
                    size_hint_y=None,
                    height="40dp",
                    spacing="10dp"
                )

                # Get project name for display
                all_projects = load_projects()
                project_data = all_projects.get(project_id, {})
                project_name = project_data.get('name', '')
                display_text = f"Project {project_id}: {project_name}" if project_name else f"Project {project_id}"

                project_box.add_widget(
                    MDLabel(
                        text=display_text,
                        size_hint_x=0.7,
                        halign="left"
                    )
                )

                remove_btn = MDRaisedButton(
                    text="REMOVE",
                    size_hint=(None, None),
                    size=("70dp", "30dp"),
                    font_size="10sp",
                    md_bg_color=(0.8, 0.2, 0.2, 1),
                    on_release=lambda x, u=user_id, idx=i: self.remove_user_project(u, idx)
                )
                project_box.add_widget(remove_btn)

                content.add_widget(project_box)
        else:
            content.add_widget(
                MDLabel(
                    text="No projects assigned",
                    theme_text_color="Hint",
                    size_hint_y=None,
                    height="30dp"
                )
            )

        # ADD PROJECT button - now opens dropdown directly
        add_btn = MDRaisedButton(
            text="ADD PROJECT",
            size_hint_y=None,
            height="45dp",
            on_release=lambda x: self.open_add_project_dropdown(user_id)
        )
        content.add_widget(add_btn)

        self.project_dialog = MDDialog(
            title="Manage Projects",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="DONE", on_release=lambda x: self.project_dialog.dismiss())
            ]
        )
        self.project_dialog.open()

    def open_add_project_dropdown(self, user_id):
        """Open dropdown to select a project to add"""
        users = load_users()
        user = users.get(user_id, {})
        season_id = user.get('season')

        if not season_id:
            self.show_message("User not assigned to a season")
            return

        # Get available projects
        all_projects = load_projects()
        user_projects = user.get('projects', [])

        available_projects = []
        for project_id, data in all_projects.items():
            if data.get('season_id') == season_id and project_id not in user_projects:
                project_name = data.get('name', 'Unnamed')
                available_projects.append((project_id, project_name))

        if not available_projects:
            self.show_message("No available projects to add")
            return

        menu_items = []
        for project_id, project_name in available_projects:
            display = f"{project_id}: {project_name}"
            menu_items.append({
                "text": display,
                "on_release": lambda x=project_id, d=display: self.add_user_project_with_id(user_id, project_id)
            })

        self.add_project_menu = MDDropdownMenu(
            caller=self.project_dialog.content_cls.children[-1],  # The ADD PROJECT button
            items=menu_items,
            width_mult=4,
        )
        self.add_project_menu.open()

    def add_user_project_with_id(self, user_id, project_id):
        """Add a project to a user using the project ID"""
        users = load_users()
        projects = load_projects()

        if user_id in users:
            if 'projects' not in users[user_id]:
                users[user_id]['projects'] = []

            if project_id in users[user_id]['projects']:
                self.show_message(f"User already assigned to project {project_id}")
                self.add_project_menu.dismiss()
                return

            # Add project to user
            users[user_id]['projects'].append(project_id)

            # ALSO add user as contributor to the project
            if project_id in projects:
                project = projects[project_id]

                if 'contributors' not in project:
                    project['contributors'] = []
                if 'contributor_names' not in project:
                    project['contributor_names'] = []

                if user_id not in project['contributors']:
                    user_name = users[user_id].get('name', user_id)
                    display_name = f"{user_id}: {user_name}"
                    project['contributors'].append(user_id)
                    project['contributor_names'].append(display_name)

            save_users(users)
            save_projects(projects)

            if hasattr(self, 'add_project_menu') and self.add_project_menu:
                self.add_project_menu.dismiss()

            # Refresh the dialog
            self.project_dialog.dismiss()
            self.manage_user_projects(user_id)
            self.show_message(f"User assigned to project {project_id}")

    def show_add_project_dialog(self, user_id):
        """Show dialog to add a project assignment with dropdown"""
        content = MDBoxLayout(
            orientation="vertical",
            spacing="10dp",
            padding="20dp",
            size_hint_y=None,
            height="150dp"
        )

        # Get available projects for current season
        seasons = load_seasons()
        projects = load_projects()

        # Get current season from the user
        users = load_users()
        user = users.get(user_id, {})
        season_id = user.get('season')

        # Find projects in this season that the user isn't already assigned to
        available_projects = []
        user_projects = user.get('projects', [])

        for project_id, data in projects.items():
            if data.get('season_id') == season_id and project_id not in user_projects:
                project_name = data.get('name', 'Unnamed')
                available_projects.append((project_id, project_name))

        if not available_projects:
            content.add_widget(
                MDLabel(
                    text="No available projects in this season",
                    theme_text_color="Hint"
                )
            )
            add_btn = MDRaisedButton(
                text="CLOSE",
                size_hint_y=None,
                height="45dp",
                on_release=lambda x: self.add_project_dialog.dismiss()
            )
            content.add_widget(add_btn)
        else:
            # Create dropdown button
            self.add_project_button = MDRaisedButton(
                text="Select Project",
                size_hint_y=None,
                height="45dp",
                on_release=lambda x: self.open_project_dropdown(available_projects, user_id)
            )
            content.add_widget(self.add_project_button)

            self.selected_project_id = None
            self.selected_project_display = None

        self.add_project_dialog = MDDialog(
            title="Add Project",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: self.add_project_dialog.dismiss())
            ] if available_projects else []
        )
        self.add_project_dialog.open()

    def open_project_dropdown(self, available_projects, user_id):
        """Open dropdown to select a project"""
        menu_items = []
        for project_id, project_name in available_projects:
            display = f"{project_id}: {project_name}"
            menu_items.append({
                "text": display,
                "on_release": lambda x=project_id, d=display: self.set_project_for_user(x, d, user_id)
            })

        self.project_menu = MDDropdownMenu(
            caller=self.add_project_button,
            items=menu_items,
            width_mult=4,
        )
        self.project_menu.open()

    def set_project_for_user(self, project_id, display, user_id):
        """Set selected project and add it to user"""
        self.selected_project_id = project_id
        self.selected_project_display = display
        self.add_project_button.text = display
        self.project_menu.dismiss()

        # Add the project immediately
        self.add_user_project_with_id(user_id, project_id)

    def remove_user_project(self, user_id, project_index):
        """Remove a project from a user (and remove user as contributor from project)"""
        users = load_users()
        projects = load_projects()

        if user_id in users and 'projects' in users[user_id]:
            if project_index < len(users[user_id]['projects']):
                removed_project = users[user_id]['projects'].pop(project_index)

                # ALSO remove user as contributor from the project
                if removed_project in projects:
                    project = projects[removed_project]
                    if 'contributors' in project and user_id in project['contributors']:
                        idx = project['contributors'].index(user_id)
                        project['contributors'].pop(idx)
                        if 'contributor_names' in project and idx < len(project['contributor_names']):
                            project['contributor_names'].pop(idx)
                        print(f"Removed user {user_id} as contributor from project {removed_project}")

                save_users(users)
                save_projects(projects)

                self.project_dialog.dismiss()
                self.manage_user_projects(user_id)
                self.show_message(f"Removed from project {removed_project}")

    def deactivate_user(self, user_id):
        """Deactivate a user"""
        users = load_users()
        if user_id in users:
            users[user_id]['status'] = 'inactive'
            save_users(users)
            self.refresh_list()
            self.show_message(f"User {user_id} deactivated")

    def reactivate_user(self, user_id):
        """Reactivate a user"""
        users = load_users()
        if user_id in users:
            users[user_id]['status'] = 'active'
            save_users(users)
            self.refresh_list()
            self.show_message(f"User {user_id} reactivated")

    def confirm_delete_user(self, user_id):
        """Confirm user deletion"""
        users = load_users()
        user = users.get(user_id, {})
        name = user.get('name', 'Unknown')

        self.delete_dialog = MDDialog(
            title="Delete User",
            text=f"Delete user {user_id}: {name}?\n\nThis cannot be undone!",
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: self.delete_dialog.dismiss()),
                MDRaisedButton(
                    text="DELETE",
                    md_bg_color=(0.8, 0.2, 0.2, 1),
                    on_release=lambda x: self.delete_user(user_id)
                )
            ]
        )
        self.delete_dialog.open()

    def delete_user(self, user_id):
        """Delete a user (and remove any admin link)"""
        users = load_users()
        admins = load_admins()

        if user_id in users:
            # Check if this user is linked to an admin
            for admin_username, admin_data in admins.items():
                if admin_data.get("user_id") == user_id:
                    self.show_message(
                        f"Cannot delete user {user_id} - this user is linked to admin '{admin_username}'. Delete the admin account first.")
                    return

            del users[user_id]
            save_users(users)
            self.delete_dialog.dismiss()
            self.refresh_list()
            self.show_message(f"User {user_id} deleted")

    def go_back(self):
        self.manager.current = "admin_dashboard"

    def show_message(self, message):
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDRaisedButton
        dialog = MDDialog(
            text=message,
            buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()

    def filter_list(self, search_text):
        """Filter user list by search text"""
        self.ids.user_list.clear_widgets()

        app = MDApp.get_running_app()
        current_role = app.current_admin.get("role")

        search_text = search_text.lower()
        for user_id, data in self.all_users:
            name = data.get('name', '').lower()
            if search_text in user_id.lower() or search_text in name:
                self.add_user_to_list(user_id, data)


class AllProjectsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.all_projects = []
        self.filter_menu = None
        self.current_filter = "all"

    def on_enter(self):
        """Called when screen is shown"""
        self.refresh_list()

    def refresh_list(self):
        """Load and display all projects across all seasons"""
        self.ids.project_list.clear_widgets()

        projects = load_projects()
        seasons = load_seasons()

        # Create a list with project data including season info
        self.all_projects = []
        for project_id, data in projects.items():
            season_id = data.get('season_id')
            season_data = seasons.get(season_id, {})
            season_name = f"{season_data.get('organization', 'Unknown')} {season_data.get('year', season_id)}"

            self.all_projects.append({
                'id': project_id,
                'name': data.get('name', 'Unnamed'),
                'description': data.get('description', ''),
                'season': season_name,
                'season_id': season_id,
                'leader': data.get('leader_name', 'Unassigned'),
                'status': data.get('status', 'active'),
                'collections': data.get('collections', 0),
                'contributors': len(data.get('contributors', []))
            })

        # Sort by season (newest first)
        self.all_projects.sort(key=lambda x: x['season_id'], reverse=True)

        # Apply current filter
        self.apply_filter(self.current_filter)

    def add_project_to_list(self, project):
        """Add a single project item to the list UI"""
        card = MDCard(
            orientation="vertical",
            size_hint_y=None,
            height="160dp",
            padding="15dp",
            spacing="5dp",
            elevation=2,
            radius=[10, 10, 10, 10]
        )

        # Status color
        status_color = (0.2, 0.8, 0.2, 1) if project['status'] == 'active' else (0.5, 0.5, 0.5, 1)
        status_text = "ACTIVE" if project['status'] == 'active' else "CLOSED"

        # Header with project ID and name
        header = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height="35dp",
            spacing="10dp"
        )

        header.add_widget(
            MDLabel(
                text=f"{project['id']}: {project['name']}",
                theme_text_color="Primary",
                font_style="H6",
                size_hint_x=0.6
            )
        )

        header.add_widget(
            MDLabel(
                text=status_text,
                theme_text_color="Custom",
                text_color=status_color,
                font_style="Subtitle1",
                size_hint_x=0.2,
                halign="center"
            )
        )
        card.add_widget(header)

        # Season and leader info
        info_box = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height="25dp",
            spacing="10dp"
        )

        info_box.add_widget(
            MDLabel(
                text=f"📅 {project['season']}",
                theme_text_color="Secondary",
                font_style="Subtitle2",
                size_hint_x=0.5
            )
        )
        info_box.add_widget(
            MDLabel(
                text=f"👤 {project['leader']}",
                theme_text_color="Secondary",
                font_style="Subtitle2",
                size_hint_x=0.5,
                halign="right"
            )
        )
        card.add_widget(info_box)

        # Stats
        stats_box = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height="25dp",
            spacing="10dp"
        )

        stats_box.add_widget(
            MDLabel(
                text=f"📊 Collections: {project['collections']}",
                theme_text_color="Hint",
                font_style="Caption",
                size_hint_x=0.5
            )
        )
        stats_box.add_widget(
            MDLabel(
                text=f"👥 Contributors: {project['contributors']}",
                theme_text_color="Hint",
                font_style="Caption",
                size_hint_x=0.5,
                halign="right"
            )
        )
        card.add_widget(stats_box)

        # Description (if exists)
        if project.get('description'):
            desc_label = MDLabel(
                text=project['description'][:60] + ("..." if len(project['description']) > 60 else ""),
                theme_text_color="Secondary",
                font_style="Caption",
                size_hint_y=None,
                height="30dp"
            )
            card.add_widget(desc_label)

        self.ids.project_list.add_widget(card)

    def filter_list(self, search_text):
        """Filter projects by search text"""
        self.ids.project_list.clear_widgets()

        search_text = search_text.lower()
        for project in self.all_projects:
            if (search_text in project['id'].lower() or
                    search_text in project['name'].lower() or
                    search_text in project['season'].lower() or
                    search_text in project['leader'].lower()):
                self.add_project_to_list(project)

    def show_filter_options(self):
        """Show filter dropdown menu"""
        menu_items = [
            {
                "text": "All Projects",
                "on_release": lambda x="all": self.set_filter("all"),
            },
            {
                "text": "Active Only",
                "on_release": lambda x="active": self.set_filter("active"),
            },
            {
                "text": "Closed Only",
                "on_release": lambda x="closed": self.set_filter("closed"),
            },
        ]

        self.filter_menu = MDDropdownMenu(
            caller=self.ids.search_field,
            items=menu_items,
            width_mult=3,
        )
        self.filter_menu.open()

    def set_filter(self, filter_type):
        """Set and apply filter"""
        self.current_filter = filter_type
        if self.filter_menu:
            self.filter_menu.dismiss()
        self.apply_filter(filter_type)

    def apply_filter(self, filter_type):
        """Apply the selected filter"""
        self.ids.project_list.clear_widgets()

        for project in self.all_projects:
            if filter_type == "all":
                self.add_project_to_list(project)
            elif filter_type == "active" and project['status'] == 'active':
                self.add_project_to_list(project)
            elif filter_type == "closed" and project['status'] == 'closed':
                self.add_project_to_list(project)

    def go_back(self):
        self.manager.current = "admin_dashboard"

    def show_message(self, message):
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDRaisedButton
        dialog = MDDialog(
            text=message,
            buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()


class AllUsersScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.all_users = []
        self.filter_menu = None
        self.current_filter = "all"

    def on_enter(self):
        """Called when screen is shown"""
        self.refresh_list()

    def refresh_list(self):
        """Load and display all users across all seasons"""
        self.ids.user_list.clear_widgets()

        users = load_users()
        seasons = load_seasons()

        # Create a list with user data including season info
        self.all_users = []
        for user_id, data in users.items():
            season_id = data.get('season', 'Not assigned')
            if season_id != 'Not assigned':
                season_data = seasons.get(season_id, {})
                season_name = f"{season_data.get('organization', 'KFFS')} {season_data.get('year', season_id)}"
            else:
                season_name = "Not assigned"

            self.all_users.append({
                'id': user_id,
                'id_num': int(user_id),  # For sorting
                'name': data.get('name', 'Unknown'),
                'user_type': data.get('user_type', 'seasonal'),
                'season': season_name,
                'season_id': season_id,
                'status': data.get('status', 'active'),
                'projects': data.get('projects', []),
                'created_at': data.get('created_at', 'Unknown')[:10]
            })

        # Sort by user ID numerically (ascending)
        self.all_users.sort(key=lambda x: x['id_num'])

        # Apply current filter
        self.apply_filter(self.current_filter)

    def add_user_to_list(self, user):
        """Add a single user item to the list UI"""
        card = MDCard(
            orientation="vertical",
            size_hint_y=None,
            height="150dp",
            padding="15dp",
            spacing="5dp",
            elevation=2,
            radius=[10, 10, 10, 10]
        )

        # Status and type colors
        status_color = (0.2, 0.8, 0.2, 1) if user['status'] == 'active' else (0.5, 0.5, 0.5, 1)
        status_text = "●" if user['status'] == 'active' else "○"

        type_color = (0.3, 0.3, 0.8, 1) if user['user_type'] == 'faculty' else (0.3, 0.8, 0.3, 1)
        type_text = "F" if user['user_type'] == 'faculty' else "S"

        # Header with user ID and name
        header = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height="30dp",
            spacing="10dp"
        )

        header.add_widget(
            MDLabel(
                text=f"{user['id']}: {user['name']}",
                theme_text_color="Primary",
                font_style="H6",
                size_hint_x=0.6
            )
        )

        header.add_widget(
            MDLabel(
                text=type_text,
                theme_text_color="Custom",
                text_color=type_color,
                font_style="Subtitle1",
                size_hint_x=0.15,
                halign="center"
            )
        )

        header.add_widget(
            MDLabel(
                text=status_text,
                theme_text_color="Custom",
                text_color=status_color,
                font_style="Subtitle1",
                size_hint_x=0.15,
                halign="center"
            )
        )
        card.add_widget(header)

        # Season info
        season_label = MDLabel(
            text=f"📅 Season: {user['season']}",
            theme_text_color="Secondary",
            font_style="Caption",
            size_hint_y=None,
            height="25dp"
        )
        card.add_widget(season_label)

        # Projects
        if user['projects']:
            projects_text = "📋 Projects: " + ", ".join(user['projects'][:3])
            if len(user['projects']) > 3:
                projects_text += f" +{len(user['projects']) - 3} more"
        else:
            projects_text = "📋 No projects assigned"

        projects_label = MDLabel(
            text=projects_text,
            theme_text_color="Secondary",
            font_style="Caption",
            size_hint_y=None,
            height="25dp"
        )
        card.add_widget(projects_label)

        # Created info
        created_label = MDLabel(
            text=f"📅 Created: {user['created_at']}",
            theme_text_color="Hint",
            font_style="Caption",
            size_hint_y=None,
            height="20dp"
        )
        card.add_widget(created_label)

        self.ids.user_list.add_widget(card)

    def filter_list(self, search_text):
        """Filter users by search text"""
        self.ids.user_list.clear_widgets()

        search_text = search_text.lower()
        for user in self.all_users:
            if (search_text in user['id'].lower() or
                    search_text in user['name'].lower() or
                    search_text in user['season'].lower()):
                self.add_user_to_list(user)

    def show_filter_options(self):
        """Show filter dropdown menu"""
        menu_items = [
            {
                "text": "All Users",
                "on_release": lambda x="all": self.set_filter("all"),
            },
            {
                "text": "Active Only",
                "on_release": lambda x="active": self.set_filter("active"),
            },
            {
                "text": "Inactive Only",
                "on_release": lambda x="inactive": self.set_filter("inactive"),
            },
            {
                "text": "Faculty Only",
                "on_release": lambda x="faculty": self.set_filter("faculty"),
            },
            {
                "text": "Seasonal Only",
                "on_release": lambda x="seasonal": self.set_filter("seasonal"),
            },
        ]

        self.filter_menu = MDDropdownMenu(
            caller=self.ids.search_field,
            items=menu_items,
            width_mult=4,
        )
        self.filter_menu.open()

    def set_filter(self, filter_type):
        """Set and apply filter"""
        self.current_filter = filter_type
        if self.filter_menu:
            self.filter_menu.dismiss()
        self.apply_filter(filter_type)

    def apply_filter(self, filter_type):
        """Apply the selected filter"""
        self.ids.user_list.clear_widgets()

        for user in self.all_users:
            if filter_type == "all":
                self.add_user_to_list(user)
            elif filter_type == "active" and user['status'] == 'active':
                self.add_user_to_list(user)
            elif filter_type == "inactive" and user['status'] == 'inactive':
                self.add_user_to_list(user)
            elif filter_type == "faculty" and user['user_type'] == 'faculty':
                self.add_user_to_list(user)
            elif filter_type == "seasonal" and user['user_type'] == 'seasonal':
                self.add_user_to_list(user)

    def go_back(self):
        self.manager.current = "admin_dashboard"

    def show_message(self, message):
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDRaisedButton
        dialog = MDDialog(
            text=message,
            buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()


class BagTagManagementScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_project_id = None
        self.current_project_data = None
        self.tag_config = None
        self.custom_fields = []

    def on_enter(self):
        """Called when screen is shown"""
        app = MDApp.get_running_app()
        self.current_project_id = app.current_bagtag_project
        self.load_project_data()

    def load_project_data(self):
        """Load project data and any existing tag configuration"""
        projects = load_projects()
        self.current_project_data = projects.get(self.current_project_id, {})

        # Load existing tag config for this project
        tags = load_tags()
        self.tag_config = tags.get(self.current_project_id, {})
        self.custom_fields = self.tag_config.get('custom_fields', [])

        self.update_ui()

    def update_ui(self):
        """Update the UI based on existing tag config"""
        if self.tag_config:
            self.show_existing_config()
        else:
            self.show_new_config_form()

    def show_existing_config(self):
        """Show existing tag configuration"""
        # Clear and build UI for existing config
        self.ids.main_layout.clear_widgets()

        # Header info
        header = MDCard(
            orientation="vertical",
            padding="15dp",
            spacing="10dp",
            size_hint_y=None,
            height="120dp"
        )
        header.add_widget(
            MDLabel(
                text=f"Tag Configuration for Project {self.current_project_id}",
                theme_text_color="Primary",
                font_style="H5",
                halign="center"
            )
        )
        header.add_widget(
            MDLabel(
                text=f"{self.current_project_data.get('name', 'Unnamed Project')}",
                theme_text_color="Secondary",
                halign="center"
            )
        )
        self.ids.main_layout.add_widget(header)

        # Custom fields display
        fields_card = MDCard(
            orientation="vertical",
            padding="15dp",
            spacing="5dp",
            size_hint_y=None,
            height=f"{60 + len(self.custom_fields) * 40}dp"
        )
        fields_card.add_widget(
            MDLabel(
                text="Custom Fields:",
                theme_text_color="Secondary",
                font_style="Subtitle1"
            )
        )

        for i, field in enumerate(self.custom_fields):
            field_box = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height="35dp",
                spacing="10dp"
            )
            field_box.add_widget(
                MDLabel(
                    text=f"{i + 1}. {field.get('label', 'Untitled')}",
                    size_hint_x=0.8
                )
            )
            field_box.add_widget(
                MDLabel(
                    text=f"[{field.get('type', 'text')}]",
                    theme_text_color="Hint",
                    size_hint_x=0.2,
                    halign="right"
                )
            )
            fields_card.add_widget(field_box)

        self.ids.main_layout.add_widget(fields_card)

        # Action buttons
        actions = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height="60dp",
            spacing="15dp",
            padding="10dp"
        )

        generate_btn = MDRaisedButton(
            text="GENERATE TAGS",
            md_bg_color=(0.2, 0.6, 0.2, 1),
            on_release=lambda x: self.show_generate_dialog()
        )
        actions.add_widget(generate_btn)

        edit_btn = MDRaisedButton(
            text="EDIT CONFIG",
            md_bg_color=(0.8, 0.5, 0.2, 1),
            on_release=lambda x: self.edit_config()
        )
        actions.add_widget(edit_btn)

        self.ids.main_layout.add_widget(actions)

    def show_new_config_form(self):
        """Show form to create new tag configuration"""
        self.ids.main_layout.clear_widgets()

        # Title
        title = MDCard(
            orientation="vertical",
            padding="15dp",
            size_hint_y=None,
            height="80dp"
        )
        title.add_widget(
            MDLabel(
                text="Create Tag Configuration",
                theme_text_color="Primary",
                font_style="H5",
                halign="center"
            )
        )
        self.ids.main_layout.add_widget(title)

        # Custom fields section
        fields_card = MDCard(
            orientation="vertical",
            padding="10dp",
            spacing="5dp",
            size_hint_y=None,
            height="360dp"  # Fixed height: header (40) + 5 fields * 64dp
        )

        fields_card.add_widget(
            MDLabel(
                text="Custom Fields (up to 5):",
                theme_text_color="Secondary",
                size_hint_y=None,
                height="30dp"
            )
        )

        self.custom_field_labels = []
        for i in range(5):
            field_box = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height="60dp",
                spacing="10dp"
            )

            label_field = MDTextField(
                hint_text=f"Field {i + 1} Label (e.g., 'Lot #')",
                mode="rectangle",
                size_hint_x=0.8,
                height="50dp"
            )

            type_btn = MDRaisedButton(
                text="Text",
                size_hint_x=0.2,
                height="40dp",
                disabled=True
            )

            field_box.add_widget(label_field)
            field_box.add_widget(type_btn)

            self.custom_field_labels.append(label_field)
            fields_card.add_widget(field_box)

        self.ids.main_layout.add_widget(fields_card)

        # Save button
        save_btn = MDRaisedButton(
            text="SAVE CONFIGURATION",
            size_hint_x=0.8,
            height="50dp",
            pos_hint={"center_x": 0.5},
            on_release=lambda x: self.save_config()
        )
        self.ids.main_layout.add_widget(save_btn)

        # Cancel button
        cancel_btn = MDFlatButton(
            text="CANCEL",
            size_hint_x=0.5,
            height="40dp",
            pos_hint={"center_x": 0.5},
            on_release=lambda x: self.go_back()
        )
        self.ids.main_layout.add_widget(cancel_btn)

    def save_config(self):
        """Save tag configuration"""
        custom_fields = []
        for i, label_field in enumerate(self.custom_field_labels):
            label = label_field.text.strip()
            if label:
                custom_fields.append({
                    'label': label,
                    'type': 'text',  # Default to text for now
                    'order': i
                })

        tags = load_tags()
        tags[self.current_project_id] = {
            'project_id': self.current_project_id,
            'custom_fields': custom_fields,
            'created_at': datetime.now().isoformat(),
            'created_by': MDApp.get_running_app().current_admin.get("username")
        }
        save_tags(tags)

        self.tag_config = tags[self.current_project_id]
        self.custom_fields = custom_fields
        self.update_ui()
        self.show_message("Configuration saved!")

    def edit_config(self):
        """Edit existing configuration"""
        self.ids.main_layout.clear_widgets()

        # Title
        title = MDCard(
            orientation="vertical",
            padding="15dp",
            size_hint_y=None,
            height="80dp"
        )
        title.add_widget(
            MDLabel(
                text="Edit Tag Configuration",
                theme_text_color="Primary",
                font_style="H5",
                halign="center"
            )
        )
        self.ids.main_layout.add_widget(title)

        # Custom fields section
        fields_card = MDCard(
            orientation="vertical",
            padding="10dp",
            spacing="5dp",
            size_hint_y=None,
            height="360dp"
        )

        fields_card.add_widget(
            MDLabel(
                text="Custom Fields (up to 5):",
                theme_text_color="Secondary",
                size_hint_y=None,
                height="30dp"
            )
        )

        self.custom_field_labels = []
        existing_fields = self.tag_config.get('custom_fields', [])

        for i in range(5):
            field_box = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height="60dp",
                spacing="10dp"
            )

            # Pre-populate if this field exists
            existing_label = existing_fields[i]['label'] if i < len(existing_fields) else ""

            label_field = MDTextField(
                hint_text=f"Field {i + 1} Label (e.g., 'Lot #')",
                mode="rectangle",
                size_hint_x=0.8,
                height="50dp",
                text=existing_label
            )

            type_btn = MDRaisedButton(
                text="Text",
                size_hint_x=0.2,
                height="40dp",
                disabled=True
            )

            field_box.add_widget(label_field)
            field_box.add_widget(type_btn)

            self.custom_field_labels.append(label_field)
            fields_card.add_widget(field_box)

        self.ids.main_layout.add_widget(fields_card)

        # Save button
        save_btn = MDRaisedButton(
            text="UPDATE CONFIGURATION",
            size_hint_x=0.8,
            height="50dp",
            pos_hint={"center_x": 0.5},
            on_release=lambda x: self.save_config()
        )
        self.ids.main_layout.add_widget(save_btn)

        # Cancel button
        cancel_btn = MDFlatButton(
            text="CANCEL",
            size_hint_x=0.5,
            height="40dp",
            pos_hint={"center_x": 0.5},
            on_release=lambda x: self.update_ui()  # Return to view mode
        )
        self.ids.main_layout.add_widget(cancel_btn)

    def show_generate_dialog(self):
        """Show dialog to generate a batch of tags"""
        content = MDBoxLayout(
            orientation="vertical",
            spacing="10dp",
            padding="20dp",
            size_hint_y=None,
            height="120dp"
        )

        content.add_widget(
            MDLabel(
                text="Number of tags to generate:",
                theme_text_color="Secondary"
            )
        )

        self.quantity_field = MDTextField(
            hint_text="Quantity (e.g., 100)",
            mode="rectangle",
            input_filter="int"
        )
        content.add_widget(self.quantity_field)

        print("🔵 Showing generate dialog")  # Debug

        self.generate_dialog = MDDialog(
            title="Generate Bag Tags",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: self.generate_dialog.dismiss()),
                MDRaisedButton(text="GENERATE", on_release=lambda x: self.generate_tags())
            ]
        )
        self.generate_dialog.open()

    def generate_tags(self):
        """Generate tags and create database entries"""
        quantity = int(self.quantity_field.text.strip() or 0)
        if quantity <= 0:
            self.show_message("Please enter a valid quantity")
            return

        # Get the highest existing sequential number for this project
        batches = load_tag_batches()
        project_num = int(self.current_project_id)

        existing_seq = []
        for batch_id, batch in batches.items():
            if batch.get('project_id') == self.current_project_id:
                for tag in batch.get('tags', []):
                    field_id = tag.get('field_id', 0)
                    if field_id >= 1000:
                        existing_seq.append(field_id % 1000)

        starting_seq = max(existing_seq) + 1 if existing_seq else 1

        # Calculate the starting field ID
        field_id_start = (project_num * 1000) + starting_seq

        # Generate tags
        tags = []
        new_database_entries = {}

        for i in range(quantity):
            # Generate 16-digit alphanumeric for barcode
            import secrets
            import string
            alphabet = string.ascii_uppercase + string.digits
            barcode = ''.join(secrets.choice(alphabet) for _ in range(16))

            # Calculate field ID
            field_id = field_id_start + i

            tags.append({
                'barcode': barcode,
                'field_id': field_id,
                'sequential': starting_seq + i,
                'project_id': self.current_project_id,
                'created': datetime.now().isoformat()
            })

            # Create database entry with empty fields
            new_database_entries[str(field_id)] = {
                "DATABASE_ID": barcode,
                "FIELD_ID": str(field_id),
                "PROJECT_ID": self.current_project_id,
                "SITE_NAME_NONSASES": "",
                "SITE_NAME_SASES": "",
                "COLLECTION_METHOD": "",
                "COLLECTOR": "",
                "MONTH": "",
                "DAY": "",
                "YEAR": "",
                "COLLECTION_MATERIAL": "",
                "CHRONOLOGY1": "",
                "CHRONOLOGY2": "",
                "CHRONOLOGY3": "",
                "LAT": "",
                "LONG": "",
                "COLLECTING_AREA": "",
                "CONTEXT": "",
                "ANALYSIS": "",
                "NOTES": "",
                "PHOTOS": [],
                "exported": False
            }

        # Save batch
        batches = load_tag_batches()
        batch_id = f"{self.current_project_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        batches[batch_id] = {
            'project_id': self.current_project_id,
            'quantity': quantity,
            'start_sequential': starting_seq,
            'end_sequential': starting_seq + quantity - 1,
            'tags': tags,
            'created_at': datetime.now().isoformat(),
            'created_by': MDApp.get_running_app().current_admin.get("username")
        }
        save_tag_batches(batches)

        # Update the master database with new entries
        self.update_master_database(new_database_entries)

        self.generate_dialog.dismiss()

        # Format display for success message
        last_field_id = field_id_start + quantity - 1
        project_num_formatted = f"{project_num:03d}"
        first_field_display = f"{project_num_formatted}{starting_seq:04d}"
        last_field_display = f"{project_num_formatted}{starting_seq + quantity - 1:04d}"

        self.show_message(
            f"Generated {quantity} tags and database entries!\nField IDs: {first_field_display} to {last_field_display}")

        # Generate PDF
        self.generate_pdf(batch_id, tags)

    def update_master_database(self, new_entries):
        """Add new database entries to the master JSON file"""
        from pathlib import Path

        # Get project info to determine export path
        projects = load_projects()
        project = projects.get(self.current_project_id, {})
        project_name = project.get('name', 'unnamed')

        # Create directory structure
        export_dir = Path.home() / "field_data_exports" / f"project_{self.current_project_id}"
        export_dir.mkdir(parents=True, exist_ok=True)

        json_path = export_dir / f"project_{self.current_project_id}_data.json"

        # Load existing data or create new
        if json_path.exists():
            with open(json_path) as f:
                existing_data = json.load(f)
        else:
            existing_data = {}

        # Add new entries (don't overwrite existing)
        for field_id, entry in new_entries.items():
            if field_id not in existing_data:
                existing_data[field_id] = entry

        # Save back
        with open(json_path, 'w') as f:
            json.dump(existing_data, f, indent=2)

        print(f"Updated master database at {json_path}")

    def generate_pdf(self, batch_id, tags):
        if not PDF_AVAILABLE:
            self.show_message("PDF generation not available")
            return

        if not tags:
            self.show_message("No tags to generate")
            return

        projects = load_projects()
        project = projects.get(self.current_project_id, {})
        project_name = project.get('name', 'Unnamed Project')
        project_leader_username = project.get('leader', '')

        seasons = load_seasons()
        season_id = project.get('season_id', '')
        season_data = seasons.get(season_id, {})
        year = season_data.get('year', 'YYYY')

        admins = load_admins()
        leader_data = admins.get(project_leader_username, {})
        leader_last = leader_data.get('last_name', '')
        if not leader_last:
            leader_clean = project.get('leader_name', '').split('(')[0].strip()
            leader_last = leader_clean.split()[-1] if leader_clean.split() else leader_clean

        project_line = f"{leader_last} - {year} - {project_name}"
        custom_fields = self.tag_config.get('custom_fields', [])
        field_labels = [f.get('label', '') for f in custom_fields[:5]]
        while len(field_labels) < 5:
            field_labels.append('')

        project_num = int(self.current_project_id)

        desktop = Path.home() / "Desktop"
        bagtags_dir = desktop / "BagTags"
        bagtags_dir.mkdir(exist_ok=True)
        filename = f"bag_tags_{self.current_project_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = bagtags_dir / filename

        # Page setup: letter, 3 columns x 6 rows = 18 tags/page
        pdf = FPDF(orientation='P', unit='mm', format='Letter')
        pdf.set_margins(6, 6, 6)
        pdf.set_auto_page_break(auto=False)

        # Tag dimensions
        page_w = 215.9  # letter width mm
        page_h = 279.4  # letter height mm
        margin = 6
        cols = 3
        rows = 6
        tag_w = (page_w - 2 * margin) / cols  # ~68mm
        tag_h = (page_h - 2 * margin) / rows  # ~44mm
        tags_per_page = cols * rows

        for page_start in range(0, len(tags), tags_per_page):
            pdf.add_page()
            page_tags = tags[page_start:page_start + tags_per_page]

            for i, tag in enumerate(page_tags):
                col = i % cols
                row = i // cols
                x = margin + col * tag_w
                y = margin + row * tag_h

                # Outer border
                pdf.set_draw_color(180, 180, 180)
                pdf.rect(x, y, tag_w, tag_h)

                # --- Header ---
                pdf.set_xy(x + 1, y + 1)
                pdf.set_font('Helvetica', 'B', 6)
                pdf.cell(tag_w - 2, 3.5,
                         'Koobi Fora Research and Training Program',
                         ln=True, align='C')

                pdf.set_xy(x + 1, y + 4.5)
                pdf.set_font('Helvetica', '', 5.5)
                pdf.cell(tag_w - 2, 3, project_line, ln=True, align='C')

                # --- Field grid ---
                # Date + custom field 1
                fy = y + 9
                half = (tag_w - 2) / 2
                pdf.set_font('Helvetica', '', 5.5)

                pdf.set_xy(x + 1, fy)
                pdf.cell(half, 3.5, 'Date: __________')
                pdf.set_xy(x + 1 + half, fy)
                lbl1 = f"{field_labels[0]}: __________" if field_labels[0] else ''
                pdf.cell(half, 3.5, lbl1)

                # Custom fields 2 & 3
                fy += 4
                pdf.set_xy(x + 1, fy)
                lbl2 = f"{field_labels[1]}: __________" if field_labels[1] else ''
                pdf.cell(half, 3.5, lbl2)
                pdf.set_xy(x + 1 + half, fy)
                lbl3 = f"{field_labels[2]}: __________" if field_labels[2] else ''
                pdf.cell(half, 3.5, lbl3)

                # Custom fields 4 & 5
                fy += 4
                pdf.set_xy(x + 1, fy)
                lbl4 = f"{field_labels[3]}: __________" if field_labels[3] else ''
                pdf.cell(half, 3.5, lbl4)
                pdf.set_xy(x + 1 + half, fy)
                lbl5 = f"{field_labels[4]}: __________" if field_labels[4] else ''
                pdf.cell(half, 3.5, lbl5)

                # --- Barcode as Code128 text representation ---
                # fpdf2 has built-in barcode support
                fy += 5.5
                barcode_val = tag['barcode']
                pdf.set_xy(x + 1, fy)
                try:
                    # fpdf2 >= 2.5 has interleaved2of5 and code39
                    # For Code128 use the barcode module
                    from fpdf.enums import TextMode
                    pdf.set_font('Courier', '', 5)
                    # Draw barcode as narrow/wide bars via built-in
                    pdf.code39(barcode_val[:15],  # code39 max practical length
                               x=x + 3,
                               y=fy,
                               w=tag_w - 6,
                               h=6)
                    fy += 7
                except Exception:
                    # Fallback: just print barcode string in courier
                    pdf.set_font('Courier', 'B', 6)
                    pdf.cell(tag_w - 2, 4, barcode_val, align='C')
                    fy += 5

                # --- Bottom row: Note + Field ID ---
                field_id_display = f"{project_num:02d}{tag['sequential']:03d}"
                pdf.set_xy(x + 1, fy)
                pdf.set_font('Helvetica', '', 5.5)
                pdf.cell(half, 3.5, 'Note: ___________')
                pdf.set_xy(x + 1 + half, fy)
                pdf.set_font('Helvetica', 'B', 7)
                pdf.cell(half, 3.5, field_id_display, align='R')

        pdf.output(str(filepath))

        if filepath.exists():
            self.open_pdf(str(filepath))
            self.show_message(f"PDF saved to:\n{filepath}")
        else:
            self.show_message("PDF generation failed")

    def open_pdf(self, filepath):
        """Open PDF with default viewer"""
        import platform
        import subprocess

        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', filepath])
            elif platform.system() == 'Windows':
                import os
                os.startfile(filepath)
            elif platform.system() == 'Linux':
                subprocess.run(['xdg-open', filepath])
        except Exception as e:
            print(f"Could not open PDF: {e}")
            self.show_message(f"PDF saved to: {filepath}")


    def go_back(self):
        """Return to project management"""
        self.manager.current = "project_management"

    def show_message(self, message):
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDRaisedButton
        dialog = MDDialog(
            text=message,
            buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()