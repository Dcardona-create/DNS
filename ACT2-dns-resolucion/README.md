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

#### Dominio .es (España)

Gestionado por Red.es, es el dominio de primer nivel correspondiente a España.

![IANA – Dominio .es](03-iana-es.png)

#### Dominio .cat (comunidades lingüísticas y culturales catalanas)

Gestionado por la Fundació puntCAT, es el TLD para la comunidad lingüística y cultural catalana.

![IANA – Dominio .cat](04-iana-cat.jpg)

#### Dominio .edu (instituciones educativas)

Gestionado por Educause, está reservado principalmente para instituciones de educación superior de EE. UU.

![IANA – Dominio .edu](05-iana-edu.jpg)

Estas capturas muestran quién gestiona cada TLD, las políticas de registro y los servidores de nombres asociados.

---

## 2. Configuración y caché DNS

### 2.1 Consulta de los servidores DNS asignados

Los servidores DNS configurados se pueden consultar desde consola. En Linux se utilizó el comando:

```bash
cat /etc/resolv.conf
```

En Windows, el comando equivalente es:

```cmd
ipconfig /all
```

En ambos casos se muestra el servidor DNS asignado a cada adaptador de red.

### 2.2 Cambio de servidores DNS

La configuración inicial del equipo utilizaba el DNS del router (`192.168.111.1`). Para realizar las pruebas se configuraron los dos DNS más rápidos obtenidos en el benchmark de la fase 1:

- DNS primario: `1.1.1.1` (Cloudflare).
- DNS secundario: `1.0.0.1` (Cloudflare).

El cambio se realizó de forma temporal editando `/etc/resolv.conf`. La consulta posterior con `nslookup www.google.com` confirmó que la resolución se efectuaba mediante `1.1.1.1`.

![Cambio de DNS y comprobación de resolución](06-cambio-dns-linux.jpg)

> Nota: en este equipo el archivo `/etc/resolv.conf` es generado por DHCP. Por eso, un reinicio o una renovación DHCP puede restaurar automáticamente los DNS proporcionados por el router.

### 2.3 DNS manual en dispositivos móviles

En Android se puede configurar DNS para una red Wi-Fi desde **Ajustes > Red e Internet (o Conexiones) > Wi-Fi > red seleccionada > editar/avanzado**. Según el dispositivo, se puede establecer DNS manual al usar IP estática o configurar **DNS privado**.

En iPhone o iPad se accede desde **Ajustes > Wi-Fi > icono de información (i) de la red > Configurar DNS > Manual**, donde se añaden los servidores deseados.

### 2.4 Comprobación de la caché DNS

Inicialmente no estaba instalado `systemd-resolved` ni otro servicio de caché DNS local. Para disponer de una caché de resoluciones se instaló y activó `nscd` (*Name Service Cache Daemon*):

```bash
sudo apt update
sudo apt install -y nscd dnsutils
systemctl status nscd --no-pager
```

Después se generaron resoluciones mediante el resolvedor del sistema:

```bash
getent hosts www.google.com
getent hosts www.wikipedia.org
getent hosts www.github.com
```

Las estadísticas se consultaron con:

```bash
sudo /usr/sbin/nscd -g
```

La salida muestra que la caché está activa y presenta el número de valores almacenados, además de los aciertos y fallos de caché.

![Estadísticas de la caché DNS con nscd](07-cache-dns-nscd.jpg)

### 2.5 Vaciado de la caché DNS

La caché de resoluciones de nombres se vació con el siguiente comando:

```bash
sudo nscd -i hosts
```

A continuación, se volvió a consultar el estado de `nscd` con `sudo /usr/sbin/nscd -g` para verificar la operación.

![Vaciado de la caché DNS](08-vaciado-cache-dns.jpg)

Vaciar la caché DNS invalida las resoluciones almacenadas y obliga al sistema a volver a preguntar al servidor DNS configurado. Es útil para un administrador de sistemas cuando un dominio ha cambiado de dirección IP, se reciben respuestas antiguas o incorrectas, se modifica la configuración DNS o se diagnostican problemas de conectividad y resolución de nombres.

---

## 3. Administración: Troubleshooting con DIG y CLI

En entornos Linux, `dig` permite consultar tipos de registros DNS concretos y analizar con detalle las respuestas. Para las pruebas se utilizó el dominio `aliexpress.com`.

### 3.1 Consulta de registros A

Se ejecutó:

```bash
dig aliexpress.com
```

La sección `ANSWER SECTION` devolvió dos registros `A`, correspondientes a direcciones IPv4 del dominio:

```text
47.246.75.137
47.246.111.53
```

El campo `IN` identifica la clase Internet y el TTL observado fue de 283 segundos. La respuesta tenía estado `NOERROR`, por lo que la resolución fue correcta.

![Consulta de registro A para aliexpress.com](09-dig-a-aliexpress.jpg)

### 3.2 Formato corto, MX y NS

El comando siguiente muestra únicamente las respuestas:

```bash
dig +short aliexpress.com
```

Devolvió las direcciones `47.246.111.53` y `47.246.75.137`. Este formato es útil en scripts Bash porque elimina cabeceras y metadatos; por ejemplo, se puede obtener la primera IP con `dig +short aliexpress.com | head -n 1`.

Para consultar el registro de correo se ejecutó:

```bash
dig MX aliexpress.com
```

El resultado fue `mx2.mail.aliyun.com` con preferencia `10`. En los registros MX, el número más bajo representa la prioridad más alta.

Finalmente, la consulta:

```bash
dig NS aliexpress.com
```

identificó los servidores autoritativos de la zona:

- `ns1.alibabadns.com`
- `ns2.alibabadns.com`

![Consultas +short, MX y NS para aliexpress.com](10-dig-short-mx-ns-aliexpress.jpg)

### 3.3 Autoridad y caché: TTL, SOA y NS

Se consultó dos veces el registro A de `aliexpress.com`, esperando cinco segundos entre consultas. El TTL pasó de `600` a `595`, exactamente cinco segundos menos.

Esto demuestra que la respuesta se sirvió desde una caché DNS intermedia: el resolvedor mantiene el registro mientras el TTL no llega a cero y reduce el contador conforme pasa el tiempo. En esta práctica, el DNS que respondió fue el router `192.168.111.1`.

![Comparación de TTL de aliexpress.com](11-dig-ttl-aliexpress.jpg)

Un registro `SOA` (*Start of Authority*) identifica el inicio de autoridad de una zona e incluye información administrativa: servidor maestro, contacto responsable, número de serie y temporizadores de refresco, reintentos, expiración y TTL negativo.

Un registro `NS` (*Name Server*) indica los servidores de nombres que responden autoritativamente por una zona. Por tanto, el SOA describe parámetros de administración y sincronización de la zona, mientras que los NS indican qué servidores tienen autoridad para responder por ella.

### 3.4 Trazabilidad completa con `dig +trace`

Se ejecutó:

```bash
dig +trace aliexpress.com
```

La traza muestra la resolución jerárquica completa:

1. El equipo parte de los servidores raíz, representados por `.` y nombres como `a.root-servers.net` hasta `m.root-servers.net`.
2. Un servidor raíz delega la consulta a los servidores responsables del TLD `.com`, como `a.gtld-servers.net`.
3. Los servidores del TLD `.com` indican los servidores autoritativos de `aliexpress.com`: `ns1.alibabadns.com` y `ns2.alibabadns.com`.
4. El servidor autoritativo responde finalmente con los registros A `47.246.75.137` y `47.246.111.53`.

Durante la traza aparecieron mensajes `network unreachable` para algunas direcciones IPv6. Esto no impidió la resolución porque `dig` continuó mediante IPv4 y obtuvo correctamente la respuesta final.

![Traza DNS completa de aliexpress.com](12-dig-trace-aliexpress.jpg)

---

## Evidencias

Las evidencias de esta actividad se encuentran en la carpeta [`ACT2-dns-resolucion/`](./).