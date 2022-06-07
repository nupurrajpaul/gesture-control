from tkinter import *
from tkinter import PhotoImage
import threading, subprocess

tk = Tk()
tk.title('Gesture Control')
tk.geometry('450x350')
tk.config(bg='deep sky blue')

process = None

CheckVar1 = IntVar()
CheckVar2 = IntVar()
RadioVar  = IntVar()
RadioVar.set(1)

imgStart = PhotoImage(file='UI/start.png')
imgStop = PhotoImage(file='UI/stop.png')

def setCam():
	camwin = Toplevel(tk)
	camwin.title('Camera Settings')
	camwin.geometry('300x200')

	def applycam():
		width = enwidth.get()
		height = enheight.get()

		f = open('Files/camSettings.txt','w')
		f.write('{} {}'.format(str(width),str(height)))
		f.close()

		camwin.destroy()

	def getCamSet():
		f = open('Files/camSettings.txt','r')
		lines1 =list(f.readline().split(' '))

		enwidth.delete(0,END)
		enwidth.insert(0,lines1[0])

		enheight.delete(0,END)
		enheight.insert(0,lines1[1])

	cframe = LabelFrame(camwin,text='Resolution of camera')
	cframe.pack(expand=True,fill=BOTH,pady=15,padx=15)

	widthLabel = Label(cframe,text='width : ')
	widthLabel.pack()

	enwidth = Entry(cframe)
	enwidth.pack()

	heightLabel = Label(cframe,text='Height : ')
	heightLabel.pack()

	enheight = Entry(cframe)
	enheight.pack()

	button = Button(cframe, text="    Apply    ",command=applycam,bg='skyblue')
	button.pack(pady=20)

	getCamSet()

def start():
	global RadioVar, CheckVar1, CheckVar2, process
	cam = CheckVar1.get()
	drw = CheckVar2.get()
	f = open('Files/camSettings.txt')
	camset = []
	for line in f:
		for word in line.split():
			camset.append(word)
	f.close()
	camw = camset[0]
	camh = camset[1]
	engine = RadioVar.get()
	if engine == 1:
		if process == None:
			ar = "'"+str(cam)+','+str(drw)+','+str(camw)+','+str(camh)+"'"
			print(ar)
			process = subprocess.Popen([sys.executable,'Engine/OpenCV/startOpenCv.py',ar])
		else:
			print('Already Running...')
	if engine == 2:
		if process == None:
			ar = "'"+str(cam)+','+str(drw)+','+str(camw)+','+str(camh)+"'"
			print(ar)
			process = subprocess.Popen([sys.executable,'Engine/MediaPipe/StartMediaPipe.py',ar])
		else:
			print('Already Running...')
	if engine == 3:
		if process == None:
			ar = "'"+str(camw)+','+str(camh)+"'"
			print(ar)
			process = subprocess.Popen([sys.executable,'testing.py',ar])
		else:
			print('Already Running...')

def stop():
	global process
	print(process)
	try:
		process.terminate()
	except:
		print('Nothing to terminate')
	process = None

def chColor():
	global process
	if process == None:
		p = subprocess.Popen([sys.executable,'changeColor.py'])

menubar = Menu(tk)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Start", command=start)
filemenu.add_command(label="Stop", command=stop)

filemenu.add_separator()

filemenu.add_command(label="Exit", command=tk.quit)
menubar.add_cascade(label="File", menu=filemenu)

editmenu = Menu(menubar, tearoff=0)

editmenu.add_command(label="Change Color", command=chColor)
editmenu.add_command(label="Adjust Camera", command=setCam)

menubar.add_cascade(label="Edit", menu=editmenu)

tk.config(menu=menubar)

upperFrame = Frame(tk)
upperFrame.pack(expand=True,fill=BOTH)

btnStart = Button(upperFrame,image=imgStart,bd=0,command=start)
btnStart.pack(side=LEFT,anchor='nw')

btnStop = Button(upperFrame,image=imgStop,bd=0,command=stop)
btnStop.pack(side=LEFT,anchor='nw')

midFrame = Frame(tk)
midFrame.pack(expand=True,fill=BOTH)

lf = LabelFrame(midFrame,text='Choose Engine ')
lf.pack(expand=True,fill=BOTH,padx=20,pady=15)

rOpenCv = Radiobutton(lf,text='Open Cv',font=('Arial',10),variable=RadioVar,value=1)
rOpenCv.pack(side=LEFT,pady=8,padx=20)

rMediaPipe = Radiobutton(lf,text='Media-Pipe',font=('Arial',10),variable=RadioVar,value=2)
rMediaPipe.pack(side=LEFT,pady=8,padx=20)

rTesting = Radiobutton(lf,text='Testing',font=('Arial',10),variable=RadioVar,value=3)
rTesting.pack(side=LEFT,pady=8,padx=20)

lowerFrame = Frame(tk)
lowerFrame.pack(expand=True,fill=BOTH)

btnCc = Button(lowerFrame,text='Change Color',bg='skyblue',command=chColor)
btnCc.pack(side=LEFT,padx=15,pady=10)

btnCamera = Button(lowerFrame,text='Camera Settings',bg='salmon',command=setCam)
btnCamera.pack(side=LEFT,padx=15,pady=10)

C1 = Checkbutton(lowerFrame, text = "Real Time Video", variable = CheckVar1,onvalue = 0, offvalue = 1)
C1.pack(side=LEFT)

C2 = Checkbutton(lowerFrame, text = "Draw Guides", variable = CheckVar2,onvalue = 0, offvalue = 1)
C2.pack(side=LEFT)

tk.mainloop()