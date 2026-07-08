import time
import os
import glob

OUTPUT_FILE = "/app/val1.txt"

def find_thermal_sensor():
    """Ищет первый доступный датчик температуры процессора в системе."""
    # 1. Сначала ищем в thermal_zone (x86_pkg_temp для Intel/AMD или cpu-thermal для ARM)
    zones = sorted(glob.glob("/sys/class/thermal/thermal_zone*"))
    for zone in zones:
        try:
            with open(os.path.join(zone, "type"), "r") as f:
                zone_type = f.read().lower()
            # Нам нужны зоны процессора или ACPI плат
            if any(x in zone_type for x in ["pkg", "cpu", "acpi", "core"]):
                temp_path = os.path.join(zone, "temp")
                if os.path.exists(temp_path):
                    return temp_path
        except:
            continue

    # 2. Если не нашли, ищем в hwmon (часто для amd_energy или coretemp)
    hwmon_inputs = sorted(glob.glob("/sys/class/hwmon/hwmon*/temp*_input"))
    if hwmon_inputs:
        return hwmon_inputs[0] # берем самый первый рабочий инпут

    return None

# Инициализация датчика
SENSOR_PATH = find_thermal_sensor()
if SENSOR_PATH:
    print(f"Успешно найден датчик температуры по пути: {SENSOR_PATH}", flush=True)
else:
    print("ВНИМАНИЕ: Ни один аппаратный датчик температуры не обнаружен!", flush=True)

while True:
    try:
        if SENSOR_PATH and os.path.exists(SENSOR_PATH):
            with open(SENSOR_PATH, "r") as f:
                raw_temp = f.read().strip()
                # Переводим из милиградусов в Цельсии (например, 45000 -> 45.0)
                celsius = round(float(raw_temp) / 1000, 1)
                
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                f.write(f"{celsius}°C\n")
        else:
            # Если датчик так и не найден, пишем заглушку
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                f.write("Датчик не найден\n")
    except Exception as e:
        print(f"Ошибка чтения: {e}", flush=True)
        
    time.sleep(1)
