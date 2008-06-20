class Sample:
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
        
        if self.tk_sound.min() < v < self.tk_sound.max():
            self.sound.sample(self.index, int(v))
        else:
            raise ValueError('Sample value is out of range.')


    def get_value(self):
        '''Return this Sample's value.'''
        
        return self.tk_sound.sample(self.index)


    def get_index(self):
        '''Return this Sample's index.'''
        
        return self.index