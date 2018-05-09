"""
McMaster University IBEHS 1P10

Team 2

DP2- Prosthetic Hand Code
    SubProgram 1:
        Inputs team number, outputs input speed, output speed, gear ratio, and team number
        Verifies by time, or by number of rotations depending on user preferance

    SubProgram 2:
        Changes direction depending on whether open, or closed
        Print information at specified intervals of rotation
        Writes information to text file named "Group2_SubProgram2_TextFile.txt"
        Creates a diagram at each interval of the position of the fingers
        
    SubProgram 3:
        Inputs object length
        Grasps and releases upon user input
        
December 5, 2017
"""
#Import Librares
import math
import time
from graphics import * #For diagrams
import RPi.GPIO as GPIO

#Set up Raspberry Pi
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Set Pins 5 and 12 as Output
GPIO.setup(5, GPIO.OUT) #Motor Direction
GPIO.setup(12, GPIO.OUT) #Motor Speed

#Set Pin 12 to PWM
motorSpeed = GPIO.PWM(12,20)

#Reference Values
gearRatio = 35/8 
fingerDisplacment = math.pi/4 #45 degrees from starting position is the max extent of the fingers
lengthFinger = 65 #mm
outSpeed = 0.1 #rps
numRevMotion = gearRatio * fingerDisplacment #calculate angular displacment of motor when opening or closeing

exitProgram = False

#Subprogram 1
def subProgram1():
    #Functions For Subprogram
    def teamSpeed(team):
        Speed = teamList[team-1][1] #select the speed from the list
        return Speed

    def gearRatio(inSpeed): #Takes team's input speed and finds output using gear ratio
        inSpeed = inSpeed * (1/60) #rpm to rps
        outSpeed = inSpeed * (1/ratio) #input divided by gear ratio
        return outSpeed

    def endChoice(outSpeed): #Decide Whether to Verify Subprogram 1 or Return to the Program Menu
        validOutput = False 
        while validOutput == False: #run following until valid output achived
            print("Would you like to verify Subprogram 1, or return to the Program Menu?")
            print("\t1. Verify Subprogram 1")
            print("\t2. Return to Program Menu")
            choice = int(input("\nEnter 1 to verify Subprogram 1, enter 2 to return to the Program Menu. \n"))

            if choice == 1:
                verify(outSpeed)
                validOutput = True
            elif choice == 2:
                validOutput = True
            else:
                print("Entry is invalid, please try again.")
                
    def verify(outSpeed): #Verification of Subprogram 1
        validOutput = False
        while validOutput == False: #repeat following until valid output achived
            ratio2 = float(input("What is the gear ratio of the test gear train? ")) #Take team gear ratio
            motorSpeed = outSpeed * speedFactor #Calaculate motor speed
            A = (motorSpeed/2.83)*100
            if ratio2 <= 0:
                print("\nEntry is invalid, please try again")
            else:
                validOutput = True #exit from function when valid
                verifyByTime(A, ratio2, motorSpeed) #By default, verify speed based on user entered time
                
    def verifyByTime(A, ratio2, motorSpeed): #Verify correctness by user specified time
        validOutput = False
        while validOutput == False:
            runTime = input("For how long should the motor run, in seconds?  ")
        
            if runTime == "skip": #Change to verification by user enter number of output gear rotations
                validOutput = True
                verifyByNumber(A,ratio2, motorSpeed)
            else:
                runTime = float(runTime)
                
                #Check validity of Run Time        
                if runTime < 0:
                    print("/nEntry is invalid, please try again")
                else:
                    validOutput = True
                    outRotation = (motorSpeed/ratio2) * runTime #calculate number of rotations of output gear

                    #Print calculations
                    print("\nPreviously calculated output speed: " + str(outSpeed) + " rps")
                    print("Speed Factor:                       " + str(speedFactor))
                    print("Resulting Motor Speed:              " + str(motorSpeed) + " rps")
                    print("User specified Run Time             " + str(runTime) + " seconds\n")
                    print("Based on the given data, the output gear should rotate a total of: ")
                    print(str(outRotation) + " times in " + str(runTime) + " seconds.")
                    print("The motor will now run for " + str(runTime) + " seconds.")

                    #Run Raspberry Pi using calculated speeds
                    go(A)
                    time.sleep(runTime) #keeps motor running for user specified length of time.
                    stop()
                    
                    print("\n")
        
    def verifyByNumber(A, ratio2, motorSpeed): # Veryify correctness by user specified number of rotations, designed for user ease
        validOutput = False
        while validOutput == False:
            
            #Take input, number of output gear rotations
            numRotations = int(input("How many times should the output gear rotate? "))
            if numRotations < 0:
                print("\nEntry is invalid, please try again")
            else: #Calculate time required to rotate output gear set number of times
                runTime = (numRotations*ratio2)/motorSpeed

                #Print Calculations
                print("\nPreviously calculated output speed: " + str(outSpeed) + " rps")
                print("Speed Factor:                       " + str(speedFactor))
                print("Resulting Motor Speed:              " + str(motorSpeed) + " rps")
                print("\nBased on the given data, it should take:")
                print(str(runTime) + " seconds for the output gear to rotate " + str(numRotations) + " times.")
                print("The motor will now rotate for " + str(runTime) + " seconds.")

                #Run Raspberry Pi based on calculated values
                go(A)
                time.sleep(runTime) #keeps motor running for user specified length of time.
                stop()
                
                print("\n")
                validOutput = True

    def go(A): #runs motor
        GPIO.output(5,1)
        motorSpeed.start(A)

    def stop(): #stops motor
        GPIO.output(5,1)
        motorSpeed.stop()        

    #Variable Initialization
    ratio = 4.375 #Our Team's gear ratio
    speedFactor = 20 
    teamList = [[1,24.75],[2,26.25],[3,27.00],\
                [4,29.25],[5,31.50],[6,33.00],\
                [7,33.75],[8,36.75],[9,37.50],\
                [10,39.00],[11,40.50],[12,41.25],\
                [13,45.00],[14,47.25],[15,48.75],\
                [16,49.50],[17,52.50],[18,56.25]] #List of all team numbers paired with input speeds

    #Main Program
    runProgram = True
    while runProgram == True:
        for i in range(len(teamList)): #Convert Team Numbers and Input Speeds to Floats
            for j in range(len(teamList[i])):
                teamList[i][j] = float(teamList[i][j])

        teamNumber = int(input("Please enter a team number from 1 to 18.\n")) #Input Team Number
        if teamNumber > 18 or teamNumber < 1: #Check Valididty of Team Number
            print("Entry is invalid, please try again.")  #if not valid team number, invalid, restart subprogram

        else: #Print Calculated Values
            inSpeed = teamSpeed(teamNumber)
            outSpeed = gearRatio(inSpeed)
            print("Given Team Number:          " + str(teamNumber))
            print("Corresponding Input Speed:  " + str(inSpeed) + " rpm")
            print("Calculated Output Speed:    " + str(round(outSpeed,3)) + " rps")
            print("Gear Ratio:                 " + str(ratio))
            print("\n")
            runProgram = False
            endChoice(outSpeed)

#SUB PROGRAM 2
def subProgram2():
    
    #Functions for Sub Program
    def angleBase(fingerRotation): #returns angle traveled from closed position agrument if wrapped angle
        if fingerRotation <= math.pi/4 or fingerRotation >= 3*math.pi/4: #if angle is on interval where abs sin is lower than abs cos
            angleFing = abs(math.sin(fingerRotation))
        elif fingerRotation < 3*math.pi/4: #if angle is on interval where abs cos is lower than abs sin
            angleFing = abs(math.cos(fingerRotation))
        return angleFing
    
    def motorDirection(rev): #find direction of motor, given number of revolutions completed
        if rev %2 != 0: #if odd number of revolutions completed, going back to original position
            if startingPosition == 1:
                directionMotor = "Clockwise"
            elif startingPosition == 2:
                directionMotor = "Counter Clockwise"
        elif rev %2 == 0:
            if startingPosition == 1:
                directionMotor = "Counter Clockwise"
            elif startingPosition == 2:
                directionMotor = "Clockwise"
        return directionMotor

    def yDelta(y): #amount to shift each point by as a result of the angle change
        delta = y * (abs(math.sin(angleFingers))) 
        delta *= 0.8 #Scale down the size to fit the graphic in the window
        return delta
        
    #Input Values
    validInput = False
    while validInput == False:
        startingPosition = int(input("What is the Starting Position of the hand?: \n1. Closed  2. Open  ")) # 1. Closed, 2. Open
        validInput = True
        if startingPosition not in [1,2]: #if user does not select 1 or 2, invalid 
            print("Invalid entry.")
            validInput = False #re-run sub program

        numRotations = float(input("How much should the motor rotate in degrees? ")) #number of motor rotations is float, in degrees
        numRotations *= (math.pi/180) #Convert to radians
        validInput = True
        if numRotations < 0: #if number of rotations negative, invalid
            print("Invalid entry, must be a positive number.")
            validInput = False
            
        numIncrements = int(input("Enter the number of increments: ")) #number of increments is integer
        validInput = True
        if numIncrements <= 0: #If number of increments negative, invalid
            print("Invalid entry, must be a positive number.")
            validInput = False

    #Obtain values for: angle of motor from start, directon of motor, position of fingers, and angle of fingers from start
    rotationalIncrements = [] #define empty list of rotational increments
    freqOfPrint = numRotations/numIncrements #program should print after this many radians
    for i in range(1,numIncrements+1): 
        rotIncrement = i * freqOfPrint #angle of increment = increment number * radians per increment
        rotationalIncrements.append(rotIncrement) #creates list of all rotational increments

    outFile = open('Group2_SubProgram2_TextFile.txt','w') #Open File
    outFile.write("%-40s%-40s%-40s%-40s" % \
                  ("Total Motor Rotation (degrees)",\
                   "Direction of Motor Rotation",\
                   "Total Finger rotation (degrees)",\
                   "Position of Fingers (mm) From Point of Contact") \
                  + "\n\n") #new lines for readability

    count = 0 #Initiates count for following for enumeration of following loop
    incInformation = [] #List for information about each increment to be appended to
    for i in rotationalIncrements:
        angleRotationMotor = i #the angular rotation of the motor at each increment
        angleRotationFingers = i/gearRatio #angular rotation of fingers = angular rotation of motor divided by gear ratio
        angleWrap = angleRotationFingers % math.pi #to wrap abgles to 0,pi, for angleOpen, and angleClosed to work
        revolution = math.trunc(i / numRevMotion) #How many full motor revolutions need to be done before increment (rotation of motor for increment/rotation of motor per cycle)

        directionMotor = motorDirection(revolution) #Find direction of motor at increment
        
        #Find angle of fingers for position 
        if startingPosition == 1:
            angleFingers = angleBase(angleWrap)
        elif startingPosition == 2:
            angleFingers = fingerDisplacment - angleBase(angleWrap)
        
        #Plot a diagram of each increment, along with the required statments
        posFingers = 2 * lengthFinger * abs(math.sin(angleFingers)) #twice the vertical displacment of one finger

        #Make values easier for user to read
        angleRotationMotor = int(angleRotationMotor * 180/math.pi) #Convert radians to degrees for user ease
        angleRotationFingers = int(angleRotationFingers * 180/math.pi)
        posFingers = int(posFingers)

        count +=1 #Counter for enumeration

        outFile.write("%-5d%25d%35s%45d%50d" % \
                      (count,\
                       angleRotationMotor, \
                       directionMotor, \
                       angleRotationFingers, \
                       posFingers) + \
                      "\n") #write data as indxed list to file
        
        #Ccreate new window for each increment
        win = GraphWin("Rotational Increment " + str(count), 600, 500) #defines new window for each increment

        #Base of figure - Black Rectangle
        base = Rectangle(Point(20,60),Point(40,240))
        base.setFill("black")
        base.draw(win)

        #Upper Finger  - Each point is a vertex on the shape
        finger = Polygon([\
            Point(40,120-yDelta(20)),\
            Point(40,140-yDelta(20)),\
            Point(140,90-yDelta(90)),\
            
            Point(190,140-yDelta(140)),\
            Point(210,140-yDelta(140)),\
            Point(140,70-1.2*yDelta(70))\
                ])
        finger.setFill("grey")
        finger.draw(win)

        #Lower Finger - Each point is a vertex on the shape
        thumb = Polygon([\
            Point(40,180+yDelta(20)),\
            Point(40,160+yDelta(20)),\
            Point(140,210+yDelta(210)),\
            Point(190,160+yDelta(160)),\
            Point(210,160+yDelta(160)),\
            Point(140,230+yDelta(230))\
                ])
        thumb.setFill("grey")
        thumb.draw(win)

        #Line with Arrow Heads
        distance = Line(Point(200,140-yDelta(140)+5),Point(200,160+yDelta(160)-5))
        distance.setArrow("both")
        distance.draw(win)

        #Define strings for text output on diagram
        string1 = "Total Motor Rotation: " + str(angleRotationMotor)  + " degrees."
        string2 = "The motor is rotating " + str(directionMotor) + "."
        string3 = "Total Finger Rotation: " + str(angleRotationFingers) + " degrees."
        string4 = "The fingers are " + str(int(posFingers)) + " mm away from each other."

        #Create and draw text on to diagram
        mess1 = Text(Point(350,120),string1)
        mess2 = Text(Point(350,140),string2)
        mess3 = Text(Point(350,160),string3)
        mess4 = Text(Point(350,180),string4)
        
        mess1.draw(win)
        mess2.draw(win)
        mess3.draw(win)
        mess4.draw(win)
        
    outFile.close() #Close text file after loop
    
#SUB PROGRAM 3
def subProgram3():
    
    #Functions for SubProgram 
    def stop():
        GPIO.output(12,0)
        print("")
        
    def grasp(rTime):
        GPIO.output(12,1)
        GPIO.output(5,1) #turn motor clockwise
        print("Grasping...")
        time.sleep(rTime)
        stop()

    def release(rTime):
        GPIO.output(12,1)
        GPIO.output(5,0) #Counter Clockwise
         #angular displacment of fingers divided by speed
        print("Releasing...")
        time.sleep(rTime)
        stop()
        
    def delta(angle): #For diagram creation
        shift = lengthFinger * (math.sin(fingerDisplacment) - math.sin(angle))
        return shift
        
    def verify(arcSpan):#Function to verify output by printing diagram of hand while grasping                  
        print("The program will now print the motion of the hand in 10 increments")
        count = 0 #initiate count
        spanFreq = arcSpan/9 # angle per increment
        incAngle = [] #empty list to be appended to in following loop
    
        for num in range(10): #Create list of all angles within range as increments
            angle = spanFreq * num
            incAngle.append(angle) #append to list
                                            
        for angle in incAngle:
            count += 1 #for enumeration
            shift = delta(angle) #define for fingers and 
            fingerPosition = int(2 * (maxRange - (tolFactor * 2 * lengthFinger * math.sin(angle))))

            #Create new window for each increment
            win = GraphWin("Position of hand at Increment " + str(count),500,400)

            #Base of Diagram - Black Rectangle
            base = Rectangle(Point(20,60),Point(40,240))
            base.setFill("black")
            base.draw(win)

            #Upper Finger - Each point is a vertex
            finger = Polygon([\
                Point(40,120-shift),\
                Point(40,140-shift),\
                Point(140,90-shift),\
                Point(190,140-shift),\
                Point(210,140-shift),\
                Point(140,70-1.2*shift)\
                    ])
            finger.setFill("grey")
            finger.draw(win)

            #Lower Finger - Each point is a vertex
            thumb = Polygon([\
                Point(40,180+shift),\
                Point(40,160+shift),\
                Point(140,210+shift),\
                Point(190,160+shift),\
                Point(210,160+shift),\
                Point(140,230+shift)\
                    ])
            thumb.setFill("grey")
            thumb.draw(win)

            #Distance arrow
            distance = Line(Point(200,145-shift),Point(200,155+shift))
            distance.setArrow("both")
            distance.draw(win)

            #Position text
            txt1 = Text(Point(350,120), "The fingers were " + str(fingerPosition))
            txt2 = Text(Point(350,140), " mm apart from each other at this increment.")
            txt1.draw(win)
            txt2.draw(win)

    #Initialize Program
    maxRange = 2 * lengthFinger * math.sin(fingerDisplacment)
    tolFactor = 0.7 #Range of tolerance for optimal grasp
    maxRange *= tolFactor #in order to properly grasp, object should be smaller than max
    maxRange = int(maxRange)

    print("This hand can only pick up objects less than " + str(maxRange) + " mm wide.\n")

    #Main Program
    runProgram = True #For following while loop
    while runProgram == True:
        objectWidth = float(input("Enter the width of the object in mm: "))
        if objectWidth not in range(0,maxRange+1): #if width is negative, or larger than max, restart sub program 3
            print("The object must be less than " + str(maxRange) + " mm. \nPlease try again.")
        else:
            angleObject = math.atan(objectWidth / (2 * lengthFinger)) #angle the finger must displace for object
            arcSpan = fingerDisplacment - angleObject #Angular displacment of finger
            timeRotation = int((arcSpan)/outSpeed) #angle of finger displacment - angle object makes with base position of hand
            
            print ("Place the object within the functional region. ")
            choice1 = input("Press Enter to Grasp") #Function will not continue until user input
            grasp(timeRotation)
            choice2 = input("Press enter to release")
            release(timeRotation)
            print("Motion Complete.")

            print("\nWould you like to verify the motion?")
            selection = int(input("1. Yes  2.No:  "))
            if selection == 1:
                verify(arcSpan)
                
            print("\nWould you like to run the program again, or exit to the menu?")
            reRun = int(input("1. Grasp   2. Exit to Menu"))
            if reRun != 1:
                runProgram = False #breaks loop, program continues to menu

#PROGRAM MENU
while exitProgram == False:
    print("Program Menu: ")
    print("\t1.  Subprogram 1")
    print("\t2.  Subprogram 2")
    print("\t3.  Subprogram 3")
    print("\t4.  Exit")
    
    choice = int(input("Enter a number from 1-3 to select a subprogram, or enter 4 to exit.\n"))
    
    if choice == 1:
        subProgram1()
    elif choice == 2:
        subProgram2()
    elif choice == 3:
        subProgram3()
    elif choice == 4:
        print ("Thank you, the program will now exit.")
        exitProgram = True
    else:
        print("\nEntry is invalid, please try again.")
