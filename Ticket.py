from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import random
import string
import qrcode
from datetime import datetime, timedelta

ruta = "C:/Users/adria/OneDrive/Escritorio/Python/"

coordenadas_productos = [(50, 500), (50, 450), (50, 400), (50, 350), (50, 300)]

def obtener_datos_cliente():
    print("Ingresa los datos del cliente:")
    nombre_cliente = input("Nombre del cliente: ")
    direccion_cliente = input("Dirección del cliente: ")
    correo_cliente = input("Correo electrónico del cliente: ")

    return {"nombre_cliente": nombre_cliente, "direccion_cliente": direccion_cliente, "correo_cliente": correo_cliente}

def obtener_datos_compra():
    print("Opciones de productos disponibles: Papas, Coca, Galletas, Papel, Tortillas")

    productos = []
    productos_precargados = {
        "Papas": 17.00,
        "Coca": 40.00,
        "Galletas": 15.00,
        "Papel": 50.00,
        "Tortillas": 30.00
    }

    coordenadas_seleccionadas = []

    while True:
        nombre_producto = input("Ingresa el nombre del producto (o escribe 'fin' para terminar): ")
        if nombre_producto == 'fin':
            break

        if nombre_producto not in productos_precargados:
            print("Producto no válido. Por favor, elige uno de los productos disponibles.")
        else:
            cantidad = int(input(f"Ingresa la cantidad de {nombre_producto.capitalize()} que vas a comprar: "))
            precio_unitario = productos_precargados[nombre_producto]
            productos.append({"nombre": nombre_producto.capitalize(), "cantidad": cantidad, "precio_unitario": precio_unitario})

            coordenadas_seleccionadas.append(coordenadas_productos[len(productos) - 1])

    return {"productos": productos, "coordenadas_seleccionadas": coordenadas_seleccionadas}

def generar_numero_rastreo():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

def generar_fecha_entrega():
    return (datetime.now() + timedelta(days=3)).strftime("%d-%m-%Y")

def generar_codigo_qr(datos_compra, total_compra):
    codigo_rastreo = generar_numero_rastreo()
    fecha_entrega = generar_fecha_entrega()

    informacion = "Compraste:\n\n"
    for producto in datos_compra["productos"]:
        nombre = producto["nombre"]
        cantidad = producto["cantidad"]
        precio_total = producto["cantidad"] * producto["precio_unitario"]
        informacion += f"{cantidad} {nombre} con un total de ${precio_total:.2f}\n"

    informacion += f"\nTotal de la compra: ${total_compra:.2f}\n"
    informacion += f"Codigo de rastreo: {codigo_rastreo}\n"
    informacion += f"Fecha de entrega: {fecha_entrega}\n"
    informacion += f"Atendido por: Adriana Mata"

    img = qrcode.make(informacion)
    nombre_imagen = ruta + "miQR.png"
    f = open(nombre_imagen, "wb")
    img.save(f)
    f.close()


def generar_ticket_compra(datos_cliente, datos_compra):
    c = canvas.Canvas(ruta + "Ticket.pdf", pagesize=A4)

    c.setFont('Helvetica-Bold', 20)
    c.drawString(230, 780, "Ticket de Compra")

    # Datos del cliente
    c.setFont('Helvetica-Bold', 16)
    c.drawString(60, 700, "Cliente:")
    c.drawString(60, 670, "Dirección:")
    c.drawString(60, 640, "Correo electrónico:")
    c.setFont('Helvetica', 16)
    c.drawString(260, 700, datos_cliente["nombre_cliente"])
    c.drawString(260, 670, datos_cliente["direccion_cliente"])
    c.drawString(260, 640, datos_cliente["correo_cliente"])

    c.setFont('Helvetica-Bold', 16)
    c.drawString(60, 600, "Fecha:")
    formatted_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    c.drawString(260, 600, str(formatted_date))

    c.setFont('Helvetica-Bold', 16)
    c.drawString(260, 570, "Productos")
    h = 610
    x = 20
    y = h - 50
    c.setLineWidth(2)
    c.line(x, y, x + 550, y)

    c.setFont('Helvetica-Bold', 16)
    c.drawString(40, 540, "Cantidad")
    c.drawString(200, 540, "Nombre")
    c.drawString(310, 540, "PrecioUni")
    c.drawString(500, 540, "Total")
    h = 580
    x = 20
    y = h - 50
    c.setLineWidth(2)
    c.line(x, y, x + 550, y)

    total_compra = 0

    for i, producto in enumerate(datos_compra["productos"], start=1):
        cantidad = producto["cantidad"]
        nombre = producto["nombre"]
        precio_unitario = producto["precio_unitario"]
        precio_total = cantidad * precio_unitario

        total_compra += precio_total

        cantidad_str = str(cantidad).rjust(5)
        nombre_str = nombre.ljust(20)
        precio_unitario_str = f"${precio_unitario:.2f}".rjust(10)
        precio_total_str = f"${precio_total:.2f}".rjust(10)

        coordenada_x, coordenada_y = datos_compra["coordenadas_seleccionadas"][i - 1]
        c.setFont('Helvetica', 16)
        c.drawString(coordenada_x, coordenada_y, cantidad_str)
        c.drawString(coordenada_x + 130, coordenada_y, nombre_str)
        c.drawString(coordenada_x + 260, coordenada_y, precio_unitario_str)
        c.drawString(coordenada_x + 430, coordenada_y, precio_total_str)

    total_compra_str = f"${total_compra:.2f}".rjust(10)
    c.setFont('Helvetica-Bold', 16)
    c.drawString(350, h-(len(datos_compra["productos"])+1)*70, "Total:")
    c.drawString(500, h-(len(datos_compra["productos"])+1)*70, total_compra_str)

    generar_codigo_qr(datos_compra, total_compra)
    nombre_imagen = ruta + "miQR.png"
    c.drawImage(nombre_imagen, 80, 40, 150, 150)

    imagen = ruta + "Imagen.jpg"
    c.drawImage(imagen, 80, 750, 90, 90)

    c.save()

def main():
    try:
        datos_cliente = obtener_datos_cliente()
        datos_compra = obtener_datos_compra()
        generar_ticket_compra(datos_cliente, datos_compra)
        print("Ticket generado exitosamente.")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
