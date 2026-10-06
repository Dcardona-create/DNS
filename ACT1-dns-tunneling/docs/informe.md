# Informe de la actividad 1: Seguridad en DNS

## 1. Datos de la práctica

| Campo | Información |
|---|---|
| Módulo | 037 Seguridad en servicios |
| Ciclo formativo | ASIX |
| Alumno | Deivid Cardona |
| Actividad | Seguridad en el DNS: DNS tunneling |
| Entorno | Una máquina GNU/Linux en localhost |

## 2. Objetivo

Analizar el funcionamiento de una comunicación DNS controlada mediante dos scripts en Python: un cliente que realiza una consulta DNS de tipo `A` y un servidor que recibe la consulta, interpreta la estructura del paquete DNS, recupera información codificada en el subdominio y genera una respuesta mínima válida.

## 3. Material utilizado

- Sistema GNU/Linux.
- Python 3.
- Script `dns_client_1_peticion.py`.
- Script `dns_server_1_peticion.py`.
- Wireshark para la captura y el análisis de tráfico.
- Interfaz loopback `lo`, con dirección IPv4 `127.0.0.1`.

La máquina también cuenta con la interfaz privada `enp0s8`, configurada con la dirección `192.168.6.100/24`. La actividad documentada se realizó localmente, por lo que cliente y servidor utilizaron `127.0.0.1`.

## 4. Desarrollo

### 4.1 Inicio del servidor

El servidor se inició con permisos de administrador, necesarios para enlazar el puerto DNS estándar 53:

```bash
sudo python3 dns_server_1_peticion.py
```

El servidor queda a la espera de una petición DNS. Al recibirla, muestra la información relevante de la consulta, obtiene el nombre completo solicitado, extrae el primer subdominio y transforma la cadena hexadecimal recibida a texto.

### 4.2 Ejecución del cliente

El cliente se ejecutó en otra terminal de la misma máquina:

```bash
sudo python3 dns_client_1_peticion.py
```

El cliente genera una consulta DNS de tipo `A` y utiliza como dominio solicitado:

```text
6461746f73206663756c746f73.secreto.com
```

El bloque hexadecimal `6461746f73206663756c746f73` representa, en ASCII, el mensaje:

```text
datos ocultos
```

### 4.3 Procesamiento en el servidor

El servidor recibió una petición DNS con identificador `1887`. La salida mostró los siguientes elementos:

```text
opcode QUERY
rcode NOERROR
flags RD
QUESTION
6461746f73206663756c746f73.secreto.com. IN A
```

Después de obtener el nombre completo, el servidor identificó el subdominio codificado y mostró:

```text
Subdominio recibido: 6461746f73206663756c746f73
Mensaje oculto recibido: datos ocultos
```

Finalmente, el servidor construyó una respuesta DNS de tipo `A` para `secreto.com` con la dirección `4.3.2.1`.

### 4.4 Respuesta recibida por el cliente

El cliente recibió una respuesta correcta (`NOERROR`) con el registro:

```text
secreto.com. 300 IN A 4.3.2.1
```

Esto confirma que el intercambio DNS se completó satisfactoriamente.

## 5. Captura con Wireshark

La captura se realizó en la interfaz loopback `lo`, aplicando el filtro de visualización:

```text
dns
```

En la traza se observa una consulta DNS cuyo origen y destino son `127.0.0.1`. La consulta se transporta mediante UDP hacia el puerto 53 y solicita un registro de tipo `A` para el dominio:

```text
6461746f73206663756c746f73.secreto.com
```

Wireshark permite examinar el encabezado DNS, el identificador de transacción, las banderas, la sección de preguntas y el nombre de dominio. La presencia del subdominio hexadecimal permite observar cómo se transporta el mensaje oculto dentro de una consulta aparentemente normal.

## 6. Resultados

- El servidor DNS recibió correctamente una consulta de tipo `A`.
- El subdominio hexadecimal fue extraído y decodificado correctamente.
- El texto recuperado fue `datos ocultos`.
- El cliente recibió una respuesta DNS válida con `rcode NOERROR`.
- Wireshark confirmó la transmisión de la consulta DNS a través de `127.0.0.1`.

## 7. Conclusión

La actividad demuestra el principio básico de DNS tunneling en un entorno controlado: los datos se codifican en hexadecimal y se incluyen como subdominio dentro de una consulta DNS. El servidor puede recuperar y decodificar ese contenido al recibir la petición.

Desde el punto de vista de la seguridad, las consultas DNS con subdominios largos, aleatorios o codificados pueden ser un indicador de un posible canal encubierto. Por ello, el análisis de logs DNS y la supervisión de patrones anómalos son medidas importantes para detectar este tipo de comunicaciones.

## 8. Evidencias pendientes de incorporar

- Captura de terminal del cliente.
- Captura de terminal del servidor.
- Captura de Wireshark con el detalle de la consulta DNS.
