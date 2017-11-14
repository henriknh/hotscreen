class MultiKeyDictionary(object):
    """ Multiple keys to one value dictionary """

    # The keys and values dict will look like this:
    # Keys: {'key1': {'value'}, 'key2': {'value'}, 'key3': {'value'}}
    # Values: {'value': {'key3', 'key1', 'key2'}}
    
    def __init__(self): # start with two empty ditionaries
        self.keys = {} 
        self.values = {}

    # first check if value already exist, then if it is 
    def __setitem__(self, key, value): # for dict[key] = value
        if key not in self.keys:
            if value not in self.values: # key and value isn't in dictionary
                self.keys[key] = value #set() # a new set of key and value
                #self.keys[key].add(value)
                self.values[value] = set() # set within dictionary
                self.values[value].add(key) # relate key to value and value to key
            elif value in self.values:
                # value already exist, add new key 'pointing' to value
                self.keys[key] = value #set()
                #self.keys[key].add(value)
                self.values[value].add(key)
        elif key in self.keys: # need old value
            old_value = self.keys[key]
            if old_value != value:
                affected_keys = self.values[old_value]
                del self.values[old_value] # immutable, so need to create new
                self.values[value] = set()
                for key in affected_keys:
                    self.values[value].add(key)
                    self.keys[key] = value
                    
    def __delitem__(self, key): # for del dict[key]
        # want to delete only a key related to a value
        try:
            value = self.keys[key]
            del self.keys[key]
            # remove it from values
            self.values[value].remove(key)
            if len(self.values[value]) == 0: #if value empty after removal
                del self.values[value]
        except KeyError:
            raise KeyError("Key not found")
            
    def remove(self, value): #want to delete value and all keys related to it
        try:
            affected_keys = self.values[value] # all related keys to value
            for key in affected_keys:
                del self.keys[key]
            del self.values[value]
        except KeyError:
            raise KeyError("Value not found")
  
    def __getitem__(self, key): # to get value with dict[key]
        value = self.keys[key]
        return value

    def add(self, key_list, value): # assign multi keys, one value
        for key in key_list:
                self.__setitem__(key, value)

    def has(self, key):
        if key in self.keys:
            return True
        else:
            return False

    def str(self): # create string representation of dictionary
        value_list = self.values.keys()
        string = ""
        for value in value_list:
            string += '{ Key(s):'
            all_keys = self.values[value]            
            for key in all_keys:
                string += ' ' + str(key) + ', '         
            string += ' Value: ' + str(value) + '}\n'
        return string
        
                
    
