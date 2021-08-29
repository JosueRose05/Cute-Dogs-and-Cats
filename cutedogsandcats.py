import requests
from tkinter import *
import  tkinter.font as tkFont
from PIL import ImageTk, Image
import time
import threading
from tkinter import messagebox

root = Tk()
root.title("Cute Dogs&Cats")
root.eval('tk::PlaceWindow . center')
root.geometry("500x500")
#Imagen del fondo (parque)
img_fondo = Image.open("fondo.jpg")
img_fondo = img_fondo.resize((500, 500), Image.ANTIALIAS)
img_fondo = ImageTk.PhotoImage(img_fondo)
background = Label(image = img_fondo, text = "Imagen S.O de fondo")
background.place(x = 0, y = 0, relwidth = 1, relheight = 1)
#Bandera para saber a que api hacemos la peticion
animalTk = IntVar()
animalTk.set(1)

def setAnimal(a):
    animalTk.set(a)
    
# Aqui debemos detener el hilo que hace las peticiones a las API, pero no se como :c
def on_closing():
    animalTk.set(0)
    root.destroy()
    print("Se cerro")

def run():
    global animalTk
    while animalTk.get() != 0:
        if animalTk.get() == 1:
            getDog()
        else:
            getCat()
        print(":)")
        time.sleep(1)

def getDog():
    global my_label
    banderajpg = False
    while not banderajpg:
        r = requests.get("https://random.dog/woof.json")
        if r.status_code == 200:
            results = r.json()
            if ".jpg" in results["url"]:   
                banderajpg = True
        else:
            print("La de perros no jala")
            return

    url = results["url"]
    with open("cuteanimal.jpg", "wb") as f:
        f.write(requests.get(url).content)

    my_label.grid_forget()
    img = Image.open("cuteanimal.jpg")
    img = img.resize((300, 300), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)

    my_label = Label(image=img)
    my_label.grid(row=3, column=0)
    my_label.image = img
    print("done")

def getCat():
    global my_label
    banderajpg = False
    while not banderajpg:
        r = requests.get("https://aws.random.cat/meow")
        if r.status_code == 200:
            results = r.json()
            if ".jpg" in results["file"]:   
                banderajpg = True
        else:
            #La API de los gatos suele fallar, volvemos a mostrar perritos mejor
            print("La API de gatos no funciona")
            response = messagebox.showwarning("F for the cats", "Sorry, but the cat API is not working :'c")
            setAnimal(1)
            return

    url = results["file"]
    with open("cuteanimal.jpg", "wb") as f:
        f.write(requests.get(url).content)

    img = Image.open("cuteanimal.jpg")
    img = img.resize((300, 300), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    
    my_label.grid_forget()
    my_label = Label(image=img)
    my_label.grid(row=3, column=0)
    my_label.image = img
    print("done")

fontStyle = tkFont.Font(family="Lucida Grande", size=20)
titulo_lbl = Label(root, text="Just Enjoy", font=fontStyle)
titulo_lbl.grid(row=0, column=0, padx=180, pady=10)

my_label = Label()
my_label.grid(row=2, column=0, rowspan=2)

Radiobutton(root, text="Dogs", variable=animalTk, value=1, command = lambda: setAnimal(1)).grid(row=4, column=0, pady=10)
Radiobutton(root, text="Cats", variable=animalTk, value=2, command = lambda: setAnimal(2)).grid(row=5, column=0)

root.protocol("WM_DELETE_WINDOW", on_closing)

response = messagebox.showwarning("F for the cats", "The cat API may not work :(")

hilo = threading.Thread(target=run)
hilo.start()

root.mainloop()