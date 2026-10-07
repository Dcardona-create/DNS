# ACT2 – DNS: resolución, caché y configuración

## 1. Investigación de dominios y DNS

En este apartado se ha realizado una investigación sobre varios dominios para entender cómo funciona la jerarquía del DNS y quién gestiona cada nivel.

### 1.1 Benchmark de servidores DNS

Se ejecutó un benchmark de servidores DNS públicos para identificar los tres más rápidos desde esta máquina. Los resultados sirvieron para seleccionar los DNS que se usarían en pruebas posteriores.

![Benchmark de Nameservers](01-benchmark-nameservers.jpg)

### 1.2 Búsqueda WHOIS de un dominio .es

Se utilizó la herramienta WHOIS para investigar el dominio `ifp.es` y obtener información sobre su registrador, fechas de creación y caducidad, y datos de contacto.

![WHOIS de ifp.es](02-whois-ifp-es.jpg)

### 1.3 Información de dominios de primer nivel (TLD)

Se consultó la base de datos de IANA para obtener información oficial sobre tres dominios de primer nivel:

- `.es` (España)
- `.cat` (comunidades lingüísticas y culturales catalanas)
- `.edu` (instituciones educativas, principalmente de EE. UU.)

![IANA – Dominio .es](03-iana-es.png)

![IANA – Dominio .cat](04-iana-cat.jpg)

![IANA – Dominio .edu](05-iana-edu.jpg)

Estas capturas muestran quién gestiona cada TLD, las políticas de registro y los servidores de nombres asociados.

---

## 2. Configuración y caché DNS (en curso)

En los siguientes pasos se trabajará sobre una máquina Linux para:

- Ver la configuración actual de DNS.
- Comprobar el funcionamiento de la caché DNS.
- Modificar los servidores DNS si fuera necesario.

*(Esta sección se irá completando a medida que se realicen las pruebas en la terminal.)*

---

## Evidencias

Todas las capturas de pantalla están disponibles en la carpeta:

[`capturas/`](./capturas)
