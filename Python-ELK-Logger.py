#SWDV-660 - Applied DevOps
#Maryville University, 2019
#Week 6 Assignment: Adding Logging to Python Applications using ELK
#Python-ELK-Logger.py
#Henrik Olsen (0913075)


#import external libraries
import logging
import logstash
import sys


#ELK server constants
host = '3.87.116.180'
port = 5959


#level = type of log
#test_boolean = successful operation (True) or not (False)
#host = 'Mickro-PC'for my home computer
#extra:
#   test_string: Operation
#   test_boolean: Successful computation
#   test_dict: dictionary holding x, y and op (= operation)
#   test_float: result of computation
#   test_integer: menu option
#   test_list: list holding op (= operation), x and y


def add(x, y, ELK_logger):
    result = x + y
    extra = {
        'test_string': 'Addition',
        'test_boolean': True,
        'test_dict': {'x': x, 'y': y, 'op': '+'},
        'test_float': result,
        'test_integer': 1,
        'test_list': ['+', x, y],
    }
    if (result < 0):
        ELK_logger.info('Negative addition: Result < zero.', extra=extra)
    elif (result == 0):
        ELK_logger.info('Neutral addition: Result = zero.', extra=extra)
    else:
        ELK_logger.info('Positive addition: Result > zero.', extra=extra)
    print('Result of {0} + {1} is {2}'.format(x, y, result))

def subtract(x, y, ELK_logger):
    result = x - y
    extra = {
        'test_string': 'Subtraction',
        'test_boolean': True,
        'test_dict': {'x': x, 'y': y, 'op': '-'},
        'test_float': result,
        'test_integer': 2,
        'test_list': ['-', x, y],
    }
    if (result < 0):
        ELK_logger.info('Negative subtraction: Result < zero.', extra=extra)
    elif (result == 0):
        ELK_logger.info('Neutral subtraction: Result = zero.', extra=extra)
    else:
        ELK_logger.info('Positive subtraction: Result > zero.', extra=extra)
    print('Result of {0} - {1} is {2}'.format(x, y, result))

def multiply(x, y, ELK_logger):
    result = x * y
    extra = {
        'test_string': 'Multiplication',
        'test_boolean': True,
        'test_dict': {'x': x, 'y': y, 'op': '*'},
        'test_float': result,
        'test_integer': 3,
        'test_list': ['*', x, y],
    }
    if (result < 0):
        ELK_logger.info('Negative multiplication: Result < zero.', extra=extra)
    elif (result == 0):
        ELK_logger.info('Neutral multiplication: Result = zero.', extra=extra)
    else:
        ELK_logger.info('Positive multiplication: Result > zero.', extra=extra)
    print('Result of {0} * {1} is {2}'.format(x, y, result))

def divide(x, y,ELK_logger):
    try:
        result = x / y
    except ZeroDivisionError:
        extra = {
            'test_string': 'Division',
            'test_boolean': False,
            'test_dict': {'x': x, 'y': y, 'op': '/'},
            'test_float': 0,
            'test_integer': 4,
            'test_list': ['/', x, y],
        }
        ELK_logger.exception('Division by zero', extra=extra)
        print('It is not possible to devide a number by zero...')

    else:
        extra = {
            'test_string': 'Division',
            'test_boolean': True,
            'test_dict': {'x': x, 'y': y, 'op': '/'},
            'test_float': result,
            'test_integer': 4,
            'test_list': ['/', x, y],
        }
        if (result < 0):
            ELK_logger.info('Negative division: Result < zero.', extra=extra)
        elif (result == 0):
            ELK_logger.info('Neutral division: Result = zero.', extra=extra)
        else:
            ELK_logger.info('Positive division: Result > zero.', extra=extra)
        print('Result of {0} / {1} is {2}'.format(x, y, result))
    return

def getOperation(ELK_logger):
    operation = -1
    while (operation not in ['0', '1', '2', '3', '4']):
        print
        print
        print('Which operation would you like to perform?')
        print('Enter "0" to exit')
        print('Enter "1" for addition')
        print('Enter "2" for subtraction')
        print('Enter "3" for multiplication')
        print('Enter "4" for division')
        operation = str(input(">>"))
        print
        if (operation not in ['0', '1', '2', '3', '4']):
            extra = {
                'test_string': 'getOperation',
                'test_boolean': False,
                'test_dict': {'op' : operation},
                'test_float': 0,
                'test_integer': 0,
                'test_list': [operation],
            }
            ELK_logger.error('Illegal user-input in menu. Operation ' + operation + ' is not allowed.', extra=extra)
            print('"{0}" is not a valid menu option!'.format(operation))
    return operation

def getNumber(question, ELK_logger):
    isNumber = False
    while (isNumber == False):
        print
        print(question)
        inputStr = str(input(">>"))
        try:
            num = float(inputStr)
        except ValueError:
            isnumber = False
            extra = {
                'test_string': 'getNumber',
                'test_boolean': False,
                'test_dict': {'x': inputStr},
                'test_float': 0,
                'test_integer': 0,
                'test_list': [inputStr],
            }
            ELK_logger.error('Illegal user-input. Number ' + num + ' is not a valid number.', extra=extra)
            print
            print("'{0}' is not a valid number...".format(inputStr))
        else:
            isNumber = True
    return num
    

def main():
    #setup ELK logging
    ELK_logger = logging.getLogger('python-logstash-logger')
    ELK_logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    ELK_logger.addHandler(logstash.LogstashHandler(host, port, version=1))

    #run infinite loop
    while True:
        operation = getOperation(ELK_logger)
        if operation == '0':
            extra = {
                'test_string': 'Exit',
                'test_boolean': True,
                'test_dict': {},
                'test_float': 0,
                'test_integer': 0,
                'test_list': []
            }
            ELK_logger.info('User request to exit.', extra=extra)
            break

        num1 = getNumber("Please enter the 1st number:", ELK_logger)
        num2 = getNumber("Please enter the 2nd number:", ELK_logger)

        if (operation == '1'):
            add(num1, num2, ELK_logger)
        elif (operation == '2'):
            subtract(num1, num2, ELK_logger)
        
        elif (operation == '3'):
            multiply(num1, num2, ELK_logger)
        
        elif (operation == '4'):
            divide(num1, num2, ELK_logger)


main()
