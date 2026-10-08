# ACT3 — Instalación y configuración de BIND9

## Objetivo

Instalar y configurar el servicio DNS BIND9 en una máquina virtual, verificando la resolución directa e inversa de las zonas configuradas y el correcto funcionamiento del servicio.

## Entorno de trabajo

- Máquina virtual con sistema GNU/Linux.
- Servicio DNS: BIND9.
- Configuración de zonas directa e inversa.

## Evidencias

Las capturas incluidas en esta carpeta documentan los principales pasos y comprobaciones de la práctica:

1. Configuración del entorno de red de la máquina virtual.
2. Instalación de BIND9 y comprobación del estado del servicio.
3. Configuración de BIND9 y de los archivos de zona directa e inversa.
4. Verificación de la resolución de nombres y de la resolución inversa.

## Comprobaciones realizadas

- El servicio BIND9 se encuentra instalado y activo.
- Las zonas DNS directa e inversa están declaradas en la configuración.
- Las consultas directas resuelven los nombres configurados.
- Las consultas inversas devuelven el nombre asociado a la dirección IP.

## Estructura

```text
ACT3-instalacion-bind9/
└── README.md
```

Las evidencias gráficas de la actividad se almacenan en esta misma carpeta.