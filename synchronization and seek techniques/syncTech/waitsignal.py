# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 10:39:24 2022

@author: Ahmed EL-brawany
"""
import time 
import threading

key = 0
waitingList = []
ProcessesList = []
UI = None
x=0
class process:
    
    def __init__(self, name):
        # creating the process 
        self.process = threading.Thread(target = self.test, name = name)
        # adding the waiting functionality to the process
        self.eve = threading.Event()
        # start the process
        #self.process.start()
        
    def wait(self):
        """
        the function wait is made to make the process wait for a signal from the 
        process that is currently running the critical region.
        """
        self.eve.wait()
        
    def signal (self):
        """
        the function signal is made to signal the waiting process to start 
        executing the critical region
        """
        global key
        self.eve.set()
        #when the process is signaled it sets the key and start executing the critical region
        key = 1
        
    def test(self):
        """
        the function test is used to make the process check the key 
        if it's not free (key=1) the process is added to a waiting list
        until it's signaled by the process that is currently running the critical region
        """
        global key, waitingList
        #process check the key.
        if key:
            # if key = 1 the process is added to a waiting list
            waitingList.append(self)
            # printing that the process is added to the waiting list 
            # just printing for the user to give a better understanding of what's happening  
            print(f"{threading.current_thread().name} is added to the waiting list")
            self.wait()
        key = 1
        critical_region()
        


def critical_region():
    """
    critical region function where only one process can access it at a time to 
    avoid deadlocks...

    """ 
    try:
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
        if waitingList:
            waitingList.pop(0).signal()
    except:
        pass
    # global key
    # #printing process name
    # print(f"Hello I'm {threading.current_thread().name}")
    # # sleep for one second
    # time.sleep(1)
    # #print hi 
    # print("Hi, welcome to Advanced OS")
    # print("----------------------------------------")
    # # when releasing the critical region the process reset the key
    # key = 0
    # # then if there are any waiting processes it signals one of them.
    # if waitingList:
    #     waitingList.pop(0).signal() 
    
    
    
def main(ui, pnum):  
    global UI
    UI = ui
    ProcessesList.clear()
    # creating threads as if they are processes going to operate concurrently 
    for num in range(pnum):
        ProcessesList.append(process(f"process {num+1}"))
    
    # staring the processes
    for p in ProcessesList:
        ui.create_process_window(p.process.name)
        p.process.daemon = True
        time.sleep(2)
        p.process.start()
        
        
# p1 = process("process 1")
# p2 = process("process 2")
# # you can comment out the line (time.sleep) below to see some differences in the output
# time.sleep(1)
# p3 = process("process 3")

# # preventing the main thread to finish execution until all threads finish execution.
# p1.process.join()
# p2.process.join()
# p3.process.join()