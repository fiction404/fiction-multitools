from core.plugin_interface import Tool
from core.ui import UI

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import ctypes
import time
from datetime import datetime
import uuid


class DbScanner(Tool):
    @property
    def name(self):
        return "DbScanner"

    @property
    def description(self):
        return "Recherche récursive (type grep) d'une chaîne dans tous les fichiers d'un dossier."

    def _estimate_workers(self):
        cpu = os.cpu_count() or 1
        mem_gb = self._get_total_ram_gb() or 4

        workers = min(cpu, max(1, mem_gb))

        workers = max(1, min(workers, 32))
        return workers

    def _get_total_ram_gb(self):
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
                return max(1, int(stat.ullTotalPhys / (1024 ** 3)))

            if os.path.exists('/proc/meminfo'):
                with open('/proc/meminfo', 'r', encoding='utf-8', errors='replace') as f:
                    for line in f:
                        if line.startswith('MemTotal:'):
                            parts = line.split()
                            kb = int(parts[1])
                            return max(1, int(kb / 1024 / 1024))

        except Exception:
            return None

        return None

    def _is_probably_binary(self, path, blocksize=1024):
        try:
            with open(path, 'rb') as f:
                chunk = f.read(blocksize)
                if b"\0" in chunk:
                    return True
        except Exception:
            return True
        return False

    def _search_file(self, path, target):
        matches = []
        try:
            if self._is_probably_binary(path):
                return matches

            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                for i, line in enumerate(f, start=1):
                    if target in line:
                        matches.append((path, i, line.rstrip('\n')))
        except Exception as e:
            matches.append((path, -1, f"<error: {e}>") )
        return matches

    def execute(self):
        directory = UI.ask("Entrez le chemin du dossier à analyser :")
        if not directory:
            UI.print_error("Chemin invalide.")
            return

        if not os.path.isdir(directory):
            UI.print_error("Le chemin fourni n'est pas un dossier existant.")
            return

        target = UI.ask("Entrez la chaîne à rechercher :")
        if not target:
            UI.print_error("Chaîne de recherche invalide.")
            return

        UI.print_info(f"Recherche de '{target}' dans {directory} ...")

        file_paths = []
        for root, dirs, files in os.walk(directory):
            for name in files:
                file_paths.append(os.path.join(root, name))

        if not file_paths:
            UI.print_info("Aucun fichier trouvé dans le dossier.")
            return

        workers = self._estimate_workers()
        UI.print_info(f"Utilisation de {workers} threads pour analyser {len(file_paths)} fichiers.")

        all_matches = []
        errors = []
        files_processed = 0

        start = time.time()
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futures = {ex.submit(self._search_file, p, target): p for p in file_paths}
            for fut in as_completed(futures):
                files_processed += 1
                try:
                    matches = fut.result()
                except Exception as e:
                    errors.append((futures.get(fut, '<unknown>'), -1, f"<executor error: {e}>"))
                    UI.print_error(f"Erreur worker: {e}")
                    continue

                for path, lineno, content in matches:
                    if lineno == -1:
                        errors.append((path, lineno, content))
                        UI.print_error(f"Erreur lecture fichier {path} : {content}")
                        continue
                    all_matches.append((path, lineno, content))
                    UI.print_info(f"{path}:{lineno}: {content}")

        elapsed = time.time() - start

        UI.print_info(f"Fichiers examinés : {files_processed}/{len(file_paths)}")
        UI.print_info(f"Temps d'exécution : {elapsed:.2f} secondes")

        if not all_matches:
            UI.print_info("Aucune occurrence trouvée.")

        save = UI.ask("Voulez-vous sauvegarder les résultats dans ./output ? (o/N)")
        if save and save.strip().lower().startswith(('o', 'y')):
            out_dir = os.path.join(os.getcwd(), 'output')
            try:
                os.makedirs(out_dir, exist_ok=True)
                fname = f"dbscan_{datetime.now().strftime('%Y%m%dT%H%M%SZ')}_{uuid.uuid4().hex[:8]}.txt"
                out_path = os.path.join(out_dir, fname)
                with open(out_path, 'w', encoding='utf-8') as fout:
                    fout.write(f"DbScanner results\n")
                    fout.write(f"Directory: {directory}\n")
                    fout.write(f"Target: {target}\n")
                    fout.write(f"Files scanned: {files_processed}/{len(file_paths)}\n")
                    fout.write(f"Elapsed (s): {elapsed:.2f}\n")
                    fout.write('\nMatches:\n')
                    for path, lineno, content in all_matches:
                        fout.write(f"{path}:{lineno}: {content}\n")
                    if errors:
                        fout.write('\nErrors:\n')
                        for path, lineno, content in errors:
                            fout.write(f"{path}:{lineno}: {content}\n")
                UI.print_info(f"Résultats sauvegardés dans {out_path}")
            except Exception as e:
                UI.print_error(f"Impossible de sauvegarder les résultats : {e}")
