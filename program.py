"""
this program is written by Abdullah Ali & Alaadin

and updated by:
    Mohamed Twfik 
    Mohamed Gad 
    Zakaria Loai 
    Hussien Wefky 
    Rabeh Rabie
"""

from tkinter import *
from tkinter.filedialog import askopenfilename
import parser_functions
from parser_functions import *

import os
os.environ["PATH"] += os.pathsep + os.getcwd() + '/inc'

root = Tk()
root.title("Tiny Scanner & Parser")
root.resizable(width=True,height=True)
img = PhotoImage(file="inc/btn.png") ##import
cnv = PhotoImage(file="inc/convert.png")
output_file = 'scanner_output.txt'

initial = ''''''



reserved_words = [
    'if',
    'else',
    'while',
    'programs',
    'for'
]
special_symbols = '+-*/=<>!({)};:'
tiny=''

def read_out():
    file_object = open(output_file)
    file_content = file_object.read()
    file_object.close()
    my_text.replace("1.0","end-1c",file_content)
    root.after(40,read_out) ##get output_file
    


def ask_open_file(event):
    filename = askopenfilename(parent=root,filetypes=[("Text files","*.txt")])
    input_f = open(filename,'r')
    input_list = input_f.readlines()
    input_lines = ''.join(input_list)
    entry.replace("1.0","end-1c",input_lines)
    input_f.close()
    
def get_token(i):
    token = ''
    token_type =''
    while tiny[i]=='/' or tiny[i]==' ' or tiny[i] == '\t':
        if tiny[i]=='/' and tiny[i+1]=='/':
            while (tiny[i]!='\n'):
                i+=1
            i+=1

        while tiny[i]==' ' or tiny[i] == '\t':
            i+=1
            if i>= len(tiny):
                return (i,'','')


    if (tiny[i].isalpha()):
        while tiny[i].isalpha():
            token+=tiny[i]
            i+=1
        if token == "cin":
            if tiny[i] == ">" and tiny[i+1] == ">":
                token += ">>"
                token_type = token
                i+=2
            else:
                token_type = token
        elif token == "cout":
            if tiny[i] == "<" and tiny[i+1] == "<":
                token += "<<"
                token_type = token
                i+=2
            else:
                token_type = token
        elif token in reserved_words:
            token_type = token
        else:
            token_type = 'identifier'
            
    elif (tiny[i].isdigit()):
        while tiny[i].isdigit():
            token+=tiny[i]
            i+=1
        token_type = 'number'

        
    elif tiny[i] in special_symbols:
        if tiny[i] == "=":
            if tiny[i+1] == "=":
                token = "=="
                i+=2
                token_type=token
            else:
                token = "="
                i+=1
                token_type=token
        elif tiny[i] == "!" and tiny[i+1] == "=":
            token = "!="
            i+=2
            token_type=token
        elif tiny[i] == ">" and tiny[i+1] == "=":
            token = ">="
            i+=2
            token_type=token
        elif tiny[i] == "<" and tiny[i+1] == "=":
            token = "<="
            i+=2
            token_type=token
        elif tiny[i] == ";" and i == len(tiny)-1:
            token = tiny[i]
            token_type=token
        else:
            token = tiny[i]
            i+=1
            token_type=token
    else:
        token_type="error"
        while (tiny[i]!=' '):
            token+=tiny[i]
            i+=1
    return (i,token,token_type)
    


def read_Entry(event):
    
    i_string = entry.get("1.0","end-1c")
    if(i_string!=''):
        global tiny
        tiny = i_string.replace('\n',' ')+' '
        index , size = 0 , len(tiny)
        output = []                  
        response = get_token (index)
        while(response[0]<size):
            output.append (response[1]+", "+response[2])
            response = get_token (response[0])

        ###############################
        fob = open(output_file,'w')
        for line in output:
            fob.write(line+'\n')
        fob.close
        read_out()##get_output_file
        # ==== parser time =====
        text = '\n'.join(output)
        tokens = [i.split(', ') for i in text.strip().split('\n')]    # explain
        i = 0
        nodes = []
        parser_functions.tokens = tokens 
        parser_functions.i = i
        parser_functions.nodes = nodes
        program()
        parser_functions.draw(parser_functions.nodes)
        
        # ======================
    
def changeCursor(event):
    event.widget.config(cursor="hand2")

##Front End
left_half = Frame(root,padx=10)
upper_part = Frame(left_half,padx=10,pady=10)
Label(upper_part,text = "write your code ",font=("Courier",13)).pack(side=LEFT,fill=Y,expand=1)#pack
import_btn = Button(upper_part,text = 'or import from file ..',image=img)
import_btn["border"]="0"
import_btn.pack(side=LEFT,fill=Y)#pack
import_btn.bind("<Motion>",changeCursor)
import_btn.bind("<Button-1>",ask_open_file)
upper_part.pack(expand=1)
#upper_part_done
mid_part = Frame(left_half)
entry = Text(mid_part,width=40,height=15,background="#d9fcf1")##height
entry.insert(END, initial)
entry.pack(side=LEFT, fill = Y,expand=1) #pack
entry.config(undo=True)
scroll = Scrollbar(mid_part,command=entry.yview)
entry['yscrollcommand'] = scroll.set
scroll.pack(side =LEFT, fill = Y,expand=1)#pack
mid_part.pack(expand=1,fill=Y)
#mid_part_is_over
lower_part = Frame(left_half)
cnv_btn = Button(lower_part,text = "CONVERT!",image=cnv)
cnv_btn["border"]="0"
cnv_btn.pack(fill=Y)#pack
cnv_btn.bind("<Motion>",changeCursor)
cnv_btn.bind("<Button-1>",read_Entry)
lower_part.pack(expand=1,fill=Y,pady=10)
### left part over
left_half.pack(side="left",fill=Y,expand=1)
##output_file
right_half = Frame(root)
my_output_frame = Frame(right_half, bd=2, relief=SUNKEN)
Label(my_output_frame,text = "Scanner Output",font=("Courier",13),pady = 10).pack()#pack
#text widget and associated Scrollbar widget
my_text=Text(my_output_frame, height=15, width =40,pady = 10)

my_text.pack(side=LEFT, fill=Y, padx=5)

#add scrollbar widget to the text widget
my_scrollbar = Scrollbar(my_output_frame, orient=VERTICAL, command=my_text.yview)
my_scrollbar.pack(fill=Y,expand=1,side=LEFT)
my_text.configure(yscrollcommand=my_scrollbar.set)
my_output_frame.pack(pady=10,fill=Y,expand=1,side=LEFT) #output frame
right_half.pack(side="left",expand=1,fill=Y,pady=5)#right half


root.mainloop()
