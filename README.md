# 🔍 Roblox Scanner Completo

Un escáner avanzado de seguridad para detectar exploits, scripts, FFlags y VPNs relacionados con Roblox en sistemas Windows.

## 📋 Descripción

Este escáner proporciona múltiples modos de análisis para detectar y documentar:
- Exploits de Roblox instalados localmente
- Procesos sospechosos en ejecución
- FFlags (Feature Flags) de Roblox
- Scripts maliciosos
- VPNs instaladas
- Historial de navegador relacionado con exploits

## ✨ Características

### 🎯 Detección Local de Exploits
- Escanea procesos en ejecución buscando exploits conocidos
- Detecta carpetas y archivos de exploits en ubicaciones comunes
- Identifica exploits populares como:
  - Wave
  - Xeno
  - Volcano
  - KRNL
  - Fluxus
  - Solara
  - Electron
  - Nexus
  - Synapse X
  - Delta

### 🚩 Búsqueda de FFlags
- Escanea repositorios de GitHub para encontrar FFlags de Roblox
- Categoriza FFlags por tipo:
  - Bloxtrap
  - Voidtrap
  - React
  - Optimización de ping
  - Gráficos
  - Rendimiento
  - Red
  - Experimental

### 🔎 Búsqueda de Exploits en GitHub
- Busca repositorios relacionados con exploits de Roblox
- Proporciona información detallada de cada repositorio encontrado

### 🛡️ Detección de VPN
- Identifica procesos de VPN en ejecución
- Detecta interfaces de red sospechosas (TUN/TAP)
- Soporta VPNs populares como:
  - NordVPN
  - ExpressVPN
  - ProtonVPN
  - Surfshark
  - WireGuard
  - OpenVPN
  - Y más...

### 📂 Búsqueda Profunda de Archivos
- Escanea ubicaciones de Roblox en busca de FFlags locales
- Detecta scripts Lua/Luau sospechosos
- Identifica keywords de exploits como:
  - loadstring
  - game:GetService
  - fireclickdetector
  - hookfunction
  - getrawmetatable

### 🌐 Análisis de Historial de Navegador
- Escanea historial de Chrome, Edge, Opera GX y Firefox
- Busca URLs relacionadas con exploits y scripts
- Identifica visitas a sitios sospechosos

## 🚀 Instalación

### Requisitos
- Python 3.7 o superior
- Windows OS

### Dependencias

```bash
pip install -r requirements.txt
```

Las dependencias incluyen:
- `requests` - Para peticiones HTTP
- `beautifulsoup4` - Para parsing HTML
- `lxml` - Parser XML/HTML
- `python-dotenv` - Para variables de entorno
- `psutil` - Para información del sistema

## 💻 Uso

### Ejecución Básica

```bash
python scanner.py
```

### Modos de Escaneo

Al ejecutar el script, se presentarán las siguientes opciones:

```
1. Detección Local - Busca exploits instalados en esta PC
2. Búsqueda de FFlags
3. Búsqueda de Exploits
4. Escaneo Completo - Ejecuta todos los modos
```

#### Modo 1: Detección Local
Escanea el sistema local en busca de exploits instalados o en ejecución.

```bash
Opción [1]: 1
```

#### Modo 2: Búsqueda de FFlags
Busca FFlags en repositorios de GitHub.

```bash
Opción [1]: 2
```

#### Modo 3: Búsqueda de Exploits
Busca repositorios de exploits en GitHub.

```bash
Opción [1]: 3
```

#### Modo 4: Escaneo Completo
Ejecuta todos los modos de escaneo:
1. Detección local de exploits
2. Búsqueda de FFlags
3. Búsqueda de exploits en GitHub
4. Detección de VPNs
5. Búsqueda profunda de archivos
6. Análisis de historial de navegador

```bash
Opción [1]: 4
```

## 📊 Reportes

Todos los escaneos generan reportes en formato JSON en la carpeta `reportes/`:

```
reportes/
├── reporte_completo.json
└── scanner.log
```

### Estructura del Reporte

Los reportes incluyen:
- **Metadatos del escaneo**: timestamp, duración, hostname, usuario
- **Exploits detectados**: nombre, estado, evidencia
- **Procesos en ejecución**: PID, nombre, ruta
- **Archivos y carpetas sospechosas**: ubicaciones, conteos
- **Estadísticas**: totales de detecciones

Ejemplo de reporte:

```json
{
  "scan_type": "local_detection",
  "scan_metadata": {
    "timestamp": "2025-11-20T11:25:00",
    "hostname": "PC-NAME",
    "username": "User",
    "scan_duration_seconds": 5.23
  },
  "detected_exploits": [],
  "statistics": {
    "total_exploits_detected": 0,
    "running_exploits": 0,
    "installed_exploits": 0
  }
}
```

## 🔧 Configuración Avanzada

### Token de GitHub (Opcional)

Para evitar límites de rate en la API de GitHub, puedes configurar un token:

```bash
set GITHUB_TOKEN=tu_token_aquí
```

O crear un archivo `.env`:

```
GITHUB_TOKEN=tu_token_aquí
```

## ⚠️ Advertencias

- Este escáner requiere permisos de administrador para acceder a ciertos procesos
- El análisis de historial de navegador puede tomar tiempo si hay muchos datos
- Algunos antivirus pueden marcar este script como sospechoso debido a su naturaleza de escaneo

## 📝 Logs

Los logs se guardan automáticamente en `reportes/scanner.log` con información detallada de:
- Procesos escaneados
- Errores encontrados
- Detecciones realizadas
- Tiempo de ejecución

## 🛠️ Solución de Problemas

### Error: "Permission Denied"
- Ejecuta el script como administrador
- Algunos procesos requieren privilegios elevados

### Error: "Module not found"
- Asegúrate de instalar todas las dependencias: `pip install -r requirements.txt`

### El escaneo es muy lento
- El modo completo puede tardar varios minutos
- Usa modos individuales para escaneos más rápidos

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso educativo y de investigación.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request para sugerencias o mejoras.

---

**by Naxel´z**
