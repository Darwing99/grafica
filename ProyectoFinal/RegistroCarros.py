from camara import CamaraEscritorio
import pymysql
import tkinter as tk
import tkinter.messagebox
import traceback

def ventanaCarros():
    ventanacarros = tk.Tk()
    ventanacarros.title ("Registro de carros")
    ventanacarros.geometry ("1800x850+0+0")
    user = tk.StringVar(ventanacarros)
    tk.Label(ventanacarros, text = "Nombre:").place(x=60,y=40)
    caja1 = tk.Entry(ventanacarros, width=100, textvariable=user).place(x=60,y=80)


    direccion = tk.StringVar(ventanacarros)
    tk.Label(ventanacarros, text = "Direccion").place(x=60,y=120)
    caja2 = tk.Entry(ventanacarros, width=100, textvariable=direccion).place(x=60,y=160)


    mail = tk.StringVar(ventanacarros)
    tk.Label(ventanacarros, text = "Correo:").place(x=60,y=200)
    caja3 = tk.Entry(ventanacarros,width=100, textvariable=mail).place(x=60,y=240)
  



    def check_table(conn):
        try:
            cursor = conn.cursor()
            cursor.execute(""" CREATE TABLE IF NOT EXISTS personas (
                                            codigo integer PRIMARY KEY,
                                            nombre text NOT NULL,
                                            direccion text NOT NULL,
                                            correo text
                                        ); """
                        )
            cursor.execute("DELETE FROM personas WHERE 1")  # ? Borra todas las filas
            conn.commit()  

        except:
            traceback.print_exc()
            return False

        return True


    def get_data():
        codigo=0;
        usuario = user.get()
        direc = direccion.get()
        destino = mail.get()

        valid = True
        if not usuario:
            
            valid = False
        if not direc:
        
            valid = False
        if not destino:
        
            valid = False

        if valid:
            return codigo,usuario, direc, destino
        return None


    def InsertPersona(conn, data):
        try:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO personas (codigo, nombre, direccion, correo) VALUES(%s, %s, %s, %s)',(data))
            conn.commit()

        except:
            traceback.print_exc()
            return False

        return True


    def login():
        
        try:
            db= pymysql.connect(
                host="localhost", port=3306, user="root",
                passwd="", db="dbdatos"
                )
        
        except:
            traceback.print_exc()
            tk.messagebox.showinfo(title="Configuraci??n incorrecta",
                                message="NO HA SIDO POSIBLE CONECTARSE CON LA BD"
                                )
            return 

        if check_table(db):
            data = get_data()
            if data is not None:
                ins = InsertPersona(db, data)
                if ins:
                    tk.messagebox.showinfo(title="Configuraci??n correcta",
                                        message="DATOS ALMACENADOS CORRECTAMENTE"
                                        )
                else:
                    tk.messagebox.showinfo(title="Configuraci??n incorrecta",
                                        message="LOS DATOS NO HAN PODIDO SER ALMACENADOS"
                                        )
            else:
                tk.messagebox.showerror(title="Entrada inv??lida",
                                    message="TODOS LOS CAMPOS SON OBLIGATORIOS"
                                    )
        else:
            tk.messagebox.showerror(title="Configuraci??n incorrecta",
                                message="NO HA SIDO POSIBLE ACCEDER NI CREAR LA TABLA 'usuarios'"
                                )

        db.rollback()
        db.close()

    def FuncionCamara():
        CamaraEscritorio()

    tk.Button (text = "Guardar", width=40, command = login).place(x=60,y=280)
    tk.Button (text = "Encender Camara", width=40, command = FuncionCamara).place(x=900,y=80)
    ventanacarros.mainloop()
