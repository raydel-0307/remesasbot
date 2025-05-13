# Sistema de Gestión de Remesas via Zelle - Telegram Bot 🤖

Bot de Telegram para administración y control automatizado de transacciones financieras a través de Zelle, con seguimiento en tiempo real de balances y reportes automatizados.

![Pyrogram](https://img.shields.io/badge/Pyrogram-2.0.106-blue)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)

## Características Principales ✨

- ✅ Confirmación/Rechazo de depósitos Zelle con capturas
- 📊 Seguimiento automático de subtotales por canal
- 📈 Actualización en tiempo real de balances financieros
- 🔔 Reportes diarios automatizados
- 🛡️ Sistema de permisos y roles (Admins/Resellers)
- ⏰ Programación inteligente de tareas recurrentes
- 📆 Gestión de zonas horarias (America/Havana)

## Requisitos e Instalación 🚀

```bash
# Clonar repositorio
git clone https://github.com/raydel-0307/remesasbot.git

# Acceder al directorio
cd remesasbot

# Instalar dependencias
pip install -r requirements.txt
```

## Configuración ⚙️ (`config.py`)

| Parámetro       | Descripción                             |
|-----------------|-----------------------------------------|
| `api_id`        | ID de API de Telegram                   |
| `api_hash`      | Hash de API de Telegram                 |
| `bot_token`     | Token del Bot de Telegram               |
| `owners`        | Usuarios admin (con @)                  |
| `settings`      | Configuración de canales y mensajes     |

Ejemplo de estructura de canal:
```python
"-1002631578411": {
    "name": "Yasmani y Rachel (Zelle)",
    "zelle": 2,          # ID mensaje para transacciones Zelle
    "balance": 4,        # ID mensaje para balances
    "financiamiento": 3, # ID mensaje para financiamientos
    "button": 2631578411 # ID para botones de enlace
}
```

## Uso del Bot 💻

### Comandos Disponibles
| Comando         | Descripción                             | Permisos       |
|-----------------|-----------------------------------------|----------------|
| `/start`        | Mensaje de bienvenida                   | Todos          |
| `/subtotal`     | Obtener subtotal actual                 | Admins         |
| `/reestart`     | Reiniciar contadores diarios            | Admins         |
| `/balance`      | Establecer balance manualmente          | Admins         |

### Flujos de Trabajo
1. **Depósito Zelle**:
   - Subir imagen con caption: `"Depósito $500 Ref: XXXX"`
   - Bot responde con menú de confirmación
   - Admins aprueban/rechazan desde la interfaz

2. **Reporte Diario**:
   - Generado automáticamente a las 3:00 AM (GMT-5)
   - Incluye subtotales por canal y total general
   - Reinicio automático de contadores

## Estructura del Proyecto 📂

```
.
├── bot.py             # Lógica principal del bot
├── functions.py       # Utilidades y helpers
├── config.py          # Configuraciones y credenciales
└── requirements.txt   # Dependencias del proyecto
```

## Tecnologías Utilizadas 🛠️

- **Pyrogram**: Framework principal para interacción con Telegram API
- **TgCrypto**: Encriptación de sesiones MTProto
- **SQLite**: Almacenamiento local de datos
- **Timezone Handling**: Gestión de zonas horarias con ZoneInfo
- **Async I/O**: Programación asíncrona para alta concurrencia

## Consideraciones de Seguridad 🔐

❗ **Importante**: 
- Mantener `config.py` fuera de control de versiones
- Usar entornos virtuales para dependencias
- Restringir acceso a los mensajes del canal `-4625105368`
- Actualizar regularmente las credenciales API

## Soporte y Contribuciones 🤝

Para reportar problemas o sugerencias, abrir un issue en el repositorio. Las contribuciones son bienvenidas mediante Pull Requests.

---

**Licencia**: [MIT License](LICENSE) © 2024
