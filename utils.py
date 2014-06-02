def dget(dictionary, cmd, default=None):
    '''get dictionary value from a nested dict'''
    cmd_list = cmd.split('.')
    tmp = dict(dictionary)
    for c in cmd_list: 
        try:
            val = tmp.get(c, None)
        except AttributeError:
            return default
        
        if val!= None:
            tmp = val
        else:
            #if val == None
            return default
    return tmp
        
if __name__ == "__main__":
    data = {'a':{'b':{'c':1}}}
    print dget(data, 'a.b.c')
