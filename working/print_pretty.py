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
