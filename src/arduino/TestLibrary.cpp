#include "TestLibrary.h"
#include "Stepper.h"
//#include "PID.h"
#include "../PID/PID_v1.h"
#include "../Encoder/Encoder.h"

//Constructor
TestLib::TestLib(bool displayMessage){
    Serial.begin(9600);
    if (displayMessage) { 
        Serial.println("Initializing...");
    }
    /*
    * Encoder declarations
    */
    myEnc = new Encoder(2,3);
    /*
    * Stepper delcarations
    */
    myStep = new Stepper(2038, 8, 9, 10, 11);
    myStep->setSpeed(10);
    
    /*
    * PID declarations
    */
    Kp= 1; 
    Ki= 1; 
    Kd= 1;
    myPID = new PID(&Input, &Output, &Setpoint, Kp, Ki, Kd, DIRECT);
    myPID->SetMode(AUTOMATIC); 
    //Adjust PID values
    myPID->SetTunings(Kp, Ki, Kd);
    myPID->SetSampleTime(1);
    myPID->SetOutputLimits(-maxSpeed, maxSpeed);
    Serial.println("Ended Initializing");
}

void TestLib::setTunings(double newKp, double newKi, double newKd) {
    Kp = newKp;
    Ki = newKi;
    Kd = newKd;    
}


void TestLib::computePID(){
    Serial.print("CurrentPulse: ");
    Serial.println(myEnc->read());
    if (Serial.available() > 0) { 
        inputDeg = Serial.parseInt(); 
        if (abs(inputDeg) > 360) { 
        Serial.println("Input degree's must be less than 360*");
        }
        
        numPulse = map(inputDeg, -360, 360, -1632, 1632) + myEnc->read();
        Serial.println(numPulse);
    }
    Serial.print("Go to pulse: ");
    Serial.println(String(numPulse));
    
    Setpoint = numPulse;
    myPID->Compute();
    while (abs(Output) > 1) { 
        Input = myEnc->read();
        myPID->Compute();
        rotate(Output);
    }
}

void TestLib::rotate(int pwmOut){
    if (pwmOut > 0) { 
        digitalWrite(inputForward, HIGH);
        digitalWrite(inputBack, LOW);
        analogWrite(pwmSetSpeedPin, abs(pwmOut));
  } else if (pwmOut < 0) { 
        digitalWrite(inputForward, LOW);
        digitalWrite(inputBack, HIGH);
        analogWrite(pwmSetSpeedPin, abs(pwmOut));
  } else if (abs(pwmOut) < 30) {
        //digitalWrite(inputForward, LOW);
        //digitalWrite(inputBack, LOW);
  }
  

    
}


void TestLib::moveNumSteps(int numSteps) {
    myStep->step(numSteps);
}
