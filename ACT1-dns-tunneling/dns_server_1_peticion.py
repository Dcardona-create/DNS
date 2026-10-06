#!/usr/bin/python3
# Archivo ....: dns_server_1.py
# Autor ......: Gabriel Martí
# Fecha ......: 20/12/2022
# Descripción : Programa que simula escuchar peticiones DNS que recibirá de un cliente específico,
#               Siempre responde a las peticiones DNS con la misma respuesta.
#               Muestra en pantalla el nombre de subdominio recibido.
#
#               Todo el código está basado en el uso de la libreria "dnslib"
#               https://pypi.org/project/dnslib/


import socket
import dns.message
import dns.name
import dns.rdata
import dns.rdataclass
import dns.rdatatype
import dns.rrset

# Declaración de variables
servidor = "0.0.0.0"        # Escucha en todos los adaptadores
puerto = 53                 # Puerto 53 DNS
buffer = 4096               # Tamaño buffer
dominio = "secreto.com."    # Nombre de dominio absoluto para la respuesta (acaba con punto)
ip_respuesta = "4.3.2.1"    # IP falsa de respuesta de ejemplo

# Crear un socket servidor UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((servidor, puerto))

print("Esperando 1 peticion DNS...")

while True:
    # Recibir una petición del cliente
    request_data, client_address = server_socket.recvfrom(buffer)

    # Deserializar la petición
    request = dns.message.from_wire(request_data)

    print("Recibida petición DNS")
    print(request)

    # Extraer el nombre de dominio completo de la petición
    full_domain_name = request.question[0].name.to_text()
    print("Nombre dominio completo: " + full_domain_name)
    # Extraer la parte del nombre de subdominio
    subdomain = full_domain_name.split(".")[0]
    print("Subdominio recibido: "+subdomain)

    try:
        # Convierte nombre de subdominio en hexadecimal a los datos reales
        datosreales = bytes.fromhex(subdomain).decode()
        print("Mensaje oculto recibido: "+datosreales)
    except Exception as e:
        print("No hay datos en hexadecimal")

    # Prepara la respuesta DNS
    response = dns.message.make_response(request)   # Crea respuesta vacía
    response.id = request.id                        # ID de la respuesta igual al de la petición
    response.set_rcode(dns.rcode.NOERROR)           # Establecer el campo rcode como NOERROR

    # Añade la respuesta a la petición con el dato del dominio ficticio
    # Es importante tener en cuenta que aquí el nombre del dominio es absoluto,
    # eso significa que el nombre de dominio acaba con un punto.
    response.answer.append(dns.rrset.from_text(dominio,
                                               300,
                                               dns.rdataclass.IN,
                                               dns.rdatatype.A,
                                               ip_respuesta))

    # Serializar la respuesta
    response_data = response.to_wire()

    # Enviar la respuesta al cliente
    server_socket.sendto(response_data, client_address)

    # Como este ejemplo solo espera una petición
    # rompe el bucle infinito y finaliza
    break


