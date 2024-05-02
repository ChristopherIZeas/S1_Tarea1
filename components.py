from utilities import borrarPantalla, gotoxy
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color
import time

class Menu:
    def __init__(self,titulo="",opciones=[],col=6,fil=1):
        self.titulo=titulo
        self.opciones=opciones
        self.col=col
        self.fil=fil
        
    def menu(self):
        gotoxy(self.col,self.fil);print(self.titulo)
        self.col-=5
        for opcion in self.opciones:
            self.fil +=1
            gotoxy(self.col,self.fil);print(opcion)
        gotoxy(self.col+5,self.fil+2)
        opc = input(f"Elija opcion[1...{len(self.opciones)}]: ") 
        return opc   

class Valida:
    def solo_enteros(stock):
        while True:
            stock = int(stock)
            if stock > 0 and stock == float(stock):
                return stock
            else:
                print("El stock debe ser un número entero mayor que 0 o no decimal")

                
    def solo_letras(descrip):
        while True:
            if descrip.isalpha():
                return descrip.capitalize()
            else:
                print("| El campo solo puede contener letras.")
                time.sleep(1)
                descrip=input("Ingrese la descripcion correctamente ")

    def solo_decimales(preci):
        while True:
            preci = float(preci)
            if preci > float(0):
                 break
        return preci

    def validar_nombre(nombre):
        while True:
            if nombre.isalpha():
                return nombre.capitalize()
            else:
                print(purple_color + "El campo solo puede contener letras.")
                time.sleep(1)
                nombre = input("Ingrese el dato correctamente o este mensaje se repetira: ")
    def validar_apellido(apellido):
        while True:
            if apellido.isalpha():
                return apellido.capitalize()
            else:
                print(purple_color + "El campo solo puede contener letras.")
                time.sleep(1)
                apellido = input("Ingrese el dato correctamente o este mensaje se repetira: ")
                 
    def validar_numeros(frase):
        while True:
            print(blue_color + f"{frase}")
            numero = input(purple_color)
            if numero.isdigit():
                return numero
            else:
                print(purple_color + "El campo solo puede contener números.")
                time.sleep(1)
                print(" " * 40)
    def validar_numeros_decimales(frase):
        while True:
            print(blue_color + f"{frase}")
            numero = input(purple_color)
            try:
                numero = float(numero)
                return numero
            except ValueError:
                print(purple_color + "El campo debe ser un número decimal.")
                time.sleep(1)
                print(" " * 40)
    def solo_numeros3(mensaje_error, col, fil):
        while True: 
            gotoxy(col, fil)            
            valor = input()
            try:
                if int(valor) > 0:
                    break
            except:
                gotoxy(col, fil)
                print(mensaje_error)
                time.sleep(1)
                gotoxy(col, fil)
                print(" "*20)
        return valor
    
    def validar_dni(dni):
        while True:
            if len(dni) < 10:
                print(purple_color + "El DNI debe tener al menos 10 caracteres.")
                dni = input("Ingrese el DNI del cliente: ")
            else:
                if dni.isdigit():
                    coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
                    suma = 0
                    for i in range(9):
                        digito = int(dni[i]) * coeficientes[i]
                        if digito > 9:
                            digito -= 9
                        suma += digito
                    total = suma % 10
                    if total != 0:
                        total = 10 - total
                    else:
                        total = 0  # Valor predeterminado si total == 0
                    if total == int(dni[9]):
                        return dni
                print(purple_color + "El formato del DNI es incorrecto.")
                dni = input("Ingrese el DNI del cliente: ")

        
class otra:
    pass    

if __name__ == '__main__':
    # instanciar el menu
    opciones_menu = ["1. Entero", "2. Letra", "3. Decimal"]
    menu = Menu(titulo="-- Mi Menú --", opciones=opciones_menu, col=10, fil=5)
    # llamada al menu
    opcion_elegida = menu.menu()
    print("Opción escogida:", opcion_elegida)
    valida = Valida()
    if(opciones_menu==1):
      numero_validado = valida.solo_numeros("Mensaje de error", 10, 10)
      print("Número validado:", numero_validado)
    
    numero_validado = valida.solo_numeros("Mensaje de error", 10, 10)
    print("Número validado:", numero_validado)
    
    letra_validada = valida.solo_letras("Ingrese una letra:", "Mensaje de error")
    print("Letra validada:", letra_validada)
    
    decimal_validado = valida.solo_decimales("Ingrese un decimal:", "Mensaje de error")
    print("Decimal validado:", decimal_validado)