from tkinter import *
from tkinter import messagebox
root = Tk()
import csv

global srno_bill
global price
srno_bill=1
global added
added=[]

global things
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
        if int(temp[3])>0:
            final=str(srno_bill)+" | "+temp[1]+" | "+temp[2]+"₹"
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
            refresh_stock()
            genbill()
        else:
            messagebox.showwarning("Warning",str("You are out of "+str(temp[1])))
    else:
        messagebox.showerror("Error","You must select an item to add")
items_tell_label=Label(root,text="Items available in stock")
items_tell_label.grid(row=0,column=0)

scrollbar_showitems = Scrollbar(root)
scrollbar_showitems.grid(row=1,column=1,ipady=60)

listbox_showitems=Listbox(root)


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

button=Button(root, text="Add to bill", command=addtobill)
button.grid(row=2,column=0)

listbox_showitems.config(yscrollcommand=scrollbar_showitems.set)
scrollbar_showitems.config(command=listbox_showitems.yview)

#Bill
bill_tell_label=Label(root,text="Bill")
bill_tell_label.grid(row=0,column=2)

scrollbar_bill = Scrollbar(root)
scrollbar_bill.grid(row=1,column=3,ipady=60)

listbox_bill=Listbox(root)
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
            final=str(srno_bill)+" | "+new[1]+" | "+new[2]+"₹"
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

deletebuttonforbill=Button(root,text="Delete item from bill",command=deleteitembill)
deletebuttonforbill.grid(row=2,column=2)

#Generating bill

def genbill():
    global price
    global things
    global added
    print(added)
    print(things)
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
    total_price_bill.config(text="Total:\n"+str(price)+"₹",fg='blue')
    finalbilllabel.grid(row=0,column=5)
    bill_srno.grid(row=1,column=4)
    bill_itemname.grid(row=1,column=5)
    bill_qty.grid(row=1,column=6)
    bill_price.grid(row=1,column=7)
    total_price_bill.grid(row=2,column=7,sticky='e')   

bill_srno=Label(root,text="Srno")
bill_srno.grid(row=1,column=4)
bill_itemname=Label(root,text="Name")
bill_itemname.grid(row=1,column=5)
bill_qty=Label(root,text="Quantity")
bill_qty.grid(row=1,column=6)
bill_price=Label(root,text="Price")
bill_price.grid(row=1,column=7)
total_price_bill=Label(root,text="Total:\n0₹",fg="blue")
total_price_bill.grid(row=2,column=7,sticky='e')   
finalbilllabel=Label(root,text="Final Bill")

#Paying bill: creates root child(called paying) - another screen controlled by root parent

def paybill():
    global price
    global added
    if len(added)!=0:
        def submitamt():
            global added
            global price
            amountgiven=amountentry.get()
            if amountgiven.isdigit():
                if int(amountgiven)>int(price):
                    okcancel=messagebox.askokcancel("Giving change","Give a change of "+str(int(amountgiven)-int(price))+"₹")
                    if okcancel==1:
                        messagebox.showinfo("Info","Transaction completed")
                        paying.destroy()
                        added=[]
                        price=0
                        genbill()
                        listbox_bill.delete(first=0,last=END)
                elif int(amountgiven)==int(price):
                    yesno=messagebox.askyesno("Proceeding","Proceed with transaction?")
                    if yesno==1:
                        messagebox.showinfo("Info","Transaction completed")
                        paying.destroy()
                        added=[]
                        price=0
                        genbill()
                        listbox_bill.delete(first=0,last=END)
                else:
                    messagebox.showwarning("Warning","Amount given is less")
        paying=Toplevel(root)
        paying.title("Pay")
        totalpricetitle=Label(paying,text="The final price is "+str(price)+"₹")
        totalpricetitle.grid(row=0,column=0)
        amountlabel=Label(paying,text="Enter amount paid")
        amountlabel.grid(row=1,column=0)
        amountentry=Entry(paying,exportselection=0)
        amountentry.grid(row=1,column=1)
        submitamountentered=Button(paying,text="Submit",command=submitamt)
        submitamountentered.grid(row=2,column=0)
    else:
        messagebox.showerror("Error","You cannot pay for an empty bill")

paybillbutton=Button(root,text="Pay Bill",command=paybill)
paybillbutton.grid(row=2,column=5)

root.mainloop()