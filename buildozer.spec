[app]

# (str) Title of your application
title = Demopy

# (str) Package name
package.name = Demopy

# (str) Package domain (needed for android/ios packaging)
package.domain = org.kivymd

# (str) Source code where the main.py live
source.dir = .

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*

# (str) Presplash of the application
presplash.filename = %(source.dir)s/assets/images/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/assets/images/logo.png

# (string) Presplash background color (for new android toolchain)
android.presplash_color = #000000

# (list) Source files to include (let empty to include all the files)
source.include_exts = py, gif, png, jpg, jpeg, ttf, kv, json, txt, md

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin, venv

# (list) List of exclusions using pattern matching
# Do not prefix with './'
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 2)
version = 0.0.1
# (list) Application requirements
# requirements = python3, kivy==2.3.1, https://github.com/kivymd/KivyMD/archive/master.zip, exceptiongroup, asynckivy, asyncgui, materialyoucolor, android, materialshapes, pycairo
requirements = python3, kivy==2.3.1, https://github.com/yuzchu/KivyMD-font/archive/master.zip, bs4, charset_normalizer, idna, pysnooper, requests, soupsieve, tenacity, urllib3, vthread, zmail, exceptiongroup, asynckivy, asyncgui, materialyoucolor, android, materialshapes, pycairo

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait
# (list) Permissions
android.permissions = INTERNET, INSTALL_SHORTCUT, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (int) Target Android API, should be as high as possible.
android.api = 36

# (int) Minimum API your APK / AAB will support.
android.minapi = 30

# (int) Android SDK version to use
#android.sdk = 28

# (str) Android NDK version to use
# android.ndk = 25b

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
# android.ndk_api = 30

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
# when an update is due and you just want to test/build your package
android.skip_update = False

# (bool) If True, then automatically accept SDK license
# agreements. This is intended for automation only. If set to False,
# the default, you will be shown the license when first running
# buildozer.
android.accept_sdk_license = True

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) The format used to package the app for release mode (aab or apk or aar).
android.release_artifact = aab

# (str) The format used to package the app for debug mode (apk or aar).
android.debug_artifact = apk

# (str) python-for-android branch to use, defaults to master
p4a.branch = develop

# (str) Bootstrap to use for android builds
# p4a.bootstrap = sdl2

# (str) extra command line arguments to pass when invoking pythonforandroid.toolchain
#p4a.extra_args = --blacklist-requirements=sqlite3,openssl

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
# bin_dir = ./bin