import cv2
import numpy as np
import ImageGrab
import math
import win32api

import util.Mouse
import util.Constants as const

"""
Created on Sep 23, 2013

@author: Karl
"""
class ImageProcessor(): 
    
    def __init__(self):
        """Initializes Image Processor"""  
        self.x_res = win32api.GetSystemMetrics (0)
        self.y_res = win32api.GetSystemMetrics (1)  
    
    def findImage(self, search_source, template_source):
        """
        Returns tuple of match_loc (x, y), where the best match was found 
            and match_val, a value between 0.00 and 1.00, the closer to 1.00
            the more confident the match is. 
        For more control see: templateMatch()
        """
        match_method = cv2.TM_CCOEFF_NORMED
        result = self.templateMatch(search_source, template_source, match_method)
        return self.__getTemplateMatchOutput(result, match_method)
    
    def findMultipleImages(self, search_source, template_source):
        """
        Returns list of tuples (x, y) for matching template locations. 
        For more control see: templateMultiMatch()
        """
        match_method = cv2.TM_CCOEFF_NORMED
        return self.templateMultiMatch(search_source, template_source, 
                                       match_method, 0.7)
    
    def templateMatch(self, search_source, template_source, match_method):
        """
        Takes two image paths and compares them with OpenCV template match method.      
        Returns tuple of maxVal and matchLoc 
            match_val is a value 0.0-1.0, the higher the result the more confident its been found. 
            match_loc is tuple (x, y) where match was found
        """
        search_image = cv2.imread(search_source)
        if search_image is None:
            raise IOError("Issue during OpenCV image read. Search image file may not exist or may have loaded incorrectly: " + 
                          search_source) 
        template_image = cv2.imread(template_source)  
        if template_image is None:
            raise IOError("Issue during OpenCV image read. Template image file may not exist or may have loaded incorrectly: " +
                          template_source)
            
        mt = [cv2.TM_SQDIFF,
              cv2.TM_SQDIFF_NORMED,
              cv2.TM_CCORR,
              cv2.TM_CCORR_NORMED,
              cv2.TM_CCOEFF,
              cv2.TM_CCOEFF_NORMED]       
        return cv2.matchTemplate(search_image, template_image, mt[match_method])
    
    def templateMultiMatch(self, search_source, template_source, match_method, threshold):
        """
        Returns list of tuples (x, y) for matching template locations 
        that exceed the threshold specified
        """
        if not threshold: 
            threshold = 0.75
        if not match_method:
            match_method = cv2.TM_CCOEFF_NORMED  
        result = self.templateMatch(search_source, template_source, match_method)
        template_image = cv2.imread(template_source) 
        t_height = template_image.shape[0]
        t_width = template_image.shape[1]
        #get all the matches above threshhold 0.75 (fairly accurate)
        loc = np.where( result >= threshold)     
        threshold_points = zip(*loc[::-1]) 
        #If no points were found, return
        if not threshold_points:
#             print "No images meet threshold"
            return None

        unique_locations = [] #Points on the image that represent unique template matches
        unique_locations.append(threshold_points[0])
        curr = 0
        for point in threshold_points:
            x_diff = math.fabs(point[0] - unique_locations[curr][0])
            y_diff = math.fabs(point[1] - unique_locations[curr][1])
            if x_diff > (t_width / 3) and y_diff > (t_height / 3):
                curr += 1
                unique_locations.append(point)            
        return unique_locations
        
    def screenshot(self, file_path):
        """
        Saves a screenshot to file_path parameter as PNG. 
        """
        try:
            img = ImageGrab.grab(bbox=(0, 0, self.x_res, self.y_res))
            img.save(file_path, 'PNG') 
        except Exception as e:
            raise Exception("Unable to capture screen. Please check input resolutions. ", e)
     
    def boundedScreenshot(self, x, y, width, height, file_path):
        """
        Saves a screenshot to file_path parameter as PNG. 
        Screenshot will be bounded by x, y, width, height
        """
        try:
            img = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            img.save(file_path, 'PNG') 
        except Exception as e:
            raise Exception("Unable to capture screen. Please check input resolutions.", e)

     
###
#Implied private methods, use at your own risk
###
    def __getTemplateMatchOutput(self, result, match_method):
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
#       cv2.normalize(result, result, 0, 1, cv2.NORM_MINMAX, -1)
#       (min_x, max_y, min_loc, max_loc) = cv2.minMaxLoc(result)
        if match_method == cv2.TM_SQDIFF or match_method == cv2.TM_SQDIFF_NORMED :
            match_loc = min_loc
            match_val = min_val
        else: 
            match_loc = max_loc
            match_val = max_val
        return (match_val, match_loc)
    
if __name__ == '__main__':
    win32api.Sleep(3000)
#     template_image_path = 'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\botany_node.png'
    template_source1 = 'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\Walnut\\botany_node.png'
    template_source2 = 'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\Walnut\\botany_node_light.png'
    template_source3 = 'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\Walnut\\botany_node_mid_cliff.png'
    template_source4 = 'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\Walnut\\botany_node_mid_river.png'
    template_source5 = 'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\Walnut\\botany_node_arbor_call.png'
    template_source6 = 'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\Walnut\\botany_node_arbor_call_light_1.png'
    template_source7 = 'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\Walnut\\botany_node_mid_fate.png'
    search_source = const.IMG_DEFAULT_SCREENSHOT_PATH
    
    image_processor = ImageProcessor()
#     image_processor.boundedScreenshot(100, 100, 600, 600, search_source)
    image_processor.screenshot(search_source)
    match = image_processor.findImage(search_source, template_source1)
    print "Node: " + str(match)
  
    match = image_processor.findImage(search_source, template_source2)
    print "Node Light: " + str(match)
    
    match = image_processor.findImage(search_source, template_source3)
    print "Node Mid Cliff: " + str(match)
    
    match = image_processor.findImage(search_source, template_source4)
    print "Node Mid River: " + str(match)
    
    match = image_processor.findImage(search_source, template_source4)
    print "Node Arbor Call: " + str(match)
    
    match = image_processor.findImage(search_source, template_source4)
    print "Node Arbor Call Light: " + str(match)
    
    match = image_processor.findImage(search_source, template_source4)
    print "Node Mid Fate: " + str(match)
    
    