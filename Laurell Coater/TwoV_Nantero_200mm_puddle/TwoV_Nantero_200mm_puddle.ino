int PreWet1_valve =7; //flow valve is on pin 7, can not be changed
int PreWet2_valve =5; //vaccum valve is on pin 6, can not be changed
int CNTDispense_valve = 6; //CNT valve is on pin 5, can not be changed
char junk;

//############1###1111#####11111 111 111111# #11112111#1111111e1#1##1########
//the following parameters can be changed

//  15.0ml = 21000ms
//  10.0ml = 13340ms
//  3.5ml = 4670ms
//  3.0ml = 4000ms
//  2.5ml = 3250ms
//  2.0ml = 2690ms
//##########################################################
// how much delay time of PreWet1_valve, count in milisecond
  int delay_time_PreWet1_valve=     2000;  //(10000=10 second, 1000=1 second)
// how much delay time of PreWet2_valve, count in milisecond
  int delay_time_CNT_valve =        2000;    // 6 seconds
// how many times to repeat
  int reps =       1;
// delay between reps  
  int delayrep =               2000;
// Between Puddle Coat Delay  
  int BetweenCoatDelay =       2300;
//#######################################
//#######################################

//Emergency Stop - Enter 2 in the Shell to Operate
void EStop()
{
if( Serial.read()=='2')
              {
                Serial.println("All Valves Closing");
                digitalWrite(PreWet1_valve,LOW);       //PreWet1_valve is normally closed
                digitalWrite(PreWet2_valve,LOW);       // flow valve is normally close
                digitalWrite(CNTDispense_valve,LOW);   // flow valve is normally close
                Serial.println("close the monitor and restart it again");
                Serial.end();
                for(;;)
                ;
              }
}

void CoatSequence()
{
  Serial.println("operation is being started, press 2 to stop process if needed");
         
            //Prewets On
           if (delay_time_PreWet1_valve > 0 ) 
                {
                digitalWrite(PreWet1_valve,HIGH); Serial.println("Prewet 1 ON"); //Sets state of relay1
                 
                } 
            
            digitalWrite(CNTDispense_valve,LOW); Serial.println("CNT Dispense OFF");  //SET state of relay3
                Serial.print("Prewet Dispense Time (ms):");
                Serial.println (delay_time_PreWet1_valve);
                delay(delay_time_PreWet1_valve);  //wait how much sec
                
            //Prewet One Off
            digitalWrite(PreWet1_valve,LOW); Serial.println("Prewet 1 Off"); //turns off relay1
            
            //Between Coat Delay
            delay(BetweenCoatDelay);
            EStop();
            
            //CNT On
             if (delay_time_CNT_valve > 0 )
            {
            digitalWrite(CNTDispense_valve, HIGH); Serial.println("CNT Dispense ON");  //SET state of relay3
                Serial.print("CNT Dispense Time (ms):");
                Serial.println (delay_time_CNT_valve);
            }

            //CNT OFF
            delay(delay_time_CNT_valve);
            digitalWrite(CNTDispense_valve, LOW); Serial.println("CNT Dispense OFF");  //SET state of relay3
}

void setup()
{
  Serial.begin(9600);
  pinMode(PreWet1_valve,OUTPUT);
  digitalWrite(PreWet1_valve,LOW);    //PreWet1_valve is normally closed
  digitalWrite(PreWet2_valve,LOW);   // flow valve is normally close
  pinMode(PreWet2_valve,OUTPUT);
  pinMode(CNTDispense_valve, OUTPUT);
  digitalWrite(CNTDispense_valve,LOW);   // flow valve is normally close
}

String getValue(String data, char separator, int index){//WORKS
  //http://arduino.stackexchange.com/questions/1013/how-do-i-split-an-incoming-string
    int found = 0;
    int strIndex[] = { 0, -1 };
    int maxIndex = data.length() - 1;

    for (int i = 0; i <= maxIndex && found <= index; i++) {
        if (data.charAt(i) == separator || i == maxIndex) {
            found++;
            strIndex[0] = strIndex[1] + 1;
            strIndex[1] = (i == maxIndex) ? i+1 : i;
        }
    }
    return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}


void loop()
{
    while(Serial.available() == 0);
    String information = Serial.readStringUntil("\n");
    String pre = getValue(information, ',', 0);
    String del = getValue(information, ',', 1);
    String CNT = getValue(information, ',', 2);
    String rep = getValue(information, ',', 3);
    String repdelay = getValue(information, ',', 4);
    delay_time_PreWet1_valve = pre.toFloat();
    BetweenCoatDelay = del.toInt();
    delay_time_CNT_valve = CNT.toFloat();
    reps = rep.toInt();
    delayrep = repdelay.toFloat();
    while (Serial.available() > 0)  // .parseFloat() can leave non-numeric characters
    { 
      junk = Serial.read(); // clear the keyboard buffer
    }
    while(Serial.available() == 0);
    char ch = Serial.read();
    if(ch=='1')
       {
       for (int i = 0; i < reps; i++)
         {
           CoatSequence();
           if (reps-i > 1 )
           {
            delay(delayrep); 
           }
       }
       Serial.println("operation is done, Arduino is sleeping");
       }
}
 


