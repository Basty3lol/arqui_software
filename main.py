from clientes.login import Login
from clientes.reg import Register
from clientes.foro_cli import preguntas_foro
from clientes.cliente import catalogo
from clientes.clientecarrito import general, compras
from clientes.Productos import inventario_cli
from os import system


isAdmin = 0
correo = ""
carro_productos=[]

def main():
    global isAdmin, carro_productos, correo
    system("clear")
    while True:
        #system("cls")
        if isAdmin == 0:
            print("Que desea hacer?")
            print("1. Crear una nueva cuenta")
            print("2. Ingresar a una cuenta existente")
            print("3. Salir")
            try:
                opcion = int(input("Ingrese una opcion: ").strip())
                if opcion == 1:
                    print("Creando nueva cuenta")
                    x = Register()
                    print("Registro exitoso")
                    system('clear')
                elif opcion == 2:
                    print("Ingresando a una cuenta existente")
                    x, y = Login()
                    correo = y
                    isAdmin = int(x)
                    system('clear')
                elif opcion == 3:
                    print("Saliendo")
                    system('clear')
                    return
                else:
                    print("Opcion invalida")
            except:
                print("Opcion invalida")
        elif isAdmin == 1:
            print('Soy Admin')
            print("Que desea hacer?")
            print("1. Revisar productos")
            print("2. Entrar al Foro")
            print("3. Modificar inventario")
            print("4. Salir")
            try:
                opcion = int(input("Ingrese una opcion: ").strip())
                if opcion == 1:
                    catalogo()
                elif opcion == 2:
                    preguntas_foro(isAdmin,correo)
                    system('clear')
                elif opcion == 3:
                    inventario_cli()
                    system('clear')
                elif opcion == 4:
                    print("Saliendo")
                    return
                else:
                    print("Opcion invalida")
            except:
                print("Opcion invalida")
        elif isAdmin == 2:
            print('Soy Cliente')
            print("Que desea hacer?")
            print("1. Revisar productos")
            print("2. Carrito")
            print("3. Comprar articulos del carrito")
            print("4. Entrar al Foro")
            print("5. Salir")
            try:
                opcion = int(input("Ingrese una opcion: ").strip())
                if opcion == 1:
                    catalogo()
                elif opcion == 2:
                    carro_productos = general(carro_productos)
                    system('clear')
                elif opcion == 3:
                    carro_productos = compras(carro_productos, correo)
                elif opcion == 4:
                    preguntas_foro(isAdmin,correo)
                    system('clear')
                elif opcion == 5:
                    print("Saliendo")
                    return
                else:
                    print("Opcion invalida")
            except:
                print("Opcion invalida")
        elif isAdmin == 3:
            print("Soy Soporte")
            print("1. Entrar al Foro")
            print("2. Salir")
            try:
                opcion = int(input("Ingrese una opcion: ").strip())
                if opcion == 1:
                    preguntas_foro(isAdmin,correo)
                    system('clear')
                elif opcion == 2:
                    print("Saliendo")
                    return
                else:
                    print("Opcion invalida")
            except:
                print("Opcion invalida")
main()