from tkinter import *
from tkinter import messagebox
import random, csv
from datetime import datetime

print("Welcome! Do remember to try our mouth-watering Singh Special Sandwich!\n")
name = input("Enter your name: ")
mobile = input("Enter your phone number: ")

f = open("Customers.csv", "r")
reader = csv.reader(f)
all_rows = []

for row in reader:
    if row != []:
        all_rows.append(row)

f.close()
cust_id = 1

if len(all_rows) > 1:
    cust_id = int(all_rows[-1][0]) + 1

all_rows.append([cust_id, name, mobile, datetime.now()])

f = open("Customers.csv", "w", newline='')
writer = csv.writer(f)
writer.writerows(all_rows)
f.close()

root = Tk()
root.title("Singh Bot")

#status: In queue, preparing, finished
feedback = False

faqs=["how does spice rating work","what kinds of payments are accepted"]
faq_replies=["This is how spice rating works -\n\t0: No spice\n\t1: Little spice \n\t2: Medium spice \n\t3: Large spice \n\tAnything above 1 is not recommended for children","PayTm, VISA and Mastercard are allowed"]

def fetch_status():
    f = open("orders.csv", "r")
    reader = csv.reader(f)
    rows = []

    for line in reader:
        if line != []:
            rows.append(line)

    status_res = "Sorry, you haven't placed an order yet!"

    if int(rows[-1][1]) == cust_id:
        status_res = "Current status of Order #"+rows[-1][0]+": "+rows[-1][-2]

    texts.configure(state='normal')
    texts.insert('end',"\n\nBot: " + status_res)
    texts.configure(state='disabled')

def fetch_menu():
    with open("menu.csv", "r") as f:
        items = csv.reader(f)
        dish_list = []

        for row in items:
            dish_list.append(row)

        dish_list[0] = ['ID', 'Dish', 'Price', 'Quantity', 'Spice']
        bot_reply = "\n".join(" ".join(row) for row in dish_list)

        texts.configure(state='normal')
        texts.insert('end',"\n\nBot: " + bot_reply)
        texts.configure(state='disabled')

def open_order():
    global things, srno_bill
    global price, added, ordering

    ordering=Toplevel(root)
    srno_bill=1
    added=[]


    f=open("menu.csv","r")
    r_obj=csv.reader(f)
    #things=f.read().split("\n")
    things=["|".join(i) for i in r_obj]
    #print(things)
    f.close()

    #Items in stock
    def addtobill():
        if listbox_showitems.curselection()!=():
            global srno_bill
            global things
            global price
            global added
            selected=listbox_showitems.curselection()[0]+1
            temp=things[selected].split("|")
            #buying.append(things)
            if int(temp[3])>0:
                final=str(srno_bill)+" | "+temp[1]+" | ₹"+temp[2]
                listbox_bill.insert(END,final)
                srno_bill+=1
                price=price+int(temp[2])
                temp[3]=str(int(temp[3])-1)
                final=''
                for i in temp:
                    if temp.index(i)!=4:
                        final=final+i+"|"
                    else:
                        final=final+i
                things[selected]=final
                #print(things)
                to_add=[i.split("|") for i in things]
                #print(to_add)
                f1=open("menu.csv","w",newline='')
                w_obj=csv.writer(f1)
                w_obj.writerows(to_add)
                f1.close()
                added.append(temp[0]) #Stores srno values of items added in order
                #print(added)
                refresh_stock()
                genbill()
            else:
                messagebox.showwarning("Warning",str("You are out of "+str(temp[1])))
        else:
            messagebox.showerror("Error","You must select an item to add")

    items_tell_label=Label(ordering,text="Items available in stock")
    items_tell_label.grid(row=0,column=0)

    scrollbar_showitems = Scrollbar(ordering)
    scrollbar_showitems.grid(row=1,column=1,ipady=60)

    listbox_showitems=Listbox(ordering)


    def refresh_stock():
        global things
        listbox_showitems.delete(first=0,last=int(things[-1].split("|")[0]))
        for i in things:
            if things.index(i)!=0:
                temp=i.split("|")
                inserting=temp[0]+" | "+temp[1]+" | "+temp[2]+"₹ |  "+temp[3]
                listbox_showitems.insert(END,inserting)

    refresh_stock()

    listbox_showitems.grid(row=1,column=0,ipadx=40)

    button=Button(ordering, text="Add to bill", command=addtobill)
    button.grid(row=2,column=0)

    listbox_showitems.config(yscrollcommand=scrollbar_showitems.set)
    scrollbar_showitems.config(command=listbox_showitems.yview)

    #Bill
    bill_tell_label=Label(ordering,text="Bill")
    bill_tell_label.grid(row=0,column=2)

    scrollbar_bill = Scrollbar(ordering)
    scrollbar_bill.grid(row=1,column=3,ipady=60)

    listbox_bill=Listbox(ordering,width=30)
    listbox_bill.grid(row=1,column=2)

    listbox_bill.config(yscrollcommand=scrollbar_bill.set)
    scrollbar_bill.config(command=listbox_bill.yview)

    price=0
    def deleteitembill():
        global things
        global price
        global srno_bill
        if listbox_bill.curselection()!=():
            taken=listbox_bill.curselection()[0]
            item_no=int(added[taken])
            added.remove(str(item_no))
            listbox_bill.delete(first=0,last=(len(added)))
            srno_bill=1
            for i in added:
                new=things[int(i)].split("|")
                final=str(srno_bill)+" | "+new[1]+" | ₹"+new[2]
                listbox_bill.insert(END,final)
                srno_bill+=1
            temp=things[item_no].split("|")
            temp[3]=str(int(temp[3])+1)
            final=''
            for i in temp:
                if temp.index(i)!=4:
                    final=final+i+"|"
                else:
                    final=final+i
            things[item_no]=final
            to_add=[i.split("|") for i in things]
            #print(to_add)
            f1=open("menu.csv","w",newline='')
            w_obj=csv.writer(f1)
            w_obj.writerows(to_add)
            f1.close()
            price=price-int(temp[2])
            refresh_stock()
            genbill()
        else:
            messagebox.showerror("Error","You must select 1 item to delete")

    deletebuttonforbill=Button(ordering,text="Delete item from bill",command=deleteitembill)
    deletebuttonforbill.grid(row=2,column=2)

    #Generating bill

    def genbill():
        global price
        global things
        global added

        count=0
        names=[]
        prices=[]

        for i in added:
            temp=things[int(i)].split("|")
            names.append(temp[1])
            prices.append(temp[2])

        final_names='Name\n'
        final_prices='Price\n'
        final_qtys='Quantity\n'
        srnos='Srno\n'
        count=1

        for i in names:
            if names.index(i)!=len(names)-1:
                final_names=final_names+i+"\n"
                srnos=srnos+str(count)+"\n"
            else:
                final_names=final_names+i
                srnos=srnos+str(count)
            count+=1
        for j in prices:
            if prices.index(j)!=len(prices)-1:
                final_prices=final_prices+j+"\n"
            else:
                final_prices=final_prices+j
        bill_srno.config(text=srnos)
        bill_itemname.config(text=final_names)
        bill_price.config(text=final_prices)
        total_price_bill.config(text="Total:\n₹"+str(price),fg='blue')
        finalbilllabel.grid(row=0,column=5)
        bill_srno.grid(row=1,column=4)
        bill_itemname.grid(row=1,column=5)
        #bill_qty.grid(row=1,column=6)
        bill_price.grid(row=1,column=7)
        total_price_bill.grid(row=2,column=7,sticky='e')

    bill_srno=Label(ordering,text="Srno")
    bill_srno.grid(row=1,column=4)
    bill_itemname=Label(ordering,text="Name")
    bill_itemname.grid(row=1,column=5)
    # bill_qty=Label(ordering,text="Quantity")
    # bill_qty.grid(row=1,column=6)
    bill_price=Label(ordering,text="Price")
    bill_price.grid(row=1,column=7)
    total_price_bill=Label(ordering,text="Total:\n₹0",fg="blue")
    total_price_bill.grid(row=2,column=7,sticky='e')
    finalbilllabel=Label(ordering,text="Final Bill")

    #Paying bill: creates ordering child(called paying) - another screen controlled by ordering parent

    def paybill():
        global price
        global added

        if len(added) != 0:
            def submitamt():
                global added
                global price
                amountgiven=amountentry.get()
                # cust_id=custidentry.get()
                people=peopleentry.get()
                if amountgiven.isdigit():
                    if int(amountgiven)>int(price):
                        okcancel=messagebox.askokcancel("Giving change","Give a change of ₹"+str(int(amountgiven)-int(price)))
                        if okcancel==1:
                            paying.destroy()
                            messagebox.showinfo("Info","Transaction completed. Thank you for placing your order! It will be ready in 10 minutes.")
                            ordering.destroy()
                            listbox_bill.delete(first=0,last=END)
                    elif int(amountgiven)==int(price):
                        yesno=messagebox.askyesno("Proceeding","Proceed with transaction?")
                        if yesno==1:
                            messagebox.showinfo("Info","Transaction completed. Thank you for placing your order! It will be ready in 10 minutes.")
                            paying.destroy()
                            ordering.destroy()
                            listbox_bill.delete(first=0,last=END)
                    else:
                        messagebox.showwarning("Warning","Amount given is less")
                        pass
                s=" ".join(added)

                with open("orders.csv","r")  as f:
                    r_obj=csv.reader(f)
                    content=[]
                    for i in r_obj:
                        content.append(i)
                    print(content)
                with open("orders.csv","a",newline='') as f:
                    w_obj=csv.writer(f)
                    n=int(content[-1][0])+1 if len(content) != 1 else 1
                    w_obj.writerow([n,cust_id,s,price,people,"In Queue",""])
                price=0
                added=[]

            paying=Toplevel(ordering)
            paying.title("Pay")
            totalpricetitle=Label(paying,text="The final price is ₹"+str(price))
            totalpricetitle.grid(row=0,column=0)
            amountlabel=Label(paying,text="Enter amount paid")
            amountlabel.grid(row=1,column=0)
            amountentry=Entry(paying,exportselection=0)
            amountentry.grid(row=1,column=1)
            peoplelabel=Label(paying,text="How many people are there")
            peoplelabel.grid(row=3,column=0)
            peopleentry=Entry(paying,exportselection=0)
            peopleentry.grid(row=3,column=1)
            submitamountentered=Button(paying,text="Submit",command=submitamt)
            submitamountentered.grid(row=4,column=0)

        else:
            messagebox.showerror("Error","You cannot pay for an empty bill")

    paybillbutton=Button(ordering,text="Pay Bill",command=paybill)
    paybillbutton.grid(row=2,column=5)

    ordering.mainloop()


def reply(t):
    global feedback
    punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    t = t.lower().strip().strip(punctuation)

    response="Sorry we couldn't understand what you were saying. Please try again!"

    if t == "take my order":
        open_order()
    elif t == "show me the menu":
        fetch_menu()
    elif t == "what is the status of my order":
        fetch_status()
    elif t in faqs:
        response = faq_replies[faqs.index(t)]
    elif t.startswith("how spicy is "):
        dish = t[13:].strip()
        response = "Sorry, we do not have a dish with that name. Please try again!"

        with open("menu.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row[1].lower() == dish:
                    response = "The spice rating of this dish is " + str(row[-1])
                    break
    else:
        greetings=['hi','hello','sup',"what's up","whats up",'wassup','hey']

        if t in greetings:
            response=t.capitalize()+"! How are you?"
        elif t in ["bye", "i'm done eating"]:
            response="Thanks for eating at Singh Restaurant! Please let us know about your experience and my service!"
            feedback = True
        elif feedback:
            curr = []

            with open("Orders.csv", "r") as f:
                reader = csv.reader(f)

                for row in reader:
                    curr.append(row)

            with open("Orders.csv", "w", newline='') as f:
                writer = csv.writer(f)
                curr[-1][-1] = t
                writer.writerows(curr)

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
        reply(to_send)

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
