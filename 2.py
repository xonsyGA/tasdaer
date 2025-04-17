import subprocess
import os
import uuid
import sys

def detect_systemd_virtualization():
    try:
        result = subprocess.run(['systemd-detect-virt'], capture_output=True, text=True)
        if result.returncode == 0:
            virt_type = result.stdout.strip()
            if virt_type != 'none':
                return f"systemd-detect-virt: {virt_type}"
    except Exception:
        pass
    return None

def detect_dmi_virtualization():
    dmi_paths = [
        '/sys/class/dmi/id/product_name',
        '/sys/class/dmi/id/sys_vendor',
        '/sys/class/dmi/id/board_vendor',
    ]
    vm_keywords = ['vmware', 'virtualbox', 'kvm', 'qemu', 'xen', 'bochs', 'bhyve', 'parallels']
    for path in dmi_paths:
        try:
            with open(path) as f:
                content = f.read().lower()
                if any(keyword in content for keyword in vm_keywords):
                    return f"DMI содержит признак виртуализации: {content.strip()}"
        except Exception:
            continue
    return None

def detect_virtual_files():
    suspicious_paths = [
        '/dev/vboxguest', '/dev/vboxuser', '/dev/vmci', '/dev/hv_vmbus'
    ]
    found = [p for p in suspicious_paths if os.path.exists(p)]
    if found:
        return f"Обнаружены подозрительные устройства: {', '.join(found)}"
    return None

def detect_mac_virtualization():
    virtual_mac_prefixes = [
        '00:05:69',  # VMware
        '00:0C:29',  # VMware
        '00:50:56',  # VMware
        '00:1C:14',  # VMware
        '08:00:27',  # VirtualBox
        '52:54:00',  # QEMU/KVM
    ]
    mac = uuid.getnode()
    mac_str = ':'.join(f'{(mac >> ele) & 0xff:02x}' for ele in range(40, -1, -8))
    for prefix in virtual_mac_prefixes:
        if mac_str.lower().startswith(prefix.lower()):
            return f"MAC-адрес виртуалки: {mac_str}"
    return None

def detect_virtual_env():
    checks = [
        detect_systemd_virtualization,
        detect_dmi_virtualization,
        detect_virtual_files,
        detect_mac_virtualization
    ]
    for check in checks:
        result = check()
        if result:
            return result
    return None

if __name__ == "__main__":
    detection = detect_virtual_env()
    if detection:
        print(f"[!] Скрипт завершён: Обнаружена виртуальная среда.\nПричина: {detection}")
        sys.exit(1)
    else:
        print("[✓] Физическая машина: выполнение продолжается.")
        # Основной код ниже
