[app]

# Название и пакет
title = Яичко-тян
package.name = eggchan
package.domain = ru.zvarichenko

# Исходники
source.dir = .
source.main = main.py
# ВАЖНО: Добавляем все форматы, чтобы картинки и шрифты попали в APK
source.include_exts = py,png,jpg,jpeg,JPG,PNG,kv,atlas,ttf,otf,json,txt,xml,wav,mp3
version = 1.0

# Требования
requirements = python3,kivy,pillow

# Иконка (твоя правильная, 512x512)
icon.filename = images/icon512.png

# Экран загрузки (вместо Loading...)
# Тут используем маскота, чтобы было красиво
presplash.filename = images/mascot.jpeg
android.presplash_color = #121212

# Ориентация и вид
orientation = portrait
fullscreen = 0

# Разрешения Android
android.permissions = INTERNET,VIBRATE

# Версии Android API
android.api = 33
android.minapi = 21

# Автоматически принимать лицензии
android.accept_sdk_license = True

# Архитектуры процессора
android.archs = arm64-v8a

# Формат сборки
android.release_artifact = apk

# Бекап
android.allow_backup = True

# Настройки Python for Android
p4a.branch = master
p4a.bootstrap = sdl2

# Ключи для подписи (важно для Gradle)
p4a.release_keystore = my-release-key.keystore
p4a.release_keyalias = my-key-alias

[buildozer]

# Уровень логов
log_level = 2

# Не предупреждать при запуске от root
warn_on_root = 0
