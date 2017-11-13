from Tkinter import *
import threading
from time import sleep
import random

class App(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()

#Declare App object
root = App()
root.master.title("Unisex Bathroom Simulation")
root.master.minsize(width=1024, height=720)
root.master.maxsize(width=1024, height=720)

#Add and align images
male = PhotoImage(file="male.gif")
female = PhotoImage(file="female.gif")
bathroom = PhotoImage(file="unisex_bathroom.gif")
#w2 = Label(root, image=female, borderwidth=2, bg="green").pack(side=LEFT, padx=10)
w3 = Label(root, image=bathroom, compound=CENTER, bg="blue").pack(side=LEFT, padx=10)
#w4 = Label(root, image=male, borderwidth=2, bg="green").pack(side=LEFT, padx=10)
global w1, w2

#constants
MALE =1
FEMALE = 0
MAX_PEOPLE = 3

# global variables
queue= list()               #to maintain queue outside bathroom
personNo=1                  # provides id for each person
PeopleInBathroom=0
GenderUsingBathroom=0


# semaphores
sem_bathroom=   threading.Semaphore( value= MAX_PEOPLE)
sem_queue = threading.Semaphore()
sem_mutex = threading.Semaphore()

def GeneratePeople():  #generates people who need to use bathroom at random times

    global queue
    global personNo
    global w1, w2


    while 1:
        sem_queue.acquire()

        if random.randint(0,1)==MALE:
            queue.insert(0,[MALE,personNo]);
            personNo+=1
            w2 = Label(root, image=male, borderwidth=2, bg="red").pack(side=LEFT, padx=10)
            print "\na male came, id=", personNo-1
        else:
            queue.insert(0,[FEMALE,personNo]);
            personNo+=1
            w1 = Label(root, image=female, borderwidth=2, bg="red").pack(side=LEFT, padx=10)
            print "\na female came, id=", personNo-1

        sem_queue.release()
        #sleep for a random time
        sleep(random.randint(1,2))


# end of GeneratePeople




def GoIn():                 # function to send people into bathroom for queue

    global queue
    global GenderUsingBathroom
    global PeopleInBathroom

    while 1:

        sem_queue.acquire()
        if len(queue)>0:
            p = queue.pop()

            sem_queue.release()

            sem_mutex.acquire()  # for GenderUsingBathroom

            if GenderUsingBathroom == p[0] :    # if same gender, go in

                sem_mutex.release()
                sem_bathroom.acquire()
                t = threading.Thread(target=UsingTime,args=(p,))
                t.start()



            else:                               # if different gender, wait till all others come out
                print "\nwaiting for other to come out"
                while PeopleInBathroom > 0:
                    sem_mutex.release()
                    sleep(1)
                    sem_mutex.acquire()

                sem_mutex.release()
                sem_bathroom.acquire()
                GenderUsingBathroom = p[0]
                t1 = threading.Thread(target=UsingTime,args=(p,))
                t1.start()


        else:
            sem_queue.release()


# end of GoIn




def UsingTime( person):             # monitors the usage of bathroom for each person

    global PeopleInBathroom

    sem_mutex.acquire()
    print "\nperson " , person[1],"entering from bathroom , gender = ",
    if person[0]==FEMALE:
        print "FEMALE"
        w1.config(bg="green")
    else:
        print "MALE"
        w2.config(bg="green")

    PeopleInBathroom+=1   #enters bathroom
    sem_mutex.release()


    sleep(random.randint(1,3))    # spend some time in bathroom

    sem_mutex.acquire()
    PeopleInBathroom-=1   #leave bathroom
    print "\nperson " , person[1],"exiting from bathroom"
    sem_mutex.release()

    sem_bathroom.release()


# end of UsingTime






if __name__ == "__main__":

    t1 = threading.Thread(target=GeneratePeople)
    #threads.append(t)
    t1.start()
    t2 = threading.Thread(target=GoIn)
    #threads.append(t)
    t2.start()

#Run event loop
root.mainloop()
