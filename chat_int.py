from tkinter import *
root = Tk()
root.title("Singh Bot")

#status: In queue, preparing, finished

faqs=["how does spice rating work?","what kinds of payments are accepted?"]
faq_replies=["This is how spice rating works", "PayTm, VISA and Mastercard are allowed"]

def fetch_status():
    pass

def fetch_menu():
    pass

def open_order():
    pass

def reply(t):
    response="Sorry we couldn't understand what you were saying. Please try again!"

    if t.lower().strip() in faqs:
        response = faq_replies[faqs.index(t)]
    else:
        greetings=['hi','hello','sup',"what's up","whats up",'wassup','hey']

        if t in greetings:
            response=t.capitalize()+"! How are you?"

    texts.configure(state='normal')
    texts.insert('end',"\n\nBot: "+response)
    texts.configure(state='disabled')


def send_text(param='no'):
    global texting

    to_send = str(texting.get(1.0,END))
    if to_send.strip() != '':
        texts.configure(state='normal')
        texts.insert(END,"\n\nYou: "+to_send.replace("\n",""))
        texts.configure(state='disabled')
        texting.delete(1.0,END)
        reply(to_send.lower().strip())

def faq(index):
    if index in [0, 1]:
        texting.delete(1.0,END)
        texting.insert(END,faqs[index])
        send_text()

#Intro
title=Label(root,text="Welcome to Singh Restaurant",font='Helvetica 20 bold')
title.grid(row=0,column=0,pady=(5,15))
texts=Text(root,state='normal')
texts.insert("end","Bot: Hello! Welcome to Singh Restaurant. How may I help you?")
texts.config(state="disabled")
texts.grid(row=1,column=0,rowspan=5)

scrollbar = Scrollbar(root)
scrollbar.grid(row=1,column=0,ipady=170,sticky='e',rowspan=5)

texts.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=texts.yview)

send=Button(root,text="Send",height=3,width=5,command=send_text)
send.grid(row=7,column=0,sticky='e')

texting=Text(root,height=3,width=75)
texting.grid(row=7,column=0,sticky='w')

#FAQ's
title_faqs=Label(root,text="Ask me something!",font='Helvetica 20 bold')
title_faqs.grid(row=0,column=1,pady=(5,15),padx=(0,10))
b1=Button(root,text="What is the status of my order?",command=lambda: fetch_status())
b1.grid(row=1,column=1)
b2=Button(root,text="How does spice rating work?",command=lambda: faq(0))
b2.grid(row=2,column=1)
b3=Button(root,text="What kinds of payments are accepted?",command=lambda: faq(1))
b3.grid(row=3,column=1)
b4=Button(root,text="Show me the menu",command=lambda: fetch_menu())
b4.grid(row=4,column=1)
b4=Button(root,text="Take my order",command=lambda: open_order())
b4.grid(row=5,column=1)


root.bind('<Return>', send_text)

root.mainloop()
