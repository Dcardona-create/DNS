# ACT1 - Seguridad en DNS: DNS Tunneling

## Descripción

Este repositorio contiene el código y la documentación de la actividad guiada sobre seguridad en DNS. La práctica demuestra cómo puede utilizarse una consulta DNS de tipo `A` para transportar información codificada dentro de un subdominio.

La ejecución se ha realizado en una única máquina GNU/Linux. El cliente y el servidor DNS se ejecutan localmente y la comunicación se realiza mediante la interfaz loopback (`127.0.0.1`).

## Objetivos

- Ejecutar y analizar un cliente y un servidor DNS implementados en Python 3.
- Enviar una consulta DNS de tipo `A` a un servidor DNS local.
- Transportar un mensaje codificado en hexadecimal dentro del subdominio consultado.
- Decodificar el subdominio en el servidor para recuperar el mensaje oculto.
- Capturar y analizar las tramas DNS con Wireshark.

## Contenido

```text
ACT1-dns-tunneling/
├── dns_client_1_peticion.py   # Cliente: genera y envía la consulta DNS
├── dns_server_1_peticion.py   # Servidor: recibe, analiza y responde la consulta
├── README.md                  # Resumen de la actividad
└── docs/
    └── informe.md             # Desarrollo detallado de la práctica
```

## Entorno de trabajo

| Elemento | Configuración |
|---|---|
| Sistema operativo | GNU/Linux |
| Lenguaje | Python 3 |
| Protocolo de transporte | UDP |
| Puerto de destino | 53 |
| Interfaz de captura | Loopback (`lo`) |
| Dirección de origen y destino | `127.0.0.1` |
| Herramienta de análisis | Wireshark |
| Filtro aplicado | `dns` |

La máquina de laboratorio también dispone de la interfaz privada `enp0s8` con la dirección `192.168.6.100/24`; no obstante, para esta práctica se ha utilizado el modo local mediante loopback.

## Ejecución

> En Linux, el servidor DNS necesita permisos de administrador para escuchar en el puerto 53.

1. Abrir dos terminales en el directorio donde están los scripts.
2. En la primera terminal, iniciar el servidor:

```bash
sudo python3 dns_server_1_peticion.py
```

3. En la segunda terminal, ejecutar el cliente:

```bash
sudo python3 dns_client_1_peticion.py
```

4. Abrir Wireshark, seleccionar la interfaz `lo` y aplicar el filtro:

```text
dns
```

5. Iniciar la captura antes de ejecutar el cliente para registrar la petición y la respuesta.

## Resultado de la prueba

El cliente realiza una consulta DNS de tipo `A` para el nombre:

```text
6461746f73206663756c746f73.secreto.com
```

La primera etiqueta del nombre de dominio contiene los datos que se quieren transportar:

```text
6461746f73206663756c746f73
```

Al interpretar la cadena hexadecimal como texto ASCII, el servidor obtiene:

```text
datos ocultos
```

La consulta observada corresponde a una operación `QUERY`, con respuesta `NOERROR`. El servidor devuelve el registro:

```text
secreto.com. 300 IN A 4.3.2.1
```

## Análisis de la comunicación

La comunicación se produce por UDP hacia el puerto 53. Wireshark permite observar la consulta DNS enviada desde `127.0.0.1` a `127.0.0.1`, el nombre de dominio solicitado y la respuesta emitida por el servidor.

Este ejemplo evidencia que un subdominio puede transportar datos codificados. En un contexto de seguridad, este comportamiento es relevante porque el DNS tunneling puede usarse para ocultar o extraer información si no se aplican medidas de supervisión y filtrado.

## Evidencias

Las evidencias de la ejecución incluyen:

- Cliente DNS enviando la consulta y recibiendo la respuesta.
- Servidor DNS recibiendo la petición, extrayendo el subdominio y recuperando el texto `datos ocultos`.
- Wireshark mostrando la consulta DNS sobre la interfaz loopback.

> Pendiente: incorporar las imágenes de las capturas dentro de una carpeta `capturas/` cuando estén disponibles como archivos para el repositorio.

## Conclusión

La práctica verifica el funcionamiento básico de un canal de comunicación basado en DNS en un entorno controlado. El cliente inserta información en formato hexadecimal dentro de un subdominio y el servidor extrae dicha información, la decodifica y responde con un registro DNS de tipo `A`. La captura en Wireshark confirma que la petición se transmite como una consulta DNS válida.

## Autor

Deivid Cardona
Ciclo Formativo ASIX - Módulo 037: Seguridad en servicios
