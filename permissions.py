"""
Android runtime permission handler for KivyMD apps
"""
from kivy.logger import Logger
from kivy.clock import mainthread
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel

try:
    from android.permissions import request_permissions, check_permission, Permission
    from android import activity

    ANDROID_AVAILABLE = True
except ImportError:
    ANDROID_AVAILABLE = False
    Logger.warning("Permissions: Not running on Android")


class PermissionManager:
    """
    Manages Android runtime permissions
    """

    # Required permissions for the app
    REQUIRED_PERMISSIONS = [
        Permission.CAMERA,
        Permission.ACCESS_FINE_LOCATION,
        Permission.ACCESS_COARSE_LOCATION,
        Permission.READ_EXTERNAL_STORAGE,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.INTERNET,
        Permission.ACCESS_NETWORK_STATE,
    ]

    def __init__(self, callback=None):
        """
        Args:
            callback: Function to call when all permissions are granted
        """
        self.callback = callback
        self.dialog = None

    def check_permissions(self):
        """Check if all required permissions are granted"""
        if not ANDROID_AVAILABLE:
            Logger.info("Permissions: Not Android, assuming all granted")
            return True

        missing = []
        for permission in self.REQUIRED_PERMISSIONS:
            if not check_permission(permission):
                missing.append(permission)

        return len(missing) == 0

    def get_missing_permissions(self):
        """Return list of missing permissions"""
        if not ANDROID_AVAILABLE:
            return []

        missing = []
        for permission in self.REQUIRED_PERMISSIONS:
            if not check_permission(permission):
                missing.append(permission)

        return missing

    def request_all_permissions(self, callback=None):
        """
        Request all required permissions

        Args:
            callback: Optional callback for when permissions are granted/denied
        """
        if not ANDROID_AVAILABLE:
            if callback:
                callback(True)
            return True

        missing = self.get_missing_permissions()

        if not missing:
            Logger.info("Permissions: All permissions already granted")
            if callback:
                callback(True)
            return True

        Logger.info(f"Permissions: Requesting {len(missing)} permissions")

        # Store callback for later
        if callback:
            self.callback = callback

        # Request permissions
        request_permissions(missing, self._permissions_callback)
        return False

    def _permissions_callback(self, permissions, results):
        """Called after permission request completes"""
        granted = all(results)

        if granted:
            Logger.info("Permissions: All permissions granted")
            if self.callback:
                self.callback(True)
        else:
            Logger.warning("Permissions: Some permissions denied")
            self._show_permission_dialog()
            if self.callback:
                self.callback(False)

    @mainthread
    def _show_permission_dialog(self):
        """Show dialog explaining why permissions are needed"""
        if self.dialog and self.dialog.open:
            self.dialog.dismiss()

        content = BoxLayout(
            orientation='vertical',
            spacing=15,
            padding=20,
            size_hint_y=None,
            height=200
        )

        content.add_widget(
            MDLabel(
                text="Permissions Required",
                font_style="H6",
                halign="center",
                size_hint_y=None,
                height=40
            )
        )

        content.add_widget(
            MDLabel(
                text="This app needs camera, GPS, and storage permissions to function.\n\n"
                     "- Camera: Take photos of observations\n"
                     "- GPS: Record location coordinates\n"
                     "- Storage: Save observations and photos",
                halign="center",
                theme_text_color="Secondary",
                size_hint_y=None,
                height=120
            )
        )

        self.dialog = MDDialog(
            title="",
            type="custom",
            content_cls=content,
            buttons=[
                MDRaisedButton(
                    text="EXIT",
                    md_bg_color=(0.8, 0.2, 0.2, 1),
                    on_release=lambda x: self._exit_app()
                ),
                MDRaisedButton(
                    text="RETRY",
                    on_release=lambda x: self._retry_permissions()
                )
            ]
        )
        self.dialog.open()

    def _retry_permissions(self):
        """Retry permission request"""
        if self.dialog:
            self.dialog.dismiss()
        self.request_all_permissions(self.callback)

    def _exit_app(self):
        """Exit the app"""
        if self.dialog:
            self.dialog.dismiss()
        import sys
        sys.exit(0)


class RuntimePermissionScreen:
    """
    Mixin class for screens that need runtime permissions.
    Add this to any screen that uses camera, GPS, or storage.
    """

    def check_and_request_permissions(self, on_granted=None, on_denied=None):
        """
        Check and request permissions for this screen

        Args:
            on_granted: Callback when permissions are granted
            on_denied: Callback when permissions are denied
        """
        if not ANDROID_AVAILABLE:
            if on_granted:
                on_granted()
            return True

        missing = self._get_missing_screen_permissions()

        if not missing:
            if on_granted:
                on_granted()
            return True

        # Store callbacks
        self._perm_on_granted = on_granted
        self._perm_on_denied = on_denied

        # Request permissions
        request_permissions(missing, self._screen_permissions_callback)
        return False

    def _get_missing_screen_permissions(self):
        """Override this in your screen to specify needed permissions"""
        # Default: no extra permissions beyond basic
        return []

    def _screen_permissions_callback(self, permissions, results):
        """Called after screen-specific permission request"""
        granted = all(results)

        if granted:
            if hasattr(self, '_perm_on_granted') and self._perm_on_granted:
                self._perm_on_granted()
        else:
            if hasattr(self, '_perm_on_denied') and self._perm_on_denied:
                self._perm_on_denied()
            else:
                self._show_permission_denied_dialog()