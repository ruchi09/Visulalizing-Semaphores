import threading
from time import sleep
import random

TIMEOUT = 4
MALE =1
FEMALE = 0
MAX_PEOPLE = 3


queue= list()
personNo=1
PeopleInBathroom=0
GenderUsingBathroom=0


# semaphores
sem_bathroom=   threading.Semaphore( value= MAX_PEOPLE)
sem_queue = threading.Semaphore()
sem_mutex = threading.Semaphore()










def GeneratePeople():

    global queue
    global personNo


    while 1:
        sem_queue.acquire()

        if random.randint(0,1)==MALE:
            queue.insert(0,[MALE,personNo]);
            personNo+=1
            print "\na male came, id=", personNo-1
        else:
            queue.insert(0,[FEMALE,personNo]);
            personNo+=1
            print "\na female came, id=", personNo-1

        sem_queue.release()
        #sleep for a random time
        sleep(random.randint(1,2))


# end of GeneratePeople




def GoIn():

    global queue
    global GenderUsingBathroom

    while 1:

        sem_queue.acquire()
        if len(queue)>0:
            p = queue.pop()

            sem_queue.release()

            sem_mutex.acquire()
            print "\nNext turn: ",p
            if GenderUsingBathroom == p[0] :    # if same gender, go in
                print "\nsame gender"
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
                t1 = threading.Thread(target=UsingTime,args=(p,))
                t1.start()
                GenderUsingBathroom = p[0]

        else:
            sem_queue.release()


# end of GoIn




def UsingTime( person):

    global PeopleInBathroom

    sem_mutex.acquire()
    print "\nperson " , person[1],"entering from bathroom , gender = ",person[0]

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
