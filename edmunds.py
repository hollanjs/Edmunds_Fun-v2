import urllib2, json, sys

#####################################
#       print pretty function       #

def even_out_array(array):
    #even out the number
    #of array elements
    if len(array)%2 == 1:
        array.append('')
    return array

#####################################
#chunking arrays for printing pretty#
def chunkIt(array, num):
    avg = len(array) / float(num)
    out = []
    last = 0.0

    while last < len(array):
        out.append(array[int(last):int(last + avg)])
        last += avg

    return out

#####################################
#           print pretty            #
def prettify(chunked_array, orig_array):
    longest = str(len(max(orig_array, key=len)))
    template = '{0:'+longest+'}  |  {1:'+longest+'}'
    try:
        for row in chunked_array:
            print template.format(*row)
    except IndexError:
        pass
    
#####################################

########################################
#combine all the pretty print functions#
def pretty_print(info):
    print prettify(chunkIt(even_out_array(info), len(info)/2), info)
    
########################################

'''
print pretty is a custom function that takes an array and
prints it out to the screen in 2 columns. the width of
the columns is determined by the longest string embedded
within the array. this helps to avoid clipping
'''

#####################################
#         Functions Below           #
#####################################

#edmunds api key
API_KEY = 'hw2p8rn9y8b4q4hy2rasxf76'

def list_check(item, array):
    item = item
    while item not in array:
        item = raw_input ('Choice not in list above - try again...\nENTER CHOICE HERE -->  ').title()
    return item

def choose_car():
    #url to pull basic info for all years, makes and models available
    url = 'https://api.edmunds.com/api/vehicle/v2/'\
    'makes?fmt=json&api_key=' + API_KEY
    
    #get response data and append to 'resp' variable as JSON
    data = json.load(urllib2.urlopen(url))
    
    #set arrays to hold dynamic information
    makes = []
    models = []
    make_and_models = []
    years = []
    trim_packages = []
    car_id =''
    template = '{0:20}{1:20}{2:20}'

    #loop through all available data and choose a car make
    for make in data['makes']:
        makes.append(make['name'])
        
    #get car make selection
    print('\nChoose a make from the following:\n')
    pretty_print(makes)  
    make_choice = raw_input('\nENTER CHOICE HERE -->  ').title()
    make_choice = list_check(make_choice, makes)

    #loop through and choose a model for the make
    for make in data['makes']:
        if make['name'] == make_choice:
            for model in make['models']:
                models.append(model['name'])

        for i in range(len(models)):
            make_and_models.append('{} {}'.format(make_choice, models[i]))
            
    #get model selection per the chosen make
    print('\nChoose a make from the following:\n')
    pretty_print(models)
    model_choice = raw_input('\nENTER CHOICE HERE -->  ').title()
    model_choice = list_check(model_choice, models)

    #loop through and get the years available for that make and model
    for make in data['makes']:
        if make['name'] == make_choice:
            for model in make['models']:
                if model['name'] == model_choice:
                    for year in model['years']:
                        years.append(str(year['year']))

    #get the year selection for selected make and model
    print('\nThe following years are available for the {} {}:\n'.format(make_choice, model_choice))
    pretty_print(years)                         
    year_choice = raw_input('\nWhich year do you want information for?\nENTER THE YEAR HERE -->  ')
    year_choice = list_check(year_choice, years)

    #get trim packaging avialable for that year-make-model
    styles_url = 'https://api.edmunds.com/api/vehicle/v2/'+make_choice+'/'+model_choice+'/'+year_choice+'/styles?fmt=json&api_key='+API_KEY
    #use new URL to pull trim data - append to 'styles_resp' as JSON
    styles_resp = json.load(urllib2.urlopen(styles_url))

    #append trim styles to trim_packaging array
    for style in styles_resp['styles']:
        trim_packages.append(style['trim'])
    
    print('\nThe following trim packaging are available for the {} {} {}:'.format(year_choice, make_choice,model_choice))

    #print out trim packages and associate them with numbers
    #this helps avoid capitalization errors and keeps things neet
    for i in range(len(trim_packages)):
        print('{} :   {}'.format(i, trim_packages[i]))

    #choose trim package by number selection
    choice = raw_input('Enter the number of the trim package you would like to select\n-->')
    trim_choice = str(trim_packages[int(choice)])
    

    print('getting data for the {} {} {} {}\n'.format(year_choice,make_choice,model_choice,trim_choice))

    #get style number
    for style in styles_resp['styles']:
        if style['trim'] == trim_choice:
            car_id = style['id']
            print('Unique car style ID --> {}'.format(car_id))
            
    car_selection = {'year': year_choice, 'make': make_choice, 'model': model_choice, 'trim': trim_choice, 'styleID': car_id}
    return car_selection

def get_options(style_ID):
    #call url to get car options
    options_url = 'https://api.edmunds.com/api/vehicle/v2/styles/'+str(style_ID)+'/options?fmt=json&api_key='+API_KEY
    options = json.load(urllib2.urlopen(options_url))

    #list out options
    print('OPTIONS\n_______\n')
    count = 1
    for feature in options['options']:
        feature_attributes = []
        print('{}. {}'.format(str(count),feature['name']))
        print('Category - {}'.format(feature['category']))
        try:
            print('DESCRIPTION:\n{}'.format(feature['description']))
        except:
            print('DESCRIPTION:\nSorry, no description available')
        #append feature attributes to 'feature_attributes' array
        for attribute in feature['attributes']:
               feature_attributes.append(attribute['name'])
        if len(feature_attributes) > 0:
            print('features: {}\n\n'.format(', '.join(feature_attributes)))
        else:
            print('\n\n')
        count += 1

def get_colors(style_ID):
    colors = []
    color_url = 'https://api.edmunds.com/api/vehicle/v2/styles/'+str(style_ID)+'/colors?fmt=json&api_key='+API_KEY
    color_data = json.load(urllib2.urlopen(color_url))

    print(' _______________\n|EXTERIOR COLORS|\n _______________')
    for color in color_data['colors']:
        if color['category'] == 'Exterior':
            print('{}'.format(color['name']))
    print('\n')
    print(' _______________\n|INTERIOR COLORS|\n _______________')
    for color in color_data['colors']:
        if color['category'] == 'Interior':
            print('{}'.format(color['name']))
    print('\n')
    
    #print json.dumps(color_data, indent = 4)

def directory(styleID):
    looking_at_info = True
    while looking_at_info:
        chose_option = {'1': ' - Get Options',
                        '2': ' - Get Colors',
                        '#': ' - Choose Another Car',
                        '0': ' - Done'}
        
        print('\nChoose and option:')
        for key in chose_option:
            print key, chose_option[key]

        chosen_option = str(raw_input('\n-->  '))
        while chosen_option not in chose_option.keys():        
            chosen_option = str(raw_input('Try again -->  '))

        if chosen_option == '1':
            get_options(styleID)
        elif chosen_option == '2':
            get_colors(styleID)
        elif chosen_option == '#':
            break
        else:
            sys.exit("Thanks!")


'''
!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Start the program loop below
||||||||||||||||||||||||||||
'''


while True:
    car = choose_car()

    styleID = car['styleID']

    directory(styleID)
    



