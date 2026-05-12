[app]

title = Habilis Data Logger
package.name = habilisdatalogger
package.domain = org.kffs

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
source.exclude_dirs = tests, bin, venv, .git, __pycache__, docs

version = 0.1

requirements = python3,kivy==2.3.0,kivymd==1.2.0,https://github.com/HyTurtle/plyer/archive/master.zip,requests,qrcode,pillow,android,pyjnius

orientation = portrait
fullscreen = 0

android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, CAMERA, ACCESS_NETWORK_STATE, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

android.api = 33
android.minapi = 21
android.ndk = 25c
android.sdk = 33
android.ndk_api = 21

android.archs = arm64-v8a, armeabi-v7a

android.gradle_dependencies = androidx.core:core:1.9.0
android.add_src = android/
android.allow_backup = True
android.logcat_filters = *:S python:D

p4a.bootstrap = sdl2
p4a.python_version = 3.11

[buildozer]
log_level = 2
warn_on_root = 1
