# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 22:26:37 2022

@author: Ahmed EL-brawany
"""
import time
import threading


key = 0
ProcessesList = []
UI = None
x=0
def test():
    """
    the function test is used to make the process continously check the key 
    until it's free (key=0) which allow the process to run the critical region
    """
    global key
    #continously checking the key...
    while key:
        #UI.refresh_label(int(threading.current_thread().name[-1])-1, text= f"{threading.current_thread().name} continously checking...")
        pass
        
    #when key=0 the process sets the key and start executing the critical region.
    key=1


def critical_region():
    """
    critical region function where only one process can access it at a time to 
    avoid deadlocks...
    
    if you comment out the test() in line 33 below we can see the difference in the output,
    where all processes will execut the same function (critical region) at the same time
    """
    try:
        test()    
        global key, UI, x
        local_x= x
        local_x += 1
        time.sleep(0.1)
        x= local_x
        #printing process name
        UI.refresh_label(int(threading.current_thread().name[-1])-1, text= f"\nStarted running critical region       value of x: {x}\n\n" + f"Hello I'm {threading.current_thread().name}")
        # sleep for one second
        time.sleep(5)
        #print hi 
        UI.refresh_label(int(threading.current_thread().name[-1])-1, text= "Hi, welcome to Advanced OS")
    
        # when releasing the critical region the process reset the key
        key=0 
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
        time.sleep(2)
        process.start()
        
    
    # calling the join function 
    #to make sure that the main thread which excuting all this code 
    #doesn't finish execution until all other thread are completed or finished 
    # for process in ProcessesList:
    #     process.join()