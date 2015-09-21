import urllib2, json
from print_pretty import pretty_print
from custom_funcs import *

'''
print pretty is a custom function that takes an array and
prints it out to the screen in 2 columns. the width of
the columns is determined by the longest string embedded
within the array. this helps to avoid clipping
'''


'''
!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Start the program loop below
||||||||||||||||||||||||||||
'''

def main():
    while True:
        car = choose_car()

        styleID = car['styleID']

        directory(styleID, car)
        
    ##################################################################################
    #       Place all data above this line. end of the loop is below - BEWARE!       #
    ##################################################################################

        #loop end to see if you want to search for another cars data
        '''
        go_again = raw_input('\nWant to go again?\nType "Yes" or "No": ').upper()
        if go_again == 'NO':
            break
        '''

main()
