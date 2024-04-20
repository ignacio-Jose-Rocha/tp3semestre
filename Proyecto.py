import os
import re
class Contacto:
    def __init__(self, nombre, telefono, email):
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.favorito = False

    def __str__(self):
        return f"Nombre: {self.nombre}, Teléfono: {self.telefono}, Email: {self.email}"

class Agenda:
    def __init__(self):
        self.contactos = []

    def validarNumero(self, telefono):
        while not telefono.isdigit():
            print("El número de teléfono debe contener numeros")
            telefono = input("Ingrese el número de teléfono del contacto: ")
        return float(telefono)
        
    def agregar_contacto(self):
        while True:
            nombre = input("Ingrese el nombre del contacto: ")
            telefono = input("Ingrese el número de teléfono del contacto: ")
            self.validarNumero(telefono)
            email = input("Ingrese el email del contacto: ")
            
            if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                nuevo_contacto = Contacto(nombre, telefono, email)
                
                exists = any(contacto.nombre == nombre or contacto.email == email or contacto.telefono == telefono for contacto in self.contactos)
                if exists:
                    print("El contacto ya existe.")
                    return False
                else:
                    favorito = input("¿Desea marcar el contacto como favorito? (s/n): ").lower()
        
                    if favorito == "s":
                        nuevo_contacto.favorito = True
                    elif favorito == "n":
                        nuevo_contacto.favorito = False
                    self.contactos.append(nuevo_contacto)
                    print("Contacto agregado correctamente.")
                    self.guardar_agenda()
                    return True
            else:
                print("El formato del correo electrónico no es válido. Por favor, inténtelo nuevamente.")
            
    def mostrar_contactos(self):
        if self.contactos:
            orden = input("¿Cómo desea ordenar los contactos? (nombre/email): ").lower()
            if orden == "nombre":
                contactos_ordenados = sorted(self.contactos, key=lambda x: x.nombre.lower())
            elif orden == "email":
                contactos_ordenados = sorted(self.contactos, key=lambda x: x.email.lower())
            else:
                print("Opción inválida. Mostrando contactos sin orden.")
                contactos_ordenados = self.contactos

            for index, contacto in enumerate(contactos_ordenados, start=1):
                if  contacto.favorito:
                    print(f"{index}. {contacto} (Favorito)")
                else:
                    print(f"{index}. {contacto}")
                
        else:
            print("No hay contactos en la agenda.")
    def mostrar_contactos2(self):
        if self.contactos:
            contactos_ordenados = sorted(self.contactos, key=lambda x: x.nombre.lower())
            for index, contacto in enumerate(contactos_ordenados, start=1):
                if  contacto.favorito:
                    print(f"{index}. {contacto} (Favorito)")
                else:
                    print(f"{index}. {contacto}")

        else:
            print("No hay contactos en la agenda.")

    def buscar_contacto(self):
        self.mostrar_contactos2()
        posicion = int(input("Ingrese la posición del contacto que desea buscar: "))
        if 1 <= posicion <= len(self.contactos):
                contacto = self.contactos[posicion - 1]
                if(contacto.favorito):
                    print(f"{contacto} (Favorito)")
                else:
                    print(f"{contacto}")
        else:
                print("Posición inválida.")
        return None

    def eliminar_contacto(self, nombre):

        contacto = self.buscar_contacto(nombre)
        if contacto:
            self.contactos.remove(contacto)
            print(f"El contacto {nombre} ha sido eliminado.")
            self.guardar_agenda()
        else:
            print("Contacto no encontrado.")

    def editar_contacto(self):
        self.mostrar_contactos2()
        opcion = input("Seleccione el número del contacto que desea editar: ")
        try:
            opcion = int(opcion)
            if 1 <= opcion <= len(self.contactos):
                contacto = self.contactos[opcion - 1]
                print("Editar contacto:")
                nuevo_nombre = input(f"Nuevo nombre ({contacto.nombre}): ") or contacto.nombre
                nuevo_telefono = input(f"Nuevo teléfono ({contacto.telefono}): ") or contacto.telefono
                nuevo_email = input(f"Nuevo email ({contacto.email}): ") or contacto.email
                favorito = input("¿Desea marcar el contacto como favorito? (s/n): ").lower()
                
                contacto.nombre = nuevo_nombre
                contacto.telefono = nuevo_telefono
                contacto.email = nuevo_email
                if favorito == "s":
                    contacto.favorito = True
                elif favorito == "n":
                    contacto.favorito = False
                print("Contacto actualizado correctamente.")
            else:
                print("Opción inválida.")
        except ValueError:
            print("Opción inválida.")

    def guardar_agenda(self):
        contactos_guardados = set()
        with open("agenda.txt", "w") as file:
            for contacto in self.contactos:
                if contacto.nombre not in contactos_guardados:
                    file.write(f"{contacto.nombre},{contacto.telefono},{contacto.email},{contacto.favorito}\n")
                    contactos_guardados.add(contacto.nombre)
                else:
                    print(f"El contacto {contacto.nombre} ya existe en la agenda y no se ha guardado nuevamente.")

    def cargar_agenda(self):
        if os.path.exists("agenda.txt"):
            with open("agenda.txt", "r") as file:
                for line in file:
                    nombre, telefono, email, favorito = line.strip().split(',')
                    favorito = favorito.lower() == 'true'
                    contacto = Contacto(nombre, telefono, email)
                    contacto.favorito = favorito
                    self.contactos.append(contacto)
        else:
            print("No hay agenda para cargar.")

def menu():
    print("\n1. Agregar contacto")
    print("2. Mostrar contactos")
    print("3. Buscar contacto")
    print("4. Eliminar contacto")
    print("5. Editar contacto")
    print("6. salir")

def main():
    agenda = Agenda()
    agenda.cargar_agenda()

    while True:
        menu()
        opcion = input("Ingrese el número de la opción que desea realizar: ")

        if opcion == '1':
            
            if agenda.agregar_contacto():
                agenda.guardar_agenda()
        elif opcion == '2':
            agenda.mostrar_contactos()
        elif opcion == '3':
            agenda.buscar_contacto()
        elif opcion == '4':
            agenda.mostrar_contactos2()
            nombre = input("Ingrese el nombre del contacto que desea eliminar: ")
            agenda.eliminar_contacto(nombre)
            agenda.guardar_agenda()
        elif opcion == '5':

            agenda.editar_contacto()
            agenda.guardar_agenda()
        elif opcion == '6':
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Por favor, ingrese un número del 1 al 6.")

if __name__ == "__main__":
    main()