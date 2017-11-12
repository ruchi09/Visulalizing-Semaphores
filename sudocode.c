
// Sudo code for Unisex Bathroom Problem




//Thread Functions Used

1) timer()            // Timeout Function to prevent starvation
2) GoIn()             // Sends people inside bathroom from queue
3) UsingTime()        // Defines the time a person stays inside bathroom
4) GeneratePeople()   // Generates people to use bathroom at random time




// semaphores Used

1) bathroom          // to go in bathroom                              value = Max people allowed inside bathroom
2) queue             // for MalesInQueue,FemalesInQueue                value =1
3) mutex             // for PeopleInBathroom, GenderUsingBathroom      value=1


#define TIMEOUT 10
#define MALE 0
#define FEMALE 1


int MalesInQueue=0,FemalesInQueue=0;
int PeopleInBathroom=0;
int GenderUsingBathroom;




void timer()
{
  while(1)
  {
    int t=TIMEOUT;

    //Wait till either timeout value is reached or given gender is done using bathroom.
    sem_wait(&mutex);
    while(t>0 && PeopleInBathroom>0)
    {
      sem_post(&mutex);
      sleep(1);
      t--;
      sem_wait(&mutex);
    }


    // Allocate bathroom to the other gender.


    if(GenderUsingBathroom==MALE)
      GenderUsingBathroom = FEMALE

    else if(GenderUsingBathroom == FEMALE)
      GenderUsingBathroom=MALE;




    //If bathroom is still occupied, wait till remaining people exits.
    while(PeopleInBathroom>0)
    {
      sem_post(&mutex);
      sleep(1);
      sem_wait(&mutex);
    }


    sem_post(&mutex);


  }// end of while

}// end of timer function





void GeneratePeople()
{

  while(1)
  {
    sem_wait(queue);

    if(rand()%2==0)
      MalesInQueue++;

    else
      FemalesInQueue++;

      sem_post(&queue);
    //sleep for a random time
    sleep(rand()%3);
  }

}// end of GeneratePeople




int GoIn()
{

  while(1)
  {
    sem_wait(&mutex);
    sem_wait(&queue);
    while(GenderUsingBathroom==MALE && MalesInQueue>0)   // men's turn
    {
      sem_post(&mutex);
      sem_post(&queue);

      sem_wait(&bathroom);   // wait for bathroom

      sem_wait(&mutex);
      sem_wait(&queue);
      MalesInQueue--;
      PeopleInBathroom++;
      sem_post(&mutex);
      sem_post(&queue);
      pthread_create : UsingTime(id);
    }

    sem_wait(&mutex);
    while(PeopleInBathroom>0)     // Waiting for remaining men to come out
    {
      sem_post(&mutex);
      sleep(1);
      sem_wait(&mutex);
    }


    sem_wait(&queue);

    while(GenderUsingBathroom==FEMALE && FemalesInQueue>0)      // Now women's turn
    {
      sem_post(&mutex);
      sem_post(&queue);

      sem_wait(&bathroom);   // wait for bathroom

      sem_wait(&mutex);
      sem_wait(&queue);
      FemalesInQueue--;
      PeopleInBathroom++;
      sem_post(&mutex);
      sem_post(&queue);
      pthread_create: UsingTime(id);  //create thread to monitor person's time in bathroom
    }


    sem_wait(&mutex);

    while(PeopleInBathroom>0)     // Waiting for remaining ladies to come out
    {
      sem_post(&mutex);
      sleep(1);
      sem_wait(&mutex);
    }

    sem_post(&mutex);

  }
}// end of GoIn




int UsingTime()
{
  sleep(rand()%2+1);    // spend some time in bathroom

  sem_wait(&mutex);
  PeopleInBathroom--;   //leave bathroom
  sem_post(&mutex);


  sem_post(&bathroom);
}// end of UsingTime


int main()
{


  // will contain respective thread calls.


  return 0;
}
