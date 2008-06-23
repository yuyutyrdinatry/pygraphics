class MonoSample(object):
    '''A sample in a sound with an index value'''
    
    def __init__(self, snd, i):
        '''Create a Sample object from Sound snd at index i.'''
        
        self.tk_sound = snd
        self.index = i


    def __str__(self):
        '''Return a str with index and value information'''
        
        return "Sample at " + str(self.index) + " with value " \
                 + str(self.get_value())
    

    def set_value(self, v):
        '''Set this Sample's value to v.'''
        
        self.tk_sound.sample(self.index, int(v))


    def get_value(self):
        '''Return this Sample's value.'''
        
        return int(self.tk_sound.sample(self.index))


    def get_index(self):
        '''Return this Sample's index.'''
        
        return self.index
    

class StereoSample(MonoSample):
    '''A sample in a two-channeled sound with a left and a right value.'''

    
    def set_value(self, v):
        '''Raise error for inheritance purposes.'''
        
        raise AttributeError("'TwoChannelSample' object has no attribute 'set_value'")

    def get_value(self):
        '''Raise error for inheritance purposes.'''
        
        raise AttributeError("'TwoChannelSample' object has no attribute 'get_value'")

    
    def set_values(self, left, right):
        '''Set this TwoChannelSample's left value to left and 
        right value to right.'''
        
        self.tk_sound.sample(self.index, int(left), int(right))
    

    def get_values(self):        
        '''Return this TwoChannelSample's left and right values as a tuple 
        (left, right) of two ints.'''
        
        res = self.tk_sound.sample(self.index).split()
        res = (int(res[0]), int(res[1]))
        return res

    
    def set_left(self, v):
        '''Set this TwoChannelSample's left value to v.'''
        
        self.tk_sound.sample(self.index, left=int(v))


    def set_right(self, v):
        '''Set this TwoChannelSample's right value to v.'''
        
        self.tk_sound.sample(self.index, right=int(v))
        
        
    def get_left(self):
        '''Return this TwoChannelSample's left value.'''

        return self.get_values()[0]
    
    
    def get_right(self):
        '''Return this TwoChannelSample's right value.'''

        return self.get_values()[1]

class MultiChannelSample(StereoSample):
    '''TODO: FIX ME UP'''
    
    def set_values(self, left, right):
        '''Set this TwoChannelSample's left value to left and 
        right value to right.'''
        
        pass

    def get_values(self):        
        '''Return this TwoChannelSample's left and right values as a tuple 
        (left, right) of two ints.'''
        
        pass

