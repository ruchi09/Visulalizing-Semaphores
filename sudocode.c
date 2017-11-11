
// Sudo code for Unisex Bathroom Problem




//Thread Functions Used

1) timer()            // Timeout Function to prevent starvation
2) GoIn()             // Sends people inside bathroom from queue
3) UsingTime()        // Defines the time a person stays inside bathroom
4) GeneratePeople()   // Generates people to use bathroom at random time


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
    while(t>0 && PeopleInBathroom>0)
    {
      sleep(1);
      t--;
    }


    // Allocate bathroom to the other gender.

    if(GenderUsingBathroom==MALE)
      GenderUsingBathroom = FEMALE

    else if(GenderUsingBathroom == FEMALE)
      GenderUsingBathroom=MALE;


      

    //If bathroom is still occupied, wait till remaining people exits.
    while(PeopleInBathroom>0)
      sleep(1);



  }// end of while

}// end of timer function





void GeneratePeople()
{

  while(1)
  {
    if(rand()%2==0)
      MalesInQueue++;

    else
      FemalesInQueue++;


    //sleep for a random time
    sleep(rand()%3);
  }

}// end of GeneratePeople




int GoIn()
{

  while(1)
  {
    while(GenderUsingBathroom==MALE && MalesInQueue>0)
    {
      sem_wait(bathroom);
      MalesInQueue--;
      PeopleInBathroom++;
      pthread_create : UsingTime(id);
    }

    while(PeopleInBathroom>0)     // Waiting for remaining men to come out
      sleep(1);

    while(GenderUsingBathroom==FEMALE && FemalesInQueue>0)
    {
      sem_wait(bathroom)
      FemalesInQueue--;
      PeopleInBathroom++;
      pthread_create: UsingTime(id);  //create thread to monitor person's time in bathroom
    }


    while(PeopleInBathroom>0)     // Waiting for remaining ladies to come out
      sleep(1);
  }
}// end of GoIn




int UsingTime()
{
  sleep(rand()%2+1);    // spend some time in bathroom
  PeopleInBathroom--;   //leave bathroom

  post(bathroom);
}// end of UsingTime


int main()
{


  // will contain respective thread calls.


  return 0;
}
