from tkinter import *
root=Tk()

# texts.configure(state='normal')
# texts.insert('end', 'Some Text')
# texts.configure(state='disabled')

def send_text(yes='ok'):
    global texting
    to_send="You: "+str(texting.get(1.0,END))
    if not(to_send.isspace()) and to_send!='':
        texts.configure(state='normal')
        texts.insert('end',to_send)
        texts.configure(state='disabled')
        texting.delete(1.0,END)

title=Label(root,text="Welcome to Singh Restaurant")
title.grid(row=0,column=0)
texts=Text(root,state='disabled')
texts.grid(row=1,column=0)

scrollbar = Scrollbar(root)
scrollbar.grid(row=1,column=0,ipady=170,sticky='e')

texts.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=texts.yview)

send=Button(root,text="Send",height=3,width=5,command=send_text)
send.grid(row=2,column=0,sticky='e')

texting=Text(root,height=3,width=75)
texting.grid(row=2,column=0,sticky='w')

root.bind('<Return>', send_text)

root.mainloop()