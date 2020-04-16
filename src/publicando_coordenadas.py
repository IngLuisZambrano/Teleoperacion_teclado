#!/usr/bin/env python
# coding: utf-8
import rospy
from ik import *
import tkMessageBox
from Tkinter import *
from proyecto_delta.msg import posicion

global x, y, z, delta, deltaz

def principal():
    global x, y, z, delta, deltaz
    pub = rospy.Publisher('coordenadas', posicion, queue_size=10) 
    rospy.init_node('pub_posicion', anonymous=True) #inicia el nodo publicador
    rate = rospy.Rate(10) #Hz
    vp = Tk()
    vp.title("Teleoperación Local")
    vp.geometry("400x200+0+0")
    vp.resizable(0, 0)
    # Configuración de Frame1
    frame1 = Frame(vp, width = 400, height = 400 )
    frame1.pack(side = "left", anchor = "n")
    frame1.config(bg="#86f1ef", cursor="hand2")
    canvas = Canvas(vp, width = 400, height = 400)
    canvas.pack()
    # Configuración de Barra de Menùs    
    barraMenu = Menu(vp)
    vp.config(menu = barraMenu, width = 10, height = 2)
    ayudaMenu = Menu(barraMenu)
    barraMenu.add_cascade(label = "Ayuda", menu = ayudaMenu)

    tc3 = Label(frame1, bg = "#86f1ef")
    tc3.grid(row = 0, column = 0, padx = 2, pady = 1)
    tc4 = Label(frame1, bg = "#86f1ef")
    tc4.grid(row = 14, column = 0, padx = 2, pady = 1)

    te1 = Label(frame1, text = "Px", bg = "#86f1ef", font=("Comic Sans MS", 10))
    te1.grid(row = 3, column = 0, sticky = "w", pady = 0, padx = 20)
    te1.config(cursor = "pirate")
    td1 = Label(frame1, bg = "#ffffff", width = 20 )
    td1.grid(row = 4, column = 0, sticky = "e", pady = 1, padx = 20)
    td1.config(fg = "blue", justify = "center")

    te1r = Label(frame1, text = "theta1", bg = "#86f1ef", font=("Comic Sans MS", 10))
    te1r.grid(row = 3, column = 1, sticky = "w", pady = 0, padx = 20)
    te1r.config(cursor = "pirate")
    td1r = Label(frame1, bg = "#ffffff", width = 20 )
    td1r.grid(row = 4, column = 1, sticky = "e", pady = 1, padx = 20)
    td1r.config(fg = "blue", justify = "center")

    te2 = Label(frame1, text = "Py", bg = "#86f1ef", font=("Comic Sans MS", 10))
    te2.grid(row = 6, column = 0, sticky = "w", pady = 0, padx = 20)
    te2.config(cursor = "pirate")
    td2 = Label(frame1, bg = "#ffffff", width = 20 )
    td2.grid(row = 7, column = 0, sticky = "e", pady = 1, padx = 20)
    td2.config(fg = "blue", justify = "center")

    te2r = Label(frame1, text = "theta2", bg = "#86f1ef", font=("Comic Sans MS", 10))
    te2r.grid(row = 6, column = 1, sticky = "w", pady = 0, padx = 20)
    te2r.config(cursor = "pirate")
    td2r = Label(frame1, bg = "#ffffff", width = 20 )
    td2r.grid(row = 7, column = 1, sticky = "e", pady = 1, padx = 20)
    td2r.config(fg = "blue", justify = "center")

    te3 = Label(frame1, text = "Pz", bg = "#86f1ef", font=("Comic Sans MS", 10))
    te3.grid(row = 9, column = 0, sticky = "w", pady = 0, padx = 20)
    te3.config(cursor = "pirate")
    td3 = Label(frame1, bg = "#ffffff", width = 20 )
    td3.grid(row = 10, column = 0, sticky = "e", pady = 1, padx = 20)
    td3.config(fg = "blue", justify = "center")

    te3r = Label(frame1, text = "tetha3", bg = "#86f1ef", font=("Comic Sans MS", 10))
    te3r.grid(row = 9, column = 1, sticky = "w", pady = 0, padx = 20)
    te3r.config(cursor = "pirate")
    td3r = Label(frame1, bg = "#ffffff", width = 20 )
    td3r.grid(row = 10, column = 1, sticky = "e", pady = 1, padx = 20)
    td3r.config(fg = "blue", justify = "center")
    
    x = 0
    y = 0
    z = -358
    delta = 5
    deltaz = 5
    td1["text"] = x
    td2["text"] = y
    td3["text"] = z
    motores = posicion()
    motores.x = x
    motores.y = y
    motores.z = z
    rospy.loginfo("Estoy publicando en el topic...")

    def codigoboton1():
        s = tkMessageBox.askyesno(message="¿Desea continuar?", title="Título")
        if s == False:
		vp.destroy()

    def codigoboton2():
	global x, y, z
        t = tkMessageBox.askyesno(message="¿Desea enviar a Home al Robot?", title="Título")
        if t == True:
		motores.x = 0
    		motores.y = 0
                motores.z = -358
                td1["text"] = 0
                td2["text"] = 0
                td3["text"] = -358
		x, y, z = [0, 0, -358]
    		pub.publish(motores)
		return t
		       

    boton1= Button(frame1, text = "Cerrar", command = codigoboton1, 
	    bg = "#f92103")
    boton1.grid(row = 12, column = 1, pady = 2, padx = 4)

    boton2= Button(frame1, text = "HOME", command = codigoboton2, 
	    bg = "#36e60f")
    boton2.grid(row = 12, column = 0, pady = 2, padx = 4)


    def Capturarevento(event):
	global x,y,z, delta, deltaz
	if  z < -410:
		deltaz = 0.1

	if z > -400:
		  	deltaz = 5

	if z >= -419.9:
		if event.keysym == 'Up':
			x = x + delta
			td1["text"] = round(x, 4)
			td2["text"] = round(y, 4)
			td3["text"] = round(z, 4)
			ri = inverse(x, y, z)
			td1r["text"] = round(ri[0], 4)
			td2r["text"] = round(ri[1], 4)
			td3r["text"] = round(ri[2], 4)
    		        motores.x = x
    		        motores.y = y
    			motores.z = z
    			pub.publish(motores)  				
		elif event.keysym == 'Down':
			x = x - delta
			td1["text"] = round(x, 4)
			td2["text"] = round(y, 4)
			td3["text"] = round(z, 4)
			ri = inverse(x, y, z)
			td1r["text"] = round(ri[0], 4)
			td2r["text"] = round(ri[1], 4)
			td3r["text"] = round(ri[2], 4)		
			motores.x = x
    		        motores.y = y
    			motores.z = z
    			pub.publish(motores)
		elif event.keysym == 'Left':
			y = y - delta
			td1["text"] = round(x, 4)
			td2["text"] = round(y, 4)
			td3["text"] = round(z, 4)
			ri = inverse(x, y, z)
			td1r["text"] = round(ri[0], 4)
			td2r["text"] = round(ri[1], 4)
			td3r["text"] = round(ri[2], 4)
			motores.x = x
    		        motores.y = y
    			motores.z = z
    			pub.publish(motores)
		elif event.keysym == 'Right':
			y = y + delta
			td1["text"] = round(x, 4)
			td2["text"] = round(y, 4)
			td3["text"] = round(z, 4)
			ri = inverse(x, y, z)
			td1r["text"] = round(ri[0], 4)
			td2r["text"] = round(ri[1], 4)
			td3r["text"] = round(ri[2], 4)
			motores.x = x
    		        motores.y = y
    			motores.z = z
    			pub.publish(motores)	
		elif event.keysym == 'z':
			z = z + deltaz
			td1["text"] = round(x, 4)
			td2["text"] = round(y, 4)
			td3["text"] = round(z, 4)
			ri = inverse(x, y, z)
			td1r["text"] = round(ri[0], 4)
			td2r["text"] = round(ri[1], 4)
			td3r["text"] = round(ri[2], 4)
			motores.x = x
    		        motores.y = y
    			motores.z = z
    			pub.publish(motores)
		elif event.keysym == 'm':
			z = z - deltaz
			td1["text"] = round(x, 4)
			td2["text"] = round(y, 4)
			td3["text"] = round(z, 4)
			ri = inverse(x, y, z)
			td1r["text"] = round(ri[0], 4)
			td2r["text"] = round(ri[1], 4)
			td3r["text"] = round(ri[2], 4)
			motores.x = x
    		        motores.y = y
    			motores.z = z
    			pub.publish(motores)
	else:
		tkMessageBox.showinfo(message="Fuera de Rango", title="Error")
		z = -419.9
   
    canvas.bind_all('<KeyPress>', Capturarevento)

    while not rospy.is_shutdown(): 
        try: 
 		rospy.loginfo("%f, %f, %f ", motores.x, motores.y, motores.z)
                vp.update()
		vp.update_idletasks()
        	rate.sleep()
	except:
		break
 
    rospy.loginfo("Finalizando nodo...")

if __name__ == '__main__':
    try:
        principal()
    except rospy.ROSInterruptException:
	pass
