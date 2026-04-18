[app]

title = Habilis Data Logger
package.name = habilisdatalogger
package.domain = org.kffs

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
source.exclude_dirs = tests, bin, venv, .git, __pycache__, docs

version = 0.1

requirements = python3,kivy==2.3.0,kivymd==1.2.0,plyer,requests,qrcode,pillow,android

orientation = portrait
fullscreen = 0

android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, CAMERA, READ_EXTERNAL_STORAGE, 
WRITE_EXTERNAL_STORAGE, ACCESS_NETWORK_STATE

android.api = 33
android.minapi = 21
android.ndk = 25c
android.sdk = 33
android.ndk_api = 21

android.archs = arm64-v8a, armeabi-v7a

android.allow_backup = True
android.logcat_filters = *:S python:D

p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1

