import os
import sys
import time
import shutil
from datetime import datetime, timedelta
from core.plugin_interface import Tool
from core.ui import UI


class Optimisation(Tool):
    @property
    def name(self):
        return "Optimisation"

    @property
    def description(self):
        return "Nettoie les fichiers temporaires et libère de l'espace disque (Windows/Linux)."

    def _default_temp_paths(self):
        paths = []
        if os.name == 'nt':
            temp = os.environ.get('TEMP') or os.environ.get('TMP')
            systemroot = os.environ.get('SystemRoot', 'C:\\Windows')
            if temp:
                paths.append(temp)
            paths.append(os.path.join(systemroot, 'Temp'))
        else:
            paths.append('/tmp')
            home = os.path.expanduser('~')
            if home:
                paths.append(os.path.join(home, '.cache'))
                paths.append(os.path.join(home, 'tmp'))
        seen = []
        for p in paths:
            if p and os.path.exists(p) and p not in seen:
                seen.append(p)
        return seen

    def _gather_stats(self, paths, older_than_days=None):
        entries = []
        cutoff = None
        if older_than_days is not None:
            cutoff = time.time() - older_than_days * 86400
        total = 0
        count = 0
        for base in paths:
            for root, dirs, files in os.walk(base):
                for name in files:
                    try:
                        fp = os.path.join(root, name)
                        if os.path.islink(fp):
                            continue
                        st = os.stat(fp)
                        mtime = st.st_mtime
                        size = st.st_size
                        if cutoff is None or mtime <= cutoff:
                            entries.append((fp, size, mtime))
                            total += size
                            count += 1
                    except Exception:
                        continue
        return count, total, entries

    def _delete_entries(self, entries):
        removed = 0
        freed = 0
        errors = []
        for fp, size, mtime in entries:
            try:
                if os.path.isfile(fp):
                    os.remove(fp)
                    removed += 1
                    freed += size
            except Exception as e:
                errors.append((fp, str(e)))
        dir_candidates = set(os.path.dirname(fp) for fp, _, _ in entries)
        for d in sorted(dir_candidates, key=lambda x: -len(x)):
            try:
                if os.path.isdir(d) and not os.listdir(d):
                    os.rmdir(d)
            except Exception:
                pass
        return removed, freed, errors

    def execute(self):
        UI.print_info('Module d\'optimisation — vérification des fichiers temporaires...')

        targets = self._default_temp_paths()
        if not targets:
            UI.print_error("Aucun dossier temporaire détecté sur ce système.")
            return

        UI.print_info('Dossiers cibles détectés :')
        for p in targets:
            UI.print_info(f' - {p}')

        days_input = UI.ask('Supprimer tous les fichiers trouvés ou seulement ceux plus vieux que N jours ? (Entrer N ou laisser vide pour supprimer tous) :')
        older_than = None
        try:
            if days_input and days_input.strip():
                older_than = int(days_input.strip())
                if older_than < 0:
                    older_than = None
        except Exception:
            older_than = None

        UI.print_info('Collecte des statistiques (cela peut prendre quelques secondes)...')
        count, total, entries = self._gather_stats(targets, older_than)

        def human(n):
            for unit in ('B','KiB','MiB','GiB','TiB'):
                if n < 1024.0:
                    return f"{n:.2f} {unit}"
                n /= 1024.0
            return f"{n:.2f} PiB"

        UI.print_info(f'Fichiers potentiels à supprimer : {count}')
        UI.print_info(f'Espace potentiellement libérable : {human(total)}')

        if count == 0:
            UI.print_info('Rien à supprimer selon les critères fournis.')
            return

        confirm = UI.ask('Confirmez-vous la suppression de ces fichiers ? (o/N) :')
        if not confirm or not confirm.strip().lower().startswith(('o','y')):
            UI.print_info('Opération annulée par l\'utilisateur.')
            return

        UI.print_info('Suppression en cours...')
        removed, freed, errors = self._delete_entries(entries)

        UI.print_info(f'Fichiers supprimés : {removed}')
        UI.print_info(f'Espace réellement libéré : {human(freed)}')
        if errors:
            UI.print_error(f'Erreurs lors de la suppression de {len(errors)} fichiers (exemples):')
            for fp, err in errors[:5]:
                UI.print_error(f'  {fp} -> {err}')

        UI.print_success('Optimisation terminée.')
