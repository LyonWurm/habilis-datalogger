from kivymd.uix.screen import MDScreen
from kivy.lang import Builder

KV = '''
<SyncScreen>:
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Sync & Export"
            elevation: 4
            left_action_items: [["arrow-left", lambda x: root.go_back()]]

        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                spacing: "16dp"
                padding: "16dp"
                size_hint_y: None
                height: self.minimum_height

                MDCard:
                    orientation: "vertical"
                    padding: "16dp"
                    spacing: "16dp"
                    size_hint_y: None
                    height: self.minimum_height

                    MDLabel:
                        text: "Pending Data"
                        theme_text_color: "Secondary"

                    MDBoxLayout:
                        spacing: "24dp"

                        MDLabel:
                            text: "Observations:"

                        MDLabel:
                            id: obs_count
                            text: "0"
                            halign: "right"

                    MDBoxLayout:
                        spacing: "24dp"

                        MDLabel:
                            text: "Photos:"

                        MDLabel:
                            id: photo_count
                            text: "0"
                            halign: "right"

                MDRaisedButton:
                    text: "SYNC WITH BASE"
                    icon: "sync"
                    size_hint_x: 1
                    on_release: root.sync_data()

                MDCard:
                    orientation: "vertical"
                    padding: "16dp"
                    spacing: "16dp"
                    size_hint_y: None
                    height: self.minimum_height

                    MDLabel:
                        text: "Export Options"
                        theme_text_color: "Secondary"

                    MDRaisedButton:
                        text: "EXPORT TO JSON"
                        icon: "code-json"
                        size_hint_x: 1
                        on_release: root.export_json()

                    MDRaisedButton:
                        text: "EXPORT TO CSV"
                        icon: "file-delimited"
                        size_hint_x: 1
                        on_release: root.export_csv()

                    MDRaisedButton:
                        text: "SHARE DATA"
                        icon: "share"
                        size_hint_x: 1
                        on_release: root.share_data()
'''


class SyncScreen(MDScreen):
    def on_enter(self):
        self.update_counts()

    def update_counts(self):
        # Get from local storage
        self.ids.obs_count.text = "12"  # Placeholder
        self.ids.photo_count.text = "8"  # Placeholder

    def sync_data(self):
        # Trigger sync with base station
        from kivymd.uix.dialog import MDDialog
        self.dialog = MDDialog(
            title="Syncing",
            text="Connecting to base station...",
            auto_dismiss=False
        )
        self.dialog.open()
        # TODO: Use your FieldDataCollector.sync_with_base()

    def export_json(self):
        # Generate JSON file
        pass

    def export_csv(self):
        # Generate CSV file
        pass

    def share_data(self):
        # Share using Android share intent
        pass

    def go_back(self):
        self.manager.current = "collect"

Builder.load_string(KV)