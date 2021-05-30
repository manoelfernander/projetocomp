from tkinter import *

inicio = Tk()
l = 800
h = 650
inicio.geometry(str.format('{}x{}',l,h))
inicio['bg']='black'
bvindo = Label(inicio,text='BEM VINDO AO',font='Britannic 15',bg='black',fg='white').place(x=l/2,y=(h/2)-300,anchor='center')
guluma = Label(inicio,text='GULUMA',font='Algerian 80 bold',bg='black',fg='red',height=1).place(x=l/2,y=(h/2)-200,anchor='center')
sub = Label(inicio,text='Seu novo sistema de recomendação de filmes!',font='Britannic 15',bg='black',fg='white').place(x=l/2,y=(h/2)-100,anchor='center')
insiranome = Label(inicio,text='Insira seu nome:',font='Britannic 15',bg='black',fg='white').place(x=l/2,y=(h/2)-40,anchor='center')
nome = Entry(inicio,font='Britannic 15',width=10).place(x=l/2,y=h/2,anchor='center')

inicio.mainloop()
