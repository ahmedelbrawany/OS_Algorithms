# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 10:18:50 2021

@author: Ahmed EL-brawany
"""

from tkinter import Label, Button, Scale, Toplevel, Entry, Frame, Tk, IntVar, HORIZONTAL,END, Radiobutton
from tkintertable import TableCanvas, TableModel
from PIL import ImageTk
import sys
from syncTech.testset import main as tsmain
from syncTech.waitsignal import main as wsmain
from syncTech.Semaphore import main as semain
from syncTech.noSynchronization import main as nosemain
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from seekTech import *


processesLabels = []
pos1 = 0
pos2 = 0

def plot(x):

    fig= plt.figure(figsize=(10,10))
    y= [n for n in range(1,len(x)+1)]
    y.reverse()
    #plt.rcParams["figure.figsize"] = [20, 20]
    #plt.rcParams["figure.autolayout"] = True
    #plt.ylim((0,50))
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.plot(x,y, color="r", marker='o', linewidth=4, markersize=10)
    for i, j in zip(x, y):
        plt.text(i, j+.1, '({}, {})'.format(i, j))
    plt.xlabel("Tracks")
    return fig
   # chart_type = FigureCanvasTkAgg(fig, h)
   # chart_type.get_tk_widget().place(x=650, y=0)

class UI:
    
    def __init__(self, root):
        """
        buliding user interface...
        """
        self.root = root
        self.root.title("User Interface")
        self.root.geometry("700x430+0+0")
        
        self.root_bg = ImageTk.PhotoImage(file="background.jpg")
        bg = Label(self.root, image = self.root_bg).place(x=0, y=0)
        
        
        self.start_btn = Button(self.root, text="Start >",font=("times new roman", 15, "bold"), bg ='green', fg="white", bd=0, command= self.start_clicked)
        self.start_btn.place(x=320, y=370)
        
        
        self.frame = Frame(self.root, width=500, height=250, bg="#444444")
       
        self.question = Label(self.frame, font=("times new roman", 13,"bold"), bg="#444444", fg="white")
        self.question.place(x=50, y= 50)

        # user interface for yes or no questions
        # var, append_here are used for controlling puproses 
        self.var = IntVar()

        self.r_control = IntVar(value=1)
        self.r_buttons_text = {"sync": ["Test & Set", "Wait & Signal", "Semaphore", "No Synchronization"], "seek": ["FCFS", "SSTF", "SCAN", "LOOK"]}
        self.r_button1 = Radiobutton(self.frame, variable= self.r_control, value=1, bg = "#444444", fg="white", activebackground="#444444", selectcolor= "#444444")
        self.r_button2 = Radiobutton(self.frame, variable= self.r_control, value=2, bg = "#444444", fg="white", activebackground="#444444", selectcolor= "#444444")
        self.r_button3 = Radiobutton(self.frame, variable= self.r_control, value=3, bg = "#444444", fg="white", activebackground="#444444", selectcolor= "#444444")
        self.r_button4 = Radiobutton(self.frame, variable= self.r_control, value=4, bg = "#444444", fg="white", activebackground="#444444",selectcolor= "#444444")
       
        self.ok = Button(self.frame, text="OK", font=("times new roman", 15), bg="green", fg="white", bd=0, width=5, height=1, command= self.ok_clicked)
        self.syncType="" 
        
        # user interface for degree questions
        self.degree_label = Label(self.frame, text="Processes: ", font=("times new roman", 12, 'bold'), bg="#444444", fg="white")
        self.slider = Scale(self.frame, from_=2, to=5, orient = HORIZONTAL, sliderrelief='flat', highlightthickness=0, bg='#444444', fg='white', troughcolor='#73B5FA', length= 300)
        
        self.entry = Entry( self.frame, font=("times new roman", 10, "bold"), justify="center", width=50)
        
        self.run = Button(self.frame, text="RUN", font=("times new roman", 10), bg="green", fg="white", bd=0, width=7, height=1, command = self.run_clicked)
        self.runType = ""
        # this button used for control purposes only not for the user to use
        self.wait_until_button_press = Button(self.frame, command = lambda: self.var.set(1))

        self.made_by = Label(self.root, text="Made by: Ahmed El-Brawany", bg="black", fg="red")
        self.made_by.place(x=4, y=410)
        
        self.logo_image = ImageTk.PhotoImage(file="FEE logo.png")
        self.logo_label = Label(self.root, image= self.logo_image)
        self.logo_label.place(x=0, y=0)        
        
        self.root.protocol("WM_DELETE_WINDOW", self.Exit)

    def start_clicked(self):
        """
        this function is activated when start button is clicked,
        used to show the frame with its children to the user for
        interaction
        """
        #self.frame.place(x=100, y=100)
        self.start_btn.place_forget()
        self.whichWindow = Toplevel(self.root)
        self.whichWindow.geometry(f"500x200+300+300")
        self.whichWindow.config(bg="#444444")
        self.whichWindow.title("choose")
        self.whichWindow.protocol("WM_DELETE_WINDOW", lambda: None)
        
        label = Label(self.whichWindow, text = "Choose which algorithms you want to proceed.", font=("times new roman", 15, "bold"), bg="#444444", fg="white")
        label.place(x=40, y=40)
        
        syncButton = Button(self.whichWindow, text="Sync Algorithms", font=("times new roman", 15, "bold"), bg ='green', fg="white", bd=0, command= lambda : self.user_interaction(1))
        syncButton.place(x=40, y=100)
        
        seekButton = Button(self.whichWindow, text="Seek Algorithms", font=("times new roman", 15, "bold"), bg ='blue', fg="white", bd=0, command= lambda : self.user_interaction(0))
        seekButton.place(x=300, y=100)

        
    def R_buttons(self, Type):
        """
        this function is used to display necessary components for 
        yes or no questions on the frame
        
        """
        self.slider.place_forget()
        self.entry.place_forget()
        self.degree_label.place_forget()
        self.run.place_forget()
        
        self.r_button1.config(text= self.r_buttons_text[Type][0])
        self.r_button2.config(text= self.r_buttons_text[Type][1])
        self.r_button3.config(text= self.r_buttons_text[Type][2])
        self.r_button4.config(text= self.r_buttons_text[Type][3])
        
        self.r_button1.place(x=20, y=100)
        self.r_button2.place(x=120, y=100)
        self.r_button3.place(x=250, y=100)
        self.r_button4.place(x=350, y=100)
        self.ok.place(x=200, y=150)
        
        
    def slider_ok(self):
        """
        this function is used to display necessary components for 
        degree questions on the frame
        """
        self.ok.place_forget()
        self.r_button1.place_forget()
        self.r_button2.place_forget()
        self.r_button3.place_forget()
        self.r_button4.place_forget()
        self.entry.place_forget()
        
        self.slider.place(x=150, y=120)
        self.degree_label.place(x=70, y=135)
        self.run.place(x=220, y=200)
        
    
    def entry_ok(self):
        self.ok.place_forget()
        self.r_button1.place_forget()
        self.r_button2.place_forget()
        self.r_button3.place_forget()
        self.r_button4.place_forget()
        
        
        self.entry.place(x=80, y=120)
        self.run.place(x=230, y=200)
    def ok_clicked(self):
        """
        this function is activated when ok button is clicked.
        """
        self.wait_until_button_press.invoke()
        self.syncType = self.r_control.get()
    
    
    def run_clicked(self):
        """
        this function is activated when run button is clicked
        """
        self.wait_until_button_press.invoke()

        if self.runType:
            processesLabels.clear()
            if self.syncType == 1:
                t = threading.Thread(target = tsmain ,args = [self, self.slider.get()])
                t.start()
            elif self.syncType==2:
                t = threading.Thread(target = wsmain, args = [self, self.slider.get()])
                t.start()
            elif self.syncType==3:
                t = threading.Thread(target = semain, args = [self, self.slider.get()])
                t.start()
            elif self.syncType==4:
                t = threading.Thread(target = nosemain, args = [self, self.slider.get()])
                t.start()
            
            self.slider.set(0)
        
        else:
            tracks = self.entry.get().replace(" ", "").split(",")
            tracks = [int(track) for track in tracks]
            seekTitle = ""
            if self.syncType == 1:
                dis_table, tracksOrder = FCFS(tracks)
                fig = plot(tracksOrder)
                seekTitle= "FCFS"
            elif self.syncType==2:
                dis_table, tracksOrder = SSTF(tracks)
                fig = plot(tracksOrder)
                seekTitle= "SSTF"
            elif self.syncType==3:
                dis_table, tracksOrder = SCAN(tracks)
                fig = plot(tracksOrder)
                seekTitle= "SCAN"
            elif self.syncType==4:
                dis_table, tracksOrder = LOOK(tracks)
                fig = plot(tracksOrder)
                seekTitle= "LOOK"
             
            
             
            seekOutput = Toplevel(self.root)
            
            myframe = Frame(seekOutput, width = 600, height=700, bg="#444444")  
            myframe.place(x=0, y=0)
            table = TableCanvas(myframe,data= dis_table,
			cellwidth=60, cellbackgr='#e3f698',
			thefont=('times new roman',20),rowheight=23, rowheaderwidth=50,
			rowselectedcolor='yellow', read_only=False)
            table.show()
            
                  
            seekOutput.geometry("1350x700+0+0")
            seekOutput.config(bg="#444444")
            seekOutput.title(f"{seekTitle} Seek Output")
            
            chart_type = FigureCanvasTkAgg(fig, seekOutput)
            chart_type.get_tk_widget().place(x=650, y=0)
            

            #label = Label(seekOutput, text = dis_label, font=("times new roman", 30, 'bold'), bg="#444444", fg="white" )

            self.entry.delete(0, END)
    
    def user_interaction(self, which):
        """
        this function is used for user interaction (display questions, saving 
        answers, show results).
        """
        try:
            self.whichWindow.destroy()
            self.frame.place(x=100, y=100)
            self.runType = which
            if which:
                self.question.config(text= "Which Synchronization technique do you want to use ?")
                self.R_buttons("sync")
                
                self.wait_until_button_press.wait_variable(self.var)
                self.var.set(0)
                    
                self.question.config(text = "How many processes do you want to execute concurrently?")
                self.slider_ok()
                
                # wait until user answers    
                
            
            else:
                self.question.config(text= "Which Seek technique do you want to use ?")
                self.R_buttons("seek")
                
                self.wait_until_button_press.wait_variable(self.var)
                self.var.set(0)
                
                self.question.config(text = "Enter the initial position of the head followed by\n tracks seperated by commas ended with . Ex: 4,15,20,5")
                self.entry_ok()
                
            
            # show the results and returning back to the begining
            self.wait_until_button_press.wait_variable(self.var)
            self.var.set(0)
            self.back_to_start() 
        except:
            print("e in user interface")
    
    def create_process_window (self, title):
        global pos1, pos2
        process_window = Toplevel(self.root)
        process_window.title(title)
        process_window.geometry(f"700x430+{pos1*650}+{pos2*400}")
        pos2 = pos1 ^ pos2
        pos1 =  not pos1
        process_window.config(bg="#444444")
        process_frame = Frame(process_window ,width=500, height=250, bg="white")
        process_frame.place(x=100,y= 100)
        process_label = Label(process_frame, text="", font=("times new roman", 12, 'bold'), bg="white", fg="black")
        process_label.place(x=50,y= 50)
        processesLabels.append(process_label)

    
    def refresh_label(self, label, text):
        if not "continously" in text:
            processesLabels[label].config(text =processesLabels[label].cget("text")+"\n"+text)
        else:
            processesLabels[label].config(text =text)
            
            
    def back_to_start(self):
       """
       this function is used to return back to the begining and clear all
       lists and variables so it can be used again.
       """ 
       global pos1, pos2
       pos1 =0
       pos2 =0
       self.frame.place_forget()
       self.start_btn.place(x=320, y=350)  

       
       
    def Exit(self): 
        self.var.set(self.var.get())
        self.root.quit()
        self.root.destroy()
        sys.exit()

       
     
def main():

    root = Tk()
    user_interface = UI(root)    
    root.mainloop()
    
   
if __name__ == "__main__":
    main()