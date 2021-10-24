from tkinter import *
root=Tk()

def reply(t,faq=False):
    response="Sorry we couldn't understand what you were saying. Please try again!"
    if not faq:
        greetings=['hi','hello','sup',"what's up","whats up",'wassup','hey']
        if t in greetings:
            response=t.capitalize()+"! How are you?"

    texts.configure(state='normal')
    texts.insert('end',"\n\nBot: "+response)
    texts.configure(state='disabled')
        

def send_text(yes='ok'):
    global texting
    to_send=str(texting.get(1.0,END))
    if to_send.strip()!='':
        texts.configure(state='normal')
        texts.insert('end',"\n\nYou: "+to_send.replace("\n",""))
        texts.configure(state='disabled')
        texting.delete(1.0,END)
        reply(to_send.lower().strip())
    if to_send in faqs:


#status: in queue, preparing, finished 

faqs=["What’s the status of my order?","How does spice rating work?","What kinds of payments are accepted?","Show me the menu","Take my order"]
faq_replies=[""]
def FAQ(i):
    if i==4:
        ###""
    
#Intro
title=Label(root,text="Welcome to Singh Restaurant")
title.grid(row=0,column=0)
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
title_faqs=Label(root,text="Ask us something!")
title_faqs.grid(row=0,column=1)
b1=Button(root,text="What is the status of my order?",command=lambda: FAQ(0))
b1.grid(row=1,column=1)
b2=Button(root,text="How does spice rating work?",command=lambda: FAQ(1))
b2.grid(row=2,column=1)
b3=Button(root,text="What kinds of payments are accepted?",command=lambda: FAQ(2))
b3.grid(row=3,column=1)
b4=Button(root,text="Show me the menu",command=lambda: FAQ(3))
b4.grid(row=4,column=1)
b4=Button(root,text="Take my order",command=lambda: FAQ(4))
b4.grid(row=5,column=1)


root.bind('<Return>', send_text)

root.mainloop()