# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 12:04:09 2022

@author: Ahmed EL-brawany
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 10:39:24 2022

@author: Ahmed EL-brawany
"""
import time 
import threading

S = 1
waitingList = []
ProcessesList = []
UI = None
os = None
x=0
class OS:
    
    def __init__(self):
        print("_____________________________\n")
        print("OS is running")
        print("_____________________________\n")

        
        
    def test(self, process):
        """
        the function test is used to make the OS check the S 
        if it's busy (S=0) the process is added to a waiting list
        until it's instructed by the OS to start executing 
        """
        global S, waitingList
        #process check the S.
        if S > 0:
            # if S > 0 the OS start a calling process to execute the critical region
            S -= 1
            print(f"OS: start executing {process.name}")
            process.start()
        else:    
            # otherwise (S=0) the OS add the process to the waiting list (process blocked) 
            print(f"\nOS: adding {process.name} to waiting list \n")
            waitingList.append(process)
        
    def increment(self):
        """
        the increment function is called when a process finishes execution of the critical
        region.
        
        it increments the S and if there is a process in the waiting list (blocked)
        the OS allow the process to start executing the critical region and decrement
        the S so that no other process can access the critical region.
        """
        global S
        S +=1
        if waitingList:
            S -= 1
            print(f"OS: start executing {waitingList[0].name}")
            waitingList.pop(0).start()
        
    def calling_process(self, process):
        """
        this function notify the OS that there is a process wants to access the critical
        region, which makes the OS activates the test function.
        """
        self.test(process)
            
        
        


def critical_region():
    """
    critical region function where only one process can access it at a time to 
    avoid deadlocks...

    """ 
    try:
        global S, os, UI, x
        
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
    
        # when the process finishes executing the critical region, the OS activates the increment function
        os.increment()
    except:
        pass
    
    
def main(ui, pnum):
    global UI, os
    
    UI = ui
    os = OS() 
        
    # creating processes to be called, you can change the number in range(number) below to create more processes 
    for num in range(pnum):
        ProcessesList.append(threading.Thread(target=critical_region, name = f"process {num+1}"))
       
    # calling all processes with difference of 1 second between each calling
    for process in ProcessesList:
        ui.create_process_window(process.name)
        process.daemon = True
        time.sleep(2)
        os.calling_process(process)
    
    # preventing main thread from finishing the execution until all threads finish execution
    # for process in ProcessesList:
    #     process.join()
    
