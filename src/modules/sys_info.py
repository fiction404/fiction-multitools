import platform
import sys
import os
import shutil
import subprocess
import ctypes
import re
from string import ascii_uppercase

from core.plugin_interface import Tool
from core.ui import UI


class SystemInfo(Tool):
    @property
    def name(self):
        return "SystemInfo"

    @property
    def description(self):
        return "Affiche les détails de la machine et de l'OS."

    def execute(self):
        UI.print_info("Récupération des informations...")

        info = {
            "Système d'exploitation": platform.system(),
            "Version de l'OS": platform.release(),
            "Architecture": platform.machine(),
            "Processeur": platform.processor() or os.environ.get('PROCESSOR_IDENTIFIER', 'Inconnu'),
            "Version Python": sys.version.split()[0],
            }

        info["Coeurs (logiques)"] = self._get_logical_cores()
        info["Coeurs (physiques)"] = self._get_physical_cores()
        info["RAM totale (GiB)"] = self._get_total_ram_gb() or 'Inconnu'

        print("\n" + "-" * 60)
        for key, value in info.items():
            print(f"{key:.<30}: {value}")

        print('\nDisques montés et taille totale :')
        for mp, size in self._get_disks_info():
            print(f"{mp:.<30}: {size} GiB")

        gpu = self._get_gpu_info()
        print('\nCarte(s) graphique(s) :')
        print(gpu)

        print('-' * 60 + '\n')

        UI.print_success("Analyse terminée.")

    def _get_logical_cores(self):
        return os.cpu_count() or 1

    def _get_physical_cores(self):
        try:
            if os.name == 'nt':
                out = subprocess.check_output(['wmic', 'cpu', 'get', 'NumberOfCores'], stderr=subprocess.DEVNULL, text=True)
                nums = re.findall(r"\d+", out)
                if nums:
                    return sum(int(n) for n in nums)
            else:
                if os.path.exists('/proc/cpuinfo'):
                    with open('/proc/cpuinfo', 'r', encoding='utf-8', errors='replace') as f:
                        cpuinfo = f.read()
                    matches = re.findall(r"physical id\s*:\s*(\d+)", cpuinfo)
                    if matches:
                        cores_match = re.search(r"cpu cores\s*:\s*(\d+)", cpuinfo)
                        if cores_match:
                            return len(set(matches)) * int(cores_match.group(1))
                        return len(set(matches))
        except Exception:
            pass
        return self._get_logical_cores()

    def _Get_total_ram_gb(self):
        try:
            if os.name == 'nt':
                class MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ("dwLength", ctypes.c_uint32),
                        ("dwMemoryLoad", ctypes.c_uint32),
                        ("ullTotalPhys", ctypes.c_uint64),
                        ("ullAvailPhys", ctypes.c_uint64),
                        ("ullTotalPageFile", ctypes.c_uint64),
                        ("ullAvailPageFile", ctypes.c_uint64),
                        ("ullTotalVirtual", ctypes.c_uint64),
                        ("ullAvailVirtual", ctypes.c_uint64),
                        ("ullAvailExtendedVirtual", ctypes.c_uint64),
                    ]
                stat = MEMORYSTATUSEX()
                stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
                if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
                    return None
                return round(stat.ullTotalPhys / (1024 ** 3), 2)
            else:
                if os.path.exists('/proc/meminfo'):
                    with open('/proc/meminfo', 'r', encoding='utf-8', errors='replace') as f:
                        for line in f:
                            if line.startswith('MemTotal:'):
                                parts = line.split()
                                kb = int(parts[1])
                                return round(kb / 1024 / 1024, 2)
        except Exception:
            return None
        return None

    def _get_total_ram_gb(self):
        return self._Get_total_ram_gb()

    def _get_disks_info(self):
        disks = []
        try:
            if os.name == 'nt':
                for letter in ascii_uppercase:
                    drive = f"{letter}:\\"
                    if os.path.exists(drive):
                        try:
                            total, used, free = shutil.disk_usage(drive)
                            disks.append((drive, round(total / (1024 ** 3), 2)))
                        except Exception:
                            pass
            else:
                mounts = set()
                if os.path.exists('/proc/mounts'):
                    with open('/proc/mounts', 'r', encoding='utf-8', errors='replace') as f:
                        for line in f:
                            parts = line.split()
                            if len(parts) >= 2:
                                mp = parts[1]
                                mounts.add(mp)
                mounts.add('/')
                for mp in sorted(mounts):
                    try:
                        total, used, free = shutil.disk_usage(mp)
                        disks.append((mp, round(total / (1024 ** 3), 2)))
                    except Exception:
                        pass
        except Exception:
            pass
        return disks

    def _get_gpu_info(self):
        try:
            if os.name == 'nt':
                try:
                    out = subprocess.check_output(['wmic', 'path', 'win32_VideoController', 'get', 'name'], stderr=subprocess.DEVNULL, text=True)
                    names = [l.strip() for l in out.splitlines() if l.strip() and 'Name' not in l]
                    return ', '.join(names) if names else 'Inconnu'
                except Exception:
                    try:
                        ps = ['powershell', '-NoProfile', "Get-WmiObject Win32_VideoController | Select-Object -ExpandProperty Name"]
                        out = subprocess.check_output(ps, stderr=subprocess.DEVNULL, text=True)
                        names = [l.strip() for l in out.splitlines() if l.strip()]
                        return ', '.join(names) if names else 'Inconnu'
                    except Exception:
                        return 'Inconnu'
            else:
                try:
                    out = subprocess.check_output(['lspci'], stderr=subprocess.DEVNULL, text=True)
                    gpus = [l for l in out.splitlines() if re.search(r'vga|3d|display', l, re.I)]
                    if gpus:
                        return '; '.join(gpus)
                except Exception:
                    pass
                try:
                    out = subprocess.check_output(['nvidia-smi', '--query-gpu=name', '--format=csv,noheader'], stderr=subprocess.DEVNULL, text=True)
                    names = [l.strip() for l in out.splitlines() if l.strip()]
                    if names:
                        return ', '.join(names)
                except Exception:
                    pass
        except Exception:
            pass
        return 'Inconnu'