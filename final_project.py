import getopt, sys
import platform
import os
import urllib
from subprocess import call

numeric_file_strings = ['0.mp3', '1.mp3', '2.mp3', '3.mp3', '4.mp3', '5.mp3', '6.mp3', '7.mp3', '8.mp3', '9.mp3']

media_files = {'male':
                 {'endings': [
                        ['Riding a Horse', 'Listening to a jingle', 'On a phone', 'Swan dive', 'Voicemail'],
                        ['m-e1-horse.mp3', 'm-e2-jingle.mp3', 'm-e3-on_phone.mp3', 'm-e4-swan_dive.mp3', 'm-e5-voicemail.mp3']
                    ],
                  'reasons': [
                        ['On top of a building', 'Cracking Walnuts', 'Polishing a monocle', 'Ripping weights'],
                        ['m-r1-building.mp3', 'm-r2-cracking_walnuts.mp3', 'm-r3-polishing_monocle.mp3', 'm-r4-ripping_weights.mp3']
                    ]
                 },
               'female':
                 {'reasons': [
                        ['Ingesting Old Spice', 'Listening to Reading', 'Lobster Dinner', 'Moon Kiss', 'Riding a Horse'],
                        ['f-r1-ingesting_old_spice.mp3', 'f-r2-listening_to_reading.mp3', 'f-r3-lobster_dinner.mp3', 'f-r4-moon_kiss.mp3', 'f-r5-riding_a_horse.mp3']
                    ],
                  'endings': [
                        ['She will get back to you', 'Thanks for Calling'],
                        ['f-e1-she_will_get_back_to_you.mp3', 'f-e2-thanks_for_calling.mp3']
                     ]
                 }
              }

default_files = ['m-b1-hello.mp3', 'm-b2-have_dialed.mp3', 'f-b1-hello_caller.mp3', 'f-b2-lady_at.mp3', 'm-r0-cannot_come_to_phone.mp3',
        'f-r0.1-unable_to_take_call.mp3', 'f-r0.2-she_is_busy.mp3', 'm-leave_a_message.mp3', 'm-youre_welcome.mp3']

mp3_file_list = list()
gender = ''
outputFile = ''

def retrieveGender( arg ):
    if(str(arg) == 'm'):
        global gender
        gender = 'male'
        mp3_file_list.append('m-b1-hello.mp3')
        mp3_file_list.append('m-b2-have_dialed.mp3')
    elif(str(arg) == 'f'):
        gender = 'female'
        mp3_file_list.append('f-b1-hello_caller.mp3')
        mp3_file_list.append('f-b2-lady_at.mp3')
    else:
        raise Exception('\''+str(arg) + '\' is not a valid gender')

def keyIsInvalid(key_arg, type):
    key = int(key_arg)
    value_type = str(type)
    if(value_type == 'reasons'):
        if(gender == 'male'):
            if(key <= 0 or key > 4):
                return True
            else:
                return False
        elif(gender == 'female'):
            if(key <= 0 or key > 5):
                return True
            else:
                return False
        else:
            return True
    elif(value_type == 'endings'):
        if(gender == 'male'):
            if(key <= 0 or key > 5):
                return True
            else:
                return False
        elif(gender == 'female'):
            if(key <=0 or key > 2):
                return True
            else:
                return False
        else:
            return True

def addStandardReasons():
    if(gender == 'male'):
        mp3_file_list.append('m-r0-cannot_come_to_phone.mp3')
    elif(gender == 'female'):
        mp3_file_list.append('f-r0.1-unable_to_take_call.mp3')
        mp3_file_list.append('f-r0.2-she_is_busy.mp3')
    else:
        raise Exception('Gender not initialized to correct value')

def retrieveMedia(input_arg, type_arg):
    length = len(str(input_arg))
    integerArg = int(input_arg)

    type = str(type_arg)

    digits = [0,0,0,0,0]

    count = 5

    digits[4] = integerArg//10000
    digits[3] = (integerArg%10000)//1000
    digits[2] = (integerArg%1000)//100
    digits[1] = (integerArg%100)//10
    digits[0] = (integerArg%10)
    usedList = list()
    for i in range(length):
        index = length-i-1
        value = digits[index]
        if(value in usedList):
            raise Exception(str(type_arg) + ' #' + str(value) + ' is already used')
            return
        elif(keyIsInvalid(value, type)):
            raise Exception(str(type_arg) + ' #' + str(value) + ' does not exist')
            return
        else:
            mp3_file_list.append(media_files[gender][type][1][value-1])
            usedList.append(value)

def getPhoneNumber(input_arg):
    input = str(input_arg)
    tempList = list()
    composite = ''
    for i in range(len(input)):
        try:
            num = int(input[i])
            composite = composite + str(num)
            tempList.append(numeric_file_strings[num])
        except ValueError:
            continue

    stringType1 = composite[:3]+'-'+composite[3:6]+'-'+composite[6:]
    stringType2 = '('+composite[:3]+') '+composite[3:6]+'-'+composite[6:]
    stringType3 = composite[:3]+'.'+composite[3:6]+'.'+composite[6:]
    stringType4 = composite[0:]

    if(not (input == stringType1 or input == stringType2
            or input == stringType3 or input == stringType4) ):
        raise Exception('Invalid Phone Number Length')

    for string in tempList:
        mp3_file_list.append(string)

def printContextualMenu(type_arg, delim = ''):
    type = str(type_arg)
    val_list = media_files[gender][type][1];
    key_list = media_files[gender][type][0];

    for i in range(len(val_list)):
        print(str(delim)+'['+str(i+1)+'] '+key_list[i])

def checkOutputFile(arg):
    file = str(arg)
    if(file in numeric_file_strings or file in media_files['male']['reasons'][1] or file in media_files['male']['endings'][1]
       or file in media_files['female']['reasons'][1] or file in media_files['female']['endings'][1] or file in default_files):
        return False
    else:
        return True

def createMP3FileWithPrompts():
    global mp3_file_list, outputFile
    global hasGender, hasPhoneNumber, hasReasons, hasEndings, hasOutputFile
    while(True):
        inputVal = raw_input('What gender are you? (m/f): ')
        try:
            if(inputVal == ''):
                continue
            retrieveGender(inputVal)
            hasGender = True
            break
        except:
            print('\tError: Use correct gender')
            continue

    while(True):
        try:
            phoneNumber = raw_input('\nWhat is your phone number? ')
            if(phoneNumber == ''):
                continue
            getPhoneNumber(phoneNumber)
            hasPhoneNumber = True
            break
        except:
            print('\tError: Enter Correct Phone Number in the Following Form:')
            composite = '1234567890'
            stringType1 = composite[:3]+'-'+composite[3:6]+'-'+composite[6:]
            stringType2 = '('+composite[:3]+') '+composite[3:6]+'-'+composite[6:]
            stringType3 = composite[:3]+'.'+composite[3:6]+'.'+composite[6:]
            stringType4 = composite[0:]
            print(stringType1)
            print(stringType2)
            print(stringType3)
            print(stringType4)
            continue

    addStandardReasons()
    print('')
    printContextualMenu('reasons')

    while(True):
        try:
            reasonKey = raw_input('\nWhich reason(s) would you like in your message (numbers above): ')
            if(reasonKey == ''):
                continue
            retrieveMedia(reasonKey, 'reasons')
            hasReasons = True
            break
        except Exception as e:
            print('\tError: This is a reason issue: '+ str(e))
            continue

    print('')
    printContextualMenu('endings')

    while(True):
        try:
            endingKey = raw_input('\nWhich ending(s) would you like in your message (numbers above): ')
            if(endingKey == ''):
                continue
            retrieveMedia(endingKey, 'endings')
            hasEndings = True
            break
        except Exception as e:
            print('This is an ending issue: ' + str(e))
            continue

    while(True):
        outputFile = raw_input("\nWhat would you like the name of this file to be: ")
        if(outputFile == ''):
            continue

        fileType = outputFile[len(outputFile)-4:]
        if(not fileType == '.mp3'):
            outputFile = outputFile+'.mp3'

        if(checkOutputFile(outputFile)):
            hasOutputFile = True
            break

        print('This is a reserved filename, please use a different one')

    if(gender == 'male'):
        mp3_file_list.append('m-leave_a_message.mp3')
        mp3_file_list.append('m-youre_welcome.mp3')

hasGender = False
hasPhoneNumber = False
hasReasons = False
hasEndings = False
hasOutputFile = False

def handleCommandLineArgs():
    global outputFile
    global hasGender, hasPhoneNumber, hasReasons, hasEndings, hasOutputFile
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'g:n:r:e:o:', ["start"])
    except getopt.GetoptError as e:
        raise Exception('Invalid argument: ' + str(e))
    options, args = zip(*opts)
    if('--start' in options):
        createMP3FileWithPrompts()
    if(not hasGender):
        raise Exception('Missing gender')
    elif(not hasPhoneNumber):
        raise Exception('Missing phone number')
    elif(not hasReasons):
        raise Exception('Missing reasons')
    elif(not hasEndings):
        raise Exception('Missing endings')
    elif(not hasOutputFile):
        raise Exception('Missing output file')

def main():
    global mp3_file_list
    global outputFile

    mp3_file_list = list()
    try:
        handleCommandLineArgs()
    except Exception as e:
        print('Error:')
        print('\t'+ str(e.args[0]))
        return

    dir = os.getcwd()

    filename = outputFile
    fileType = outputFile[len(outputFile)-4:]
    if(not fileType == '.mp3'):
        outputFile = outputFile+'.mp3'
        filename = filename+'.mp3'
    name = outputFile[:len(outputFile)-4]


    slash = '/'
    command = 'cat'
    commandOperator = ' > '
    delete = 'rm '
    if(platform.system() == 'Windows'):
        slash = '\\'
        command = 'copy /b '
        delete = 'DEL '
        commandOperator = ' '

    outputFile = str(dir)+str(slash)+str(outputFile)

    for string in mp3_file_list:

        fragment_path = str(dir) + str(slash) + string
        if(platform.system() == 'Windows'):
            command = command + ' + ' + string
        else:
            command = command + ' ' + string
        frag_file = open(fragment_path, 'w')
        urllib.urlretrieve('http://www-bcf.usc.edu/~chiso/itp125/project_version_1/'+str(string), fragment_path)
        frag_file.close()

    file_temp = open(outputFile, 'w')
    cmd = command + commandOperator + filename
    file_temp.close()
    os.system(cmd)

    deleted_list = list()

    for string in mp3_file_list:
        fragment_path = str(dir) + str(slash) + string
        if(not fragment_path in deleted_list):
            deleted_list.append(fragment_path)
            os.system(delete + ' ' + fragment_path)

main()
