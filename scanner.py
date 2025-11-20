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
            'pizzaboxer/bloxstrap'
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
        
        duration = time.time() - self.start_time
        self.results['scan_metadata']['duration_seconds'] = round(duration, 2)
        self.results['statistics']['total_fflags_found'] = sum(len(f) for f in self.results['fflags'].values())
        self.results['statistics']['unique_fflags'] = len(all_fflags)
        
        logger.info("=" * 70)
        logger.info(f"FFlags únicos: {len(all_fflags)}")
        logger.info(f"Total de entradas: {self.results['statistics']['total_fflags_found']}")
        logger.info("=" * 70)
    
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
        
        search_terms = ['wave executor', 'xeno executor', 'volcano executor', 'krnl executor']
        
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
            'Edge': Path.home() / 'AppData/Local/Microsoft/Edge/User Data/Default/History',
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
    
    def save_report(self, filename: str = 'reportes/reporte_completo.json'):
        
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
    
    print("\nSelecciona el modo de escaneo:")
    print("1. Detección Local - Busca exploits instalados en esta PC")
    print("2. Búsqueda de FFlags")
    print("3. Búsqueda de Exploits")
    print("4. Escaneo Completo - Ejecuta todos los modos")
    
    choice = input("\nOpción [1]: ").strip() or "1"
    
    scanner = RobloxScanner()
    
    try:
        if choice == "1":
            scanner.scan_local_exploits()
        elif choice == "2":
            scanner.scan_fflags()
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
            
            print("\n[3/6] Ejecutando búsqueda de exploits..")
            scanner = RobloxScanner()
            scanner.scan_github_exploits()
            github_results = scanner.results.copy()

            print("\n[4/6] Buscando VPNs...")
            scanner = RobloxScanner()
            scanner.scan_vpns()
            vpn_results = scanner.results.copy()

            print("\n[5/6] Búsqueda profunda de archivos...")
            scanner = RobloxScanner()
            scanner.scan_local_fflags_scripts()
            deep_results = scanner.results.copy()

            print("\n[6/6] Analizando historial de navegación...")
            scanner = RobloxScanner()
            scanner.scan_browser_history()
            history_results = scanner.results.copy()
            
            scanner.results = {
                'scan_type': 'complete',
                'local_detection': local_results,
                'fflags': fflag_results,
                'github_exploits': github_results,
                'vpn_detection': vpn_results,
                'deep_scan': deep_results,
                'browser_history': history_results
            }
        else:
            print("Opción inválida")
            return
        
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
    
    except KeyboardInterrupt:
        print("\n\nEscaneo interrumpido")
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        print(f"\nError: {str(e)}")


if __name__ == '__main__':
    main()
