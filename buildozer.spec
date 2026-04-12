[app]

# (str) Title of your application
title = Habilis Data Logger

# (str) Package name
package.name = habilisdatalogger

# (str) Package domain (needs to be unique)
package.domain = org.habilis

# (str) Source code directory where your main.py lives
source.dir = .

# (list) Source files to include (all .py files by default)
source.include_exts = py,png,jpg,kv,atlas,ttf,json

requirements = python3,kivy==2.1.0,kivymd==1.1.1,plyer,requests,reportlab,pillow,qrcode,flask,flask-cors,cython

# (list) Version number
version = 0.1

# (str) The branch of python-for-android to use (for development)
p4a.branch = develop

# (str) Presplash file (loading screen image)
# presplash.filename = %(source.dir)s/assets/presplash.png

# (str) Icon file
# icon.filename = %(source.dir)s/assets/icon.png

# (str) Supported orientation (portrait, landscape or both)
orientation = portrait

# (bool) Indicates if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = 
INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (list) Android API to use
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (int) Target API
android.targetapi = 33

# (list) Gradle dependencies
android.gradle_dependencies = 
'com.google.android.gms:play-services-location:21.0.1'

# (bool) Enable or disable AndroidX
android.use_androidx = True

# (str) Android NDK version
android.ndk = 25b

# (str) Android SDK version
android.sdk = 30

# (list) Permissions (additional)
android.add_permissions = android.permission.ACCESS_BACKGROUND_LOCATION

# (str) Log level (debug, info, warning, error, critical)
log_level = 2

# (bool) Whether to warn if the build version is too old
warn_on_root = 1

# (bool) Whether to allow the application to be debuggable
android.debug = True

# (bool) Whether to enable the Java debugger
android.enable_java_debugging = False

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Copy libs (if False, uses the libs in the APK)
android.copy_libs = 1

# (str) Architectures to build for (armeabi-v7a, arm64-v8a, x86, x86_64)
android.archs = arm64-v8a, armeabi-v7a

# (str) Java source code directory
android.add_src =

# (list) Java jars to add
android.add_jars =

# (list) Python modules to include
android.add_python_modules =

# (list) AAR files to include
android.add_aars =

# (bool) Whether to use the SDL2 backend (always true for Kivy)
ios.kivy_ios = False

# (str) iOS bundle identifier
ios.bundle_identifier = org.habilis.fieldlogger

# (str) iOS version
ios.version = 0.1.0

# (bool) Whether to enable iOS bitcode
ios.enable_bitcode = False

# (list) iOS frameworks to add
ios.frameworks =

# (list) iOS plist keys
ios.plist_keys =

# (str) iOS Xcode project path
ios.xcode_project_path =

# (str) iOS Xcode scheme
ios.xcode_scheme =

# (list) iOS entitlements
ios.entitlements =

# (list) iOS info_plist additions
ios.info_plist =

# (str) iOS icon file
ios.icon.filename =

# (str) iOS presplash file
ios.presplash.filename =
