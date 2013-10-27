import util.Keyboard as keyboard

import win32api

'''
Created on Sep 24, 2013

@author: Karl
'''

class Map(object):
    """Class representing in-game Map."""
    
    __state = 'closed'

    def __init__(self):
        '''Initializes Map Object'''
        self.keyboard = keyboard.Keyboard()
        
    def open(self):
        '''Opens Map'''
        if self.__state is 'closed':
            self.keyboard.press('m')
            self.__state = 'open'
        
    def close(self):
        '''Closes Map'''
        if self.__state is 'open':
            self.keyboard.press('m')
            self.__state = 'closed'
    
if __name__ == '__main__':
    win32api.Sleep(2000)
    m = Map()
    m.Minimap.findMinimap()