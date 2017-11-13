import threading
from time import sleep
import random

TIMEOUT = 4
MALE =1
FEMALE = 0
MAX_PEOPLE = 3

MalesInQueue=0
FemalesInQueue=0
PeopleInBathroom=0
GenderUsingBathroom=0


# semaphores
bathroom=   threading.Semaphore( value= MAX_PEOPLE)
queue = threading.Semaphore()
mutex = threading.Semaphore()








def timer():
    global GenderUsingBathroom

    global PeopleInBathroom

    while 1 :
        t=TIMEOUT
    #    print "Timer starts"

    #     if GenderUsingBathroom == MALE:
    # #        print "MALE's turn"
    #     else:
    # #        print "Female's turn"


        while t>0 and PeopleInBathroom>0:
            mutex.acquire()
            sleep(1)
            t-=1
            mutex.release()

        if GenderUsingBathroom == MALE:
            GenderUsingBathroom = FEMALE
            #print "Now FEMALE's turn"

        elif GenderUsingBathroom == FEMALE:
            #print "Now MALE's turn"
            GenderUsingBathroom= MALE

        while PeopleInBathroom>0:
            mutex.release()
            sleep(1)
            mutex.acquire()

        mutex.release()

    #    print "\n Timeout"



def GeneratePeople():

    global MalesInQueue
    global FemalesInQueue

    while 1:
        queue.acquire()

        if random.randint(0,1)==MALE:
            MalesInQueue+=1
            print "a male came"
        else:
            FemalesInQueue+=1
            print "a female came"

        queue.release()
        #sleep for a random time
        sleep(random.randint(1,2))


# end of GeneratePeople




def GoIn():

    global GenderUsingBathroom
    global MalesInQueue
    global FemalesInQueue
    global PeopleInBathroom

    male_flag=0
    female_flag=0
    while 1:
        male_flag=0
        female_flag=0
        mutex.acquire()
        queue.acquire()
        print "inside while"

        if GenderUsingBathroom == MALE:
            print "MALE turn"

        else:
            print "FEMALE TURN"



        while GenderUsingBathroom==MALE and MalesInQueue>0 :   # men's turn
            print "inside male while"
            mutex.release()
            queue.release()
            male_flag=1
            bathroom.acquire()   # wait for bathroom

            mutex.acquire()
            queue.acquire()
            MalesInQueue-=1
            PeopleInBathroom+=1
            mutex.release()
            queue.release()
            print "male went into bathroom"
            t = threading.Thread(target=UsingTime,args=(MALE,))
            # threads.append(t)
            t.start()

            #pthread_create : UsingTime(id);

        if male_flag==0:
            mutex.release()
            queue.release()

        mutex.acquire()
        while PeopleInBathroom>0 :    # Waiting for remaining men to come out

            mutex.release()
            sleep(1)
            mutex.acquire()



        queue.acquire()

        while GenderUsingBathroom==FEMALE and FemalesInQueue>0:      # Now women's turn
            print "inside female while"
            mutex.release()
            queue.release()
            female_flag=1
            bathroom.acquire()   # wait for bathroom

            mutex.acquire()
            queue.acquire()
            FemalesInQueue-=1
            PeopleInBathroom+=1
            mutex.release()
            queue.release()
            #pthread_create: UsingTime(id)  #create thread to monitor person's time in bathroom
            print "female went into bathroom"
            t = threading.Thread(target=UsingTime,args=(FEMALE,))
            # threads.append(t)
            t.start()



        if female_flag==0:
            mutex.release()
            queue.release()
        mutex.acquire()

        while PeopleInBathroom>0:    # Waiting for remaining ladies to come out
            mutex.release()
            sleep(1)
            mutex.acquire()


        mutex.release()


# end of GoIn




def UsingTime(  gender):

    sleep(random.randint(1,3))    # spend some time in bathroom
    global PeopleInBathroom
    mutex.acquire()
    PeopleInBathroom-=1   #leave bathroom
    mutex.release()

    bathroom.release()
    if gender==FEMALE:
        print "FEMALE"
    else:
        print "MALE"

    print "exiting from bathroom"
# end of UsingTime






if __name__ == "__main__":
    print "fbef"



    t = threading.Thread(target=timer)
    #threads.append(t)
    t.start()
    t1 = threading.Thread(target=GeneratePeople)
    #threads.append(t)
    t1.start()
    t2 = threading.Thread(target=GoIn)
    #threads.append(t)
    t2.start()
