from admin import load_users, save_users, save_projects, save_seasons, load_projects,load_seasons
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDRectangleFlatButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDRectangleFlatButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
from pathlib import Path
import json
from datetime import datetime
from kivy.uix.widget import Widget

try:
    from permissions import RuntimePermissionScreen, ANDROID_AVAILABLE
except ImportError:
    ANDROID_AVAILABLE = False
    class RuntimePermissionScreen:
        def check_and_request_permissions(self, on_granted=None, on_denied=None):
            if on_granted: on_granted()
            return True


try:
    from plyer import camera
    CAMERA_AVAILABLE = True
except ImportError:
    CAMERA_AVAILABLE = False
    print("Camera not available - using mock photos")

# For GPS (will be used when testing on phone)
try:
    from plyer import gps

    GPS_AVAILABLE = True
except ImportError:
    GPS_AVAILABLE = False
    print("GPS not available - using mock data")

KV = '''
<CollectScreen>:
    MDBoxLayout:
        orientation: "vertical"
        size_hint: (1, 1)  
        pos_hint: {'x': 0, 'y': 0}

        MDTopAppBar:
            id: top_app_bar
            title: "Data Collection"
            left_action_items: [["menu", lambda x: root.open_menu()]]
            right_action_items: [["refresh", lambda x: root.reset_form()]]

        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                spacing: "16dp"
                padding: "16dp"
                size_hint_y: None
                height: self.minimum_height
        
                # Field ID, Site Name, and SASES Name Card
                MDCard:
                    orientation: "vertical"
                    padding: "3dp"
                    spacing: "3dp"
                    size_hint_y: None
                    height: "180dp"
        
                    MDBoxLayout:
                        orientation: "horizontal"
                        spacing: "8dp"
        
                        MDLabel:
                            text: "Field ID:"
                            theme_text_color: "Primary"
                            font_style: "H6"
                            size_hint_x: 0.3
        
                        MDTextField:
                            id: field_id_field
                            hint_text: "Field ID"
                            mode: "rectangle"
                            size_hint_x: 0.7
                            input_filter: "int"
                            max_text_length: 5
        
                    MDTextField:
                        id: site_name_field
                        hint_text: "Site Name"
                        mode: "rectangle"
        
                    MDTextField:
                        id: sases_name_field
                        hint_text: "SASES Name"
                        mode: "rectangle"
                                
                # GPS Card
                MDCard:
                    orientation: "vertical"
                    padding: "16dp"
                    spacing: "16dp"
                    size_hint_y: None
                    height: self.minimum_height

                    MDBoxLayout:
                        orientation: "horizontal"
                        spacing: "10dp"
                        size_hint_y: None
                        height: "30dp"

                        MDLabel:
                            text: "Current Location:"
                            theme_text_color: "Secondary"
                            size_hint_x: 0.5
                            halign: "left"

                        MDIcon:
                            icon: "crosshairs-gps"
                            size_hint_x: None
                            width: "24dp"

                    MDBoxLayout:
                        orientation: "horizontal"
                        size_hint_y: None
                        height: "48dp"
                        spacing: "10dp"

                        MDLabel:
                            text: "Lat:"
                            theme_text_color: "Secondary"
                            size_hint_x: 0.2
                            halign: "right"

                        MDLabel:
                            id: lat_label
                            text: "---"
                            halign: "left"
                            size_hint_x: 0.3

                        MDLabel:
                            text: "Lon:"
                            theme_text_color: "Secondary"
                            size_hint_x: 0.2
                            halign: "right"

                        MDLabel:
                            id: lon_label
                            text: "---"
                            halign: "left"
                            size_hint_x: 0.3


                        
                    MDBoxLayout:
                        orientation: "horizontal"
                        spacing: "10dp"
                        size_hint_y: None
                        height: "48dp"
                        
                        MDRaisedButton:
                            text: "REFRESH GPS"
                            icon: "refresh"
                            size_hint_x: 0.5
                            pos_hint: {"center_x": 0.5}
                            on_release: root.update_gps()
                        
                        MDRaisedButton:
                            text: "DROP CRUMB"
                            icon: "map-marker"
                            size_hint_x: 0.5
                            on_release: root.drop_breadcrumb()
                        

                # Collector Info Card
                MDCard:
                    orientation: "vertical"
                    padding: "16dp"
                    spacing: "16dp"
                    size_hint_y: None
                    height: self.minimum_height

                    MDLabel:
                        text: "Collection Information"
                        theme_text_color: "Primary"
                        font_style: "H6"

                    MDTextField:
                        id: collecting_area_field
                        hint_text: "Collecting Area"
                        mode: "rectangle"

                    MDTextField:
                        id: analysis_field
                        hint_text: "Analysis"
                        mode: "rectangle"
                        multiline: True

                # Dropdown Selections Card
                MDCard:
                    orientation: "vertical"
                    padding: "16dp"
                    spacing: "16dp"
                    size_hint_y: None
                    height: self.minimum_height

                    MDLabel:
                        text: "Collection Parameters"
                        theme_text_color: "Primary"
                        font_style: "H6"

                    # Two-column grid for dropdowns
                    MDBoxLayout:
                        orientation: "horizontal"
                        spacing: "16dp"
                        size_hint_y: None
                        height: self.minimum_height

                        # Left column
                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: "12dp"
                            size_hint_x: 0.5
                            size_hint_y: None
                            height: self.minimum_height

                            # Collection Method Dropdown
                            MDBoxLayout:
                                orientation: "vertical"
                                spacing: "4dp"
                                size_hint_y: None
                                height: "70dp"

                                MDLabel:
                                    text: "Collection Method:"
                                    theme_text_color: "Secondary"
                                    font_style: "Caption"
                                    size_hint_y: None
                                    height: "20dp"

                                MDRaisedButton:
                                    id: collection_method_button
                                    text: "Select Method"
                                    size_hint_x: 1
                                    size_hint_y: None
                                    height: "48dp"
                                    on_release: root.open_collection_method_menu()

                            # Collection Material Dropdown
                            MDBoxLayout:
                                orientation: "vertical"
                                spacing: "4dp"
                                size_hint_y: None
                                height: "70dp"

                                MDLabel:
                                    text: "Collection Material:"
                                    theme_text_color: "Secondary"
                                    font_style: "Caption"
                                    size_hint_y: None
                                    height: "20dp"

                                MDRaisedButton:
                                    id: collection_material_button
                                    text: "Select Material"
                                    size_hint_x: 1
                                    size_hint_y: None
                                    height: "48dp"
                                    on_release: root.open_collection_material_menu()

                        # Right column
                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: "12dp"
                            size_hint_x: 0.5
                            size_hint_y: None
                            height: self.minimum_height

                            # Chronology 1 Dropdown
                            MDBoxLayout:
                                orientation: "vertical"
                                spacing: "4dp"
                                size_hint_y: None
                                height: "70dp"

                                MDLabel:
                                    text: "Chronology 1:"
                                    theme_text_color: "Secondary"
                                    font_style: "Caption"
                                    size_hint_y: None
                                    height: "20dp"

                                MDRaisedButton:
                                    id: chronology1_button
                                    text: "Select Chronology 1"
                                    size_hint_x: 1
                                    size_hint_y: None
                                    height: "48dp"
                                    on_release: root.open_chronology1_menu()

                            # Chronology 2 Dropdown
                            MDBoxLayout:
                                orientation: "vertical"
                                spacing: "4dp"
                                size_hint_y: None
                                height: "70dp"

                                MDLabel:
                                    text: "Chronology 2:"
                                    theme_text_color: "Secondary"
                                    font_style: "Caption"
                                    size_hint_y: None
                                    height: "20dp"

                                MDRaisedButton:
                                    id: chronology2_button
                                    text: "Select Chronology 2"
                                    size_hint_x: 1
                                    size_hint_y: None
                                    height: "48dp"
                                    on_release: root.open_chronology2_menu()

                    # Context Dropdown - Centered full width (outside the two-column layout)
                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: "4dp"
                        size_hint_y: None
                        height: "70dp"
                        padding: ["20dp", "10dp", "20dp", "0dp"]

                        MDLabel:
                            text: "Context:"
                            theme_text_color: "Secondary"
                            font_style: "Caption"
                            size_hint_y: None
                            height: "20dp"
                            halign: "center"

                        MDRaisedButton:
                            id: context_button
                            text: "Select Context"
                            size_hint_x: 1
                            size_hint_y: None
                            height: "48dp"
                            pos_hint: {"center_x": 0.5}
                            on_release: root.open_context_menu()

                    MDTextField:
                        id: chronology3_field
                        hint_text: "Chronology 3"
                        mode: "rectangle"

                # Notes Card
                MDCard:
                    orientation: "vertical"
                    padding: "16dp"
                    spacing: "16dp"
                    size_hint_y: None
                    height: self.minimum_height

                    MDLabel:
                        text: "Observation Notes:"
                        theme_text_color: "Secondary"

                    MDTextField:
                        id: notes_field
                        hint_text: "Enter any observations..."
                        mode: "rectangle"
                        multiline: True

                # Action Buttons
                MDRaisedButton:
                    text: "TAKE PHOTO"
                    icon: "camera"
                    size_hint: None, None
                    size: "200dp", "48dp"
                    pos_hint: {"center_x": 0.5}
                    on_release: root.take_photo()

                MDRectangleFlatButton:
                    text: "SAVE OBSERVATION"
                    size_hint: None, None
                    size: "200dp", "48dp"
                    pos_hint: {"center_x": 0.5}
                    on_release: root.save_observation()
'''


class CollectScreen(MDScreen, RuntimePermissionScreen):  # Add RuntimePermissionScreen
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu = None
        self.current_field_num = 0
        self.collection_method_menu = None
        self.collection_material_menu = None
        self.chronology1_menu = None
        self.chronology2_menu = None
        self.context_menu = None
        self.current_gps = None
        self.photos = []

    def on_enter(self):
        """Called when screen is shown"""
        # Check permissions before using camera/GPS
        self.check_and_request_permissions(
            on_granted=self._on_permissions_granted,
            on_denied=self._on_permissions_denied
        )

    def _on_permissions_granted(self):
        """Permissions granted, proceed normally"""
        self.update_gps()
        self.load_saved_observations()

    def _on_permissions_denied(self):
        """Permissions denied, show error"""
        self.show_message("Camera and GPS permissions are required for data collection")

    def get_data_dir(self):
        from pathlib import Path
        data_dir = Path('field_data')
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir

    def test_sync_to_server(self):
        """Test sending data to the base station server"""
        import requests

        # Your laptop's IP from the server output
        SERVER_IP = "10.0.0.3"  # Replace with your actual IP
        url = f"http://{SERVER_IP}:5000/api/sync"

        # Sample data to send
        test_data = {
            "device_id": "test_device_1",
            "observations": {
                "10001": {
                    "field_id": "10001",
                    "site_name": "Test Site",
                    "timestamp": "2024-01-01T12:00:00"
                }
            }
        }

        try:
            response = requests.post(url, json=test_data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                self.show_message(f"Sync successful! Added {result.get('added', 0)} records")
            else:
                self.show_message(f"Sync failed: {response.status_code}")
        except Exception as e:
            self.show_message(f"Connection error: {str(e)}")

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
            # Find the status label and update it
            for child in self.settings_dialog.content_cls.children:
                if isinstance(child, MDBoxLayout):
                    for subchild in child.children:
                        if isinstance(subchild, MDLabel) and subchild.text in ["ON", "OFF"]:
                            subchild.text = current_theme
                            break

        # Save preference
        data_dir = self.get_data_dir()
        prefs_file = data_dir / "preferences.json"
        # No need for mkdir() here because get_data_dir() already creates the directory

        if prefs_file.exists():
            with open(prefs_file) as f:
                prefs = json.load(f)
        else:
            prefs = {}

        prefs['theme_style'] = app.theme_cls.theme_style
        with open(prefs_file, 'w') as f:
            json.dump(prefs, f, indent=2)

    def sync_to_base(self):
        """Send unsynced observations to base station"""
        import requests
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.textfield import MDTextField
        from kivy.uix.boxlayout import BoxLayout

        # First, ask for the base station IP
        content = BoxLayout(orientation='vertical', spacing=10, padding=20, size_hint_y=None, height=100)

        self.base_ip_field = MDTextField(
            hint_text="Base Station IP (e.g., 10.0.0.3)",
            mode="rectangle",
            text="10.0.0.3"
        )
        content.add_widget(self.base_ip_field)

        self.sync_dialog = MDDialog(
            title="Sync to Base Station",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: self.sync_dialog.dismiss()),
                MDRaisedButton(text="SYNC", on_release=lambda x: self.perform_sync(self.base_ip_field.text.strip()))
            ]
        )
        self.sync_dialog.open()

    def perform_sync(self, base_ip):
        """Perform the actual sync to base station"""
        import requests
        from kivy.clock import Clock

        if self.sync_dialog:
            self.sync_dialog.dismiss()

        if not base_ip:
            self.show_message("Please enter a valid IP address")
            return

        # Show progress dialog
        self.progress_dialog = MDDialog(
            title="Syncing...",
            text="Sending data to base station...",
            auto_dismiss=False
        )
        self.progress_dialog.open()

        # Run sync in a separate thread to not freeze UI
        Clock.schedule_once(lambda dt: self._do_sync(base_ip), 0.1)

    def _do_sync(self, base_ip):
        """Actually send the data and images to base station"""
        import requests
        import json
        from pathlib import Path

        print(f"🔵 Starting sync to {base_ip}")

        # Load local observations - FIXED: add filename
        data_dir = self.get_data_dir()
        obs_file = data_dir / "observations.json"  # ← Added filename
        if not obs_file.exists():
            self.progress_dialog.dismiss()
            self.show_message("No observations to sync")
            return

        with open(obs_file) as f:
            all_observations = json.load(f)

        print(f"🔵 Loaded {len(all_observations)} total observations")

        # Get current user info
        app = MDApp.get_running_app()
        current_user = getattr(app, 'current_user', None)
        device_id = current_user.get('user_id', 'unknown') if current_user else 'unknown'

        print(f"🔵 Device ID: {device_id}")

        # Filter unsynced observations
        unsynced = {}
        for field_id, obs in all_observations.items():
            if not obs.get('synced', False):
                unsynced[field_id] = obs

        print(f"🔵 Found {len(unsynced)} unsynced observations")

        if not unsynced:
            self.progress_dialog.dismiss()
            self.show_message("All observations already synced")
            return

        # Prepare payload
        payload = {
            "device_id": device_id,
            "observations": unsynced
        }

        url = f"http://{base_ip}:5000/api/sync"
        print(f"🔵 Sending to URL: {url}")

        try:
            print("🔵 Testing connection...")
            status_response = requests.get(f"http://{base_ip}:5000/api/status", timeout=5)
            print(f"🔵 Status response: {status_response.status_code}")

            print("🔵 Sending sync request...")
            response = requests.post(url, json=payload, timeout=30)

            self.progress_dialog.dismiss()

            print(f"🔵 Response status: {response.status_code}")
            print(f"🔵 Response body: {response.text}")

            if response.status_code == 200:
                result = response.json()
                added = result.get('added', 0)

                # Mark synced observations as synced
                for field_id in unsynced.keys():
                    all_observations[field_id]['synced'] = True
                    all_observations[field_id]['synced_at'] = datetime.now().isoformat()

                with open(obs_file, 'w') as f:
                    json.dump(all_observations, f, indent=2)

                self.show_message(f"Sync complete!\nAdded {added} observations to base station")
            else:
                self.show_message(f"Sync failed: Server returned {response.status_code}\n{response.text}")

        except requests.exceptions.ConnectionError as e:
            self.progress_dialog.dismiss()
            print(f"🔴 Connection error: {e}")
            self.show_message(f"Cannot connect to {base_ip}. Make sure the base station server is running.")
        except Exception as e:
            self.progress_dialog.dismiss()
            print(f"🔴 Sync error: {e}")
            import traceback
            traceback.print_exc()
            self.show_message(f"Sync error: {str(e)}")

    def scan_project_qr(self):
        """Scan QR code to join a project"""
        if CAMERA_AVAILABLE and camera:
            # On real device, use camera
            try:
                camera.take_picture(on_complete=self.on_qr_captured)
                self.show_message("Take a photo of the QR code...")
            except Exception as e:
                print(f"Camera error: {e}")
                self.show_qr_input_dialog()
        else:
            # For testing on computer, use input dialog
            self.show_qr_input_dialog()

    def on_qr_captured(self, filepath):
        """Handle captured QR code image"""
        # This would need QR decoding library (like pyzbar)
        # For now, fall back to manual input
        self.show_qr_input_dialog()
        self.show_message("QR scanning coming soon. Please enter data manually.")

    def show_qr_input_dialog(self):
        """Show dialog to enter QR code data (for testing)"""
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
                MDRaisedButton(text="JOIN", on_release=lambda x: self.process_project_qr(self.qr_input_field.text))
            ]
        )
        self.qr_dialog.open()

    def process_project_qr(self, qr_data):
        """Process scanned QR code and import project configuration"""
        import json
        from kivymd.app import MDApp
        from pathlib import Path

        if hasattr(self, 'qr_dialog') and self.qr_dialog:
            self.qr_dialog.dismiss()

        try:
            config = json.loads(qr_data)

            if config.get('version') != '1.0':
                self.show_message("Unsupported QR code version")
                return

            project_id = config.get('project_id')
            project_name = config.get('project_name')
            season_id = config.get('season_id')
            users_data = config.get('users', {})

            # Load existing data (using imported functions)
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

            # Update current user's session if this is the logged-in user
            app = MDApp.get_running_app()
            if hasattr(app, 'current_user') and app.current_user:
                # Check if the logged-in user is in the imported users
                current_user_id = app.current_user.get('user_id')
                if current_user_id and current_user_id in users_data:
                    app.current_user['season'] = season_id
                    app.current_user['project'] = project_id
                    app.current_user['user_name'] = users_data[current_user_id].get('name', '')

                    # Update saved credentials - UPDATED
                    data_dir = self.get_data_dir()
                    cred_file = data_dir / "credentials.json"
                    if cred_file.exists():
                        with open(cred_file) as f:
                            creds = json.load(f)
                        creds['season'] = season_id
                        creds['project'] = project_id
                        with open(cred_file, 'w') as f:
                            json.dump(creds, f, indent=2)

            self.show_message(f"Joined project '{project_name}'\nImported {imported_count} users")

        except json.JSONDecodeError:
            self.show_message("Invalid QR code data")
        except Exception as e:
            self.show_message(f"Error: {str(e)}")

    def update_gps(self):
        """Update GPS coordinates"""
        if GPS_AVAILABLE:
            try:
                gps.configure(on_location=self.on_gps_location, on_status=self.on_gps_status)
                gps.start()
            except NotImplementedError:
                self.use_mock_gps()
        else:
            self.use_mock_gps()

    def use_mock_gps(self):
        """Use mock GPS data for testing"""
        self.current_gps = (-1.2921, 36.8219)  # Nairobi
        self.ids.lat_label.text = f"{self.current_gps[0]:.6f}"
        self.ids.lon_label.text = f"{self.current_gps[1]:.6f}"

    def on_gps_location(self, **kwargs):
        """Called when GPS location updates"""
        lat = kwargs.get('lat')
        lon = kwargs.get('lon')
        if lat and lon:
            self.current_gps = (lat, lon)
            self.ids.lat_label.text = f"{lat:.6f}"
            self.ids.lon_label.text = f"{lon:.6f}"

    def on_gps_status(self, stype, status):
        """Called when GPS status changes"""
        if stype == 'provider-enabled':
            print("GPS provider enabled")
        elif stype == 'provider-disabled':
            print("GPS provider disabled")

    def start_live_tracking(self, target_bc):
        """Start live tracking to selected breadcrumb"""
        self.tracking_target = target_bc
        self.tracking_active = True

        self.tracking_target = target_bc
        self.tracking_active = True

        from kivy.uix.boxlayout import BoxLayout
        from kivymd.uix.label import MDLabel

        content = BoxLayout(
            orientation='vertical',
            spacing=15,
            padding=[20, 40, 20, 25],
            size_hint_y=None,
            height=380
        )

        # Target name (use custom name if available)
        target_name = target_bc.get('name', f"Pin {target_bc['id']}")
        content.add_widget(
            MDLabel(
                text=f"Target: {target_name}",
                font_style="H6",
                halign="center",
                size_hint_y=None,
                height=35
            )
        )
        content.add_widget(Widget(size_hint_y=None, height=5))

        # Distance (large)
        self.tracking_distance_label = MDLabel(
            text="-- m",
            font_style="H2",
            halign="center",
            size_hint_y=None,
            height=70
        )
        content.add_widget(self.tracking_distance_label)
        content.add_widget(Widget(size_hint_y=None, height=5))

        # Direction to target
        self.tracking_direction_label = MDLabel(
            text="To target: --",
            font_style="H4",
            halign="center",
            size_hint_y=None,
            height=50
        )
        content.add_widget(self.tracking_direction_label)
        content.add_widget(Widget(size_hint_y=None, height=5))

        # Your heading
        self.tracking_heading_label = MDLabel(
            text="Heading: --",
            font_style="H4",
            halign="center",
            size_hint_y=None,
            height=50
        )
        content.add_widget(self.tracking_heading_label)
        content.add_widget(Widget(size_hint_y=None, height=5))

        # Your Location
        self.tracking_status_label = MDLabel(
            text="Location: --",
            font_style="Caption",
            halign="center",
            size_hint_y=None,
            height=35
        )
        content.add_widget(self.tracking_status_label)

        self.tracking_dialog = MDDialog(
            title="Live Tracking:",
            type="custom",
            content_cls=content,
            size_hint=(0.9, None),
            height=460,
            auto_dismiss=False,
            buttons=[
                MDRaisedButton(
                    text="STOP",
                    md_bg_color=(0.8, 0.2, 0.2, 1),
                    on_release=lambda x: self.stop_tracking()
                )
            ]
        )
        self.tracking_dialog.open()

        Clock.schedule_interval(self.update_tracking_display_simple, 1.0)

    def update_tracking_display_simple(self, dt):
        """Update tracking display with current GPS"""
        if not self.tracking_active or not hasattr(self, 'tracking_dialog') or not self.tracking_dialog:
            return

        if not self.current_gps:
            self.tracking_status_label.text = "Location: --"
            return

        lat1, lon1 = self.current_gps
        lat2, lon2 = self.tracking_target['lat'], self.tracking_target['lon']

        from math import radians, sin, cos, sqrt, atan2

        R = 6371000
        φ1 = radians(lat1)
        φ2 = radians(lat2)
        Δφ = radians(lat2 - lat1)
        Δλ = radians(lon2 - lon1)

        a = sin(Δφ / 2) ** 2 + cos(φ1) * cos(φ2) * sin(Δλ / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c

        # Bearing to target
        y = sin(Δλ) * cos(φ2)
        x = cos(φ1) * sin(φ2) - sin(φ1) * cos(φ2) * cos(Δλ)
        bearing = atan2(y, x)
        bearing_deg = (bearing * 180 / 3.14159 + 360) % 360

        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        idx = round(bearing_deg / 45) % 8
        cardinal = directions[idx]

        # Simple heading calculation from previous GPS reading
        if hasattr(self, '_last_gps'):
            last_lat, last_lon = self._last_gps
            if last_lat != lat1 or last_lon != lon1:
                # Calculate heading from movement
                Δφ_heading = radians(lat1 - last_lat)
                Δλ_heading = radians(lon1 - last_lon)
                heading = atan2(Δλ_heading, Δφ_heading)
                heading_deg = (heading * 180 / 3.14159 + 360) % 360
                heading_idx = round(heading_deg / 45) % 8
                heading_cardinal = directions[heading_idx]
            else:
                heading_cardinal = "?"
        else:
            heading_cardinal = "?"

        # Store current GPS for next calculation
        self._last_gps = (lat1, lon1)

        self.tracking_distance_label.text = f"{distance:.0f} m"
        self.tracking_direction_label.text = f"To Target: {cardinal} ({bearing_deg:.0f}°)"
        self.tracking_heading_label.text = f"Heading: {heading_cardinal}"
        self.tracking_status_label.text = f"Location: {lat1:.6f}, {lon1:.6f}"

        if distance < 10:
            self.tracking_distance_label.text_color = (0.2, 0.8, 0.2, 1)
        elif distance < 50:
            self.tracking_distance_label.text_color = (0.8, 0.8, 0.2, 1)
        else:
            self.tracking_distance_label.text_color = (1, 1, 1, 1)

    def stop_tracking(self):
        """Stop live tracking"""
        self.tracking_active = False
        if hasattr(self, 'tracking_dialog') and self.tracking_dialog:
            self.tracking_dialog.dismiss()
            self.tracking_dialog = None
        Clock.unschedule(self.update_tracking_display_simple)

    def drop_breadcrumb(self):
        """Save current GPS location as a named breadcrumb"""
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.textfield import MDTextField
        from kivymd.uix.button import MDRaisedButton, MDFlatButton
        from kivy.uix.boxlayout import BoxLayout

        if not self.current_gps:
            self.show_message("No GPS fix yet. Wait for GPS to update.")
            return

        # Create dialog for entering breadcrumb name
        content = BoxLayout(orientation='vertical', spacing=10, padding=20, size_hint_y=None, height=100)

        self.breadcrumb_name_field = MDTextField(
            hint_text="Enter a name for this location (e.g., 'Water Source', 'Excavation Site A')",
            mode="rectangle",
            multiline=False
        )
        content.add_widget(self.breadcrumb_name_field)

        self.name_dialog = MDDialog(
            title="Name Your Location",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: self.name_dialog.dismiss()),
                MDRaisedButton(text="SAVE", on_release=lambda x: self.save_named_breadcrumb())
            ]
        )
        self.name_dialog.open()

    def save_named_breadcrumb(self):
        """Save the breadcrumb with the entered name"""
        name = self.breadcrumb_name_field.text.strip()
        if not name:
            name = f"Location {self.get_next_breadcrumb_id()}"

        lat, lon = self.current_gps

        # Load existing breadcrumbs - FIXED: ensure filename is appended
        data_dir = self.get_data_dir()
        bc_file = data_dir / "breadcrumbs.json"  # ← Already correct, but ensure pattern

        if bc_file.exists():
            with open(bc_file) as f:
                breadcrumbs = json.load(f)
        else:
            breadcrumbs = []

        # Create new breadcrumb with name
        timestamp = datetime.now()
        breadcrumb = {
            "id": len(breadcrumbs) + 1,
            "name": name,
            "lat": lat,
            "lon": lon,
            "timestamp": timestamp.isoformat(),
            "time_str": timestamp.strftime("%H:%M:%S"),
            "date_str": timestamp.strftime("%Y-%m-%d")
        }

        breadcrumbs.append(breadcrumb)

        # Save
        with open(bc_file, 'w') as f:
            json.dump(breadcrumbs, f, indent=2)

        self.name_dialog.dismiss()
        self.show_message(f"Saved: {name}\nLat: {lat:.6f}, Lon: {lon:.6f}")

    def get_next_breadcrumb_id(self):
        """Get the next available breadcrumb ID"""
        data_dir = self.get_data_dir()
        bc_file = data_dir / "breadcrumbs.json"
        if bc_file.exists():
            with open(bc_file) as f:
                breadcrumbs = json.load(f)
            return len(breadcrumbs) + 1
        return 1

    def view_breadcrumbs(self):
        """Show list of named breadcrumbs"""
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.label import MDLabel
        from kivy.uix.boxlayout import BoxLayout

        data_dir = self.get_data_dir()
        bc_file = data_dir / "breadcrumbs.json"
        if not bc_file.exists():
            self.show_message("No breadcrumbs dropped yet")
            return

        with open(bc_file) as f:
            breadcrumbs = json.load(f)

        if not breadcrumbs:
            self.show_message("No breadcrumbs dropped yet")
            return

        # Limit to show up to 15 breadcrumbs
        limited_bc = breadcrumbs[-15:]
        total_count = len(breadcrumbs)
        showing_count = len(limited_bc)

        # Calculate height based on number of items
        item_height = 40
        total_height = showing_count * item_height + 20

        # Create a vertical layout with exact height
        layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=total_height,
            spacing=2,
            padding=5
        )

        # Add each breadcrumb in reverse order (newest first)
        for bc in reversed(limited_bc):
            name = bc.get('name', f"Pin {bc['id']}")
            date_str = bc.get('date_str', 'Unknown')

            # Simple text display without icon
            display_text = f"{name} ({date_str})"

            label = MDLabel(
                text=display_text,
                size_hint_y=None,
                height=item_height,
                font_style="Body1"
            )
            layout.add_widget(label)

        # Create dialog with buttons
        title = f"Breadcrumb Trail ({total_count})"
        if total_count > 15:
            title += f" - showing most recent 15"

        self.bc_dialog = MDDialog(
            title=title,
            type="custom",
            content_cls=layout,
            size_hint=(0.9, None),
            height=total_height + 100,
            buttons=[
                MDRaisedButton(
                    text="RETRACE",
                    on_release=lambda x: self.show_retrace_options(breadcrumbs)
                ),
                MDRaisedButton(
                    text="CLEAR ALL",
                    md_bg_color=(0.8, 0.2, 0.2, 1),
                    on_release=lambda x: self.clear_breadcrumbs()
                ),
                MDRaisedButton(
                    text="CLOSE",
                    on_release=lambda x: self.bc_dialog.dismiss()
                )
            ]
        )
        self.bc_dialog.open()

    def show_retrace_options(self, breadcrumbs):
        """Show a list of breadcrumbs to retrace to"""
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.label import MDLabel
        from kivy.uix.boxlayout import BoxLayout

        self.bc_dialog.dismiss()

        if not breadcrumbs:
            self.show_message("No breadcrumbs available")
            return

        # Limit to show up to 15 breadcrumbs
        limited_bc = breadcrumbs[-15:]
        total_count = len(breadcrumbs)
        showing_count = len(limited_bc)

        # Calculate height based on number of items
        item_height = 40
        total_height = showing_count * item_height + 20

        # Create a vertical layout with exact height
        layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=total_height,
            spacing=2,
            padding=5
        )

        # Add each breadcrumb as a clickable label
        for bc in reversed(limited_bc):
            name = bc.get('name', f"Pin {bc['id']}")
            date_str = bc.get('date_str', 'Unknown')

            display_text = f"{name} ({date_str})"

            label = MDLabel(
                text=display_text,
                size_hint_y=None,
                height=item_height,
                font_style="Body1"
            )
            # Bind touch event directly to the label
            label.bind(on_touch_down=lambda instance, touch, b=bc: self.retrace_from_label(b, instance, touch))
            layout.add_widget(label)

        title = "Select a location to retrace"
        if total_count > 15:
            title += f" (showing most recent 15 of {total_count})"

        self.retrace_dialog = MDDialog(
            title=title,
            type="custom",
            content_cls=layout,
            size_hint=(0.9, None),
            height=total_height + 80,
            buttons=[
                MDRaisedButton(
                    text="CANCEL",
                    on_release=lambda x: self.retrace_dialog.dismiss()
                )
            ]
        )
        self.retrace_dialog.open()

    def retrace_from_label(self, bc, instance, touch):
        """Handle retrace selection from label"""
        if self.retrace_dialog:
            self.retrace_dialog.dismiss()
        self.retrace_to_breadcrumb(bc)
        return True


    def retrace_to_breadcrumb(self, target_bc):
        """Offer options for retracing to selected breadcrumb"""
        from kivymd.uix.dialog import MDDialog
        from math import radians, sin, cos, sqrt, atan2

        print("=== retrace_to_breadcrumb called ===")

        if not self.current_gps:
            self.show_message("No GPS fix. Please refresh GPS.")
            return

        # Calculate distance
        lat1, lon1 = self.current_gps
        lat2, lon2 = target_bc['lat'], target_bc['lon']

        R = 6371000
        φ1 = radians(lat1)
        φ2 = radians(lat2)
        Δφ = radians(lat2 - lat1)
        Δλ = radians(lon2 - lon1)

        a = sin(Δφ / 2) ** 2 + cos(φ1) * cos(φ2) * sin(Δλ / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c

        # Show options dialog
        option_dialog = MDDialog(
            title=f"Pin {target_bc['id']}",
            text=f"Distance: {distance:.0f} meters\n\nHow would you like to navigate?",
            buttons=[
                MDFlatButton(
                    text="ONE-TIME INFO",
                    on_release=lambda x: self.show_one_time_info(target_bc, distance, option_dialog)
                ),
                MDRaisedButton(
                    text="LIVE TRACKING",
                    on_release=lambda x: self.start_live_tracking(target_bc)
                ),
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda x: option_dialog.dismiss()
                )
            ]
        )
        option_dialog.open()

    def show_one_time_info(self, target_bc, distance, parent_dialog):
        """Show one-time distance/direction info"""
        parent_dialog.dismiss()

        lat1, lon1 = self.current_gps
        lat2, lon2 = target_bc['lat'], target_bc['lon']

        from math import radians, sin, cos, sqrt, atan2

        # Calculate bearing
        φ1 = radians(lat1)
        φ2 = radians(lat2)
        Δλ = radians(lon2 - lon1)

        y = sin(Δλ) * cos(φ2)
        x = cos(φ1) * sin(φ2) - sin(φ1) * cos(φ2) * cos(Δλ)
        bearing = atan2(y, x)
        bearing_deg = (bearing * 180 / 3.14159 + 360) % 360

        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        idx = round(bearing_deg / 45) % 8
        cardinal = directions[idx]

        self.show_message(
            f"📍 Pin {target_bc['id']}\n\n"
            f"Distance: {distance:.0f} meters\n"
            f"Direction: {cardinal} ({bearing_deg:.0f}°)\n\n"
            f"Dropped: {target_bc['time_str']}"
        )

    def clear_breadcrumbs(self):
        """Clear all breadcrumbs"""
        from kivymd.uix.dialog import MDDialog

        def confirm_clear():
            data_dir = self.get_data_dir()
            bc_file = data_dir / "breadcrumbs.json"
            if bc_file.exists():
                bc_file.unlink()
            if hasattr(self, 'bc_dialog') and self.bc_dialog:
                self.bc_dialog.dismiss()
            self.show_message("Breadcrumbs cleared")

        confirm_dialog = MDDialog(
            title="Clear Trail",
            text="Are you sure you want to clear all breadcrumbs?",
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: confirm_dialog.dismiss()),
                MDRaisedButton(
                    text="CLEAR",
                    md_bg_color=(0.8, 0.2, 0.2, 1),
                    on_release=lambda x: confirm_clear()
                )
            ]
        )
        confirm_dialog.open()

    def reset_form(self):
        """Reset all form fields (called by refresh button)"""
        # Clear Field ID
        self.ids.field_id_field.text = ""

        # Clear Site Name and SASES Name on manual reset
        self.ids.site_name_field.text = ""
        self.ids.sases_name_field.text = ""

        # Clear text fields
        self.ids.chronology3_field.text = ""
        self.ids.collecting_area_field.text = ""
        self.ids.analysis_field.text = ""
        self.ids.notes_field.text = ""

        # Reset dropdown buttons
        self.ids.collection_method_button.text = "Select Method"
        self.ids.collection_material_button.text = "Select Material"
        self.ids.chronology1_button.text = "Select Chronology 1"
        self.ids.chronology2_button.text = "Select Chronology 2"
        self.ids.context_button.text = "Select Context"

        # Reset photos
        self.photos = []

        self.show_message("Form reset")

    def check_duplicate_field_id(self, field_id):
        """Check if Field ID already exists"""
        data_dir = self.get_data_dir()
        obs_file = data_dir / "observations.json"
        if obs_file.exists():
            with open(obs_file) as f:
                observations = json.load(f)
            return field_id in observations
        return False

    def load_saved_observations(self):
        """Load saved observations for duplicate checking"""
        data_dir = self.get_data_dir()
        obs_file = data_dir / "observations.json"  # ← Already correct, but ensure this pattern
        if obs_file.exists():
            with open(obs_file) as f:
                self.saved_observations = json.load(f)
        else:
            self.saved_observations = {}

    # Dropdown menu methods
    def open_collection_method_menu(self):
        menu_items = [
            {"text": "Photo", "on_release": lambda x="Photo": self.set_collection_method(x)},
            {"text": "Observation", "on_release": lambda x="Observation": self.set_collection_method(x)},
            {"text": "Excavation in situ", "on_release": lambda x="Excavation in situ": self.set_collection_method(x)},
            {"text": "Excavation Sieve", "on_release": lambda x="Excavation Sieve": self.set_collection_method(x)},
            {"text": "Surface Collection", "on_release": lambda x="Surface Collection": self.set_collection_method(x)},
            {"text": "Field Note", "on_release": lambda x="Field Note": self.set_collection_method(x)},
            {"text": "Photogrammetry", "on_release": lambda x="Photogrammetry": self.set_collection_method(x)},
            {"text": "Experimental", "on_release": lambda x="Experimental": self.set_collection_method(x)},
            {"text": "Bonewalk", "on_release": lambda x="Bonewalk": self.set_collection_method(x)},
            {"text": "GeoTrench", "on_release": lambda x="GeoTrench": self.set_collection_method(x)},
        ]
        self.collection_method_menu = MDDropdownMenu(
            caller=self.ids.collection_method_button,
            items=menu_items,
            width_mult=4,
        )
        self.collection_method_menu.open()

    def set_collection_method(self, text):
        self.ids.collection_method_button.text = text
        self.collection_method_menu.dismiss()

    def open_collection_material_menu(self):
        menu_items = [
            {"text": "Lithic", "on_release": lambda x="Lithic": self.set_collection_material(x)},
            {"text": "Bone", "on_release": lambda x="Bone": self.set_collection_material(x)},
            {"text": "Pottery", "on_release": lambda x="Pottery": self.set_collection_material(x)},
            {"text": "Shell", "on_release": lambda x="Shell": self.set_collection_material(x)},
            {"text": "Tooth", "on_release": lambda x="Tooth": self.set_collection_material(x)},
            {"text": "Section", "on_release": lambda x="Section": self.set_collection_material(x)},
            {"text": "Observation", "on_release": lambda x="Observation": self.set_collection_material(x)},
            {"text": "Cast", "on_release": lambda x="Cast": self.set_collection_material(x)},
            {"text": "Metal", "on_release": lambda x="Metal": self.set_collection_material(x)},
            {"text": "Glass", "on_release": lambda x="Glass": self.set_collection_material(x)},
            {"text": "Sediment", "on_release": lambda x="Sediment": self.set_collection_material(x)},
            {"text": "Sample(Geochron)", "on_release": lambda x="Sample(Geochron)": self.set_collection_material(x)},
            {"text": "Sample(Phytolith)", "on_release": lambda x="Sample(Phytolith)": self.set_collection_material(x)},
            {"text": "Sample(Micromorph)",
             "on_release": lambda x="Sample(Micromorph)": self.set_collection_material(x)},
            {"text": "Sample(Paleosol)", "on_release": lambda x="Sample(Paleosol": self.set_collection_material(x)},
            {"text": "Sample(Paleomag)", "on_release": lambda x="Sample(Paleomag)": self.set_collection_material(x)},
            {"text": "Clast", "on_release": lambda x="Clast": self.set_collection_material(x)},
            {"text": "Charcoal", "on_release": lambda x="Charcoal": self.set_collection_material(x)},
            {"text": "Wood", "on_release": lambda x="Wood": self.set_collection_material(x)},
            {"text": "Other", "on_release": lambda x="Other": self.set_collection_material(x)},
            {"text": "Fossil Wood", "on_release": lambda x="Fossil Wood": self.set_collection_material(x)},
            {"text": "Carbonate", "on_release": lambda x="Carbonate": self.set_collection_material(x)},
            {"text": "Stromatolite", "on_release": lambda x="Stromatolite": self.set_collection_material(x)},
            {"text": "Unknown", "on_release": lambda x="Unknown": self.set_collection_material(x)},
            {"text": "Ochre", "on_release": lambda x="Ochre": self.set_collection_material(x)},
            {"text": "Pebble", "on_release": lambda x="Pebble": self.set_collection_material(x)},
            {"text": "Bone Harpoon", "on_release": lambda x="Bone Harpoon": self.set_collection_material(x)},
            {"text": "Bead", "on_release": lambda x="Bead": self.set_collection_material(x)},
            {"text": "Trace Fossil", "on_release": lambda x="Trace Fossil": self.set_collection_material(x)},
            {"text": "Photo", "on_release": lambda x="Photo": self.set_collection_material(x)},
            {"text": "Oyster Shell", "on_release": lambda x="Oyster Shell": self.set_collection_material(x)},
            {"text": "Cobble", "on_release": lambda x="Cobble": self.set_collection_material(x)},
            {"text": "Stone", "on_release": lambda x="Stone": self.set_collection_material(x)},
            {"text": "Clast", "on_release": lambda x="Clast": self.set_collection_material(x)},

        ]
        self.collection_material_menu = MDDropdownMenu(
            caller=self.ids.collection_material_button,
            items=menu_items,
            width_mult=4,
        )
        self.collection_material_menu.open()

    def set_collection_material(self, text):
        self.ids.collection_material_button.text = text
        self.collection_material_menu.dismiss()

    def open_chronology1_menu(self):
        menu_items = [
            {"text": "Pliocene", "on_release": lambda x="Pliocene": self.set_chronology1(x)},
            {"text": "Pleistocene", "on_release": lambda x="Pleistocene": self.set_chronology1(x)},
            {"text": "Holocene", "on_release": lambda x="Holocene": self.set_chronology1(x)},
            {"text": "ESA", "on_release": lambda x="ESA": self.set_chronology1(x)},
            {"text": "MSA", "on_release": lambda x="MSA": self.set_chronology1(x)},
            {"text": "LSA", "on_release": lambda x="LSAe": self.set_chronology1(x)},
            {"text": "Unknown", "on_release": lambda x="Unknown": self.set_chronology1(x)},
            {"text": "Modern", "on_release": lambda x="Modern": self.set_chronology1(x)},
            {"text": "Late Pleistocene", "on_release": lambda x="Late Pleistocene": self.set_chronology1(x)},
            {"text": "Miocene", "on_release": lambda x="Miocene": self.set_chronology1(x)},
            {"text": "Plio/Pleistocene", "on_release": lambda x="Plio/Pleistocene": self.set_chronology1(x)},
        ]
        self.chronology1_menu = MDDropdownMenu(
            caller=self.ids.chronology1_button,
            items=menu_items,
            width_mult=4,
            position="auto",
            hor_growth="left",

        )
        self.chronology1_menu.open()

    def set_chronology1(self, text):
        self.ids.chronology1_button.text = text
        self.chronology1_menu.dismiss()

    def open_chronology2_menu(self):
        menu_items = [
            {"text": "KBS Mbr", "on_release": lambda x="KBS Mbr": self.set_chronology2(x)},
            {"text": "Koobi Fora Fm", "on_release": lambda x="Koobi Fora Fm": self.set_chronology2(x)},
            {"text": "Galana Boi Fm", "on_release": lambda x="Galana Boi Fm": self.set_chronology2(x)},
            {"text": "Tulu Bor Mbr", "on_release": lambda x="Tulu Bor Mbr": self.set_chronology2(x)},
            {"text": "Upper Burgi Mbr", "on_release": lambda x="Upper Burgi Mbr": self.set_chronology2(x)},
            {"text": "Lower Burgi Mbr", "on_release": lambda x="Lower Burgi Mbr": self.set_chronology2(x)},
            {"text": "Okote Mbr", "on_release": lambda x="Okote Mbr": self.set_chronology2(x)},
            {"text": "Chari Mbr", "on_release": lambda x="Chari Mbr": self.set_chronology2(x)},
            {"text": "Unknown", "on_release": lambda x="Unknown": self.set_chronology2(x)},
            {"text": "Lonyumun Mbr", "on_release": lambda x="Lonyumun Mbr": self.set_chronology2(x)},
            {"text": "Lokochot Mbr", "on_release": lambda x="Lokochot Mbr": self.set_chronology2(x)},
            {"text": "Modern", "on_release": lambda x="Modern": self.set_chronology2(x)},
            {"text": "Moiti Mbr", "on_release": lambda x="Moiti Mbr": self.set_chronology2(x)},
            {"text": "Buluk Mbr", "on_release": lambda x="Buluk Mbr": self.set_chronology2(x)},
            {"text": "Burgi Mbr", "on_release": lambda x="Burgi Mbr": self.set_chronology2(x)},
            {"text": "Tulu Bor-Burgi Mbr", "on_release": lambda x="Tulu Bor-Burgi Mbr": self.set_chronology2(x)},
        ]
        self.chronology2_menu = MDDropdownMenu(
            caller=self.ids.chronology2_button,
            items=menu_items,
            width_mult=4,
            hor_growth="left",
        )
        self.chronology2_menu.open()

    def set_chronology2(self, text):
        self.ids.chronology2_button.text = text
        self.chronology2_menu.dismiss()

    def open_context_menu(self):
        menu_items = [
            {"text": "Sand", "on_release": lambda x="Sand": self.set_context(x)},
            {"text": "Silt", "on_release": lambda x="Silt": self.set_context(x)},
            {"text": "Clay", "on_release": lambda x="Clay": self.set_context(x)},
            {"text": "Gravel", "on_release": lambda x="Gravel": self.set_context(x)},
            {"text": "Pedogenic Clay", "on_release": lambda x="Pedogenic Clay": self.set_context(x)},
            {"text": "Paleosol", "on_release": lambda x="Paleosol": self.set_context(x)},
            {"text": "Gravel Lag", "on_release": lambda x="Gravel Lag": self.set_context(x)},
            {"text": "Tuff", "on_release": lambda x="Tuff": self.set_context(x)},
            {"text": "Deflated", "on_release": lambda x="Deflated": self.set_context(x)},
            {"text": "Sand/Silt", "on_release": lambda x="Sand/Silt": self.set_context(x)},
            {"text": "Sand/Clay", "on_release": lambda x="Sand/Clay": self.set_context(x)},
            {"text": "Sand/Gravel", "on_release": lambda x="Sand/Gravel": self.set_context(x)},
            {"text": "Silt/Clay", "on_release": lambda x="Silt/Clay": self.set_context(x)},
            {"text": "NA", "on_release": lambda x="NA": self.set_context(x)},
            {"text": "Silt/Gravel", "on_release": lambda x="Silt/Gravel": self.set_context(x)},
            {"text": "Clay/Gravel", "on_release": lambda x="Clay/Gravel": self.set_context(x)},
            {"text": "Silt/Sand", "on_release": lambda x="Silt/Sand": self.set_context(x)},
            {"text": "Gravel/Sand", "on_release": lambda x="Gravel/Sand": self.set_context(x)},
            {"text": "Tuff/Silt", "on_release": lambda x="Tuff/Silt": self.set_context(x)},
            {"text": "Sandstone", "on_release": lambda x="Sandstone": self.set_context(x)},
            {"text": "Clay Cylinder", "on_release": lambda x="Clay Cylinder": self.set_context(x)},
            {"text": "Clay (mud)", "on_release": lambda x="Clay (mud)": self.set_context(x)},
            {"text": "Tuffaceos Silt", "on_release": lambda x="Tuffaceos Silt": self.set_context(x)},
            {"text": "Vertisol", "on_release": lambda x="Vertisol": self.set_context(x)},
            {"text": "Beach", "on_release": lambda x="Beach": self.set_context(x)},

        ]
        self.context_menu = MDDropdownMenu(
            caller=self.ids.context_button,
            items=menu_items,
            width_mult=4,
        )
        self.context_menu.open()

    def set_context(self, text):
        self.ids.context_button.text = text
        self.context_menu.dismiss()

    def open_menu(self):
        """Open dropdown menu from top-left icon"""
        if self.menu:
            self.menu.dismiss()

        menu_items = [
            {
                "text": "My Observations",
                "leading_icon": "format-list-bulleted",
                "on_release": lambda x="my_obs": self.menu_callback("my_obs"),
            },
            {
                "text": "Breadcrumb Trail",
                "leading_icon": "map-marker-path",
                "on_release": lambda x="breadcrumb": self.menu_callback("breadcrumb"),
            },
            {
                "text": "Join Project",
                "leading_icon": "qrcode",
                "on_release": lambda x="join_project": self.menu_callback("join_project"),
            },
            {
                "text": "Sync to Base",
                "leading_icon": "sync",
                "on_release": lambda x="sync_to_base": self.menu_callback("sync_to_base"),
            },
            {
                "text": "Save My Data",
                "leading_icon": "content-save",
                "on_release": lambda x="save_my_data": self.menu_callback("save_my_data"),
            },
            {
                "text": "Export Data",
                "leading_icon": "export",
                "on_release": lambda x="export": self.menu_callback("export"),
            },
            {
                "text": "Settings",
                "leading_icon": "cog",
                "on_release": lambda x="settings": self.menu_callback("settings"),
            },
            {
                "text": "Logout",
                "leading_icon": "logout",
                "on_release": lambda x="logout": self.menu_callback("logout"),
            },
        ]

        self.menu = MDDropdownMenu(
            caller=self.ids.top_app_bar.ids.left_actions,
            items=menu_items,
            width_mult=4,
            position="auto",
            hor_growth="left",
        )
        self.menu.open()

    def menu_callback(self, item):
        self.menu.dismiss()
        if item == "logout":
            self.logout()
        elif item == "my_obs":
            self.show_my_observations()
        elif item == "breadcrumb":
            self.view_breadcrumbs()
        elif item == "join_project":
            self.scan_project_qr()
        elif item == "sync_to_base":
            self.sync_to_base()
        elif item == "save_my_data":
            self.save_my_data()
        elif item == "export":
            self.export_data()
        elif item == "settings":
            self.show_settings()

    def show_my_observations(self):
        """Show current user's observations (capped at 15)"""
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.label import MDLabel
        from kivymd.uix.button import MDRaisedButton
        from kivy.uix.boxlayout import BoxLayout

        print("Starting show_my_observations")

        # Get user observations
        app = MDApp.get_running_app()
        current_user = getattr(app, 'current_user', None)

        if not current_user:
            self.show_message("No user logged in")
            return

        user_id = current_user.get('user_id')

        # Load observations
        data_dir = self.get_data_dir()
        obs_file = data_dir / "observations.json"
        if not obs_file.exists():
            self.show_message("No observations found")
            return

        with open(obs_file) as f:
            observations = json.load(f)

        # Filter by current user
        user_observations = {
            field_id: obs for field_id, obs in observations.items()
            if obs.get('user_id') == user_id
        }

        if not user_observations:
            self.show_message(f"No observations found for user {user_id}")
            return

        # Limit to first 15 observations
        limited_obs = dict(list(user_observations.items())[:15])
        total_count = len(user_observations)
        showing_count = len(limited_obs)

        # Calculate height based on number of items
        item_height = 35
        total_height = showing_count * item_height + 20

        # Create a vertical layout with exact height
        layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=total_height,
            spacing=2,
            padding=5
        )

        # Add each observation as a simple label
        for field_id, obs in limited_obs.items():
            method = obs.get('collection_method', 'No method')
            if method == 'Select Method':
                method = 'No method'

            label = MDLabel(
                text=f"Field ID: {field_id} - {method}",
                size_hint_y=None,
                height=item_height
            )
            layout.add_widget(label)

        # Show message if some observations are hidden
        title = f"My Observations ({total_count})"
        if total_count > 15:
            title += f" - showing first 15 of {total_count}"

        # Create dialog
        dialog = MDDialog(
            title=title,
            type="custom",
            content_cls=layout,
            size_hint=(0.9, None),
            height=total_height + 80,  # Add space for title and buttons
            buttons=[MDRaisedButton(text="CLOSE", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()

    def show_team_observations(self):
        """Show team observations for current user's project (capped at 25)"""
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.label import MDLabel
        from kivymd.uix.button import MDRaisedButton
        from kivy.uix.boxlayout import BoxLayout

        print("Starting show_team_observations")

        app = MDApp.get_running_app()
        current_user = getattr(app, 'current_user', None)

        if not current_user:
            self.show_message("No user logged in")
            return

        project_id = current_user.get('project')

        # Load observations
        data_dir = self.get_data_dir()
        obs_file = data_dir / "observations.json"
        if not obs_file.exists():
            self.show_message("No observations found")
            return

        with open(obs_file) as f:
            observations = json.load(f)

        # Filter by current project
        team_observations = {
            field_id: obs for field_id, obs in observations.items()
            if obs.get('project') == project_id
        }

        if not team_observations:
            self.show_message(f"No observations found for project {project_id}")
            return

        # Limit to first 25 observations
        limited_obs = dict(list(team_observations.items())[:25])
        total_count = len(team_observations)
        showing_count = len(limited_obs)

        # Calculate height based on number of items
        item_height = 40  # Slightly taller for more info
        total_height = showing_count * item_height + 20

        # Create a vertical layout with exact height
        layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=total_height,
            spacing=2,
            padding=5
        )

        # Add each observation with formatted display
        for field_id, obs in limited_obs.items():
            # Get user info
            user_id = obs.get('user_id', '??')
            user_name = obs.get('user_name', 'Unknown')

            # Get method and timestamp
            method = obs.get('collection_method', 'No method')
            if method == 'Select Method':
                method = 'No method'

            timestamp = obs.get('timestamp', '')
            # Format timestamp to show only date and time
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp)
                    time_str = dt.strftime("%m/%d %H:%M")
                except:
                    time_str = timestamp[:16]
            else:
                time_str = 'No date'

            # Create display string with user ID embedded in Field ID format
            # Field ID format: {user_id}{project_id}{sequential}
            # For display, we show: "User 14: Field ID 1403xxxx"
            display_text = f"👤 {user_name} ({user_id}) | {field_id} | {method} | {time_str}"

            label = MDLabel(
                text=display_text,
                size_hint_y=None,
                height=item_height,
                font_style="Caption"
            )
            layout.add_widget(label)

        # Show message if some observations are hidden
        title = f"Team Observations ({total_count})"
        if total_count > 25:
            title += f" - showing first 25 of {total_count}"

        # Create dialog
        dialog = MDDialog(
            title=title,
            type="custom",
            content_cls=layout,
            size_hint=(0.95, None),
            height=total_height + 80,
            buttons=[MDRaisedButton(text="CLOSE", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()

    def view_observation_detail(self, field_id, observations):
        """Show detailed view of a single observation"""
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDRaisedButton
        from kivymd.uix.label import MDLabel
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivy.uix.scrollview import ScrollView
        from kivymd.uix.card import MDSeparator

        obs = observations.get(field_id, {})

        # Build content
        content = MDBoxLayout(
            orientation="vertical",
            spacing="8dp",
            padding="15dp",
            size_hint_y=None,
            height="auto"
        )

        # === HEADER SECTION ===
        content.add_widget(
            MDLabel(
                text=f"Field ID: {field_id}",
                font_style="H5",
                theme_text_color="Primary"
            )
        )

        # === TIMESTAMP SECTION ===
        timestamp = obs.get('timestamp', 'Unknown')
        if timestamp:
            try:
                dt = datetime.fromisoformat(timestamp)
                formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                formatted_time = timestamp
            content.add_widget(
                MDLabel(
                    text=f"📅 {formatted_time}",
                    theme_text_color="Secondary",
                    font_style="Caption"
                )
            )

        content.add_widget(MDSeparator())

        # === USER & PROJECT INFO ===
        user_info = MDBoxLayout(orientation="vertical", spacing="4dp")

        user_id = obs.get('user_id', 'Unknown')
        user_name = obs.get('user_name', 'Unknown')
        user_info.add_widget(
            MDLabel(
                text=f"👤 User: {user_name} ({user_id})",
                theme_text_color="Secondary"
            )
        )

        project = obs.get('project', 'Unknown')
        season = obs.get('season', 'Unknown')
        user_info.add_widget(
            MDLabel(
                text=f"📁 Project: {project} (Season: {season})",
                theme_text_color="Secondary"
            )
        )

        content.add_widget(user_info)
        content.add_widget(MDSeparator())

        # === GPS LOCATION ===
        lat = obs.get('gps_latitude')
        lon = obs.get('gps_longitude')
        if lat and lon:
            location_box = MDBoxLayout(orientation="vertical", spacing="4dp")
            location_box.add_widget(
                MDLabel(
                    text="📍 GPS Location:",
                    theme_text_color="Primary",
                    font_style="Subtitle2"
                )
            )
            location_box.add_widget(
                MDLabel(
                    text=f"Latitude: {lat:.6f}",
                    theme_text_color="Secondary",
                    font_style="Caption"
                )
            )
            location_box.add_widget(
                MDLabel(
                    text=f"Longitude: {lon:.6f}",
                    theme_text_color="Secondary",
                    font_style="Caption"
                )
            )
            content.add_widget(location_box)
            content.add_widget(MDSeparator())

        # === COLLECTION PARAMETERS ===
        content.add_widget(
            MDLabel(
                text="Collection Parameters:",
                theme_text_color="Primary",
                font_style="Subtitle2"
            )
        )

        params = [
            ("Method", obs.get('collection_method', 'Not selected')),
            ("Material", obs.get('collection_material', 'Not selected')),
            ("Chronology 1", obs.get('chronology1', 'Not selected')),
            ("Chronology 2", obs.get('chronology2', 'Not selected')),
            ("Chronology 3", obs.get('chronology3', '')),
            ("Context", obs.get('context', 'Not selected')),
        ]

        for label, value in params:
            if value and value not in ['Not selected', 'Select Method', 'Select Material', 'Select Chronology 1',
                                       'Select Chronology 2', 'Select Context']:
                content.add_widget(
                    MDLabel(
                        text=f"• {label}: {value}",
                        theme_text_color="Secondary",
                        font_style="Caption"
                    )
                )

        content.add_widget(MDSeparator())

        # === LOCATION INFO ===
        collecting_area = obs.get('collecting_area', '')
        if collecting_area:
            content.add_widget(
                MDLabel(
                    text="Location Details:",
                    theme_text_color="Primary",
                    font_style="Subtitle2"
                )
            )
            content.add_widget(
                MDLabel(
                    text=f"Collecting Area: {collecting_area}",
                    theme_text_color="Secondary",
                    font_style="Caption"
                )
            )
            content.add_widget(MDSeparator())

        # === ANALYSIS ===
        analysis = obs.get('analysis', '')
        if analysis:
            content.add_widget(
                MDLabel(
                    text="Analysis:",
                    theme_text_color="Primary",
                    font_style="Subtitle2"
                )
            )
            content.add_widget(
                MDLabel(
                    text=analysis,
                    theme_text_color="Secondary",
                    font_style="Caption",
                    size_hint_y=None,
                    height="auto"
                )
            )
            content.add_widget(MDSeparator())

        # === NOTES ===
        notes = obs.get('notes', '')
        if notes:
            content.add_widget(
                MDLabel(
                    text="Notes:",
                    theme_text_color="Primary",
                    font_style="Subtitle2"
                )
            )
            content.add_widget(
                MDLabel(
                    text=notes,
                    theme_text_color="Secondary",
                    font_style="Caption",
                    size_hint_y=None,
                    height="auto"
                )
            )
            content.add_widget(MDSeparator())

        # === PHOTOS ===
        photos = obs.get('photos', [])
        if photos:
            photo_box = MDBoxLayout(orientation="vertical", spacing="4dp")
            photo_box.add_widget(
                MDLabel(
                    text=f"📸 Photos ({len(photos)}):",
                    theme_text_color="Primary",
                    font_style="Subtitle2"
                )
            )
            for i, photo in enumerate(photos, 1):
                photo_box.add_widget(
                    MDLabel(
                        text=f"  {i}. {photo}",
                        theme_text_color="Secondary",
                        font_style="Caption"
                    )
                )
            content.add_widget(photo_box)

        # Calculate total height based on content
        content.height = 800  # Set a reasonable default height

        # Wrap in ScrollView
        scroll = ScrollView()
        scroll.add_widget(content)

        # Create dialog
        self.detail_dialog = MDDialog(
            title="Observation Details",
            type="custom",
            content_cls=scroll,
            size_hint=(0.95, 0.9),
            buttons=[
                MDRaisedButton(
                    text="CLOSE",
                    on_release=lambda x: self.detail_dialog.dismiss()
                )
            ]
        )
        self.detail_dialog.open()

    def get_export_paths(self):
        """Get the export directory and file paths for the current season"""
        from pathlib import Path
        from datetime import datetime

        # Get current user info
        app = MDApp.get_running_app()
        current_user = getattr(app, 'current_user', None)

        if not current_user:
            self.show_message("No user logged in")
            return None, None

        season = current_user.get('season', '')
        if not season:
            self.show_message("No season found")
            return None, None

        # Create export directory structure
        export_dir = Path.home() / "field_data_exports" / season
        export_dir.mkdir(parents=True, exist_ok=True)

        # Create images directory
        images_dir = export_dir / "images"
        images_dir.mkdir(exist_ok=True)

        # JSON file path
        json_path = export_dir / f"{season}_data.json"

        return json_path, images_dir

    def load_existing_export_data(self, json_path):
        """Load existing export JSON file, create if doesn't exist"""
        if json_path.exists():
            with open(json_path, 'r') as f:
                return json.load(f)
        else:
            return []

    def save_export_data(self, json_path, data):
        """Save export data to JSON file"""
        with open(json_path, 'w') as f:
            json.dump(data, f, indent=2)

    def export_data(self):
        """Export completed observations to master database (JSON and CSV)"""
        from datetime import datetime
        import csv

        # Get paths
        json_path, images_dir = self.get_export_paths()
        if not json_path:
            return

        # Get current user info
        app = MDApp.get_running_app()
        current_user = getattr(app, 'current_user', None)

        if not current_user:
            self.show_message("No user logged in")
            return

        user_id = current_user.get('user_id')
        season = current_user.get('season')

        # Load user data for collector name
        users = load_users()
        user_data = users.get(user_id, {})
        collector_name = user_data.get('name', current_user.get('user_name', ''))

        # Load saved observations
        data_dir = self.get_data_dir()
        obs_file = data_dir / "observations.json"
        if not obs_file.exists():
            self.show_message("No saved observations found")
            return

        with open(obs_file) as f:
            all_observations = json.load(f)

        # Filter observations for this user and season
        user_observations = {}
        for field_id, obs in all_observations.items():
            if obs.get('user_id') == user_id and obs.get('season') == season:
                user_observations[field_id] = obs

        if not user_observations:
            self.show_message("No observations found for current user/season")
            return

        # Load existing master database
        if not json_path.exists():
            self.show_message("Master database not found. Please generate tags first.")
            return

        with open(json_path) as f:
            master_data = json.load(f)

        # Update existing entries with collected data
        updated_count = 0
        csv_data = []  # For CSV export

        for field_id, obs in user_observations.items():
            if field_id in master_data:
                # Parse timestamp
                timestamp = obs.get('timestamp', '')
                try:
                    dt = datetime.fromisoformat(timestamp)
                    month = dt.strftime("%m")
                    day = dt.strftime("%d")
                    year = dt.strftime("%Y")
                except:
                    month = day = year = ''

                # Update the record with collected data
                master_data[field_id].update({
                    "SITE_NAME_NONSASES": obs.get('site_name', ''),
                    "SITE_NAME_SASES": obs.get('sases_name', ''),
                    "COLLECTION_METHOD": obs.get('collection_method', ''),
                    "COLLECTOR": collector_name,
                    "MONTH": month,
                    "DAY": day,
                    "YEAR": year,
                    "COLLECTION_MATERIAL": obs.get('collection_material', ''),
                    "CHRONOLOGY1": obs.get('chronology1', ''),
                    "CHRONOLOGY2": obs.get('chronology2', ''),
                    "CHRONOLOGY3": obs.get('chronology3', ''),
                    "LAT": obs.get('gps_latitude', ''),
                    "LONG": obs.get('gps_longitude', ''),
                    "COLLECTING_AREA": obs.get('collecting_area', ''),
                    "CONTEXT": obs.get('context', ''),
                    "ANALYSIS": obs.get('analysis', ''),
                    "NOTES": obs.get('notes', ''),
                    "exported": True,
                    "exported_at": datetime.now().isoformat()
                })
                updated_count += 1

                # Add to CSV data
                csv_data.append({
                    "DATABASE_ID": master_data[field_id].get("DATABASE_ID", ""),
                    "FIELD_ID": field_id,
                    "SITE_NAME_NONSASES": obs.get('site_name', ''),
                    "SITE_NAME_SASES": obs.get('sases_name', ''),
                    "COLLECTION_METHOD": obs.get('collection_method', ''),
                    "COLLECTOR": collector_name,
                    "MONTH": month,
                    "DAY": day,
                    "YEAR": year,
                    "COLLECTION_MATERIAL": obs.get('collection_material', ''),
                    "CHRONOLOGY1": obs.get('chronology1', ''),
                    "CHRONOLOGY2": obs.get('chronology2', ''),
                    "CHRONOLOGY3": obs.get('chronology3', ''),
                    "LAT": obs.get('gps_latitude', ''),
                    "LONG": obs.get('gps_longitude', ''),
                    "COLLECTING_AREA": obs.get('collecting_area', ''),
                    "CONTEXT": obs.get('context', ''),
                    "ANALYSIS": obs.get('analysis', ''),
                    "NOTES": obs.get('notes', '')
                })

                # Export photos
                photos = obs.get('photos', [])
                for i, photo_name in enumerate(photos):
                    data_dir = self.get_data_dir()
                    src_photo = data_dir / "photos" / photo_name
                    if src_photo.exists():
                        ext = src_photo.suffix or '.jpg'
                        new_photo_name = f"{field_id}_photo_{i + 1}{ext}"
                        dst_photo = images_dir / new_photo_name
                        import shutil
                        shutil.copy2(src_photo, dst_photo)
            else:
                print(f"Warning: Field ID {field_id} not found in master database")

        if updated_count == 0:
            self.show_message("No matching records found in master database")
            return

        # Save updated master data (JSON)
        with open(json_path, 'w') as f:
            json.dump(master_data, f, indent=2)

        # Save CSV file
        csv_path = json_path.parent / f"{json_path.stem}.csv"
        if csv_data:
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = csv_data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(csv_data)

        self.show_message(
            f"Updated {updated_count} observations\nJSON: {json_path}\nCSV: {csv_path}\nPhotos: {images_dir}")

    def save_my_data(self):
        """Save user's own data as a personal backup (separate from master database)"""
        from datetime import datetime
        import csv
        import shutil

        # Get current user info
        app = MDApp.get_running_app()
        current_user = getattr(app, 'current_user', None)

        if not current_user:
            self.show_message("No user logged in")
            return

        user_id = current_user.get('user_id')
        user_name = current_user.get('user_name', user_id)
        season = current_user.get('season')

        # Create personal backup directory
        backup_dir = Path.home() / "field_data_backups" / f"{user_name}_{user_id}" / season
        backup_dir.mkdir(parents=True, exist_ok=True)

        # Create images subdirectory
        images_dir = backup_dir / "images"
        images_dir.mkdir(exist_ok=True)

        # Load saved observations
        data_dir = self.get_data_dir()
        obs_file = data_dir / "observations.json"
        if not obs_file.exists():
            self.show_message("No saved observations found")
            return

        with open(obs_file) as f:
            all_observations = json.load(f)

        # Filter observations for this user and season
        user_observations = {}
        for field_id, obs in all_observations.items():
            if obs.get('user_id') == user_id and obs.get('season') == season:
                user_observations[field_id] = obs

        if not user_observations:
            self.show_message("No observations found for current user/season")
            return

        # Prepare data for export
        export_data = []
        photos_copied = 0

        for field_id, obs in user_observations.items():
            # Parse timestamp
            timestamp = obs.get('timestamp', '')
            try:
                dt = datetime.fromisoformat(timestamp)
                month = dt.strftime("%m")
                day = dt.strftime("%d")
                year = dt.strftime("%Y")
            except:
                month = day = year = ''

            record = {
                "FIELD_ID": field_id,
                "SITE_NAME_NONSASES": obs.get('site_name', ''),
                "SITE_NAME_SASES": obs.get('sases_name', ''),
                "COLLECTION_METHOD": obs.get('collection_method', ''),
                "COLLECTOR": current_user.get('user_name', ''),
                "MONTH": month,
                "DAY": day,
                "YEAR": year,
                "COLLECTION_MATERIAL": obs.get('collection_material', ''),
                "CHRONOLOGY1": obs.get('chronology1', ''),
                "CHRONOLOGY2": obs.get('chronology2', ''),
                "CHRONOLOGY3": obs.get('chronology3', ''),
                "LAT": obs.get('gps_latitude', ''),
                "LONG": obs.get('gps_longitude', ''),
                "COLLECTING_AREA": obs.get('collecting_area', ''),
                "CONTEXT": obs.get('context', ''),
                "ANALYSIS": obs.get('analysis', ''),
                "NOTES": obs.get('notes', ''),
                "exported_at": datetime.now().isoformat()
            }
            export_data.append(record)

            # Copy photos
            photos = obs.get('photos', [])
            for i, photo_name in enumerate(photos):
                data_dir = self.get_data_dir()
                src_photo = data_dir / "photos" / photo_name
                if src_photo.exists():
                    ext = src_photo.suffix or '.jpg'
                    new_photo_name = f"{field_id}_photo_{i + 1}{ext}"
                    dst_photo = images_dir / new_photo_name
                    shutil.copy2(src_photo, dst_photo)
                    photos_copied += 1

        # Save JSON
        json_path = backup_dir / f"{user_name}_{user_id}_data.json"
        with open(json_path, 'w') as f:
            json.dump(export_data, f, indent=2)

        # Save CSV
        csv_path = backup_dir / f"{user_name}_{user_id}_data.csv"
        if export_data:
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = export_data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(export_data)

        self.show_message(f"Personal backup saved!\n\n"
                          f"Location: {backup_dir}\n"
                          f"Observations: {len(export_data)}\n"
                          f"Photos: {photos_copied}\n\n"
                          f"Files saved to your device.")

    def export_photos(self, images_dir, field_id):
        """Export photos to the images directory"""
        import shutil

        photos_exported = 0
        for i, photo_name in enumerate(self.photos):
            # Source path (where photos are stored)
            data_dir = self.get_data_dir()
            src_photo = data_dir / "photos" / photo_name

            if src_photo.exists():
                # New filename: {field_id}_photo_{i+1}.jpg
                ext = src_photo.suffix or '.jpg'
                new_photo_name = f"{field_id}_photo_{i + 1}{ext}"
                dst_photo = images_dir / new_photo_name

                # Copy photo (don't move, keep original)
                shutil.copy2(src_photo, dst_photo)
                photos_exported += 1

        print(f"Exported {photos_exported} photos for Field ID {field_id}")

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
            spacing=15,
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

    def take_photo(self):
        """Open camera and capture photo"""
        if not CAMERA_AVAILABLE or camera is None:
            self.show_message("Camera not available on this device")
            return

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"photo_{timestamp}.jpg"
        data_dir = self.get_data_dir()
        photos_dir = data_dir / "photos"
        photos_dir.mkdir(parents=True, exist_ok=True)
        filepath = photos_dir / filename

        try:
            camera.take_picture(
                filename=str(filepath),
                on_complete=self.on_photo_captured
            )
        except Exception as e:
            self.show_message(f"Camera error: {str(e)}")

    def on_photo_captured(self, filepath):
        """Called by plyer camera when photo is taken"""
        if filepath and Path(filepath).exists():
            filename = Path(filepath).name
            self.photos.append(filename)
            self.show_message(f"Photo captured ({len(self.photos)} total)")
        else:
            self.show_message("Photo capture failed")

    def save_observation(self):
        """Save current observation"""
        from core.models import FieldObservation
        from datetime import datetime

        # Get Field ID
        field_id = self.ids.field_id_field.text.strip()

        # Validate Field ID
        if not field_id:
            self.show_message("Field ID is required")
            return

        if len(field_id) != 5 or not field_id.isdigit():
            self.show_message("Field ID must be a 5-digit number")
            return

        # Check for duplicates
        if self.check_duplicate_field_id(field_id):
            self.show_message(f"Field ID {field_id} already exists!")
            return

        # Get current user info
        app = MDApp.get_running_app()
        current_user = getattr(app, 'current_user', None)

        if not current_user:
            self.show_message("No user logged in")
            return

        # Collect all the new field data
        collection_data = {
            "site_name": self.ids.site_name_field.text.strip(),
            "sases_name": self.ids.sases_name_field.text.strip(),
            "chronology3": self.ids.chronology3_field.text,
            "collecting_area": self.ids.collecting_area_field.text,
            "analysis": self.ids.analysis_field.text,
            "collection_method": self.ids.collection_method_button.text,
            "collection_material": self.ids.collection_material_button.text,
            "chronology1": self.ids.chronology1_button.text,
            "chronology2": self.ids.chronology2_button.text,
            "context": self.ids.context_button.text,
        }

        obs = FieldObservation(
            field_id=field_id,
            season_id=current_user.get('season'),
            project_id=current_user.get('project'),
            user_id=current_user.get('user_id'),
            user_name=current_user.get('user_name'),
            gps_latitude=self.current_gps[0] if self.current_gps else None,
            gps_longitude=self.current_gps[1] if self.current_gps else None,
            notes=self.ids.notes_field.text,
            custom_fields=collection_data,
            photo_paths=self.photos,
            timestamp=datetime.now()
        )

        # Save to local JSON file - FIXED: use full file path
        data_dir = self.get_data_dir()
        obs_file = data_dir / "observations.json"  # ← Ensure filename is appended

        if obs_file.exists():
            with open(obs_file) as f:
                observations = json.load(f)
        else:
            observations = {}

        observations[field_id] = {
            "field_id": field_id,
            "site_name": self.ids.site_name_field.text.strip(),
            "sases_name": self.ids.sases_name_field.text.strip(),
            "user_id": current_user.get('user_id'),
            "user_name": current_user.get('user_name'),
            "season": current_user.get('season'),
            "project": current_user.get('project'),
            "timestamp": datetime.now().isoformat(),
            "gps_latitude": self.current_gps[0] if self.current_gps else None,
            "gps_longitude": self.current_gps[1] if self.current_gps else None,
            "chronology3": self.ids.chronology3_field.text.strip(),
            "collecting_area": self.ids.collecting_area_field.text.strip(),
            "analysis": self.ids.analysis_field.text.strip(),
            "collection_method": self.ids.collection_method_button.text,
            "collection_material": self.ids.collection_material_button.text,
            "chronology1": self.ids.chronology1_button.text,
            "chronology2": self.ids.chronology2_button.text,
            "context": self.ids.context_button.text,
            "notes": self.ids.notes_field.text.strip(),
            "photos": self.photos,
            "synced": False
        }

        with open(obs_file, 'w') as f:
            json.dump(observations, f, indent=2)

        # Clear form and show success
        self.clear_form(keep_site_fields=True)
        self.show_message(f"Observation {field_id} saved!")

    def clear_form(self, keep_site_fields=False):
        """Clear all input fields"""
        # Clear Field ID
        self.ids.field_id_field.text = ""

        # Conditionally clear site fields
        if not keep_site_fields:
            self.ids.site_name_field.text = ""
            self.ids.sases_name_field.text = ""

        # Clear text fields
        self.ids.chronology3_field.text = ""
        self.ids.collecting_area_field.text = ""
        self.ids.analysis_field.text = ""
        self.ids.notes_field.text = ""

        # Reset dropdown buttons
        self.ids.collection_method_button.text = "Select Method"
        self.ids.collection_material_button.text = "Select Material"
        self.ids.chronology1_button.text = "Select Chronology 1"
        self.ids.chronology2_button.text = "Select Chronology 2"
        self.ids.context_button.text = "Select Context"

        # Reset photos
        self.photos = []

    def show_message(self, message):
        """Show a simple message dialog"""
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDRaisedButton

        dialog = MDDialog(
            text=message,
            buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()

    def go_to_sync(self):
        """Sync data with base station"""
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.textfield import MDTextField

        # Create dialog with IP input
        content = MDBoxLayout(
            orientation="vertical",
            spacing="10dp",
            padding="20dp",
            size_hint_y=None,
            height="150dp"
        )

        content.add_widget(
            MDLabel(
                text="Enter Base Station IP Address:",
                theme_text_color="Secondary"
            )
        )

        self.base_ip_field = MDTextField(
            hint_text="e.g., 192.168.1.100",
            mode="rectangle"
        )
        content.add_widget(self.base_ip_field)

        self.sync_dialog = MDDialog(
            title="Sync Data",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: self.sync_dialog.dismiss()),
                MDRaisedButton(
                    text="SYNC",
                    on_release=lambda x: self.perform_sync(self.base_ip_field.text.strip())
                )
            ]
        )
        self.sync_dialog.open()

    def logout(self):
        data_dir = self.get_data_dir()
        cred_file = data_dir / "credentials.json"
        if cred_file.exists():
            cred_file.unlink()
        self.manager.current = "login"