#from paths import shapes
#import paths
#import texts
import threading
from time import sleep
import random
from visual import *

#constants
MALE =1
FEMALE = 0
MAX_PEOPLE = 3



# global variables
queue= list()               #to maintain queue outside bathroom
workers = list()
working = list()

# coordinates to stop at when entering bathroom
bathroom_coordinates = list()
bathroom_coordinates.append([-10,-3,-4])
bathroom_coordinates.append([-9,-3,-4])
bathroom_coordinates.append([-8,-3,-4])



personNo=0                  # provides id for each person
PeopleInBathroom=0
GenderUsingBathroom=0

#current pos in queue
queue_x = -1
queue_y = -3
queue_z = 0

# semaphores
sem_bathroom=   threading.Semaphore( value= MAX_PEOPLE)
sem_queue = threading.Semaphore()
sem_mutex = threading.Semaphore()


# to create balls (people)
class myclass(object):
    def __init__(self, k,x,y):
        if (k  == MALE):
            self.k = sphere(pos =(x,y,0),radius = 0.3,color = color.blue)
        else :
            self.k = sphere(pos =(x,y,0),radius = 0.3,color = color.red)






# function to move the object to specified coordinates

def approach(obj, x,y):


    x_sign=0
    y_sign=0


    # checking whether to move left or right
    if (workers[obj][2].k.pos.y < y):
        y_sign = 1
    else:
        y_sign = -1

    if (workers[obj][2].k.pos.x < x):
        x_sign = 1
    else:
        x_sign = -1


    #moving
    while  workers[obj][2].k.pos.y!=y:
        workers[obj][2].k.pos.y+=y_sign
        sleep(0.1);


    while workers[obj][2].k.pos.x != x:
        workers[obj][2].k.pos.x+=x_sign
        sleep(0.1)

# end of approach




# function to create working area

def WorkingArea():
    global personNo
    sem_mutex.acquire()
    for i in range(0,5):
        for j in range (0,5):
            num=random.randint(1,20)%2
            workers.append([num,personNo,myclass(num,i,j),i,j])
            working.append(personNo)
            personNo+=1

    sem_mutex.release()












def ApproachBathroom():  #generates people who need to use bathroom at random times

    global queue
    global personNo
    global queue_x
    global queue_y

    while 1:
        sem_queue.acquire()
        sem_mutex.acquire()
        temp = random.randint(0,len(working))

        a = working[temp]
        working.remove(a)

        while workers[a][2].k.pos.x < 7:
            workers[a][2].k.pos.x+=1

        approach(a,queue_x,queue_y)
        queue_x+=1

        if workers[a][0]==MALE:
            queue.insert(0,a)
            #myclass(MALE,random.randint(1,10))
            #personNo+=1
            print "\na male came, id=",  workers[a][1]

        else:
            queue.insert(0,a)
            #myclass(FEMALE,random.randint(1,10))
            #personNo+=1
            print "\na female came, id=", workers[a][1]

        sem_mutex.release()
        sem_queue.release()
        #sleep for a random time
        sleep(random.randint(1,2))


# end of ApproachBathroom




def StandInQueue():                 # function to send people into bathroom for queue

    global queue
    global GenderUsingBathroom
    global PeopleInBathroom
    global queue_x

    while 1:

        sem_queue.acquire()
        if len(queue)>0:
            p = queue[len(queue)-1]

            sem_queue.release()

            sem_mutex.acquire()  # for GenderUsingBathroom

            if GenderUsingBathroom == workers[p][0] :    # if same gender, go in

                sem_mutex.release()
                sem_bathroom.acquire()
                queue.pop()
                t = threading.Thread(target=Use,args=(p,))
                t.start()



            else:                               # if different gender, wait till all others come out
                print "\nwaiting for other to come out"
                while PeopleInBathroom > 0:
                    sem_mutex.release()
                    sleep(1)
                    sem_mutex.acquire()



                sem_mutex.release()
                sem_bathroom.acquire()
                queue.pop()
                GenderUsingBathroom = workers[p][0]
                t1 = threading.Thread(target=Use,args=(p,))
                t1.start()





        else:
            sem_queue.release()


# end of StandInQueue




def Use( person):             # monitors the usage of bathroom for each person

    global PeopleInBathroom
    global queue_x
    global queue



    sem_mutex.acquire()
    coordinates = bathroom_coordinates.pop()


    approach(person,coordinates[0],coordinates[1])

    for i in queue:
        workers[i][2].k.pos.x-=1

    queue_x-=1

    print "\nperson " , workers[person][1],"entering from bathroom , gender = ",
    if workers[person][0]==FEMALE:
        print "FEMALE"
    else:
        print "MALE"

    PeopleInBathroom+=1   #enters bathroom
    sem_mutex.release()


    sleep(random.randint(3,5))    # spend some time in bathroom

    sem_mutex.acquire()

    print "\nperson " , workers[person][1],"exiting from bathroom"


    while workers[person][2].k.pos.y < 1:
        workers[person][2].k.pos.y+=1


    PeopleInBathroom-=1   #leave bathroom
    sem_mutex.release()

    bathroom_coordinates.insert(0,coordinates)
    sem_bathroom.release()

    approach(person,workers[person][3],workers[person][4])

    sleep(1)
    sem_mutex.acquire()
    working.append(person)
    sem_mutex.release()


# end of Use






if __name__ == "__main__":

    #rt = paths.rectangle(pos=(-2,3), width=5, height=3)
    mybox = box(pos=(-10,-4,-4), length=8, height=4, width=0.1)
    #text(text='Bathroom', align='center', depth=-0.3, color=color.green, height = 1, start= -8)
    label( pos=vector(-10,-8,-4), text='  Bathroom  ' ,height = 16)
    label( pos=vector(3,-5,-4), text='  Queue  ' ,height = 16)
    label( pos=vector(2.5,6,0), text='  Workers: Males (blue) \n      Females (red)  ' ,height = 16)
    t1 = threading.Thread(target=ApproachBathroom)
    #threads.append(t)
    WorkingArea()
    t1.start()
    t2 = threading.Thread(target=StandInQueue)
    #threads.append(t)
    t2.start()
