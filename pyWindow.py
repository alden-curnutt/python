from tkinter import *
from tkinter import ttk

def commandChanged(*args):
    if cmd_combobox.current() == 2: 
        cmd_Label.config(text="\nEnter the directory below:")
        cText.delete('1.0', END)
    if cmd_combobox.current() == 3: 
        cmd_Label.config(text="\nEnter machine code (as hex) below:")
        cText.delete('1.0', END)
    cmd_combobox.selection_clear()

def execute(*args):
    try:
        #ipAddress = ipAddr.get()
        #portNum = pNum.get()
        #root.title("Client Software *CONNECTED*")
        executeButton.config(text="Working")
    except ValueError: #FIXME what exception for executing
        pass
    
def connect(*args):
    try:
        ipAddress = ipAddr.get()
        portNum = pNum.get()
        #meters.set((0.3048 * value * 10000.0 + 0.5)/10000.0)
        root.title("Client Software *CONNECTED*")
        aButton.config(text="Disconnect")
    except ValueError: #FIXME what exception for ipaddress
        pass
    
root = Tk()
root.title("Client Software *NOT CONNECTED*")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

ipAddr = StringVar()
pNum = StringVar()
meters = StringVar()

ipAddr_entry = ttk.Entry(mainframe, width=15, textvariable=ipAddr)
pNum_entry = ttk.Entry(mainframe, width=6, textvariable=pNum) #FIXME seems that the six is ignored, the frame chooses the bigger 15 above
ipAddr_entry.grid(column=2, row=1, sticky=(W))
pNum_entry.grid(column=2, row=2, sticky=(W))

ttk.Label(mainframe, textvariable=meters).grid(column=2, row=3, sticky=(W, E))
aButton = ttk.Button(mainframe, text="Connect", command=connect)
aButton.grid(column=2, row=3, sticky=(N,W))
executeButton = ttk.Button(mainframe, text="Execute", command=execute)
executeButton.grid(column=4, row=5, sticky=(N,W))

ttk.Label(mainframe, text="IP Address").grid(column=1, row=1, sticky=E)
ttk.Label(mainframe, text="Port Number").grid(column=1, row=2, sticky=E)
cmd_Label = ttk.Label(mainframe, text="\nEnter machine code (as hex) below:", justify=LEFT)
cmd_Label.grid(column=2, row=6, sticky=(S,W))
ttk.Label(mainframe, text="Choose a command below:").grid(column=2, row=4, sticky=(N,W))
ttk.Label(mainframe, text="\nResults:", justify=LEFT).grid(column=4, row=6, sticky=(S,W))

command='1.  Retrieve OS info.'
cmd_combobox = ttk.Combobox(mainframe, width=30, textvariable=command, state='readonly')
cmd_combobox.grid(column=2, row=5, sticky=(S,W))
cmd_combobox['values']=('1.  Retrieve OS info.','2.  Get list of processes.','3.  List directory.','4.  Execute shell code.')
cmd_combobox.current(0)
cmd_combobox.bind('<<ComboboxSelected>>', commandChanged)
cText = Text(mainframe, width=40, height=20)
cText.grid(column=2, row=7, sticky=W)

rText = Text(mainframe, width=40, height=20)
rText.grid(column=4, row=7, sticky=(E,W))

for child in mainframe.winfo_children(): child.grid_configure(padx=2, pady=10)

ipAddr_entry.focus()
root.bind('<Return>', connect)

root.mainloop()

