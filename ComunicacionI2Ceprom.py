import smbus
import time
from PIL import Image, ImageDraw, ImageFont
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

bus = smbus.SMBus(1)
RST = None
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)


# Initialize library.
disp.begin()
# Clear display.
disp.clear()
disp.display()
# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
x=0
# Load default font.
font = ImageFont.load_default()

#Direccion Memoria
address = 0x50

data = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
ArregloPares = [2,4,6,8,10,12,14,16,18,20]
ArregloNones = [1,3,5,7,9,11,13,15,17,19]
ArregloPrimo = [2,3,5,7,11,13,17,19]
ArregloMultiplo = [3,6,9,12,15,18]

#Guardar los valores en matrices
DatosPares=[]
DatosNones=[]
DatosPrimo=[]
DatosMultiplo=[]

def EscribiraMemoria(i,Localidad,BanderaSencillo,Valor):
	if  BanderaSencillo==0:
		for x in range (i):
			Dato = int(input("dato " + str(x+1) + ": "))
			ArregloDato = [Localidad, Dato]
			bus.write_i2c_block_data(address,0x00,ArregloDato)
			Localidad += 1
			time.sleep(0.01)
	elif BanderaSencillo==1:
			print("Estoy poniendo en la localidad: "+str(Localidad)+" El valor de: "+str(Valor)) 
			ArregloDato = [Localidad,Valor]
			bus.write_i2c_block_data(address,0x00,ArregloDato)
			Localidad += 1
			time.sleep(0.01)
			
		
def LeerElemento(addrs):
	bus.write_i2c_block_data(address, 0x00, [addrs])
	return bus.read_byte(address)
	
def MostrarPantalla(DatoMostrar):
	draw.rectangle((0,0,width,height), outline=0, fill=0)
	draw.text((x,top),DatoMostrar,  font=font, fill=255)
	disp.image(image)
	disp.clear()
	disp.display()
	time.sleep(5)

def MostrarFinal():
	for i in range (21,25):
		Resultado=LeerElemento(i)
		
def SepararDatos(i):
	i=1
	for j in range (20):
		Valor=LeerElemento(i)
		#par
		if i in ArregloPares:
			DatosPares.append(Valor)
		#Nones
		if i in ArregloNones:
			DatosNones.append(Valor)
		#Primos
		if i in ArregloPrimo:
			DatosPrimo.append(Valor)
		#Multiplos
		if i in ArregloMultiplo:
			DatosMultiplo.append(Valor)
		i+=1

def Sumar():
	Suma=0
	longitud=len(DatosPares)
	for j in range (longitud):
		Valor=DatosPares[j]
		ValorInt=int(Valor)
		Suma2=Suma
		Suma=Suma+ValorInt
		draw.rectangle((0,0,width,height), outline=0, fill=0)
		draw.text((x,top),"Sumando " + str(Suma2)+ "+" + str(ValorInt),  font=font, fill=255)
		draw.text((x, top+8),"Resultado:" + str(Suma) , font=font, fill=255)
		disp.image(image)
		disp.display()
		time.sleep(1)
		disp.clear()
	EscribiraMemoria(0,21,1,Suma)

def Restar():
	Resta=1
	longitud=len(DatosNones)
	for j in range (longitud-1):
		Valor=DatosNones[j+1]
		ValorInt=int(Valor)
		Resta2=Resta
		Resta=Resta-ValorInt
		draw.rectangle((0,0,width,height), outline=0, fill=0)
		draw.text((x,top),"Restando " + str(Resta2)+ "-" + str(ValorInt),  font=font, fill=255)
		draw.text((x, top+8),"Resultado:" + str(Resta) , font=font, fill=255)
		disp.image(image)
		disp.display()
		time.sleep(1)
		disp.clear()
	EscribiraMemoria(0,22,1,Resta)
		
def Multiplicar():
	Mult=DatosPrimo[0]
	longitud=len(DatosPrimo)
	for j in range (longitud-1):
		Valor=DatosPrimo[j+1]
		ValorInt=int(Valor)
		Mult2=Mult
		Mult=Mult*ValorInt
		draw.rectangle((0,0,width,height), outline=0, fill=0)
		draw.text((x,top),str(Mult2),  font=font, fill=255)
		draw.text((x, top+8),"x", font=font, fill=255)
		draw.text((x, top+16),str(ValorInt), font=font, fill=255)
		draw.text((x, top+24),"Resultado:" + str(Mult) , font=font, fill=255)
		disp.image(image)
		disp.display()
		time.sleep(1)
		disp.clear
	EscribiraMemoria(0,23,1,Mult)
		
def Cuadrado():
	Pot=DatosMultiplo[0]
	Resultado=Pot**2
	longitud=len(DatosMultiplo)
	for j in range (longitud-1):
		Valor=DatosMultiplo[j+1]
		ValorInt=int(Valor)
		Pot2=ValorInt**2
		Pot3=Resultado
		Resultado=Pot2+Resultado
		draw.rectangle((0,0,width,height), outline=0, fill=0)
		draw.text((x,top),str(Pot2),  font=font, fill=255)
		draw.text((x, top+8),"+", font=font, fill=255)
		draw.text((x, top+16),str(Pot3), font=font, fill=255)
		draw.text((x, top+24),"Resultado:" + str(Resultado) , font=font, fill=255)
		disp.image(image)
		disp.display()
		time.sleep(1)
		disp.clear()
	EscribiraMemoria(0,24,1,Resultado)
	
def Modificar2124():
	SumaPar=0
	SumaNumerosPares=LeerElemento(21)
	for x in range (21,25):
		Dato = int(input("dato " + str(x) + ": "))
		ArregloDato = [x, Dato]
		bus.write_i2c_block_data(address,0x00,ArregloDato)
		time.sleep(0.01)
	for i in range(21,25):
		Valor=LeerElemento(i)
		#print("El valor de la localidad: "+str(i)+" es: "+str(Valor))
		SumaPar=SumaPar+int(Valor)
		Resultado=SumaNumerosPares+SumaPar
	disp.clear()	
	draw.rectangle((0,0,width,height), outline=0, fill=0)
	draw.text((0,top),"Sumando "+str(SumaNumerosPares)+"+"+str(SumaPar),  font=font, fill=255)
	draw.text((0,top+8),"Resultado: "+str(Resultado),font=font, fill=255)
	disp.image(image)
	disp.display()
	time.sleep(1)
	disp.clear()
		
#Codigo Principal
EscribiraMemoria(20,1,0,0)
SepararDatos(20)
Sumar()
Restar()
Multiplicar()
Cuadrado()
MostrarFinal()
Modificar2124()
bus.close()
