#include <Keypad.h>
#include <Servo.h>

#define BUZZER A4 
#define LED 13
#define Photoresis A0
#define RED A2
#define GREEN 12
#define BLUE 10
#define Temp A1
#define enable2 11
#define in4 A3
//#define in3 1 
#define pir A5

Servo myservo;           //define myservo object for servo class 
int Ldrvalue;            // define a varabile contain value for ldr 
float Celsius;           // define a varabile contains value of Celsius degree 
const byte NumofRows= 4; //number of rows on the keypad
const byte NumofCols= 3; //number of columns on the keypad

void Home_system_ON();

//keymap defines the key pressed according to the row and columns just as appears on the keypad
char keys[NumofRows][NumofCols]= 
{
{'1', '2', '3'}, 
{'4', '5', '6'}, 
{'7', '8', '9'},
{'*', '0', '#'}
};


byte RowsPins[NumofRows] = {8,2,7,6}; //pins connected to Rows on Arduino
byte ColPins[NumofCols]= {5,4,3}; ////pins connected to Columns on Arduino
// removed pin from 0 and put in 2 ,and removed a coulmn no 1 was in pin 2
//initialize a Keypad class with the name m_keypad  
Keypad m_Keypad= Keypad(makeKeymap(keys), RowsPins, ColPins, NumofRows, NumofCols);

String input = "";        //initialize the user input
String password = "1234"; //set the default passowrd 

void setup()
{
  Serial.begin(9600);           //initializing serial monitor
  pinMode(BUZZER, OUTPUT);      //Set BUZZER pin(A4) as output
  pinMode(LED,OUTPUT);          // set Led to pin 13 output
  pinMode(RED,OUTPUT);          // set Red to pin A2 used as digital pin output
  pinMode(GREEN,OUTPUT);        //set Green to pin 12 output
  pinMode(BLUE,OUTPUT);         //set Blue to pin 10 output
  pinMode(Temp,INPUT);          //set Tempsensor to pin A1 input
  pinMode(Photoresis,INPUT);    //set photoresistor or ldr to pin A0
  pinMode(enable2,OUTPUT);      // set enable pin in ic to control speed 0~255
  //pinMode(in3,OUTPUT);          // set in3 pin in ic to control direction of rotation
  pinMode(in4,OUTPUT);          // set in4 pin in ic to control direction of rotation
  pinMode(pir,INPUT);           // set pir to pin 1 to dectect objects
  
 
}


void loop() 
{
  
  int pir_value = digitalRead(pir);
  char key_pressed = m_Keypad.getKey();
  
  
  //check if someone is inside the house using pir sensor 
  if(pir_value )
  {
    delay(500);
    Serial.println("Someone is inside the House!!");
    delay(2000);
  }
  if (Serial.available() > 0) {
  int IN = readAndConvertToInt();  // Read the first input

    if (IN == 1) {
      Serial.println("\nFace recognized");
      Home_system_ON();
      Serial.flush();
    } 
    else if (IN == 2) {
      Serial.println("Type (3) to let the user enter or Type (4) to let him enter the password");

      // Ensure the buffer is clear before waiting for the next input
      while (Serial.available()) {
        Serial.read();  // Flush any remaining characters in the serial buffer
      }

      delay(500);  // Wait a bit for the user to enter the next input

      // Wait until the second input is available
      while (Serial.available() == 0) {
        // Waiting for input
      }

      int IN2 = readAndConvertToInt();  // Read the second input

      if (IN2 == 3) {
        Serial.println("Door opened!!");
        Home_system_ON();
      } 
      else if (IN2 == 4) {
        Serial.print("Face is not recognized, Type the password: ");
      }
    }
  }

  
 

  
  if (key_pressed != NO_KEY) //make sure a key is pressed
  {
    if (key_pressed == '#') // made '#' as "Enter" key on keyboard to confirm the input 
    {
      if (input == password ) //Correct password case
      {
        Serial.println("\nPassword correct!"); //print "Password correct!" on serial monitor
        Home_system_ON();
        
      } 
      else //Wrong password case
      {
        Serial.println("\nWarning!!!! Wrong password"); 
  		 
  		  tone(BUZZER, 1000, 500); //Set the Buzzer tone to 1000Hz for 0.5 s(500ms)  
      }
      
      
      input = "";  // Clear the buffer for new input
    }
    
    else if (key_pressed == '*') //set '*' as the Backspace key in keyboard
    {
      if (input.length()>0) //make sure there is a char written before deleting 
      {
        input.remove(input.length()-1);  //Remove last character
        Serial.println();                //make a new line
        Serial.print(input);             //Display updated input on the new line
      }
    }
    else if (key_pressed == '0') // 0 to set new password
    {
      Serial.println("\nEnter new password:");
      password = "";  // Clear the old password
      
      while (true) //infinte loop to set the password
      {
        key_pressed = m_Keypad.getKey();
        
        if (key_pressed == '#') // '#' to confirm the new password
        {  
          Serial.println("\nNew password set!");
          break;  //to exit the loop
        } 
        else if (key_pressed != NO_KEY && key_pressed != '*' && key_pressed != '0') //check if key is pressed  and it is not '*' as it is Backspace
        { 
          password += key_pressed;    //incremet on password string to set the new password
          Serial.print(key_pressed);  // Display the entered characters on the serial monitor
        } 
        else if (key_pressed == '*') // '*' to delete a character from password
        { 
          if (password.length() > 0) //check if there is a character
          {
            password.remove(password.length() - 1);  // Remove last character
            Serial.println(); //make a new line
            Serial.print(password); // Display updated input on the new line
          }
        }
      }
    } 
    else //Typing case
    {
      
      input += key_pressed;       // Insert the pressed key to the input 
      Serial.print("\r");         // Return to the start of the line
      Serial.print(key_pressed);  // Display the current input
    }
  }
}


void Home_system_ON()
{
          myservo.attach(9);  //attach myservo to pin 9
        myservo.write(90); //open it as door by changing the angle to 90 degree
        
        int Ldrvalue = analogRead(Photoresis); //reads the value of LDR 
        
        if (Ldrvalue <= 200) //low lighting case  
        {
           digitalWrite(LED,HIGH); //Led is on
           delay(100);
           Serial.println(Ldrvalue); //show the lighting value on serial monitor
        }
        else  //High lighting case 
        {
           digitalWrite(LED,LOW);    //led is off
           Serial.println(Ldrvalue); //show the lighting value on serial monitor
        }
        
        Celsius = analogRead(Temp)*(5/1023.0);  // take voltage
        Celsius = (Celsius-0.5)*100;            // convert voltage to celsius
        int speed = map(Celsius,10,70,0,255);   // Maps the Celsius temperature from 10 to 70 to a speed value from 0 to 255
        Serial.println(Celsius);                //show the temperature value in celsius on serial monitor
        if (Celsius > 30.0) //Hot temperature case
        {
            //RED light is ON
            digitalWrite(RED,HIGH);  
            digitalWrite(GREEN,LOW); 
            digitalWrite(BLUE,LOW);
          
            analogWrite(enable2,speed); //Speed of motor varies with the temperature
            
            //setting the direction of motor(Fan)
            //digitalWrite(in3,HIGH);
            digitalWrite(in4,HIGH); //LOW
            delay(100);
        }
        else if (Celsius >= 20.0 && Celsius < 30.0) //Normal temperature case
        {
            //GREEN light is ON
            digitalWrite(GREEN,HIGH);
            digitalWrite(RED,LOW);
            digitalWrite(BLUE,LOW);
          
            analogWrite(enable2,speed); //Speed of motor varies with the temperature 
            
            //setting the direction of motor(Fan)
            //digitalWrite(in3,HIGH);
            digitalWrite(in4,HIGH);//LOW
            delay(100);
        }
        else if (Celsius <20.0)
        {
            //BLUE light is ON
            digitalWrite(BLUE,HIGH);
            digitalWrite(RED,LOW);
            digitalWrite(GREEN,LOW);
            
            analogWrite(enable2,speed); //Speed of motor varies with the temperature 
            
            //setting the direction of motor(Fan)
            //digitalWrite(in3,LOW);
            digitalWrite(in4,HIGH);
            delay(100);
        }
       
        //Wait for 5 sec then close the door(servo return to normal state) 
        delay(5000);
        myservo.attach(9);
        myservo.write(0); 
}

int readAndConvertToInt() {
  String inputString = "";  // A string to hold incoming characters

  // Wait until there is data available
  while (Serial.available()) {
    char inChar = (char)Serial.read();  // Read each character from the serial buffer

    // If we receive a newline or carriage return, we stop
    if (inChar == '\n' || inChar == '\r') {
      break;
    }

    inputString += inChar;  // Append the character to the string
  }

  // Convert the string to an integer
  int result = inputString.toInt();
  return result;
}