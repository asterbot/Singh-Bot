import csv
from tkinter import *
from tkinter import messagebox
root=Tk()
root.title("Edit")

#Refreshes the whole shown database
def refresh():
    f = open("menu.csv","r")
    items = csv.reader(f)
    dish_list = []
    for row in items:
        dish_list.append(row)
    f.close()

    dish_list[0] = ['ID', 'Dish', 'Price', 'Quantity', 'Spice']
    srno=''; names=''; prices=''; qtys=''; types=''

    #[['Sr No.', 'Items', 'Price', 'Quantity', 'Type'], ['1', 'Apple', '50', '10', 'kg'], ['2', 'Banana', '30', '20', 'kg'], ['3', 'Chocolate', '50', '30', 'qty'], ['4', 'Ice Cream', '40', '15', 'qty'], ['5', 'Pizza', '70', '20', 'qty'], ['6', 'Pasta', '30', '20', 'kg']]
    for d in dish_list:
        srno += d[0] + "\n"
        names += d[1] + "\n"
        prices += d[2] + "\n"
        qtys += d[3] + "\n"
        types += d[4] + "\n"

    #adding everything
    srno_label.config(text=srno)
    names_label.config(text=names)
    prices_label.config(text=prices)
    qtys_label.config(text=qtys)
    types_label.config(text=types)

srno_label=Label(root)
srno_label.grid(row=0,column=0)
names_label=Label(root)
names_label.grid(row=0,column=1)
prices_label=Label(root)
prices_label.grid(row=0,column=2)
qtys_label=Label(root)
qtys_label.grid(row=0,column=3)
types_label=Label(root)
types_label.grid(row=0,column=4)


def backediting():
    srno_edit_label.grid_forget()
    srno_edit_entry.grid_forget()
    new_edit_label.grid_forget()
    new_edit_entry.grid_forget()
    submitbutton_edit.grid_forget()
    backfromediting.grid_forget()
    rad_kg.grid_forget()
    rad_qty.grid_forget()
    add_name_label.grid_forget()
    add_name_entry.grid_forget()
    add_price_label.grid_forget()
    add_price_entry.grid_forget()
    add_qty_label.grid_forget()
    add_qty_entry.grid_forget()
    radio_none.grid_forget()
    radio_low.grid_forget()
    radio_med.grid_forget()
    radio_high.grid_forget()
    submit_additems.grid_forget()
    srno_removeitems_label.grid_forget()
    srno_removeitems_entry.grid_forget()
    submit_removeitems.grid_forget()

backfromediting=Button(root,text="Cancel",command=backediting)
backfromediting.grid_forget()

refresh()


# 1= Name 2=Prices 3=Quantity 4=Type
global mode
mode=0
modes=['','Name','Price','Quantity','Type']

#Editing options
def edit():
    srno_new=srno_edit_entry.get()
    new=new_edit_entry.get()
    file1=open("items.txt","r")
    first=file1.read().split("\n")
    file1.close()
    n=first[-1][0] #Max sr no
    if not(srno_new).isdigit(): #Makes sure srno is an integer
        messagebox.showerror("Error","You must enter a number for srno")
        return
    elif int(srno_new)<1 or int(srno_new)>int(n): #Makes sure srno is in range
        messagebox.showerror("Error","You must enter a number within range")
        return
    elif (mode==2 or mode==3) and not(new.isdigit()):  #Makes sure price and quantity are integers
        messagebox.showerror("Error","You must enter number for price/quantity")
        return
    else:
        item=first[int(srno_new)].split("|")
        item[mode]=new #Update the correct mode
        final=''
        for i in item:
            if i!="kg" and i!="qty":
                final+=i+"|"
            else:
                final+=i
        first[int(srno_new)]=final
        file2=open("items.txt","w")
        file2.write("")
        file2.close()
        file2=open("items.txt","a")
        for i in first:
            if first.index(i)!=int(n):
                file2.write(i+"\n")
            else:
                file2.write(i)
        file2.close()
        messagebox.showinfo("Info","Database Updated")
        refresh()
        srno_edit_entry.delete(0,END)
        new_edit_entry.delete(0,END)

def type_edit(k):
    srno_new=srno_edit_entry.get()
    file1=open("items.txt","r")
    first=file1.read().split("\n")
    file1.close()
    n=first[-1][0] #Max sr no
    if not(srno_new).isdigit(): #Makes sure srno is an integer
        messagebox.showerror("Error","You must enter a number for srno")
        return
    elif int(srno_new)<1 or int(srno_new)>int(n): #Makes sure srno is in range
        messagebox.showerror("Error","You must enter a number within range")
        return
    else:
        item=first[int(srno_new)].split("|")
        item[mode]=k #Update the correct mode
        final=''
        for i in item:
            if i!="kg" and i!="qty":
                final+=i+"|"
            else:
                final+=i
        first[int(srno_new)]=final
        file2=open("items.txt","w")
        file2.write("")
        file2.close()
        file2=open("items.txt","a")
        for i in first:
            if first.index(i)!=int(n):
                file2.write(i+"\n")
            else:
                file2.write(i)
        file2.close()
        messagebox.showinfo("Info","Database Updated")
        refresh()
        srno_edit_entry.delete(0,END)

global new_edit_label
srno_edit_label=Label(root,text="Enter srno of item")
srno_edit_label.grid_forget()
srno_edit_entry=Entry(root,exportselection=0,fg='blue')
srno_edit_entry.grid_forget()
new_edit_label=Label(root,text="Enter new")
new_edit_label.grid_forget()
type_get=IntVar()
rad_kg=Button(root,text="kg",command=lambda: type_edit("kg"))
rad_kg.grid_forget()
rad_qty=Button(root,text="qty",command=lambda: type_edit("qty"))
rad_qty.grid_forget()
new_edit_entry=Entry(root,exportselection=0,fg='blue')
new_edit_entry.grid_forget()
submitbutton_edit=Button(root,text="Submit",command=edit)
submitbutton_edit.grid_forget()

#all buttons
def editopen(m):
    backediting()
    global new_edit_label
    global mode
    mode=m
    if mode!=4:
        srno_edit_label.grid(row=1,column=5)
        srno_edit_entry.grid(row=1,column=6)
        new_edit_label.grid_forget()
        rad_kg.grid_forget()
        rad_qty.grid_forget()
        new_edit_label=Label(root,text="Enter New "+modes[mode])
        new_edit_label.grid(row=2,column=5)
        new_edit_entry.grid(row=2,column=6)
        submitbutton_edit.grid(row=3,column=5)
        backfromediting.grid(row=3,column=6)
    else:
        srno_edit_label.grid(row=1,column=5)
        srno_edit_entry.grid(row=1,column=6)
        new_edit_label.grid_forget()
        new_edit_entry.grid_forget()
        rad_kg.grid(row=2,column=5)
        rad_qty.grid(row=2,column=6)
        submitbutton_edit.grid_forget()
        backfromediting.grid(row=3,column=5)


edit_name_button=Button(root,text="Edit Name",command= lambda: editopen(1))
edit_name_button.grid(row=1,column=0)
edit_prices_button=Button(root,text="Edit Prices",command=lambda: editopen(2))
edit_prices_button.grid(row=1,column=1)
edit_qty_button=Button(root,text="Edit Quantity",command=lambda: editopen(3))
edit_qty_button.grid(row=1,column=2)
edit_type_button=Button(root,text="Edit Type",command=lambda: editopen(4))
edit_type_button.grid(row=1,column=3)

def showadditems():
    backediting()
    add_name_label.grid(row=1,column=5)
    add_name_entry.grid(row=1,column=6)
    add_price_label.grid(row=2,column=5)
    add_price_entry.grid(row=2,column=6)
    add_qty_label.grid(row=3,column=5)
    add_qty_entry.grid(row=3,column=6)
    radio_none.grid(row=4,column=5)
    radio_low.grid(row=4,column=6)
    radio_med.grid(row=4, column=7)
    radio_high.grid(row=4, column=8)
    submit_additems.grid(row=5,column=5)
    backfromediting.grid(row=5,column=6)

def showremoveitems():
    backediting()
    srno_removeitems_label.grid(row=1,column=5)
    srno_removeitems_entry.grid(row=1,column=6)
    submit_removeitems.grid(row=2,column=5)
    backfromediting.grid(row=2,column=6)

add_button=Button(root,text="Add Item",command=showadditems)
add_button.grid(row=1,column=4)
remove_button=Button(root,text="Remove Item",command=showremoveitems)
remove_button.grid(row=2,column=2)

#Add items options
add_name_label=Label(root,text="Enter Name")
add_name_label.grid_forget()
add_name_entry=Entry(root,exportselection=0, fg='blue')
add_name_entry.grid_forget()
add_price_label=Label(root,text="Enter Price")
add_price_label.grid_forget()
add_price_entry=Entry(root,exportselection=0, fg='blue')
add_price_entry.grid_forget()
add_qty_label=Label(root,text="Enter quantity")
add_qty_label.grid_forget()
add_qty_entry=Entry(root,exportselection=0, fg='blue')
add_qty_entry.grid_forget()
text = ""
additem_type=""

def type_add():
    global additem_type
    additem_type=typeforadd.get()

typeforadd = IntVar()
radio_none = Radiobutton(root, text="None", variable=typeforadd, value=0, command=type_add)
radio_low = Radiobutton(root, text="Low", variable=typeforadd, value=1, command=type_add)
radio_high = Radiobutton(root, text="High", variable=typeforadd, value=3, command=type_add)
radio_med = Radiobutton(root, text="Medium", variable=typeforadd, value=2, command=type_add)
radio_none.grid_forget()
radio_low.grid_forget()
radio_med.grid_forget()
radio_high.grid_forget()

def submitforadd():
    global additem_type
    newname=add_name_entry.get()
    newprice=add_price_entry.get()
    newqty=add_qty_entry.get()
    if not(newprice.isdigit()) or not(newqty.isdigit()):
        messagebox.showerror("Error","Price and Quantity must be integer values")
        return
    elif not(additem_type=="kg" or additem_type=="qty"):
        messagebox.showerror("Error","You must choose a type")
        return
    file=open("items.txt","r")
    things=file.read().split("\n")
    file.close()
    last=things[-1].split("|")
    last_srno=last[0]
    adding=str(int(last_srno)+1)+"|"+str(newname)+"|"+str(newprice)+"|"+str(newqty)+"|"+str(additem_type)
    things.append(adding)
    file=open("items.txt","w")
    file.write("")
    file.close()
    file2=open("items.txt","a")
    count=0
    for i in things:
        if count!=int(last_srno)+1:
            file2.write(i+"\n")
        else:
            file2.write(i)
        count+=1
    file2.close()
    messagebox.showinfo("Info","Database Updated")
    refresh()
    add_name_entry.delete(0,END)
    add_price_entry.delete(0,END)
    add_qty_entry.delete(0,END)
    if additem_type=="kg":
        radio_kg.deselect()
    else:
        radio_qty.deselect()
submit_additems=Button(root,text="Submit",command=submitforadd)
submit_additems.grid_forget()

#Remove items

def removeitem():
    file=open("items.txt","r")
    things=file.read().split("\n")
    file.close()
    last=things[-1]
    last_srno=last[0]
    remove_srno=srno_removeitems_entry.get()
    if not(remove_srno.isdigit()):
        messagebox.showerror("Error","Enter integer for srno")
        return
    elif int(remove_srno)>int(last_srno) or int(remove_srno)<1:
        messagebox.showerror("Error","You must enter value within range")
        return
    ans=messagebox.askyesno("Question","Are you sure you want to delete item "+str(remove_srno)+"?")
    if ans==0:
        return
    stuff=[]
    #stuff:[['Sr No.', 'Items', 'Price', 'Quantity', 'Type'], ['1', 'Apple', '50', '10', 'kg'], ['2', 'Banana', '25', '20', 'kg']]
    for i in things:
        stuff.append(i.split("|"))
    stuff.pop(int(remove_srno))
    for k in range(int(remove_srno),len(stuff)):  #Changes every next index by -1 so that order remains
        stuff[k][0]=str(int(stuff[k][0])-1)
    count=0
    for i in stuff:
        temp=""
        for j in i:
            if (j!="kg" and j!="qty" and j!="Type"):
                temp=temp+j+"|"
            else:
                temp=temp+j
        stuff[count]=temp
        count+=1
    file=open("items.txt","w")
    file.write("")
    file.close()
    file2=open("items.txt","a")
    newcount=0
    for i in stuff:
        if newcount!=(int(last_srno)-1):
            file2.write(i+"\n")
        else:
            file2.write(i)
        newcount+=1
    file2.close()
    messagebox.showinfo("Info","Database Updated")
    srno_removeitems_entry.delete(0,END)
    refresh()

srno_removeitems_label=Label(root,text="Enter srno of item to remove")
srno_removeitems_label.grid_forget()
srno_removeitems_entry=Entry(root,exportselection=0,fg="blue")
srno_removeitems_entry.grid_forget()
submit_removeitems=Button(root,text="Submit",command=removeitem)
submit_removeitems.grid_forget()

root.mainloop()
