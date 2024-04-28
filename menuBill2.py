from components import Menu,Valida
from utilities import borrarPantalla,gotoxy
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color
from clsJson import JsonFile
from company  import Company
from customer import RegularClient,VipClient
from sales import Sale
from product  import Product
from iCrud import ICrud
import datetime
import time,os
from functools import reduce

path, _ = os.path.split(os.path.abspath(__file__))
# Procesos de las Opciones del Menu Facturacion
class CrudClients(ICrud):
    def create(self):
        borrarPantalla()
        gotoxy(2, 1)
        print(green_color + "=" * 90 + reset_color)
        gotoxy(2, 2)
        print(blue_color + "Registro de Cliente")
        gotoxy(2, 3)
        print(blue_color + "Empresa: Corporación el Rosado RUC: 0876543294001")
        gotoxy(2, 4)
        print(purple_color + "Seleccione el tipo de cliente:")
        gotoxy(2, 5)
        print("1) Cliente Regular")
        gotoxy(2, 6)
        print("2) Cliente VIP")
        tipo_cliente = input("Seleccione una opción: ")

        if tipo_cliente == "1":
            print("Cliente Regular")
            nombre = Valida.validar_nombre(input("Ingrese el nombre del cliente: "))
            apellido = Valida.validar_apellido(input("Ingrese el apellido del cliente: "))
            dni = Valida.validar_dni(input("Ingrese el DNI del cliente: "))
            card = input("¿El cliente tiene tarjeta de descuento? (s/n): ").lower() == "s"
            new_client = RegularClient(nombre, apellido, dni, card)
        elif tipo_cliente == "2":
            print("Cliente VIP")
            nombre = Valida.validar_nombre(input("Ingrese el nombre del cliente: "))
            apellido = Valida.validar_apellido(input("Ingrese el apellido del cliente: "))
            dni = Valida.validar_dni(input("Ingrese el DNI del cliente: "))
            new_client = VipClient(nombre, apellido, dni)
        else:
            print("Opción inválida")
            return

        json_file = JsonFile(path + '/archivos/clients.json')
        clients = json_file.read()
        clients.append(new_client.getJson())
        json_file.save(clients)
        print("Cliente registrado exitosamente!")
        time.sleep(2)

    def update(self):
        borrarPantalla()
        gotoxy(2, 1)
        print(green_color + "=" * 90 + reset_color)
        gotoxy(2, 2)
        print(blue_color + "Actualización de Cliente")
        gotoxy(2, 3)
        print(blue_color + "Empresa: Corporación el Rosado RUC: 0876543294001")
        dni =  Valida.validar_dni(input("Ingrese el DNI del cliente que desea actualizar: "))
        json_file = JsonFile(path + '/archivos/clients.json')
        clients = json_file.read()

        # Buscar el cliente por su DNI
        found = False
        updated_clients = []
        for client in clients:
            if client['dni'] == dni:
                found = True
                # Si se encuentra el cliente, solicitar nueva información
                gotoxy(2, 5)
                print("Cliente encontrado:")
                gotoxy(2, 6)
                print(f"Nombre: {client['nombre']}")
                gotoxy(2, 7)
                print(f"Apellido: {client['apellido']}")
                gotoxy(2, 8)
                print(f"DNI: {client['dni']}")
                print()
                # Solicitar nueva información para el cliente
                new_nombre = input("Ingrese el nuevo nombre del cliente (deje en blanco para mantener el mismo): ")
                new_apellido = input("Ingrese el nuevo apellido del cliente (deje en blanco para mantener el mismo): ")
                # Actualizar la información si se proporcionó
                if new_nombre:
                    client['nombre'] = new_nombre
                if new_apellido:
                    client['apellido'] = new_apellido
            updated_clients.append(client)

        if found:
            # Guardar los cambios en el archivo JSON
            json_file.save(updated_clients)
            print("Cliente actualizado exitosamente!")
        else:
            print("Cliente no encontrado.")
        time.sleep(2)

    def delete(self):
        borrarPantalla()
        gotoxy(2, 1)
        print(green_color + "=" * 90 + reset_color)
        gotoxy(2, 2)
        print(blue_color + "Eliminación de Cliente")
        gotoxy(2, 3)
        print(blue_color + "Empresa: Corporación el Rosado RUC: 0876543294001")
        dni = input("Ingrese el DNI del cliente que desea eliminar: ")
        json_file = JsonFile(path + '/archivos/clients.json')
        clients = json_file.read()

        filtered_clients = [client for client in clients if client['dni'] != dni]

        if len(filtered_clients) < len(clients):
            json_file.save(filtered_clients)
            print("Cliente eliminado, recuerde que tiene que salir utilizando las opciones para que los cambios sean guardados")
        else:
            print("Cliente no encontrado.")
        time.sleep(2)

    def consult(self):
        borrarPantalla()
        gotoxy(2, 1)
        print(green_color + "=" * 90)
        gotoxy(2, 2)
        print("==" + " " * 34 + "Consulta de Cliente" + " " * 35 + "==")
        gotoxy(2, 4)
        dni = input("Ingrese DNI del cliente: ")
        json_file = JsonFile(path + '/archivos/clients.json')
        clients = json_file.find("dni", dni)

        if clients:
            client = clients[0]
            gotoxy(2, 6)
            print(f"Nombre: {client['nombre']}")
            gotoxy(2, 7)
            print(f"Apellido: {client['apellido']}")
            gotoxy(2, 8)
            print(f"DNI: {client['dni']}")
        else:
            print("Cliente no encontrado.")
        input("Presione una tecla para continuar...")
        
class CrudProducts(ICrud):
    def create(self):
        borrarPantalla()
        gotoxy(2, 1)
        print(green_color + "=" * 90 + reset_color)
        gotoxy(2, 2)
        print(blue_color + "Registro de Producto")
        gotoxy(2, 3)
        descrip = Valida.solo_letras(input("Ingrese la descripción del producto: "))
        preci = Valida.solo_decimales(float(input("Ingrese el precio del producto: ")))
        stock = Valida.solo_enteros(input("Ingrese el stock inicial del producto -----solo nueros enteros o mayores que 0 ----: "))
        
        json_file = JsonFile(path + '/archivos/products.json')
        products = json_file.read()
        
        # Obtener el último ID utilizado
        last_id = max([product['id'] for product in products]) if products else 0
        
        # Verificar si el producto ya existe
        existing_product = next((product for product in products if product['descripcion'] == descrip), None)
        
        if existing_product:
            print("El producto ya existe:")
            print(f"ID: {existing_product['id']}, Descripción: {existing_product['descripcion']}, Precio: {existing_product['precio']}, Stock: {existing_product['stock']}")
            actualizar = input("¿Desea actualizar este producto? (s/n): ").lower()
            if actualizar == 's':
                # Actualizar el producto existente
                id_producto = existing_product['id']
                descrip = input(f"Ingrese la nueva descripción del producto (actual: {existing_product['descripcion']}): ")
                preci = float(input(f"Ingrese el nuevo precio del producto (actual: {existing_product['precio']}): "))
                stock = int(input(f"Ingrese el nuevo stock del producto (actual: {existing_product['stock']}): "))
                
                existing_product['descripcion'] = descrip if descrip else existing_product['descripcion']
                existing_product['precio'] = preci if preci else existing_product['precio']
                existing_product['stock'] = stock if stock else existing_product['stock']
                
                # Guardar los cambios en el archivo JSON
                json_file.save(products)
                print("Producto actualizado exitosamente!")
            else:
                print("Registro cancelado.")
        else:
            # Crear un nuevo producto con un nuevo ID único
            new_id = last_id + 1
            new_product = Product(id=new_id, descrip=descrip, preci=preci, stock=stock)
            products.append(new_product.getJson())
            json_file.save(products)
            print("Producto registrado exitosamente!")
        time.sleep(2)


    def update(self):
        borrarPantalla()
        gotoxy(2, 1)
        print(blue_color + "Empresa: Corporación el Rosado RUC: 0876543294001")
        gotoxy(2, 2)
        gotoxy(2, 3)
        print(blue_color + "Actualización de Producto")
        gotoxy(2, 4)
        print(green_color + "=" * 90 + reset_color)
        gotoxy(2, 5)
        id_producto = int(input("Ingrese el ID del producto que desea actualizar: "))
        json_file = JsonFile(path + '/archivos/products.json')
        products = json_file.read()

        # Buscar el producto por su ID
        found = False
        updated_products = []
        for product in products:
            if product['id'] == id_producto:
                found = True
                # Si se encuentra el producto, solicitar nueva información
                descrip = input(f"Ingrese la nueva descripción del producto (actual: {product['descripcion']}): ")
                preci = float(input(f"Ingrese el nuevo precio del producto (actual: {product['precio']}): "))
                stock = int(input(f"Ingrese el nuevo stock del producto (actual: {product['stock']}): "))
                # Actualizar la información si se proporcionó
                product['descripcion'] = descrip if descrip else product['descripcion']
                product['precio'] = preci if preci else product['precio']
                product['stock'] = stock if stock else product['stock']
            updated_products.append(product)

        if found:
            # Guardar los cambios en el archivo JSON
            json_file.save(updated_products)
            print("Producto actualizado exitosamente!")
        else:
            print("Producto no encontrado.")
        time.sleep(2)

    def delete(self):
        borrarPantalla()
        gotoxy(2, 1)
        print(blue_color + "Empresa: Corporación el Rosado RUC: 0876543294001")
        gotoxy(2, 2)
        gotoxy(2, 3)
        print(blue_color + "Eliminación de Producto")
        gotoxy(2, 4)
        print(green_color + "=" * 90 + reset_color)
        id_producto = int(input("Ingrese el ID del producto que desea eliminar: "))
        json_file = JsonFile(path + '/archivos/products.json')
        products = json_file.read()

        filtered_products = [product for product in products if product['id'] != id_producto]

        if len(filtered_products) < len(products):
            json_file.save(filtered_products)
            print("Producto eliminado exitosamente!")
        else:
            print("Producto no encontrado.")
        time.sleep(2)

    def consult(self):
      borrarPantalla()
      gotoxy(2, 1)
      print(blue_color + "Empresa: Corporación el Rosado RUC: 0876543294001")
      gotoxy(2, 2)
      print(blue_color + "Consulta de Productos")
      gotoxy(2, 3)
      print(green_color + "=" * 90 + reset_color)
      json_file = JsonFile(path + '/archivos/products.json')
      products = json_file.read()

      if products:
        print("""ID   Descripción   Precio   Stock""")
        for product in products:
            print(f"""{product['id']} {product['descripcion']} {product['precio']} {product['stock']}""")

        # Opción de búsqueda por descripción
        search_term = input("Ingrese la descripción del producto a buscar (o dejar en blanco para omitir): ").strip()
        if search_term:
            found = False
            for product in products:
                if search_term.lower() in product['descripcion'].lower():
                    found = True
                    print(f"ID: {product['id']}, Descripción: {product['descripcion']}, Precio: {product['precio']}, Stock: {product['stock']}")
            if not found:
                print("No se encontraron productos con esa descripción.")
      else:
         print("No hay productos registrados.")

      input("Presione una tecla para continuar...")

class CrudSales(ICrud):
    def create(self):
        # cabecera de la venta
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Registro de Venta")
        gotoxy(17,3);print(blue_color+Company.get_business_name())
        gotoxy(5,4);print(f"Factura#:F0999999 {' '*3} Fecha:{datetime.datetime.now()}")
        gotoxy(66,4);print("Subtotal:")
        gotoxy(66,5);print("Decuento:")
        gotoxy(66,6);print("IVA     :")
        gotoxy(66,7);print("Total   :")
        gotoxy(15,6);print("Cedula:")
        dni=Valida.solo_numeros3("Error: en este campo solo se ingresan numeros",23,6)      
        json_file = JsonFile(path+'/archivos/clients.json')
        client = json_file.find("dni",dni)
        if not client:
            gotoxy(35,6);print("Cliente no existente")
            return
        client = client[0]
        cli = RegularClient(client["nombre"],client["apellido"], client["dni"], card=True) 
        sale = Sale(cli)
        gotoxy(2, 6); print(cli.fullName(), end="")
        gotoxy(2, 8); print(green_color + "*" * 90 + reset_color, end="")
        gotoxy(5, 9); print(purple_color + "Linea", end="")
        gotoxy(12, 9); print("Id_Articulo", end="")
        gotoxy(24, 9); print("Descripcion", end="")
        gotoxy(38, 9); print("Precio", end="")
        gotoxy(48, 9); print("Cantidad", end="")
        gotoxy(58, 9); print("Subtotal", end="")
        gotoxy(70, 9); print("n->Terminar Venta)" + reset_color, end="")
        # detalle de la venta
        follow ="s"
        line=1
        while follow.lower()=="s":
            gotoxy(7,9+line);print(line)
            gotoxy(15,9+line);
            id=int(Valida.solo_numeros3("Error: Solo numeros",15,9+line))
            json_file = JsonFile(path+'/archivos/products.json')
            prods = json_file.find("id",id)
            if not prods:
                gotoxy(24,9+line);print("Producto no existente o no en stock")
                time.sleep(1)
                gotoxy(24,9+line);print(" "*20)
            else:    
                prods = prods[0]
                product = Product(prods["id"],prods["descripcion"],prods["precio"],prods["stock"])
                gotoxy(24,9+line);print(product.descrip)
                gotoxy(38,9+line);print(product.preci)
                gotoxy(49,9+line);qyt=int(Valida.solo_numeros3("Error:Solo numeros",49,9+line))
                gotoxy(59,9+line);print(product.preci*qyt)
                sale.add_detail(product,qyt)
                gotoxy(76,4);print(round(sale.subtotal,2))
                gotoxy(76,5);print(round(sale.discount,2))
                gotoxy(76,6);print(round(sale.iva,2))
                gotoxy(76,7);print(round(sale.total,2))
                gotoxy(74,9+line);follow=input() or "s"  
                gotoxy(76,9+line);print(green_color+"✓"+reset_color)  
                line += 1
        gotoxy(15,9+line);print(red_color+"Esta seguro de grabar la venta(s/n):")
        gotoxy(54,9+line);procesar = input().lower()
        if procesar == "s":
            gotoxy(15,10+line);print(" Venta guardada "+reset_color)
            # print(sale.getJson())  
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            ult_invoices = invoices[-1]["factura"]+1
            data = sale.getJson()
            data["factura"]=ult_invoices
            invoices.append(data)
            json_file = JsonFile(path+'/archivos/invoices.json')
            json_file.save(invoices)
        else:
            gotoxy(20,10+line);print(" Venta no finalizada "+reset_color)    
        time.sleep(2)    
     
    def update(self):
        borrarPantalla()
        gotoxy(2, 1)
        print(green_color + "=" * 90 + reset_color)
        gotoxy(30, 2)
        print(blue_color + "Actualización de Venta")
        gotoxy(17, 3)
        print(blue_color + Company.get_business_name())
        invoice_number = input("Ingrese el número de factura que desea actualizar: ")
        json_file = JsonFile(path + '/archivos/invoices.json')
        invoices = json_file.read()

        if invoices:
            # Buscar la factura específica
            for invoice in invoices:
                if invoice["factura"] == int(invoice_number):
                    cliente = invoice["cliente"]
                    gotoxy(2, 5)
                    print(f"Número de Factura: {invoice['factura']}")
                    print(f"Fecha: {invoice['Fecha']}")
                    print(f"Cliente: {cliente}")
                    print(f"Total: {invoice['total']}")
                    print("\nDetalle de la Venta:")
                    detalles = invoice['detalle']
                    for i, detalle in enumerate(detalles, start=1):
                        print(f"{detalle['poducto']}: {detalle['cantidad']} x {detalle['precio']}")
                    print(green_color + "=" * 90 + reset_color)

                    # Opciones para modificar la factura
                    while True:
                        print("\nOpciones:")
                        print("1. Modificar cantidad de un producto")
                        print("2. Eliminar un producto")
                        print("3. Agregar un nuevo producto")
                        print("4. Terminar los cambios")
                        option = input("Seleccione una opción: ")

                        if option == "1":
                            # Modificar cantidad de un producto en la factura
                            detalle_index = int(input("Ingrese el número de línea del detalle que desea modificar: ")) - 1
                            if 0 <= detalle_index < len(detalles):
                                new_quantity = int(input("Ingrese la nueva cantidad: "))
                                detalles[detalle_index]['cantidad'] = new_quantity
                                print("Cantidad modificada .")
                            else:
                                print("Número de línea inválido.")
                        elif option == "2":
                            # Eliminar un producto de la factura
                            detalle_index = int(input("Ingrese el número de línea del detalle que desea eliminar: ")) - 1
                            if 0 <= detalle_index < len(detalles):
                                del detalles[detalle_index]
                                print("Producto eliminado .")
                            else:
                                print("Número de línea inválido.")
                        elif option == "3":
                            # Agregar un nuevo producto a la factura
                            product_id = int(input("Ingrese el ID del nuevo producto: "))
                            product_quantity = int(input("Ingrese la cantidad del nuevo producto: "))
                            json_file_products = JsonFile(path + '/archivos/products.json')
                            products = json_file_products.find("id", product_id)
                            if products:
                                product = products[0]
                                new_product = {
                                    'poducto': product['descripcion'],
                                    'precio': product['precio'],
                                    'cantidad': product_quantity
                                }
                                detalles.append(new_product)
                                print("Producto agregado correctamente.")
                            else:
                                print("Producto no encontrado.")
                        elif option == "4":
                            print("Actualización de factura terminada.")
                            # Guardar los cambios en el archivo JSON
                            invoice['detalle'] = detalles
                            json_file.save(invoices)
                            break
                        else:
                            print("Opción inválida. Intente nuevamente.")
                    break
            else:
                print("Factura no encontrada.")
        else:
            print("No hay facturas disponibles.")
        input("Presione una tecla para continuar...")
        
    def delete(self):
        borrarPantalla()
        gotoxy(2, 1)
        print(green_color + "=" * 90 + reset_color)
        gotoxy(30, 2)
        print(blue_color + "Eliminación de Venta")
        gotoxy(17, 3)
        print(blue_color + Company.get_business_name())
        invoice_number = input("Ingrese el número de factura que desea eliminar: ")
        json_file = JsonFile(path + '/archivos/invoices.json')
        invoices = json_file.read()

        # Buscar la factura específica
        found = False
        updated_invoices = []
        for invoice in invoices:
            if invoice["factura"] == int(invoice_number):
                found = True
                # Mostrar la factura antes de eliminarla
                print(f"Factura encontrada:")
                print(f"Número de Factura: {invoice['factura']}")
                print(f"Fecha: {invoice['Fecha']}")
                print(f"Cliente: {invoice['cliente']}")
                print(f"Total: {invoice['total']}")
                print("\nDetalle de la Venta:")
                for detalle in invoice['detalle']:
                    print(f"{detalle['poducto']}: {detalle['cantidad']} x {detalle['precio']}")
                print(green_color + "=" * 90 + reset_color)

                # Confirmar la eliminación
                confirmacion = input("¿Está seguro que desea eliminar esta factura? (s/n): ").lower()
                if confirmacion == "s":
                    print("Factura eliminada exitosamente.")
                else:
                    print("Eliminación cancelada.")
            else:
                updated_invoices.append(invoice)

        if not found:
            print("Factura no encontrada.")

        # Guardar los cambios en el archivo JSON
        json_file.save(updated_invoices)
        time.sleep(2)
    def consult(self):
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta de Venta"+" "*35+"██")
        gotoxy(2,4);invoice= input("Ingrese Factura: ")
        if invoice.isdigit():
            invoice = int(invoice)
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.find("factura",invoice)
            print(f"Impresion de la Factura#{invoice}")
            print(invoices)
        else:    
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            print("Consulta de Facturas")
            for fac in invoices:
                print(f"{fac['factura']}   {fac['Fecha']}   {fac['cliente']}   {fac['total']}")
            
            suma = reduce(lambda total, invoice: round(total+ invoice["total"],2), 
            invoices,0)
            totales_map = list(map(lambda invoice: invoice["total"], invoices))
            total_client = list(filter(lambda invoice: invoice["cliente"] == "Dayanna Vera", invoices))

            max_invoice = max(totales_map)
            min_invoice = min(totales_map)
            tot_invoices = sum(totales_map)
            print("filter cliente: ",total_client)
            print(f"map Facturas:{totales_map}")
            print(f"              max Factura:{max_invoice}")
            print(f"              min Factura:{min_invoice}")
            print(f"              sum Factura:{tot_invoices}")
            print(f"              reduce Facturas:{suma}")
        x=input("Presione una tecla para continuar...")    

#Menu Proceso Principal
opc=''
while opc !='4':  
    borrarPantalla()      
    menu_main = Menu("Menu Facturacion",["1) Clientes","2) Productos","3) Ventas","4) Salir"],20,10)
    opc = menu_main.menu()
    if opc == "1":
        opc1 = ''
        while opc1 !='5':
            borrarPantalla()    
            menu_clients = Menu("Menu Cientes",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc1 = menu_clients.menu()
            if opc1 == "1":
                crud_clients = CrudClients()
                crud_clients.create()
            elif opc1 == "2":
                crud_clients = CrudClients()
                crud_clients.update()
            elif opc1 == "3":
                crud_clients = CrudClients()
                crud_clients.delete()
            elif opc1 == "4":
                crud_clients = CrudClients()
                crud_clients.consult()
            print("Regresando al menu Clientes...")
            # time.sleep(2)            
    elif opc == "2":
        opc2 = ''
        while opc2 !='5':
            borrarPantalla()    
            menu_products = Menu("Menu Productos",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc2 = menu_products.menu()
            if opc2 == "1":
                crudProducts = CrudProducts()
                crudProducts.create()
            elif opc2 == "2":
                crudProducts = CrudProducts()
                crudProducts.update()
            elif opc2 == "3":
                crudProducts = CrudProducts()
                crudProducts.delete()
            elif opc2 == "4":
                crudProducts = CrudProducts()
                crudProducts.consult()
    elif opc == "3":
        opc3 =''
        while opc3 !='5':
            borrarPantalla()
            sales = CrudSales()
            menu_sales = Menu("Menu Ventas",["1) Registro Venta","2) Consultar","3) Modificar","4) Eliminar","5) Salir"],20,10)
            opc3 = menu_sales.menu()
            if opc3 == "1":
                sales.create()
            elif opc3 == "2":
                sales.consult()
                time.sleep(2)
            elif opc3 == "3":
                sales.update()
                
            elif opc3 == "4":
                sales.delete()
     
    print("Regresando al menu Principal...")
    # time.sleep(2)            

borrarPantalla()
input("Presione cualquier tecla para salir de la terminal ")
borrarPantalla()
