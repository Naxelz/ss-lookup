import psutil
import requests
import json
import os
import time
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Set, Optional
from bs4 import BeautifulSoup
import logging
import sqlite3
import shutil
import tempfile
import glob
import subprocess
import re
from dotenv import load_dotenv
try:
    import winreg
except Exception:
    winreg = None

Path('reportes').mkdir(exist_ok=True)
Path('informes').mkdir(exist_ok=True)
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('reportes/scanner.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class RobloxScanner:
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        self.github_token = os.getenv('GITHUB_TOKEN', '')
        if self.github_token:
            self.session.headers.update({'Authorization': f'token {self.github_token}'})
        
        self.start_time = time.time()
        
        self.exploit_signatures = {
            'Wave': {
                'processes': ['wave.exe', 'waveexecutor.exe', 'wave_injector.exe'],
                'files': ['wave.exe', 'waveexecutor.exe'],
                'folders': ['Wave', 'WaveExecutor']
            },
            'Xeno': {
                'processes': ['xeno.exe', 'xenoexecutor.exe', 'xeno_bootstrap.exe'],
                'files': ['xeno.exe', 'xenoexecutor.exe'],
                'folders': ['Xeno', 'XenoExecutor']
            },
            'Volcano': {
                'processes': ['volcano.exe', 'volcanoexecutor.exe', 'volcano_injector.exe'],
                'files': ['volcano.exe', 'volcanoexecutor.exe'],
                'folders': ['Volcano', 'VolcanoExecutor']
            },
            'KRNL': {
                'processes': ['krnl.exe', 'krnlss.exe', 'krnl_bootstrap.exe'],
                'files': ['krnl.exe', 'krnlss.exe'],
                'folders': ['KRNL', 'krnl']
            },
            'Fluxus': {
                'processes': ['fluxus.exe', 'fluxus_bootstrap.exe'],
                'files': ['fluxus.exe'],
                'folders': ['Fluxus']
            },
            'Solara': {
                'processes': ['solara.exe', 'solara_executor.exe'],
                'files': ['solara.exe'],
                'folders': ['Solara']
            },
            'Electron': {
                'processes': ['electron.exe', 'electron_executor.exe'],
                'files': ['electron.exe'],
                'folders': ['Electron', 'ElectronExecutor']
            },
            'Nexus': {
                'processes': ['nexus.exe', 'nexus_roblox.exe'],
                'files': ['nexus.exe'],
                'folders': ['Nexus', 'NexusExecutor']
            },
            'Synapse X': {
                'processes': ['synapse.exe', 'synapsex.exe'],
                'files': ['synapse.exe', 'sxlib.dll'],
                'folders': ['Synapse', 'SynapseX']
            },
            'Delta': {
                'processes': ['delta.exe', 'deltaexecutor.exe'],
                'files': ['delta.exe'],
                'folders': ['Delta', 'DeltaExecutor']
            },
            'Zenith': {
                'processes': ['zenith.exe', 'zenithexecutor.exe'],
                'files': ['zenith.exe'],
                'folders': ['Zenith']
            },
            'Bunni': {
                'processes': ['bunni.exe', 'bunny.exe', 'buni.exe'],
                'files': ['bunni.exe', 'bunny.exe', 'buni.exe'],
                'folders': ['Bunni', 'Bunny', 'Buni']
            },
            'Buni LOL': {
                'processes': ['buni_lol.exe', 'buni-lol.exe', 'bunilol.exe'],
                'files': ['buni_lol.exe', 'bunilol.exe'],
                'folders': ['BuniLOL']
            },
            'TGX': {
                'processes': ['tgx.exe', 'thegabloxiagang.exe', 'gabloxia.exe'],
                'files': ['tgx.exe'],
                'folders': ['TGX', 'TheGabloxiaGang']
            },
            'Volt': {
                'processes': ['volt.exe', 'voltexecutor.exe'],
                'files': ['volt.exe'],
                'folders': ['Volt', 'VoltExecutor']
            },
            'Seliware': {
                'processes': ['seliware.exe', 'seliware_bootstrap.exe'],
                'files': ['seliware.exe'],
                'folders': ['Seliware']
            },
            'Valex': {
                'processes': ['valex.exe', 'valexexecutor.exe'],
                'files': ['valex.exe'],
                'folders': ['Valex']
            },
            'Potassium': {
                'processes': ['potassium.exe', 'pottasium.exe'],
                'files': ['potassium.exe', 'pottasium.exe'],
                'folders': ['Potassium', 'Pottasium']
            },
            'Hydrogen': {
                'processes': ['hydrogen.exe', 'hydrogen_bootstrap.exe'],
                'files': ['hydrogen.exe'],
                'folders': ['Hydrogen']
            },
            'Arceus X': {
                'processes': ['arceusx.exe', 'arceus_x.exe'],
                'files': ['arceusx.exe'],
                'folders': ['ArceusX']
            },
            'Codex': {
                'processes': ['codex.exe', 'codexexecutor.exe'],
                'files': ['codex.exe'],
                'folders': ['Codex']
            },
            'Oxygen U': {
                'processes': ['oxygen.exe', 'oxygenu.exe'],
                'files': ['oxygenu.exe', 'oxygen.exe'],
                'folders': ['Oxygen', 'OxygenU']
            },
            'Vega X': {
                'processes': ['vegax.exe', 'vega_x.exe'],
                'files': ['vegax.exe'],
                'folders': ['VegaX']
            },
            'Trigon': {
                'processes': ['trigon.exe', 'trigon_bootstrap.exe'],
                'files': ['trigon.exe'],
                'folders': ['Trigon']
            },
            'Evon': {
                'processes': ['evon.exe', 'evon_bootstrap.exe'],
                'files': ['evon.exe'],
                'folders': ['Evon']
            },
            'JJSploit': {
                'processes': ['jjsploit.exe'],
                'files': ['jjsploit.exe'],
                'folders': ['JJSploit']
            },
            'SirHurt': {
                'processes': ['sirhurt.exe'],
                'files': ['sirhurt.exe'],
                'folders': ['SirHurt']
            },
            'Elysian': {
                'processes': ['elysian.exe'],
                'files': ['elysian.exe'],
                'folders': ['Elysian']
            },
            'Sentinel': {
                'processes': ['sentinel.exe'],
                'files': ['sentinel.exe'],
                'folders': ['Sentinel']
            },
            'Calamari': {
                'processes': ['calamari.exe'],
                'files': ['calamari.exe'],
                'folders': ['Calamari']
            },
            'ProtoSmasher': {
                'processes': ['protosmasher.exe', 'ps.exe'],
                'files': ['protosmasher.exe'],
                'folders': ['ProtoSmasher']
            },
            'Visenya': {
                'processes': ['visenya.exe'],
                'files': ['visenya.exe'],
                'folders': ['Visenya']
            },
            'Nihon': {
                'processes': ['nihon.exe'],
                'files': ['nihon.exe'],
                'folders': ['Nihon']
            },
            'Skisploit': {
                'processes': ['skisploit.exe'],
                'files': ['skisploit.exe'],
                'folders': ['Skisploit']
            },
            'Calamity': {
                'processes': ['calamity.exe'],
                'files': ['calamity.exe'],
                'folders': ['Calamity']
            },
            'Trojan': {
                'processes': ['trojan.exe', 'trojanexecutor.exe'],
                'files': ['trojan.exe'],
                'folders': ['Trojan']
            },
            'Apex': {
                'processes': ['apex.exe', 'apexexecutor.exe'],
                'files': ['apex.exe'],
                'folders': ['ApexExecutor', 'Apex']
            },
            'Zen': {
                'processes': ['zen.exe', 'zenexecutor.exe'],
                'files': ['zen.exe'],
                'folders': ['ZenExecutor', 'Zen']
            },
            'Phoenix': {
                'processes': ['phoenix.exe', 'phoenixexecutor.exe'],
                'files': ['phoenix.exe'],
                'folders': ['PhoenixExecutor', 'Phoenix']
            },
            'Solix': {
                'processes': ['solix.exe'],
                'files': ['solix.exe'],
                'folders': ['Solix']
            },
            'Electron X': {
                'processes': ['electronx.exe'],
                'files': ['electronx.exe'],
                'folders': ['ElectronX']
            },
            'Nitro': {
                'processes': ['nitro.exe', 'nitroexecutor.exe'],
                'files': ['nitro.exe'],
                'folders': ['Nitro']
            },
            'Vortex': {
                'processes': ['vortex.exe', 'vortexexecutor.exe'],
                'files': ['vortex.exe'],
                'folders': ['Vortex']
            },
            'Aero': {
                'processes': ['aero.exe', 'aeroexecutor.exe'],
                'files': ['aero.exe'],
                'folders': ['Aero']
            },
            'Tempest': {
                'processes': ['tempest.exe'],
                'files': ['tempest.exe'],
                'folders': ['Tempest']
            },
            'Neptune': {
                'processes': ['neptune.exe'],
                'files': ['neptune.exe'],
                'folders': ['Neptune']
            },
            'Aurora': {
                'processes': ['aurora.exe'],
                'files': ['aurora.exe'],
                'folders': ['Aurora']
            },
            'Krypton': {
                'processes': ['krypton.exe'],
                'files': ['krypton.exe'],
                'folders': ['Krypton']
            },
            'Helix': {
                'processes': ['helix.exe'],
                'files': ['helix.exe'],
                'folders': ['Helix']
            },
            'Ignis': {
                'processes': ['ignis.exe'],
                'files': ['ignis.exe'],
                'folders': ['Ignis']
            }
        }
        
        self.results = {}
    
    def scan_local_exploits(self):
        
        logger.info("=" * 70)
        logger.info("MODO: deteccion local de exploits")
        logger.info("=" * 70)
        
        self.results = {
            'scan_type': 'local_detection',
            'scan_metadata': {
                'timestamp': datetime.now().isoformat(),
                'hostname': os.environ.get('COMPUTERNAME', 'Unknown'),
                'username': os.environ.get('USERNAME', 'Unknown'),
                'scan_duration_seconds': 0
            },
            'detected_exploits': [],
            'running_processes': [],
            'suspicious_files': [],
            'suspicious_folders': [],
            'roblox_info': {
                'roblox_running': False,
                'roblox_processes': []
            },
            'statistics': {
                'total_exploits_detected': 0,
                'running_exploits': 0,
                'installed_exploits': 0
            }
        }
        
        logger.info("Escaneando procesos en ejecución...")
        self._scan_processes()
        
        logger.info("Escaneando ubicaciones comunes...")
        self._scan_common_locations()
        
        self._consolidate_detections()
        
        duration = time.time() - self.start_time
        self.results['scan_metadata']['scan_duration_seconds'] = round(duration, 2)
        
        logger.info("=" * 70)
        logger.info(f"Exploits detectados: {self.results['statistics']['total_exploits_detected']}")
        logger.info(f"En ejecución: {self.results['statistics']['running_exploits']}")
        logger.info(f"Instalados: {self.results['statistics']['installed_exploits']}")
        logger.info("=" * 70)
    
    def _scan_processes(self):
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    proc_info = proc.info
                    proc_name = proc_info['name'].lower() if proc_info['name'] else ''
                    
                    if 'roblox' in proc_name:
                        self.results['roblox_info']['roblox_running'] = True
                        self.results['roblox_info']['roblox_processes'].append({
                            'pid': proc_info['pid'],
                            'name': proc_info['name']
                        })
                    
                    for exploit_name, signatures in self.exploit_signatures.items():
                        for process_sig in signatures['processes']:
                            if process_sig.lower() in proc_name:
                                detection = {
                                    'exploit_name': exploit_name,
                                    'detection_type': 'Running Process',
                                    'process_name': proc_info['name'],
                                    'pid': proc_info['pid'],
                                    'exe_path': proc_info.get('exe', 'N/A')
                                }
                                self.results['running_processes'].append(detection)
                                logger.warning(f"Proceso detectado: {exploit_name} - {proc_info['name']}")
                
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        except Exception as e:
            logger.error(f"Error escaneando procesos: {str(e)}")

    def scan_process_modules(self):
        logger.info("=" * 70)
        logger.info("MODO: módulos cargados en procesos")
        logger.info("=" * 70)
        self.results = {
            'scan_type': 'process_modules',
            'scan_metadata': {'timestamp': datetime.now().isoformat()},
            'matches': []
        }
        suspects = ['blackbone', 'winring0', 'capcom', 'hyperion', 'krnl', 'synapse', 'fluxus', 'bloxstrap']
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    maps = proc.memory_maps()
                    for m in maps:
                        path = getattr(m, 'path', '')
                        low = str(path).lower()
                        if any(s in low for s in suspects):
                            self.results['matches'].append({'pid': proc.info['pid'], 'process': proc.info['name'], 'module': path})
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
                except Exception:
                    pass
        except Exception as e:
            logger.error(f"Error módulos de procesos: {e}")
    
    def _scan_common_locations(self):
        
        common_paths = [
            Path.home() / 'Downloads',
            Path.home() / 'Desktop',
            Path.home() / 'Documents',
            Path.home() / 'AppData' / 'Local',
            Path.home() / 'AppData' / 'Roaming'
        ]
        
        for base_path in common_paths:
            if not base_path.exists():
                continue
            
            try:
                for exploit_name, signatures in self.exploit_signatures.items():
                    for folder_name in signatures['folders']:
                        potential_path = base_path / folder_name
                        if potential_path.exists() and potential_path.is_dir():
                            detection = {
                                'exploit_name': exploit_name,
                                'detection_type': 'Folder Found',
                                'path': str(potential_path),
                                'files_count': len(list(potential_path.glob('*')))
                            }
                            self.results['suspicious_folders'].append(detection)
                            logger.warning(f"Carpeta detectada: {exploit_name} - {potential_path}")
            except (PermissionError, OSError):
                pass

    def scan_system_exploits(self):
        logger.info("=" * 70)
        logger.info("MODO: búsqueda de exploits en todo el sistema")
        logger.info("=" * 70)
        self.results = {
            'scan_type': 'system_exploits',
            'scan_metadata': {'timestamp': datetime.now().isoformat()},
            'files_found': [],
            'folders_found': []
        }
        targets_files = set()
        targets_folders = set()
        for name, sig in self.exploit_signatures.items():
            for f in sig.get('files', []):
                targets_files.add(f.lower())
            for p in sig.get('processes', []):
                targets_files.add(p.lower())
            for d in sig.get('folders', []):
                targets_folders.add(d.lower())
        roots = []
        base = Path.home()
        roots += [
            base / 'Downloads',
            base / 'Desktop',
            base / 'Documents',
            base / 'AppData/Local',
            base / 'AppData/Roaming',
            Path('C:/Program Files'),
            Path('C:/Program Files (x86)'),
            Path('C:/ProgramData'),
            Path('C:/Users/Public')
        ]
        max_hits = 3000
        hits = 0
        visited = set()
        for root in roots:
            try:
                for r, dirs, files in os.walk(root):
                    if hits >= max_hits:
                        break
                    rl = r.lower()
                    if any(x in rl for x in ['\\windows\\winsxs', '\\windows\\servicing']):
                        continue
                    for d in list(dirs):
                        dl = d.lower()
                        if dl in targets_folders:
                            p = Path(r) / d
                            k = str(p).lower()
                            if k not in visited:
                                visited.add(k)
                                self.results['folders_found'].append({'path': str(p)})
                                hits += 1
                    for fn in files:
                        fl = fn.lower()
                        if fl in targets_files:
                            p = Path(r) / fn
                            k = str(p).lower()
                            if k not in visited:
                                visited.add(k)
                                self.results['files_found'].append({'path': str(p)})
                                hits += 1
                    if hits >= max_hits:
                        break
            except Exception:
                pass
        logger.info(f"Archivos: {len(self.results['files_found'])}")
        logger.info(f"Carpetas: {len(self.results['folders_found'])}")

    def scan_startup_entries(self):
        logger.info("=" * 70)
        logger.info("MODO: entradas de inicio y tareas programadas")
        logger.info("=" * 70)
        self.results = {
            'scan_type': 'startup_tasks',
            'scan_metadata': {'timestamp': datetime.now().isoformat()},
            'startup': [],
            'scheduled_tasks': []
        }
        startup_paths = [
            Path.home() / 'AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup',
            Path('C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Startup')
        ]
        for sp in startup_paths:
            try:
                for f in sp.glob('**/*'):
                    if f.is_file():
                        self.results['startup'].append({'path': str(f)})
            except Exception:
                pass
        if winreg:
            for hive in [winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE]:
                for key in [r'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run', r'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\RunOnce']:
                    try:
                        k = winreg.OpenKey(hive, key)
                        i = 0
                        while True:
                            try:
                                val = winreg.EnumValue(k, i)
                            except OSError:
                                break
                            i += 1
                            name = str(val[0])
                            data = str(val[1])
                            self.results['startup'].append({'registry': key, 'name': name, 'value': data})
                    except Exception:
                        pass
        try:
            p = subprocess.run(['schtasks', '/query', '/fo', 'LIST', '/v'], capture_output=True, text=True)
            block = []
            for line in p.stdout.splitlines():
                if line.strip() == '':
                    if block:
                        txt = '\n'.join(block)
                        if any(x in txt.lower() for x in ['roblox', 'executor', 'bloxstrap', 'voidstrap', 'voidtrap']):
                            self.results['scheduled_tasks'].append({'raw': txt[:500]})
                        block = []
                else:
                    block.append(line)
        except Exception:
            pass
    
    def _consolidate_detections(self):
        
        detected_exploits = {}
        
        all_detections = (
            self.results['running_processes'] +
            self.results['suspicious_files'] +
            self.results['suspicious_folders']
        )
        
        for detection in all_detections:
            exploit_name = detection['exploit_name']
            
            if exploit_name not in detected_exploits:
                detected_exploits[exploit_name] = {
                    'name': exploit_name,
                    'status': 'Detected',
                    'evidence': [],
                    'running': False,
                    'installed': False
                }
            
            detected_exploits[exploit_name]['evidence'].append(detection)
            
            if detection['detection_type'] == 'Running Process':
                detected_exploits[exploit_name]['running'] = True
            if detection['detection_type'] in ['Folder Found', 'File Found']:
                detected_exploits[exploit_name]['installed'] = True
        
        self.results['detected_exploits'] = list(detected_exploits.values())
        self.results['statistics']['total_exploits_detected'] = len(detected_exploits)
        self.results['statistics']['running_exploits'] = sum(1 for e in detected_exploits.values() if e['running'])
        self.results['statistics']['installed_exploits'] = sum(1 for e in detected_exploits.values() if e['installed'])
    
    def scan_fflags(self):
        
        logger.info("=" * 70)
        logger.info("MODO: BÚSQUEDA DE FFLAGS")
        logger.info("=" * 70)
        
        self.results = {
            'scan_type': 'fflags',
            'scan_metadata': {
                'timestamp': datetime.now().isoformat(),
                'duration_seconds': 0,
                'sources_scanned': []
            },
            'fflags': {
                'bloxtrap': [],
                'voidtrap': [],
                'react': [],
                'ping_optimization': [],
                'network': [],
                'graphics': [],
                'performance': [],
                'experimental': [],
                'other': []
            },
            'statistics': {
                'total_fflags_found': 0,
                'unique_fflags': 0
            }
        }
        
        repos = [
            'MaximumADHD/Roblox-FFlag-Tracker',
            'Dantezz025/Roblox-Fast-Flags',
            'catb0x/Roblox-Potato-FFlags',
            'pizzaboxer/bloxstrap',
            'MaximumADHD/Roblox-Client-Tracker',
            'glina-roblox/Roblox-FFlag-Tracker',
            'roblox-on-linux/bloxstrap-configs'
        ]
        
        all_fflags = set()
        
        for repo in repos:
            logger.info(f"Escaneando repositorio: {repo}")
            fflags = self._search_github_repo_fflags(repo)
            
            for fflag in fflags:
                category = fflag['category']
                if category in self.results['fflags']:
                    self.results['fflags'][category].append(fflag)
                    all_fflags.add(fflag['name'])
            
            time.sleep(2)

        queries = [
            'ClientAppSettings.json+fflag',
            'Bloxstrap+ClientAppSettings.json',
            'Roblox+FFlag+filename:*.json'
        ]
        for q in queries:
            try:
                results = self._search_github_code_fflags(q)
                for item in results:
                    self.results['scan_metadata']['sources_scanned'].append(f'GitHubCode: {item.get("repo")}/{item.get("path")}')
                    content = self._download_file(item['download_url'])
                    if content:
                        self.results['fflags'][self._categorize_fflag(item.get('filename',''))].extend(self._extract_fflags(content, item.get('filename','')))
                time.sleep(1)
            except Exception as e:
                logger.error(f"Error búsqueda de código '{q}': {e}")
        
        duration = time.time() - self.start_time
        self.results['scan_metadata']['duration_seconds'] = round(duration, 2)
        self.results['statistics']['total_fflags_found'] = sum(len(f) for f in self.results['fflags'].values())
        self.results['statistics']['unique_fflags'] = len(all_fflags)
        
        logger.info("=" * 70)
        logger.info(f"FFlags únicos: {len(all_fflags)}")
        logger.info(f"Total de entradas: {self.results['statistics']['total_fflags_found']}")
        logger.info("=" * 70)

    def scan_fflags_all(self):
        logger.info("=" * 70)
        logger.info("MODO: FFlags completo (GitHub + Sistema + Targets)")
        logger.info("=" * 70)
        self.results = {'scan_type': 'fflags_all'}
        self.scan_fflags()
        fflags_external = self.results.copy()
        self.scan_system_fflags()
        fflags_system = self.results.copy()
        self.scan_fflags_from_txt()
        fflags_targets = self.results.copy()
        self.results = {
            'scan_type': 'fflags_all',
            'external': fflags_external,
            'system': fflags_system,
            'targets': fflags_targets
        }
    
    def _search_github_repo_fflags(self, repo: str) -> List[Dict[str, Any]]:
        
        fflags = []
        
        try:
            api_url = f'https://api.github.com/repos/{repo}/contents'
            response = self.session.get(api_url, timeout=10)
            
            if response.status_code == 200:
                contents = response.json()
                self.results['scan_metadata']['sources_scanned'].append(f'GitHub: {repo}')
                
                for item in contents:
                    if item['type'] == 'file' and any(ext in item['name'].lower() for ext in ['.json', 'fflag']):
                        time.sleep(0.5)
                        file_content = self._download_file(item['download_url'])
                        if file_content:
                            fflags.extend(self._extract_fflags(file_content, item['name']))
        
        except Exception as e:
            logger.error(f"Error escaneando {repo}: {str(e)}")
        
        return fflags
    
    def _download_file(self, url: str) -> str:
        
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                return response.text
        except:
            pass
        return ""
    
    def _extract_fflags(self, content: str, filename: str) -> List[Dict[str, Any]]:
        
        fflags = []
        
        try:
            if filename.endswith('.json'):
                data = json.loads(content)
                fflags.extend(self._parse_json_fflags(data, filename))
        except:
            pass
        
        return fflags

    def _search_github_code_fflags(self, query: str) -> List[Dict[str, Any]]:
        items = []
        try:
            url = f'https://api.github.com/search/code?q={query}&per_page=10'
            r = self.session.get(url, timeout=15)
            if r.status_code == 200:
                data = r.json()
                for it in data.get('items', []):
                    items.append({
                        'repo': it.get('repository', {}).get('full_name', ''),
                        'path': it.get('path', ''),
                        'name': it.get('name',''),
                        'filename': it.get('name',''),
                        'download_url': it.get('html_url','').replace('github.com','raw.githubusercontent.com').replace('/blob/','/')
                    })
        except Exception:
            pass
        return items
    
    def _parse_json_fflags(self, data: Any, source: str) -> List[Dict[str, Any]]:
        
        fflags = []
        
        if isinstance(data, dict):
            for key, value in data.items():
                if any(prefix in key for prefix in ['FFlag', 'DFFlag', 'FInt', 'DFInt', 'FString', 'DFString']):
                    fflags.append({
                        'name': key,
                        'value': value,
                        'type': 'Flag' if 'Flag' in key else ('Int' if 'Int' in key else 'String'),
                        'source': source,
                        'category': self._categorize_fflag(key)
                    })
                elif isinstance(value, dict):
                    fflags.extend(self._parse_json_fflags(value, source))
        
        return fflags
    
    def _categorize_fflag(self, name: str) -> str:
        
        name_lower = name.lower()
        
        categories = {
            'bloxtrap': ['bloxstrap', 'bloxtrap', 'bootstrap'],
            'voidtrap': ['voidstrap', 'voidtrap', 'void'],
            'react': ['react', 'uiblox', 'roact'],
            'ping_optimization': ['ping', 'latency', 'network', 'raknet'],
            'graphics': ['graphics', 'render', 'vulkan', 'dx11'],
            'performance': ['fps', 'performance', 'optimization', 'memory'],
            'network': ['http', 'websocket', 'datamodel'],
            'experimental': ['debug', 'experimental', 'beta', 'test']
        }
        
        for category, keywords in categories.items():
            if any(keyword in name_lower for keyword in keywords):
                return category
        
        return 'other'
    
    def scan_github_exploits(self):
        
        logger.info("=" * 70)
        logger.info("MODO:buscando exploits x github")
        logger.info("=" * 70)
        
        self.results = {
            'scan_type': 'github_exploits',
            'scan_metadata': {
                'timestamp': datetime.now().isoformat(),
                'duration_seconds': 0
            },
            'github_repos': [],
            'statistics': {
                'repos_found': 0
            }
        }
        
        search_terms = [
            'wave executor', 'xeno executor', 'volcano executor', 'krnl executor',
            'zenith executor', 'bunni executor', 'tgx executor', 'the gabloxia gang roblox',
            'volt executor roblox', 'seliware roblox', 'valex executor roblox', 'potassium executor roblox'
        ]
        
        for term in search_terms:
            logger.info(f"Buscando: {term}")
            repos = self._search_github_api(term)
            self.results['github_repos'].extend(repos)
            time.sleep(2)
        
        self.results['statistics']['repos_found'] = len(self.results['github_repos'])
        
        duration = time.time() - self.start_time
        self.results['scan_metadata']['duration_seconds'] = round(duration, 2)
        
        logger.info("=" * 70)
        logger.info(f"Repositorios encontrados: {len(self.results['github_repos'])}")
        logger.info("=" * 70)

    def scan_weao_exploits(self):
        logger.info("=" * 70)
        logger.info("MODO: catálogo WEAO de exploits")
        logger.info("=" * 70)
        self.results = {
            'scan_type': 'weao_exploits',
            'scan_metadata': {'timestamp': datetime.now().isoformat()},
            'catalog': [],
            'statistics': {'count': 0}
        }
        endpoints = [
            'https://weao.xyz/api/status/exploits',
            'https://whatexpsare.online/api/status/exploits'
        ]
        for url in endpoints:
            try:
                headers = {'User-Agent': 'WEAO-3PService'}
                r = requests.get(url, headers=headers, timeout=15)
                if r.status_code == 200:
                    data = r.json()
                    items = data if isinstance(data, list) else data.get('data') or data.get('exploits') or []
                    for it in items:
                        name = str(it.get('name') or it.get('exploit') or '').strip()
                        status = str(it.get('status') or it.get('state') or '').strip().lower()
                        discontinued = 'zenith' in name.lower()
                        present = []
                        tokens = [t for t in re.split(r'\W+', name.lower()) if len(t) >= 3]
                        try:
                            for p in psutil.process_iter(['pid', 'name']):
                                n = str(p.info.get('name') or '').lower()
                                if n and any(tok in n for tok in tokens):
                                    present.append({'type': 'process', 'name': p.info.get('name'), 'pid': p.info.get('pid')})
                        except Exception:
                            pass
                        roots = []
                        base = Path.home()
                        roots += [
                            base / 'Downloads',
                            base / 'Desktop',
                            base / 'Documents',
                            base / 'AppData/Local',
                            base / 'AppData/Roaming'
                        ]
                        cap = 200
                        hits = 0
                        for root in roots:
                            try:
                                for rdir, dnames, fnames in os.walk(root):
                                    if hits >= cap:
                                        break
                                    for d in dnames:
                                        dl = d.lower()
                                        if any(tok in dl for tok in tokens):
                                            pth = str(Path(rdir) / d)
                                            present.append({'type': 'folder', 'path': pth})
                                            hits += 1
                                    for fn in fnames:
                                        fl = fn.lower()
                                        if any(tok in fl for tok in tokens):
                                            pth = str(Path(rdir) / fn)
                                            present.append({'type': 'file', 'path': pth})
                                            hits += 1
                                    if hits >= cap:
                                        break
                            except Exception:
                                pass
                        self.results['catalog'].append({'name': name, 'status': status, 'discontinued': discontinued, 'present_on_system': present})
                    break
            except Exception:
                pass
        self.results['statistics']['count'] = len(self.results['catalog'])
        logger.info(f"Catálogo WEAO: {len(self.results['catalog'])}")
    
    def _search_github_api(self, query: str) -> List[Dict[str, Any]]:
        
        repos = []
        
        try:
            url = f'https://api.github.com/search/repositories?q={query}+roblox&per_page=20'
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                for repo in data.get('items', []):
                    repos.append({
                        'name': repo['name'],
                        'full_name': repo['full_name'],
                        'description': repo.get('description', ''),
                        'url': repo['html_url'],
                        'stars': repo['stargazers_count'],
                        'language': repo.get('language', 'Unknown')
                    })
        except Exception as e:
            logger.error(f"Error buscando '{query}': {str(e)}")
        
        return repos

    def scan_vpns(self):
        logger.info("=" * 70)
        logger.info("MODO: DETECCIÓN DE VPN")
        logger.info("=" * 70)

        self.results = {
            'scan_type': 'vpn_detection',
            'scan_metadata': {
                'timestamp': datetime.now().isoformat(),
            },
            'detected_vpns': [],
            'suspicious_interfaces': []
        }

        vpn_processes = [
            'nordvpn', 'expressvpn', 'protonvpn', 'surfshark', 'cyberghost', 
            'hotspotshield', 'mullvad', 'windscribe', 'tunnelbear', 'pia_manager',
            'wireguard', 'openvpn', 'softether'
        ]

        for proc in psutil.process_iter(['pid', 'name']):
            try:
                p_name = proc.info['name'].lower()
                for vpn in vpn_processes:
                    if vpn in p_name:
                        self.results['detected_vpns'].append({
                            'name': proc.info['name'],
                            'pid': proc.info['pid'],
                            'type': 'Process'
                        })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        try:
            stats = psutil.net_if_addrs()
            for nic, addrs in stats.items():
                nic_lower = nic.lower()
                if any(x in nic_lower for x in ['vpn', 'tun', 'tap', 'wireguard']):
                    self.results['suspicious_interfaces'].append({
                        'interface': nic,
                        'addresses': [addr.address for addr in addrs]
                    })
        except Exception as e:
            logger.error(f"Error scanning interfaces: {e}")

        logger.info(f"VPNs detectadas: {len(self.results['detected_vpns'])}")
        logger.info(f"Interfaces sospechosas: {len(self.results['suspicious_interfaces'])}")

    def scan_vpn_registry_services(self):
        logger.info("=" * 70)
        logger.info("MODO: VPN en registro y servicios")
        logger.info("=" * 70)
        self.results = {
            'scan_type': 'vpn_services_registry',
            'scan_metadata': {'timestamp': datetime.now().isoformat()},
            'services': [],
            'installed': []
        }
        names = ['nordvpn', 'expressvpn', 'protonvpn', 'surfshark', 'cyberghost', 'windscribe', 'wireguard', 'openvpn', 'softether', 'pia', 'mullvad']
        if winreg:
            try:
                base = r'SYSTEM\\CurrentControlSet\\Services'
                h = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, base)
                i = 0
                while True:
                    try:
                        svc = winreg.EnumKey(h, i)
                    except OSError:
                        break
                    i += 1
                    if any(x in svc.lower() for x in names):
                        self.results['services'].append({'name': svc})
            except Exception:
                pass
            try:
                for hive in [(winreg.HKEY_CURRENT_USER, 'HKCU'), (winreg.HKEY_LOCAL_MACHINE, 'HKLM')]:
                    base = r'SOFTWARE'
                    h = winreg.OpenKey(hive[0], base)
                    i = 0
                    while True:
                        try:
                            sub = winreg.EnumKey(h, i)
                        except OSError:
                            break
                        i += 1
                        if any(x in sub.lower() for x in names):
                            self.results['installed'].append({'hive': hive[1], 'vendor': sub})
            except Exception:
                pass

    def scan_local_fflags_scripts(self):
        logger.info("=" * 70)
        logger.info("MODO: buscando fflags & scripts")
        logger.info("=" * 70)

        self.results = {
            'scan_type': 'deep_scan',
            'scan_metadata': {'timestamp': datetime.now().isoformat()},
            'fflags_found': [],
            'scripts_found': []
        }

        search_paths = [
            Path.home() / 'AppData' / 'Local' / 'Roblox',
            Path.home() / 'AppData' / 'Local' / 'Bloxstrap',
            Path.home() / 'Downloads',
            Path.home() / 'Desktop'
        ]

        keywords = ['loadstring', 'game:GetService', 'fireclickdetector', 'firetouchinterest', 'hookfunction', 'getrawmetatable']

        for base_path in search_paths:
            if not base_path.exists(): continue
            
            logger.info(f"Explorando: {base_path}")
            try:
                for root, dirs, files in os.walk(base_path):
                    if 'node_modules' in root or '.git' in root: continue

                    for file in files:
                        file_lower = file.lower()
                        full_path = Path(root) / file

                        if file_lower == 'clientappsettings.json':
                            try:
                                with open(full_path, 'r', errors='ignore') as f:
                                    content = json.load(f)
                                    self.results['fflags_found'].append({
                                        'path': str(full_path),
                                        'content': content
                                    })
                            except: pass

                        if file_lower.endswith(('.lua', '.txt', '.luau')):
                            try:
                                if full_path.stat().st_size > 1_000_000: continue
                                
                                with open(full_path, 'r', errors='ignore') as f:
                                    content = f.read()
                                    if any(k in content for k in keywords):
                                        self.results['scripts_found'].append({
                                            'path': str(full_path),
                                            'preview': content[:200]
                                        })
                            except: pass
            except Exception as e:
                logger.error(f"Error en búsqueda profunda: {e}")

        logger.info(f"Archivos FFlag encontrados: {len(self.results['fflags_found'])}")
        logger.info(f"Scripts sospechosos: {len(self.results['scripts_found'])}")

    def scan_system_fflags(self):
        logger.info("=" * 70)
        logger.info("MODO: FFlags en sistema y registro")
        logger.info("=" * 70)
        self.results = {
            'scan_type': 'system_fflags',
            'scan_metadata': {'timestamp': datetime.now().isoformat()},
            'fflags_files': [],
            'registry_matches': []
        }
        targets = [
            'ClientAppSettings.json',
            'GlobalSettings.json',
            'AppSettings.json',
            'Bloxstrap.json'
        ]
        roots = []
        try:
            for part in psutil.disk_partitions(all=False):
                if part.fstype and 'fixed' or True:
                    roots.append(Path(part.mountpoint))
        except Exception:
            roots.append(Path('C:/'))
        homes = [Path.home(), Path(os.path.expanduser('~'))]
        for h in homes:
            for p in ['AppData/Local/Roblox', 'AppData/Local/Bloxstrap', 'AppData/LocalLow/Roblox']:
                roots.append(h / p)
            roots.append(h / 'AppData/Local/Roblox/Versions')
        seen = set()
        for root in roots:
            try:
                for name in targets:
                    for found in root.glob(f'**/{name}'):
                        k = str(found).lower()
                        if k in seen:
                            continue
                        seen.add(k)
                        try:
                            with open(found, 'r', errors='ignore') as f:
                                data = json.load(f)
                            self.results['fflags_files'].append({'path': str(found), 'count': len(data), 'keys': [k for k in data.keys() if any(x in k for x in ['FFlag', 'DFFlag', 'FInt', 'DFInt', 'FString', 'DFString'])]})
                        except Exception:
                            pass
            except Exception:
                pass
        try:
            versions = Path.home() / 'AppData/Local/Roblox/Versions'
            for v in versions.glob('*/ClientSettings/ClientAppSettings.json'):
                try:
                    with open(v, 'r', errors='ignore') as f:
                        data = json.load(f)
                    self.results['fflags_files'].append({'path': str(v), 'count': len(data), 'keys': [k for k in data.keys() if any(x in k for x in ['FFlag', 'DFFlag', 'FInt', 'DFInt', 'FString', 'DFString'])]})
                except Exception:
                    pass
        except Exception:
            pass
        if winreg:
            try:
                for hive in [(winreg.HKEY_CURRENT_USER, 'HKCU'), (winreg.HKEY_LOCAL_MACHINE, 'HKLM')]:
                    for base in [r'SOFTWARE', r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', r'SOFTWARE\Bloxstrap', r'SOFTWARE\Roblox']:
                        try:
                            h = winreg.OpenKey(hive[0], base)
                            i = 0
                            while True:
                                try:
                                    subname = winreg.EnumKey(h, i)
                                except OSError:
                                    break
                                i += 1
                                try:
                                    subkey = winreg.OpenKey(hive[0], base + '\\' + subname)
                                    j = 0
                                    while True:
                                        try:
                                            value = winreg.EnumValue(subkey, j)
                                        except OSError:
                                            break
                                        j += 1
                                        vname = str(value[0])
                                        vdata = str(value[1])
                                        if any(x in vname for x in ['FFlag', 'DFFlag', 'FInt', 'DFInt', 'FString', 'DFString']) or any(x in vdata for x in ['FFlag', 'DFFlag', 'FInt', 'DFInt', 'FString', 'DFString']):
                                            self.results['registry_matches'].append({'hive': hive[1], 'path': base + '\\' + subname, 'name': vname, 'value': vdata})
                                except Exception:
                                    pass
                        except Exception:
                            pass
            except Exception as e:
                logger.error(f"Error leyendo registro: {e}")
        logger.info(f"FFlags archivos: {len(self.results['fflags_files'])}")
        logger.info(f"FFlags en registro: {len(self.results['registry_matches'])}")

    def scan_fflags_from_txt(self, path: str = 'fflags_targets.txt'):
        logger.info("=" * 70)
        logger.info("MODO: FFlags desde archivo de objetivos")
        logger.info("=" * 70)
        self.results = {
            'scan_type': 'fflags_targets',
            'scan_metadata': {'timestamp': datetime.now().isoformat(), 'source_file': path},
            'targets': [],
            'matches': []
        }
        targets = []
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    s = line.strip()
                    if not s or s.startswith('#'):
                        continue
                    targets.append(s)
        except Exception as e:
            logger.error(f"No se pudo leer {path}: {e}")
        self.results['targets'] = targets
        if not targets:
            return
        def has_target(s: str) -> bool:
            low = s.lower()
            return any(t.lower() in low for t in targets)
        homes = [Path.home(), Path(os.path.expanduser('~'))]
        search_dirs = []
        for h in homes:
            search_dirs += [
                h / 'AppData/Local/Roblox',
                h / 'AppData/Local/Bloxstrap',
                h / 'AppData/LocalLow/Roblox',
                h / 'AppData/Local/Roblox/Versions'
            ]
        for base in search_dirs:
            try:
                for p in base.glob('**/*.json'):
                    try:
                        if p.stat().st_size > 2_000_000:
                            continue
                        with open(p, 'r', errors='ignore') as f:
                            data = json.load(f)
                        if isinstance(data, dict):
                            for k, v in data.items():
                                s = str(k)
                                if has_target(s):
                                    self.results['matches'].append({'type': 'file', 'path': str(p), 'key': k, 'value': v})
                    except Exception:
                        pass
            except Exception:
                pass
        if winreg:
            try:
                for hive in [(winreg.HKEY_CURRENT_USER, 'HKCU'), (winreg.HKEY_LOCAL_MACHINE, 'HKLM')]:
                    base = r'SOFTWARE'
                    h = winreg.OpenKey(hive[0], base)
                    i = 0
                    while True:
                        try:
                            sub = winreg.EnumKey(h, i)
                        except OSError:
                            break
                        i += 1
                        try:
                            k = winreg.OpenKey(hive[0], base + '\\' + sub)
                            j = 0
                            while True:
                                try:
                                    val = winreg.EnumValue(k, j)
                                except OSError:
                                    break
                                j += 1
                                n = str(val[0])
                                d = str(val[1])
                                if has_target(n) or has_target(d):
                                    self.results['matches'].append({'type': 'registry', 'hive': hive[1], 'path': base + '\\' + sub, 'name': n, 'value': d})
                        except Exception:
                            pass
            except Exception as e:
                logger.error(f"Error leyendo registro: {e}")
        logger.info(f"Objetivos: {len(self.results['targets'])}")
        logger.info(f"Coincidencias: {len(self.results['matches'])}")

    def scan_registry_exploits(self):
        logger.info("=" * 70)
        logger.info("MODO: exploits en el registro")
        logger.info("=" * 70)
        self.results = {
            'scan_type': 'registry_exploits',
            'scan_metadata': {'timestamp': datetime.now().isoformat()},
            'matches': []
        }
        keywords = set()
        for name in self.exploit_signatures.keys():
            keywords.add(name.lower())
        extras = ['executor', 'roblox exploit', 'bloxstrap']
        for e in extras:
            keywords.add(e)
        if not winreg:
            return
        try:
            for hive in [(winreg.HKEY_CURRENT_USER, 'HKCU'), (winreg.HKEY_LOCAL_MACHINE, 'HKLM')]:
                base = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'
                try:
                    h = winreg.OpenKey(hive[0], base)
                    i = 0
                    while True:
                        try:
                            sub = winreg.EnumKey(h, i)
                        except OSError:
                            break
                        i += 1
                        try:
                            k = winreg.OpenKey(hive[0], base + '\\' + sub)
                            name = ''
                            icon = ''
                            loc = ''
                            pub = ''
                            try:
                                name = str(winreg.QueryValueEx(k, 'DisplayName')[0])
                            except Exception:
                                pass
                            try:
                                icon = str(winreg.QueryValueEx(k, 'DisplayIcon')[0])
                            except Exception:
                                pass
                            try:
                                loc = str(winreg.QueryValueEx(k, 'InstallLocation')[0])
                            except Exception:
                                pass
                            try:
                                pub = str(winreg.QueryValueEx(k, 'Publisher')[0])
                            except Exception:
                                pass
                            line = ' '.join([name, icon, loc, pub]).lower()
                            if any(kw in line for kw in keywords):
                                self.results['matches'].append({'hive': hive[1], 'path': base + '\\' + sub, 'name': name, 'icon': icon, 'location': loc, 'publisher': pub})
                        except Exception:
                            pass
                except Exception:
                    pass
                for runkey in [r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', r'SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce']:
                    try:
                        k = winreg.OpenKey(hive[0], runkey)
                        j = 0
                        while True:
                            try:
                                val = winreg.EnumValue(k, j)
                            except OSError:
                                break
                            j += 1
                            nm = str(val[0])
                            data = str(val[1])
                            line = (nm + ' ' + data).lower()
                            if any(kw in line for kw in keywords):
                                self.results['matches'].append({'hive': hive[1], 'path': runkey, 'name': nm, 'value': data})
                    except Exception:
                        pass
                try:
                    compkey = r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Compatibility Assistant\Store'
                    k = winreg.OpenKey(hive[0], compkey)
                    i = 0
                    while True:
                        try:
                            val = winreg.EnumValue(k, i)
                        except OSError:
                            break
                        i += 1
                        path = str(val[0]).lower()
                        data = str(val[1])
                        if any(kw in path for kw in keywords):
                            self.results['matches'].append({'hive': hive[1], 'path': compkey, 'recent_exec': path, 'data': data})
                except Exception:
                    pass
        except Exception as e:
            logger.error(f"Error registro exploits: {e}")

    def scan_kernel_drivers(self):
        logger.info("=" * 70)
        logger.info("MODO: drivers del kernel y servicios")
        logger.info("=" * 70)
        self.results = {
            'scan_type': 'kernel_drivers',
            'scan_metadata': {'timestamp': datetime.now().isoformat()},
            'drivers': [],
            'suspicious': []
        }
        names = ['kdmapper', 'blackbone', 'hyperion', 'winring0', 'capcom', 'rtcore64', 'iqvw64e', 'secdrv', 'easyanticheat']
        try:
            p = subprocess.run(['sc', 'query', 'type=', 'driver'], capture_output=True, text=True)
            out = p.stdout
            for block in out.split('\n\n'):
                m = re.search(r'SERVICE_NAME:\s*(.+)', block)
                if not m:
                    continue
                name = m.group(1).strip()
                self.results['drivers'].append({'name': name})
                if any(x in name.lower() for x in names):
                    self.results['suspicious'].append({'name': name})
        except Exception as e:
            logger.error(f"Error consultando sc: {e}")
        if winreg:
            try:
                base = r'SYSTEM\\CurrentControlSet\\Services'
                h = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, base)
                i = 0
                while True:
                    try:
                        svc = winreg.EnumKey(h, i)
                    except OSError:
                        break
                    i += 1
                    try:
                        k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, base + '\\' + svc)
                        path = ''
                        try:
                            path = winreg.QueryValueEx(k, 'ImagePath')[0]
                        except Exception:
                            pass
                        if path:
                            if any(x in svc.lower() for x in names):
                                self.results['suspicious'].append({'name': svc, 'path': path})
                    except Exception:
                        pass
            except Exception as e:
                logger.error(f"Error leyendo servicios: {e}")
        logger.info(f"Drivers: {len(self.results['drivers'])}")
        logger.info(f"Sospechosos: {len(self.results['suspicious'])}")

    def scan_open_ports(self):
        logger.info("=" * 70)
        logger.info("MODO: puertos abiertos")
        logger.info("=" * 70)
        self.results = {
            'scan_type': 'open_ports',
            'scan_metadata': {'timestamp': datetime.now().isoformat()},
            'ports': []
        }
        pid_map = {}
        try:
            for p in psutil.process_iter(['pid', 'name']):
                pid_map[p.info['pid']] = p.info['name']
        except Exception:
            pass
        try:
            p = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
            for line in p.stdout.splitlines():
                if 'TCP' in line or 'UDP' in line:
                    parts = re.split(r'\s+', line.strip())
                    if len(parts) >= 5:
                        proto = parts[0]
                        local = parts[1]
                        foreign = parts[2]
                        state = parts[3] if proto == 'TCP' else 'UDP'
                        pid = int(parts[4]) if parts[4].isdigit() else None
                        name = pid_map.get(pid)
                        self.results['ports'].append({'proto': proto, 'local': local, 'foreign': foreign, 'state': state, 'pid': pid, 'process': name})
        except Exception as e:
            logger.error(f"Error leyendo netstat: {e}")
        logger.info(f"Puertos: {len(self.results['ports'])}")

    def scan_open_ports_psutil(self):
        logger.info("=" * 70)
        logger.info("MODO: puertos abiertos (psutil)")
        logger.info("=" * 70)
        self.results = {
            'scan_type': 'open_ports_psutil',
            'scan_metadata': {'timestamp': datetime.now().isoformat()},
            'ports': []
        }
        try:
            conns = psutil.net_connections(kind='inet')
            for c in conns:
                laddr = f"{c.laddr.ip}:{c.laddr.port}" if c.laddr else ''
                raddr = f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else ''
                pid = c.pid
                name = None
                try:
                    if pid:
                        p = psutil.Process(pid)
                        name = p.name()
                except Exception:
                    pass
                self.results['ports'].append({'proto': 'TCP' if c.type == psutil.SOCK_STREAM else 'UDP', 'local': laddr, 'foreign': raddr, 'state': str(c.status), 'pid': pid, 'process': name})
        except Exception as e:
            logger.error(f"Error psutil conexiones: {e}")
        logger.info(f"Puertos: {len(self.results['ports'])}")

    def scan_logs(self):
        logger.info("=" * 70)
        logger.info("MODO: logs de Roblox/Bloxstrap/launchers")
        logger.info("=" * 70)
        self.results = {
            'scan_type': 'logs_scan',
            'scan_metadata': {'timestamp': datetime.now().isoformat()},
            'logs': []
        }
        candidates = []
        base = Path.home()
        candidates += [
            base / 'AppData/Local/Roblox/logs',
            base / 'AppData/Local/Bloxstrap/logs',
            base / 'AppData/LocalLow/Roblox/logs',
            base / 'AppData/Roaming/Roblox',
            base / 'AppData/Roaming/Bloxstrap'
        ]
        for c in candidates:
            try:
                for f in c.glob('**/*'):
                    if f.is_file() and f.suffix.lower() in {'.log', '.txt'}:
                        try:
                            with open(f, 'r', errors='ignore') as fh:
                                head = fh.read(5000)
                            if any(x in head.lower() for x in ['voidtrap', 'voidstrap', 'bloxstrap', 'executor', 'fflag', 'hookfunction']):
                                self.results['logs'].append({'path': str(f), 'preview': head[:200]})
                        except Exception:
                            pass
            except Exception:
                pass
        logger.info(f"Logs relevantes: {len(self.results['logs'])}")

    def scan_suspicious_processes(self):
        logger.info("=" * 70)
        logger.info("MODO: procesos sospechosos de exploits")
        logger.info("=" * 70)
        self.results = {
            'scan_type': 'suspicious_processes',
            'scan_metadata': {'timestamp': datetime.now().isoformat()},
            'processes': []
        }
        keywords = set()
        for name, sig in self.exploit_signatures.items():
            keywords.add(name.lower())
            for p in sig.get('processes', []):
                keywords.add(Path(p).stem.lower())
        extras = ['executor', 'injector', 'roblox']
        for e in extras:
            keywords.add(e)
        for proc in psutil.process_iter(['pid','name','exe','ppid','create_time']):
            try:
                pname = str(proc.info.get('name') or '').lower()
                pexe = str(proc.info.get('exe') or '').lower()
                match = any(k in pname or (pexe and k in pexe) for k in keywords)
                modules = []
                try:
                    for m in proc.memory_maps():
                        ml = str(getattr(m, 'path', '')).lower()
                        if any(k in ml for k in keywords):
                            modules.append(ml)
                except Exception:
                    pass
                if match or modules:
                    item = {
                        'pid': proc.info.get('pid'),
                        'name': proc.info.get('name'),
                        'exe': proc.info.get('exe'),
                        'ppid': proc.info.get('ppid'),
                        'create_time': proc.info.get('create_time'),
                        'modules': modules[:20]
                    }
                    self.results['processes'].append(item)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        logger.info(f"Procesos sospechosos: {len(self.results['processes'])}")

    def scan_last_play_roblox(self):
        logger.info("=" * 70)
        logger.info("MODO: última vez jugado Roblox")
        logger.info("=" * 70)
        self.results = {
            'scan_type': 'roblox_last_play',
            'scan_metadata': {'timestamp': datetime.now().isoformat()},
            'last_seen': {
                'logs': None,
                'prefetch': None
            }
        }
        base = Path.home()
        log_dirs = [
            base / 'AppData/Local/Roblox/logs',
            base / 'AppData/LocalLow/Roblox/logs'
        ]
        latest = None
        try:
            for d in log_dirs:
                for f in d.glob('**/*'):
                    if f.is_file() and f.suffix.lower() in {'.log','.txt'}:
                        mt = f.stat().st_mtime
                        if not latest or mt > latest:
                            latest = mt
        except Exception:
            pass
        if latest:
            self.results['last_seen']['logs'] = datetime.fromtimestamp(latest).isoformat()
        try:
            pf_dir = Path('C:/Windows/Prefetch')
            if pf_dir.exists():
                pf_latest = None
                for pf in pf_dir.glob('ROBLOXPLAYERBETA.EXE-*.pf'):
                    mt = pf.stat().st_mtime
                    if not pf_latest or mt > pf_latest:
                        pf_latest = mt
                if pf_latest:
                    self.results['last_seen']['prefetch'] = datetime.fromtimestamp(pf_latest).isoformat()
        except Exception:
            pass
        logger.info(f"Última vez (logs): {self.results['last_seen']['logs']}")
        logger.info(f"Última vez (prefetch): {self.results['last_seen']['prefetch']}")

    def scan_prefetch_executions(self):
        logger.info("=" * 70)
        logger.info("MODO: últimas ejecuciones (Prefetch)")
        logger.info("=" * 70)
        self.results = {
            'scan_type': 'prefetch_executions',
            'scan_metadata': {'timestamp': datetime.now().isoformat()},
            'executions': []
        }
        keywords = set()
        for name, sig in self.exploit_signatures.items():
            keywords.add(name.lower())
            for p in sig.get('processes', []):
                keywords.add(Path(p).stem.lower())
        keywords.add('robloxplayerbeta')
        try:
            pf_dir = Path('C:/Windows/Prefetch')
            if pf_dir.exists():
                for pf in pf_dir.glob('*.pf'):
                    nm = pf.name.lower()
                    if any(k in nm for k in keywords):
                        self.results['executions'].append({'file': pf.name, 'path': str(pf), 'timestamp': datetime.fromtimestamp(pf.stat().st_mtime).isoformat()})
        except Exception as e:
            logger.error(f"Prefetch error: {e}")
        logger.info(f"Prefetch coincidencias: {len(self.results['executions'])}")

    def scan_loose_dlls(self):
        logger.info("=" * 70)
        logger.info("MODO: DLLs sueltas de posibles scripts")
        logger.info("=" * 70)
        self.results = {
            'scan_type': 'loose_dlls',
            'scan_metadata': {'timestamp': datetime.now().isoformat()},
            'dlls': []
        }
        suspicious = {'sxlib.dll','inject.dll','hook.dll','krnl.dll','synapse.dll','fluxus.dll'}
        roots = []
        base = Path.home()
        roots += [
            base / 'Downloads',
            base / 'Desktop',
            base / 'Documents',
            base / 'AppData/Local',
            base / 'AppData/Roaming',
            base / 'AppData/Local/Temp'
        ]
        cap = 2000
        hits = 0
        for root in roots:
            try:
                for r, d, files in os.walk(root):
                    for fn in files:
                        fl = fn.lower()
                        if fl.endswith('.dll') and (fl in suspicious or any(x in fl for x in ['inject','hook','roblox','executor','synapse','krnl','fluxus'])):
                            p = Path(r)/fn
                            self.results['dlls'].append({'path': str(p), 'modified': datetime.fromtimestamp(p.stat().st_mtime).isoformat()})
                            hits += 1
                            if hits >= cap:
                                break
                    if hits >= cap:
                        break
            except Exception:
                pass
        logger.info(f"DLLs sospechosas: {len(self.results['dlls'])}")

    def scan_deleted_files_list(self):
        logger.info("=" * 70)
        logger.info("MODO: listar archivos borrados (Papelera)")
        logger.info("=" * 70)
        self.results = {
            'scan_type': 'deleted_files',
            'scan_metadata': {'timestamp': datetime.now().isoformat()},
            'deleted': []
        }
        try:
            import winshell
            bin = winshell.recycle_bin()
            for item in bin:
                orig = getattr(item, 'original_filename', None) or ''
                dt = getattr(item, 'deletion_date', None)
                if orig:
                    self.results['deleted'].append({'path': orig, 'deleted_at': str(dt) if dt else None})
        except Exception as e:
            logger.error(f"No se pudo listar Papelera: {e}")
        logger.info(f"Borrados: {len(self.results['deleted'])}")

    def scan_recent_closed_processes(self):
        logger.info("=" * 70)
        logger.info("MODO: procesos cerrados recientemente")
        logger.info("=" * 70)
        self.results = {
            'scan_type': 'recent_closed_processes',
            'scan_metadata': {'timestamp': datetime.now().isoformat()},
            'events': []
        }
        keywords = set()
        for name, sig in self.exploit_signatures.items():
            keywords.add(name.lower())
            for p in sig.get('processes', []):
                keywords.add(Path(p).stem.lower())
        try:
            p = subprocess.run(['wevtutil', 'qe', 'Security', '/q:*[System[(EventID=4689)]]', '/f:xml', '/c:200'], capture_output=True, text=True)
            xml = p.stdout
            for m in re.finditer(r'<Event>[\s\S]*?<EventData>[\s\S]*?</EventData>[\s\S]*?</Event>', xml):
                block = m.group(0)
                proc = ''
                pid = ''
                tstamp = ''
                mt = re.search(r'<TimeCreated SystemTime="([^"]+)"', block)
                if mt:
                    tstamp = mt.group(1)
                md = re.findall(r'<Data Name="([^"]+)">([\s\S]*?)</Data>', block)
                data = {k:v for k,v in md}
                proc = data.get('ProcessName') or data.get('NewProcessName') or ''
                pid = data.get('TargetProcessId') or data.get('ProcessId') or ''
                s = (proc or '').lower()
                if s and any(k in s for k in keywords):
                    self.results['events'].append({'process': proc, 'pid': pid, 'time': tstamp})
        except Exception:
            pass
        logger.info(f"Eventos 4689: {len(self.results['events'])}")

    def scan_hidden_processes(self):
        logger.info("=" * 70)
        logger.info("MODO: procesos escondidos")
        logger.info("=" * 70)
        self.results = {
            'scan_type': 'hidden_processes',
            'scan_metadata': {'timestamp': datetime.now().isoformat()},
            'suspects': []
        }
        ps_names = set()
        for p in psutil.process_iter(['name']):
            try:
                n = str(p.info.get('name') or '').lower()
                if n:
                    ps_names.add(n)
            except Exception:
                pass
        tasklist = []
        try:
            t = subprocess.run(['tasklist', '/FO', 'CSV'], capture_output=True, text=True)
            for line in t.stdout.splitlines()[1:]:
                parts = [x.strip('"') for x in line.split(',')]
                if len(parts) >= 2:
                    tasklist.append({'name': parts[0].lower(), 'pid': parts[1]})
        except Exception:
            pass
        keywords = set()
        for name, sig in self.exploit_signatures.items():
            keywords.add(name.lower())
            for p in sig.get('processes', []):
                keywords.add(Path(p).stem.lower())
        for it in tasklist:
            n = it['name']
            if any(k in n for k in keywords) and n not in ps_names:
                self.results['suspects'].append({'name': it['name'], 'pid': it['pid']})
        logger.info(f"Escondidos detectados: {len(self.results['suspects'])}")

    def scan_fflags_all_users(self):
        logger.info("=" * 70)
        logger.info("MODO: FFlags en todos los usuarios")
        logger.info("=" * 70)
        self.results = {
            'scan_type': 'fflags_all_users',
            'scan_metadata': {'timestamp': datetime.now().isoformat()},
            'matches': []
        }
        try:
            users_root = Path('C:/Users')
            for u in users_root.glob('*'):
                base = u / 'AppData/Local/Roblox/Versions'
                for ver in base.glob('*'):
                    p = ver / 'ClientSettings/ClientAppSettings.json'
                    if p.exists():
                        try:
                            with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                                txt = f.read()
                            for m in re.finditer(r'"(FFlag|DFFlag|FInt|DFInt|FString|DFString)[^"]*"\s*:\s*([^,\n]+)', txt):
                                self.results['matches'].append({'user': u.name, 'path': str(p), 'raw': m.group(0)})
                        except Exception:
                            pass
        except Exception:
            pass
        logger.info(f"FFlags por usuarios: {len(self.results['matches'])}")

    def scan_registry_mui_recent(self):
        logger.info("=" * 70)
        logger.info("MODO: MUICache recientes")
        logger.info("=" * 70)
        self.results = {
            'scan_type': 'mui_recent',
            'scan_metadata': {'timestamp': datetime.now().isoformat()},
            'entries': []
        }
        if not winreg:
            return
        keys = [
            (winreg.HKEY_CURRENT_USER, r'SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\Shell\MuiCache'),
            (winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\ShellNoRoam\MuiCache')
        ]
        keywords = set()
        for name, sig in self.exploit_signatures.items():
            keywords.add(name.lower())
            for p in sig.get('processes', []):
                keywords.add(Path(p).stem.lower())
        try:
            for hive, key in keys:
                try:
                    k = winreg.OpenKey(hive, key)
                    i = 0
                    while True:
                        try:
                            val = winreg.EnumValue(k, i)
                        except OSError:
                            break
                        i += 1
                        nm = str(val[0]).lower()
                        data = str(val[1]).lower()
                        if any(kw in nm or kw in data for kw in keywords):
                            self.results['entries'].append({'path': key, 'name': nm, 'value': data})
                except Exception:
                    pass
        except Exception:
            pass
        logger.info(f"MUICache coinc: {len(self.results['entries'])}")

    def scan_recent_shortcuts(self):
        logger.info("=" * 70)
        logger.info("MODO: accesos directos recientes")
        logger.info("=" * 70)
        self.results = {
            'scan_type': 'recent_shortcuts',
            'scan_metadata': {'timestamp': datetime.now().isoformat()},
            'shortcuts': []
        }
        keywords = set()
        for name, sig in self.exploit_signatures.items():
            keywords.add(name.lower())
            for p in sig.get('processes', []):
                keywords.add(Path(p).stem.lower())
        base = Path.home() / 'AppData/Roaming/Microsoft/Windows/Recent'
        try:
            for f in base.glob('*.lnk'):
                nm = f.name.lower()
                if any(kw in nm for kw in keywords):
                    self.results['shortcuts'].append({'file': f.name, 'path': str(f), 'modified': datetime.fromtimestamp(f.stat().st_mtime).isoformat()})
        except Exception:
            pass
        logger.info(f"Accesos directos: {len(self.results['shortcuts'])}")

    def send_webhook_report(self, url: Optional[str] = None, report_file: Optional[str] = None):
        data = getattr(self, 'results', {})
        if not url:
            url = os.getenv('SCANNER_WEBHOOK_URL', '').strip()
            if not url:
                try:
                    with open('reportes/webhook.txt', 'r') as f:
                        url = f.read().strip()
                except Exception:
                    url = ''
        if not url:
            return False
        if not report_file:
            report_file = 'informes/reporte_completo.json'
        try:
            is_discord = 'discord.com/api/webhooks' in url or 'discordapp.com/api/webhooks' in url
            if is_discord:
                content = 'Roblox Scanner — ' + str(data.get('scan_type') or 'reporte')
                payload = {'content': content}
                files = None
                try:
                    if Path(report_file).exists():
                        files = {'file': ('reporte_completo.json', open(report_file, 'rb'), 'application/json')}
                except Exception:
                    files = None
                if files:
                    r = requests.post(url, data={'payload_json': json.dumps(payload)}, files=files, timeout=15)
                else:
                    r = requests.post(url, json=payload, timeout=10)
                return r.status_code in (200, 204)
            else:
                r = requests.post(url, json=data, timeout=15)
                return r.status_code in (200, 204)
        except Exception:
            return False

    def restore_deleted_files(self):
        logger.info("=" * 70)
        logger.info("MODO: restaurar archivos borrados")
        logger.info("=" * 70)
        self.results = {
            'scan_type': 'restore_deleted',
            'scan_metadata': {'timestamp': datetime.now().isoformat()},
            'restored': [],
            'failed': []
        }
        ok = False
        try:
            import winshell
            bin = winshell.recycle_bin()
            for item in bin:
                try:
                    orig = getattr(item, 'original_filename', None) or ''
                    if orig:
                        item.restore()
                        self.results['restored'].append({'path': orig})
                        ok = True
                except Exception as e:
                    self.results['failed'].append({'error': str(e)})
        except Exception as e:
            logger.error(f"No se pudo usar winshell: {e}")
        logger.info(f"Restaurados: {len(self.results['restored'])}")
        return ok

    def scan_browser_history(self):
        logger.info("=" * 70)
        logger.info("MODO: analizando el navegador :V")
        logger.info("=" * 70)

        self.results = {
            'scan_type': 'browser_history',
            'scan_metadata': {'timestamp': datetime.now().isoformat()},
            'history_matches': []
        }

        browsers = {
            'Chrome': Path.home() / 'AppData/Local/Google/Chrome/User Data/Default/History',
            'ChromeCanary': Path.home() / 'AppData/Local/Google/Chrome SxS/User Data/Default/History',
            'Edge': Path.home() / 'AppData/Local/Microsoft/Edge/User Data/Default/History',
            'EdgeBeta': Path.home() / 'AppData/Local/Microsoft/Edge Beta/User Data/Default/History',
            'Brave': Path.home() / 'AppData/Local/BraveSoftware/Brave-Browser/User Data/Default/History',
            'Vivaldi': Path.home() / 'AppData/Local/Vivaldi/User Data/Default/History',
            'Opera': Path.home() / 'AppData/Roaming/Opera Software/Opera Stable/History',
            'OperaGX': Path.home() / 'AppData/Roaming/Opera Software/Opera GX Stable/History',
            'Firefox': Path.home() / 'AppData/Roaming/Mozilla/Firefox/Profiles'
        }

        search_terms = [
            'roblox', 'script', 'exploit', 'executor', 'fflag', 'bypass', 
            'synapse', 'krnl', 'fluxus', 'wave', 'hydrogen', 'delta', 'codex'
        ]

        temp_dir = tempfile.mkdtemp()

        try:
            for browser, path in browsers.items():
                db_path = path
                
                if browser == 'Firefox':
                    profiles = list(path.glob('*.default-release'))
                    if profiles:
                        db_path = profiles[0] / 'places.sqlite'
                    else:
                        continue

                if not db_path.exists(): continue

                try:
                    temp_db = Path(temp_dir) / f"{browser}_History"
                    shutil.copy2(db_path, temp_db)

                    conn = sqlite3.connect(str(temp_db))
                    cursor = conn.cursor()

                    query = ""
                    if browser == 'Firefox':
                        query = "SELECT url, title, last_visit_date FROM moz_places WHERE " + \
                                " OR ".join([f"url LIKE '%{t}%' OR title LIKE '%{t}%'" for t in search_terms])
                    else:
                        query = "SELECT url, title, last_visit_time FROM urls WHERE " + \
                                " OR ".join([f"url LIKE '%{t}%' OR title LIKE '%{t}%'" for t in search_terms])

                    cursor.execute(query)
                    
                    for row in cursor.fetchall():
                        self.results['history_matches'].append({
                            'browser': browser,
                            'url': row[0],
                            'title': row[1],
                            'timestamp': row[2]
                        })
                    
                    conn.close()
                except Exception as e:
                    logger.error(f"Error leyendo historial de {browser}: {e}")

        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

        logger.info(f"Coincidencias en historial: {len(self.results['history_matches'])}")

    def scan_browser_cookies(self):
        logger.info("=" * 70)
        logger.info("MODO: analizando cookies de navegadores")
        logger.info("=" * 70)
        self.results = {
            'scan_type': 'browser_cookies',
            'scan_metadata': {'timestamp': datetime.now().isoformat()},
            'cookies_matches': []
        }
        terms = ['roblox', 'executor', 'fflag', 'bloxstrap', 'voidtrap', 'voidstrap', 'krnl', 'synapse', 'fluxus', 'weao']
        chromium_profiles = [
            ('Chrome', Path.home() / 'AppData/Local/Google/Chrome/User Data'),
            ('ChromeCanary', Path.home() / 'AppData/Local/Google/Chrome SxS/User Data'),
            ('Edge', Path.home() / 'AppData/Local/Microsoft/Edge/User Data'),
            ('Brave', Path.home() / 'AppData/Local/BraveSoftware/Brave-Browser/User Data'),
            ('Vivaldi', Path.home() / 'AppData/Local/Vivaldi/User Data'),
            ('Opera', Path.home() / 'AppData/Roaming/Opera Software')
        ]
        temp_dir = tempfile.mkdtemp()
        try:
            for name, base in chromium_profiles:
                if not base.exists():
                    continue
                try:
                    for cookies_path in list(base.glob('**/Cookies')) + list(base.glob('**/Network/Cookies')):
                        if not cookies_path.exists():
                            continue
                        try:
                            temp_db = Path(temp_dir) / f"{name}_Cookies"
                            shutil.copy2(cookies_path, temp_db)
                            conn = sqlite3.connect(str(temp_db))
                            cur = conn.cursor()
                            try:
                                cur.execute("SELECT host_key, name FROM cookies")
                                rows = cur.fetchall()
                                for host, cname in rows:
                                    s1 = str(host).lower()
                                    s2 = str(cname).lower()
                                    if any(t in s1 or t in s2 for t in terms):
                                        self.results['cookies_matches'].append({'browser': name, 'path': str(cookies_path), 'host': host, 'name': cname})
                            finally:
                                conn.close()
                        except Exception:
                            pass
                except Exception:
                    pass
            ff_profiles_dir = Path.home() / 'AppData/Roaming/Mozilla/Firefox/Profiles'
            try:
                for prof in ff_profiles_dir.glob('*.default-release'):
                    db = prof / 'cookies.sqlite'
                    if not db.exists():
                        continue
                    try:
                        temp_db = Path(temp_dir) / f"Firefox_Cookies"
                        shutil.copy2(db, temp_db)
                        conn = sqlite3.connect(str(temp_db))
                        cur = conn.cursor()
                        cur.execute("SELECT host, name, value FROM moz_cookies")
                        for host, name, val in cur.fetchall():
                            s = ' '.join([str(host), str(name), str(val)]).lower()
                            if any(t in s for t in terms):
                                self.results['cookies_matches'].append({'browser': 'Firefox', 'path': str(db), 'host': host, 'name': name})
                        conn.close()
                    except Exception:
                        pass
            except Exception:
                pass
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
        logger.info(f"Coincidencias en cookies: {len(self.results['cookies_matches'])}")
    
    def save_report(self, filename: str = 'informes/reporte_completo.json'):
        
        try:
            output_path = Path(filename)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Reporte guardado en: {output_path.absolute()}")
            return str(output_path.absolute())
        
        except Exception as e:
            logger.error(f"Error guardando reporte: {str(e)}")
            return None


def main():
    
    def _render_menu():
        os.system('cls' if os.name == 'nt' else 'clear')
        print("".ljust(70,'='))
        print(" ROBLOX SECURITY SCANNER ".center(70))
        print("".ljust(70,'='))
        print("  1  Detección Local         - Exploits instalados y procesos")
        print("  2  FFlags Completo         - GitHub, Sistema y Targets")
        print("  3  Exploits (GitHub)       - Repos y términos")
        print("  4  Escaneo Completo        - Todo en uno")
        print("  5  Cookies Navegadores     - Perfiles Chromium/Firefox")
        print("  6  FFlags desde archivo    - fflags_targets.txt")
        print("  7  Catálogo WEAO           - Estado y presencia local")
        print("  8  VPNs (procesos)         - Procesos y NIC sospechosas")
        print("  9  VPNs (servicios)        - Servicios y registro")
        print(" 10  Puertos (netstat)       - Mapeo de procesos")
        print(" 11  Puertos (psutil)        - Conexiones y estados")
        print(" 12  Kernel/Servicios        - Drivers y servicios")
        print(" 13  Búsqueda profunda       - Scripts/FFlags locales")
        print(" 14  Historial Navegadores   - URLs con términos")
        print(" 15  Exploits en sistema     - Rutas objetivo")
        print(" 16  Exploits en registro    - Claves y valores")
        print(" 17  Inicio/Tareas           - Persistencia")
        print(" 18  Módulos de procesos     - DLLs cargadas")
        print(" 19  Procesos sospechosos    - Ejecutores y módulos")
        print(" 20  Última vez Roblox       - Logs y Prefetch")
        print(" 21  Prefetch ejecuciones    - Ejecutores/Roblox")
        print(" 22  DLLs sueltas            - Hooks e injectors")
        print(" 23  Listar papelera         - Archivos borrados")
        print(" 24  Procesos cerrados       - Eventos 4689 Security")
        print(" 25  Procesos escondidos     - Tasklist vs psutil")
        print(" 26  FFlags todos usuarios   - ClientSettings.json")
        print(" 27  MUICache recientes      - Ejecutores")
        print(" 28  Accesos directos        - .lnk sospechosos")
        print("  0  Salir")
        print("".ljust(70,'='))
    
    while True:
        _render_menu()
        choice = input("\nOpción [4]: ").strip() or "4"
        scanner = RobloxScanner()
        try:
            if choice == "1":
                scanner.scan_local_exploits()
            elif choice == "2":
                scanner.scan_fflags_all()
            elif choice == "3":
                scanner.scan_github_exploits()
            elif choice == "4":
                print("\n[1/6] Ejecutando detección local...")
                scanner.scan_local_exploits()
                local_results = scanner.results.copy()
                
                print("\n[2/6] Ejecutando búsqueda de FFlags...")
                scanner = RobloxScanner()
                scanner.scan_fflags()
                fflag_results = scanner.results.copy()
                
                print("\n[3/8] Ejecutando búsqueda de exploits..")
                scanner = RobloxScanner()
                scanner.scan_github_exploits()
                github_results = scanner.results.copy()
                
                print("\n[4/8] Catálogo WEAO de exploits...")
                scanner = RobloxScanner()
                scanner.scan_weao_exploits()
                weao_results = scanner.results.copy()

                print("\n[5/8] Buscando VPNs...")
                scanner = RobloxScanner()
                scanner.scan_vpns()
                vpn_results = scanner.results.copy()

                print("\n[6/8] Búsqueda profunda de archivos...")
                scanner = RobloxScanner()
                scanner.scan_local_fflags_scripts()
                deep_results = scanner.results.copy()

                print("\n[7/11] Analizando historial de navegación...")
                scanner = RobloxScanner()
                scanner.scan_browser_history()
                history_results = scanner.results.copy()
            
                print("\n[7/10] FFlags en sistema y registro...")
            
                print("\n[8/11] Objetivos de FFlags desde archivo...")
                scanner = RobloxScanner()
                scanner.scan_fflags_from_txt()
                fflags_targets = scanner.results.copy()
                scanner = RobloxScanner()
                scanner.scan_system_fflags()
                system_fflags = scanner.results.copy()
            
                print("\n[9/11] Cookies de navegadores...")
                scanner = RobloxScanner()
                scanner.scan_browser_cookies()
                cookies_results = scanner.results.copy()
                
                print("\n[8/10] Drivers del kernel y servicios...")
                scanner = RobloxScanner()
                scanner.scan_kernel_drivers()
                kernel_results = scanner.results.copy()
            
                print("\n[9/10] Puertos abiertos...")
                scanner = RobloxScanner()
                scanner.scan_open_ports()
                ports_results = scanner.results.copy()
            
                print("\n[10/11] Escaneo de logs...")
                scanner = RobloxScanner()
                scanner.scan_logs()
                logs_results = scanner.results.copy()
            
                print("\n[11/11] Restaurando archivos borrados...")
                scanner = RobloxScanner()
                scanner.restore_deleted_files()
                restore_results = scanner.results.copy()
            
                print("\n[12/12] Exploits en todo el sistema...")
                scanner = RobloxScanner()
                scanner.scan_system_exploits()
                sys_exploits = scanner.results.copy()
                
                print("\n[13/15] Exploits en el registro...")
                scanner = RobloxScanner()
                scanner.scan_registry_exploits()
                reg_exploits = scanner.results.copy()
                
                print("\n[14/15] Entradas de inicio y tareas programadas...")
                scanner = RobloxScanner()
                scanner.scan_startup_entries()
                startup_tasks = scanner.results.copy()
                
                print("\n[15/15] Módulos cargados en procesos...")
                scanner = RobloxScanner()
                scanner.scan_process_modules()
                proc_modules = scanner.results.copy()
                
                print("\n[16/18] Procesos sospechosos...")
                scanner = RobloxScanner()
                scanner.scan_suspicious_processes()
                suspicious_procs = scanner.results.copy()
                
                print("\n[17/18] Última vez Roblox y ejecuciones...")
                scanner = RobloxScanner()
                scanner.scan_last_play_roblox()
                last_play = scanner.results.copy()
                scanner = RobloxScanner()
                scanner.scan_prefetch_executions()
                prefetch_execs = scanner.results.copy()
                
                print("\n[18/18] DLLs sueltas y accesos directos...")
                scanner = RobloxScanner()
                scanner.scan_loose_dlls()
                loose_dlls = scanner.results.copy()
                scanner = RobloxScanner()
                scanner.scan_recent_shortcuts()
                recent_shortcuts = scanner.results.copy()
            
                scanner.results = {
                    'scan_type': 'complete',
                    'local_detection': local_results,
                    'fflags': fflag_results,
                    'fflags_targets': fflags_targets,
                    'github_exploits': github_results,
                    'weao_exploits': weao_results,
                    'vpn_detection': vpn_results,
                    'deep_scan': deep_results,
                    'browser_history': history_results,
                    'browser_cookies': cookies_results,
                    'system_fflags': system_fflags,
                    'kernel_drivers': kernel_results,
                    'open_ports': ports_results,
                    'logs_scan': logs_results
                    ,
                    'restore_deleted': restore_results,
                    'system_exploits': sys_exploits,
                    'registry_exploits': reg_exploits
                    ,
                    'startup_tasks': startup_tasks,
                    'process_modules': proc_modules,
                    'suspicious_processes': suspicious_procs,
                    'roblox_last_play': last_play,
                    'prefetch_executions': prefetch_execs,
                    'loose_dlls': loose_dlls,
                    'recent_shortcuts': recent_shortcuts
                }
            elif choice == "5":
                scanner.scan_browser_cookies()
            elif choice == "6":
                scanner.scan_fflags_from_txt()
            elif choice == "7":
                scanner.scan_weao_exploits()
            elif choice == "8":
                scanner.scan_vpns()
            elif choice == "9":
                scanner.scan_vpn_registry_services()
            elif choice == "10":
                scanner.scan_open_ports()
            elif choice == "11":
                scanner.scan_open_ports_psutil()
            elif choice == "12":
                scanner.scan_kernel_drivers()
            elif choice == "13":
                scanner.scan_local_fflags_scripts()
            elif choice == "14":
                scanner.scan_browser_history()
            elif choice == "15":
                scanner.scan_system_exploits()
            elif choice == "16":
                scanner.scan_registry_exploits()
            elif choice == "17":
                scanner.scan_startup_entries()
            elif choice == "18":
                scanner.scan_process_modules()
            elif choice == "19":
                scanner.scan_suspicious_processes()
            elif choice == "20":
                scanner.scan_last_play_roblox()
            elif choice == "21":
                scanner.scan_prefetch_executions()
            elif choice == "22":
                scanner.scan_loose_dlls()
            elif choice == "23":
                scanner.scan_deleted_files_list()
            elif choice == "24":
                scanner.scan_recent_closed_processes()
            elif choice == "25":
                scanner.scan_hidden_processes()
            elif choice == "26":
                scanner.scan_fflags_all_users()
            elif choice == "27":
                scanner.scan_registry_mui_recent()
            elif choice == "28":
                scanner.scan_recent_shortcuts()
            elif choice == "0":
                break
            else:
                print("Opción inválida")
                input("\nPulsa ENTER para volver al menú...")
                continue
        
            report_path = scanner.save_report()
            
            if report_path:
                print(f"\n{'='*70}")
                print("ESCANEO COMPLETADO")
                print(f"{'='*70}")
                print(f"✓ Reporte guardado: {report_path}")
                
                if choice == "1" or choice == "4":
                    stats = scanner.results.get('statistics', scanner.results.get('local_detection', {}).get('statistics', {}))
                    print(f"\n📊 DETECCIÓN LOCAL:")
                    print(f"   • Exploits detectados: {stats.get('total_exploits_detected', 0)}")
                    print(f"   • En ejecución: {stats.get('running_exploits', 0)}")
                    print(f"   • Instalados: {stats.get('installed_exploits', 0)}")
                
                print(f"\n{'='*70}")
                ok = scanner.send_webhook_report()
                if ok:
                    print("\n✓ Informe enviado por webhook")
            input("\nPulsa ENTER para volver al menú...")
        
        except KeyboardInterrupt:
            print("\nEscaneo interrumpido")
            input("\nPulsa ENTER para volver al menú...")
        except Exception as e:
            logger.error(f"Error: {str(e)}", exc_info=True)
            print(f"\nError: {str(e)}")
            input("\nPulsa ENTER para volver al menú...")


if __name__ == '__main__':
    main()
