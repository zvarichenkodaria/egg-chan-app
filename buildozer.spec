[app]

# Название и пакет
title = Яичко-тян
package.name = eggchan
package.domain = ru.zvarichenko

# Исходники
source.dir = .
source.main = main.py
version = 1.0

# Требования
requirements = python3,kivy

# Иконка
icon.filename = %(source.dir)s/images/icon512.png

# Ориентация и вид
orientation = portrait
fullscreen = 0

# Разрешения Android
android.permissions = INTERNET,VIBRATE

# Версии Android API
android.api = 33
android.minapi = 21

# Автоматически принимать лицензии (ВАЖНО)
android.accept_sdk_license = True

# Архитектуры процессора
android.archs = armeabi-v7a

# Формат сборки (APK)
android.release_artifact = apk

# Бекап
android.allow_backup = True

# Настройки Python for Android
p4a.branch = master
p4a.bootstrap = sdl2

[buildozer]

# Уровень логов (2 = debug)
log_level = 2

# Не предупреждать при запуске от root (ВАЖНО для Docker)
warn_on_root = 0

