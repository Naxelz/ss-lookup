## 🔍 Roblox Scanner Completo
Un escáner avanzado de seguridad para detectar exploits, scripts, FFlags y VPNs relacionados con Roblox en sistemas Windows.

## 📋 Descripción
Este escáner proporciona múltiples modos de análisis para detectar y documentar:
- Exploits de Roblox instalados localmente
- Procesos sospechosos en ejecución y cerrados recientemente
- FFlags (Feature Flags) de Roblox en GitHub, sistema y targets personalizados
- Scripts maliciosos y DLLs sueltas
- VPNs instaladas y persistencias
- Historial y cookies de navegadores relacionadas con exploits

## ✨ Características
### 🎯 Detección Local de Exploits
- Escanea procesos en ejecución buscando exploits conocidos
- Detecta carpetas y archivos de exploits en ubicaciones comunes
- Consolida evidencia (en ejecución/instalado) y estadísticas
- Exploits populares detectados, entre otros:
  - Wave, Xeno, Volcano, KRNL, Fluxus, Solara, Electron, Nexus, Synapse X, Delta, Zenith, Bunni, TGX, Volt, Seliware, Valex, Potassium, Hydrogen, Arceus X, Codex, Oxygen U, Vega X, Trigon, Evon, JJSploit, SirHurt, Elysian, Sentinel, Calamari, ProtoSmasher, Visenya, Nihon, Skisploit, Calamity, Trojan, Apex, Zen, Phoenix, Solix, Electron X, Nitro, Vortex, Aero, Tempest, Neptune, Aurora, Krypton, Helix

### 🚩 Búsqueda de FFlags
- Escanea repositorios de GitHub y código para encontrar FFlags de Roblox
- Categoriza FFlags por tipo:
  - Bloxstrap, Voidtrap, React, Optimización de ping, Gráficos, Rendimiento, Red, Experimental
- Modo unificado `FFlags Completo` (GitHub + sistema + `fflags_targets.txt`)
- Opción dedicada para `FFlags todos usuarios` (recorre `ClientSettings` de cada perfil)

### 🔎 Búsqueda de Exploits en GitHub
- Busca repositorios relacionados con exploits de Roblox
- Proporciona información básica y listado de repos

### 🛡️ Detección de VPN
- Identifica procesos de VPN en ejecución
- Detecta interfaces de red sospechosas (TUN/TAP/WireGuard)
- Soporta VPNs populares: NordVPN, ExpressVPN, ProtonVPN, Surfshark, WireGuard, OpenVPN, y más

### 📂 Búsqueda Profunda de Archivos
- Escanea ubicaciones de Roblox en busca de FFlags locales
- Detecta scripts Lua/Luau sospechosos
- Identifica keywords de exploits como `loadstring`, `game:GetService`, `fireclickdetector`, `hookfunction`, `getrawmetatable`

### 🌐 Análisis de Navegadores
- Historial: Chrome, Edge, Opera/Opera GX, Brave, Vivaldi, Firefox
- Cookies: perfiles Chromium y Firefox
- Busca URLs y cookies relacionadas con exploits/scripts/launchers

### 🧠 Evidencia de ejecución
- Prefetch: ejecutores y `ROBLOXPLAYERBETA.EXE`
- MUICache y AppCompat Store: evidencia de programas ejecutados recientemente
- Accesos directos recientes (.lnk)
- Procesos cerrados (EventID 4689, si disponible)
- Procesos escondidos (tasklist vs psutil)

## 🚀 Instalación
### Requisitos
- Windows 10/11
- Python 3.9 o superior (recomendado 3.10+)

### Dependencias
Instala dependencias:
```
pip install requests psutil python-dotenv winshell
```
`winshell` es opcional (listar/restaurar Papelera). Si no está, esas funciones se limitan.

Descarga o clona este repositorio en tu PC. Asegúrate de tener Python en el `PATH`.

## 🔧 Configuración Avanzada
### Webhook
1. `.env`:
```
SCANNER_WEBHOOK_URL=https://discord.com/api/webhooks/TU_ID/TU_TOKEN
```
2. Alternativa: `reportes/webhook.txt` (una línea). Si `.env` no está presente, se usa ese archivo.

### Token de GitHub (Opcional)
Para evitar límites de rate:
```
set GITHUB_TOKEN=tu_token_aqui
```
O `.env`:
```
GITHUB_TOKEN=tu_token_aqui
```

## 💻 Uso
### Ejecución básica
Ejecuta el escáner:
```
python scanner.py
```
Se abrirá el menú persistente. Selecciona la opción por número; tras el modo, pulsa ENTER para volver.

## Modos de Escaneo
- 1 Detección Local — Exploits instalados y procesos
- 2 FFlags Completo — GitHub, Sistema y Targets
- 3 Exploits (GitHub) — Repos y términos
- 4 Escaneo Completo — Todo en uno
- 5 Cookies Navegadores — Profiles Chromium/Firefox
- 6 FFlags desde archivo — `fflags_targets.txt`
- 7 Catálogo WEAO — Estado y presencia local
- 8/9 VPNs — Procesos/Servicios y registro
- 10/11 Puertos — netstat/psutil
- 12 Kernel/Servicios — Drivers/servicios
- 13 Búsqueda profunda — Scripts/FFlags locales
- 14 Historial Navegadores — URLs con términos
- 15 Exploits en sistema — Rutas objetivo
- 16 Exploits en registro — Claves/valores
- 17 Inicio/Tareas — Persistencia
- 18 Módulos de procesos — DLLs cargadas
- 19 Procesos sospechosos — Ejecutores y módulos
- 20 Última vez Roblox — Logs/Prefetch
- 21 Prefetch ejecuciones — Ejecutores/Roblox
- 22 DLLs sueltas — Hooks/injectors
- 23 Listar Papelera — Borrados
- 24 Procesos cerrados — EventID 4689
- 25 Procesos escondidos — tasklist vs psutil
- 26 FFlags todos usuarios — `ClientSettings`
- 27 MUICache recientes — Ejecutores
- 28 Accesos directos recientes — .lnk

## 📊 Reportes
- Todos los escaneos generan `informes/reporte_completo.json` y logs en `reportes/scanner.log`.
- Si el webhook es Discord, se adjunta el archivo `reporte_completo.json` al mensaje.

### Estructura del reporte
Incluye:
- Metadatos del escaneo: `timestamp`, duración, tipo
- Exploits detectados: nombre, estado, evidencia
- Procesos en ejecución: PID, nombre, ruta
- Archivos y carpetas sospechosas: ubicaciones, conteos
- Estadísticas: totales

Ejemplo:
```
{
  "scan_type": "local_detection",
  "scan_metadata": {
    "timestamp": "2025-11-20T11:25:00"
  },
  "detected_exploits": [],
  "statistics": {
    "total_exploits_detected": 0,
    "running_exploits": 0,
    "installed_exploits": 0
  }
}
```

## 📝 Logs
Los logs se guardan en `reportes/scanner.log` con información de:
- Procesos escaneados
- Errores
- Detecciones
- Tiempos

## 🛠️ Solución de Problemas
- Permission Denied: Ejecuta como Administrador.
- Module not found: Instala dependencias.
- Escaneo lento: El modo completo puede tardar; usa modos individuales.
- Prefetch vacío: Puede estar deshabilitado por políticas.
- EventID 4689: Actívalo en auditorías de Seguridad.

## 📄 Licencia
Uso educativo y de investigación.

## 🤝 Contribuciones
Se aceptan mejoras vía issues o pull requests.

by Naxel´z
