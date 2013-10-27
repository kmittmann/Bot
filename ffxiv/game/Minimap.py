import util.Mouse as mouse
import util.Constants as const
import util.ImageProcessor as imaging

import math
import win32api



 
class Minimap(object):
        
        def __init__(self):
            """Initializes Minimap Object"""  
            self.image_processor = imaging.ImageProcessor()  
            self.mouse = mouse.Mouse()     
            match_loc = self.findMinimap()
            self.x_char_pos = match_loc[0]
            self.y_char_pos = match_loc[1]
            #Set minimap bounding coordinates (estimates)
            #Used to reduce node search time and increase accuracy
            self.x_map_pos = self.x_char_pos - 100
            if self.x_map_pos < 0:
                self.x_map_pos = 0
                
            self.y_map_pos = self.y_char_pos - 100
            if self.y_map_pos < 0:
                self.y_map_pos = 0
                
            self.map_width = 215
            if self.x_map_pos + self.map_width > self.image_processor.x_res:
                self.map_width = self.image_processor.x_res - self.x_map_pos
                
            self.map_height = 215
            if self.y_map_pos + self.map_height > self.image_processor.y_res:
                self.map_height = self.image_processor.y_res - self.y_map_pos
            
            self.minimap_level = 0
            self.zoomIn(7)

        
        def findMinimap(self):
            """Finds position of minimap character icon in UI"""               
            template_image_path = const.IMG_MINIMAP_CHARACTER
            
            self.image_processor.screenshot(const.IMG_DEFAULT_SCREENSHOT_PATH)
            match_val, match_loc = self.image_processor.findImage(const.IMG_DEFAULT_SCREENSHOT_PATH, 
                                                                  template_image_path)
            if match_val < 0.80: 
                raise Exception("Minimap not found. Please enable minimap.")
            return match_loc
        
        def findImageOnMinimap(self, template_source):
            """
            Returns list of tuples (x, y) containing image positions within
            the bounds of the minimap
            """
 #           self.image_processor.screenshot(self.screenshot_path)
            self.image_processor.boundedScreenshot(self.x_map_pos, self.y_map_pos, 
                                                   self.map_width, self.map_height, 
                                                   const.IMG_DEFAULT_SCREENSHOT_PATH)
            
            locations = self.image_processor.findMultipleImages(const.IMG_DEFAULT_SCREENSHOT_PATH, template_source)
            absolute_loc = []
            if locations:
                for loc in locations:
                    absolute_loc.append(self.__getAbsolutePoint(loc))
            return absolute_loc
#            return self.image_processor.templateMultiMatch(self.screenshot_path, 
#                                                           template_source, match_method, threshold)
        
        def setZoomLevel(self, level):
            """Zooms into minimap one step""" 
            steps = self.minimap_level - level
            if steps > 0:
                steps = int(math.fabs(steps))
                self.zoomOut(steps)
            else:       
                steps = int(math.fabs(steps))
                self.zoomIn(steps)        
        
        def zoomIn(self, steps):
            """Zooms into minimap one step"""        
            if self.minimap_level < 7:
#                self.__minimapAction('zoom in', steps)\
                self.mouse.move(self.x_char_pos, self.y_char_pos)
                win32api.Sleep(200) 
                self.mouse.wheelUp(steps)
                win32api.Sleep(200) 
                if self.minimap_level + steps < 7:
                    self.minimap_level += steps
                else:
                    self.minimap_level = 7
                self.mouse.move(0,0) 
            
        def zoomOut(self, steps):
            """ Zooms out of minimap one step""" 
            if self.minimap_level > 1:
#                 self.__minimapAction('zoom out', steps)
                self.mouse.move(self.x_char_pos, self.y_char_pos)
                win32api.Sleep(200) 
                self.mouse.wheelDown(steps)
                win32api.Sleep(200) 
                if self.minimap_level - steps > 1:
                    self.minimap_level -= steps
                else:
                    self.minimap_level = 1  
                self.mouse.move(0,0) 
            
        def lockUnlock(self):
            """Locks minimap 'default' position"""
            self.__minimapAction('lock', 0)
            
        def distanceFromCharacter(self, x, y):
            """Returns distance between point (x, y) and character icon""" 
            return math.sqrt(((self.x_char_pos - x) ** 2)
                              + ((self.y_char_pos - y) **2))
            
        def determinePixelsPerSec(self, travel_type):
            '''
            Returns the pixel distance for 1 second at each minimap level
            Coefficients:
                        0.3452381    5.8452381   14.42857143'''        
            x = self.minimap_level
            #Divided by 5 because poly fit was determined with 5 second runs
            run_per_sec =  ((0.3452381 * (x**2)) + (5.8452381 * (x)) + 14.42857143) / 5
            if travel_type is 'mount':
                return run_per_sec * (1.5)
            elif travel_type is 'walk': 
                return run_per_sec * (0.4)
            else:
                return run_per_sec
###
#Implied Private Methods (Use at your own risk)
### 
        def __minimapAction(self, action, steps):
            """
            Protected method handles minimap actions
            action param options: 'zoom in', 'zoom out', 'lock'
            """
            if action == 'zoom in':
                template_image_path = const.IMG_MINIMAP_ZOOM_IN
            elif action == 'zoom out':
                template_image_path = const.IMG_MINIMAP_ZOOM_OUT
            elif action == 'lock':
                template_image_path = const.IMG_MINIMAP_LOCK
            else: #No action specified
                raise Exception("Invalid minimap action specified. " + 
                                "Valid actions: 'zoom in', 'zoom out', 'lock'")
            self.image_processor.boundedScreenshot(self.x_map_pos, self.y_map_pos,
                                     self.map_width, 
                                     self.map_height,
                                     const.IMG_DEFAULT_SCREENSHOT_PATH)
            match_val, match_loc =  self.image_processor.findImage(const.IMG_DEFAULT_SCREENSHOT_PATH, 
                                                                   template_image_path)
            match_loc = self.__getAbsolutePoint(match_loc)
            for x in range(0, steps):
                self.mouse.leftClick(match_loc[0] + 5, match_loc[1] + 5)

        def __getAbsolutePoint(self, minimap_point):
            return (minimap_point[0] + self.x_map_pos, minimap_point[1] + self.y_map_pos)
        
if __name__ == '__main__':
    win32api.Sleep(2000)
    m = Minimap()
    m.findMinimap()
    m.zoomIn(3)
    m.zoomOut(3)