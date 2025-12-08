[app]
title = Яичко-тян
version = 1.0
package.name = eggchan
package.domain = ru.zvarichenko
source.dir = .
source.main = main.py

# минимальный Android
android.minapi = 21
android.api = 33

# иконка
icon = images/icon512.png

# поддерживаемые архитектуры
android.archs = armeabi-v7a, arm64-v8a

# только APK
android.packaging = apk

# разрешения
android.permissions = INTERNET, VIBRATE

# ориентация
orientation = portrait

# убрать консоль
log_level = 1

# (оставь так)
fullscreen = 0

# ===== Python и модули =====
requirements = python3,kivy

[buildozer]
log_level = 2
warn_on_root = 0

# путь к ключу подписи (в корне проекта)
p4a.release_keystore = my-release-key.keystore
p4a.release_keystore_passwd = 58Dasha58.
p4a.release_keyalias = my-key-alias
p4a.release_keyalias_passwd = 58Dasha58.
