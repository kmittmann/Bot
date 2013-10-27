import win32api, win32con

class Mouse(object):
    
    mouse_action = {'move':win32con.MOUSEEVENTF_MOVE,
                   'right_up':win32con.MOUSEEVENTF_RIGHTUP,
                   'right_down':win32con.MOUSEEVENTF_RIGHTDOWN}
    
    def __init__(self):
        self.x_res = win32api.GetSystemMetrics(0)
        self.y_res = win32api.GetSystemMetrics(1)

    def rightClick(self, x, y):
        nx = x*65535/self.x_res
        ny = y*65535/self.y_res
        win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_MOVE,nx,ny)
        win32api.Sleep(200)
        win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
        win32api.Sleep(200)
        win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)
        win32api.Sleep(700)
        
    def leftClick(self, x, y):
        nx = x*65535/self.x_res
        ny = y*65535/self.y_res
        win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_MOVE,nx,ny)
        win32api.Sleep(200)
        win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.Sleep(200)
        win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
        win32api.Sleep(700)
        
    def doubleClick(self, x, y):
        nx = x*65535/self.x_res
        ny = y*65535/self.y_res
        win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_MOVE,nx,ny)
        win32api.Sleep(300)        
        win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.Sleep(300)
        win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
        
        win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.Sleep(300)
        win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
        win32api.Sleep(300)
        
    def move(self, x, y):
        nx = x*65535/self.x_res
        ny = y*65535/self.y_res
        win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_MOVE,nx,ny)
    
    def wheelUp(self, clicks):
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, win32con.WHEEL_DELTA * clicks, 0)
        
    def wheelDown(self, clicks):
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, win32con.WHEEL_DELTA * -clicks, 0)
            

    def clickAndDrag(self, x, y, x_dist, y_dist, mouse_click, release):
        """
        Drags cursor from given x, y position to a coordinate of distance x_dist,
        y_dist away.
        mouse_click determines which mouse button is used. default is left, 
        'right' and 'both' can also be used. 
        """
        nx = x*65535/self.x_res
        ny = y*65535/self.y_res
        n_x_dist = x_dist*65535/self.x_res
        n_y_dist = y_dist*65535/self.y_res
        win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_MOVE,nx, ny, 0, 0)
        win32api.Sleep(300)
        if mouse_click is 'right':
            win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_RIGHTDOWN,nx, ny,0,0)
            win32api.Sleep(300)
            win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_MOVE,nx + n_x_dist, ny + n_y_dist, 0, 0)
            if release:
                win32api.Sleep(300)
                win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_RIGHTUP,nx + n_x_dist,ny + n_y_dist,0,0)
        elif mouse_click is 'both':
            win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_LEFTDOWN,nx, ny,0,0)
            win32api.Sleep(150)
            win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_RIGHTDOWN,nx, ny,0,0)
            win32api.Sleep(150)
            win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_MOVE,nx + n_x_dist, ny + n_y_dist, 0, 0)
            if release:
                win32api.Sleep(150)
                win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_LEFTUP,nx + n_x_dist, ny + n_y_dist, 0, 0)
                win32api.Sleep(150)
                win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_RIGHTUP,nx + n_x_dist, ny + n_y_dist, 0, 0)
        else:
            win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_LEFTDOWN,nx, ny,0,0)
            win32api.Sleep(150)
            win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_MOVE,nx + n_x_dist, ny + n_y_dist, 0, 0)
            if release:
                win32api.Sleep(150)
                win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_LEFTUP,nx + n_x_dist, ny + n_y_dist, 0, 0)
        win32api.Sleep(300)
        
if __name__ == '__main__':
    '''
    Mouse Testing
    '''
    mouse = Mouse()
    win32api.Sleep(2000)
    x = 1680 / 2
    y = 1050 / 2
    x_dist = 10
    y_dist = 0
#     mouse.rightClick(x,y)
    mouse.clickAndDrag(x, y, x_dist, y_dist, 'right', False)