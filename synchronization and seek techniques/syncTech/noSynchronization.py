# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 18:22:28 2022

@author: Ahmed EL-brawany
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 22:26:37 2022

@author: Ahmed EL-brawany
"""
import time
import threading



ProcessesList = []
UI = None

x=0

def critical_region():
    try:
        global UI, x
        #printing process name
        local_x= x
        local_x += 1
        time.sleep(0.1)
        x= local_x
        UI.refresh_label(int(threading.current_thread().name[-1])-1, text= f"\nStarted running critical region       value of x: {x}\n\n" + f"Hello I'm {threading.current_thread().name}")
        # sleep for one second
        time.sleep(5)
        #print hi 
        UI.refresh_label(int(threading.current_thread().name[-1])-1, text= "Hi, welcome to Advanced OS")
    except:
        pass



def main(ui, pnum):

    global UI
    UI = ui
    ProcessesList.clear()
    # creating threads as if they are processes going to operate concurrently 
    for num in range(pnum):
        ProcessesList.append(threading.Thread(target=critical_region, name = f"process {num+1}"))
    
    # staring the processes
    for process in ProcessesList:
        ui.create_process_window(process.name)
        process.daemon = True
        process.start()
        
    
    # calling the join function 
    #to make sure that the main thread which excuting all this code 
    #doesn't finish execution until all other thread are completed or finished 
    # for process in ProcessesList:
    #     process.join()