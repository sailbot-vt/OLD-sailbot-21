#ifndef tl
#define tl 
//#include "Stepper.h"
#include "../PID/PID_v1.h"
#if (ARDUINO >= 100)
  #include "Arduino.h"
#else 
  #include "WProgram.h"
#endif
class Stepper;
class Encoder;
class PID;
class TestLib { 
    public: 
    TestLib(bool displayMessage=false);
    Encoder* myEnc;
    
    //PID stuff 
    double Setpoint = 0; 
    double Input = 0; 
    double Output = 0;
    int maxSpeed = 100;
    double Kp, Ki, Kd;
    PID* myPID;
    void moveNumSteps(int numSteps);
    void computePID();
    void setTunings(double newKp, double newKi, double newKd);
    // Stepper stuff
    Stepper* myStep;
    
    private:
    // More PID stuff  
    int inputDeg;
    int numPulse = 0;
    int pwmSetSpeedPin = 9;   //L982N pin: ENA **MUST BE A PWM ENABLED PIN
    int inputForward = 10;    //L982N pin: IN2
    int inputBack = 11;       //L982N pin: IN1
    int speedInput;
    void rotate(int pwmOut);
};




#endif
