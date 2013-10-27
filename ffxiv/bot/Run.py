import util.Constants as const
import util.ImageProcessor as imaging
import util.MathExtended as math_ext
import util.Mouse
import ffxiv.game.Player as player
import ffxiv.bot.Botany as botany
import ffxiv.game.Minimap

import os
import cv2
import math
import time
import win32api

'''
Created on Oct 6, 2013

@author: Karl
'''

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
    image_processor = imaging.ImageProcessor()

#     image_processor.boundedScreenshot(100, 100, 600, 600, search_source)
    image_processor.boundedScreenshot(1443, 30, 215, 215, search_source)
    mouse = util.Mouse.Mouse()

    start=time.clock()
    template_dir = 'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\Rosewood\\'
    nodes = []
    for fn in os.listdir(template_dir):
        template_source = template_dir + fn
        match = image_processor.findImage(search_source, template_source)
        print template_source
        print match
    print "Node: " + str(nodes)
#     match = image_processor.findImage(search_source, template_source1)
#     print "Node: " + str(match)
#     duration = time.clock() - start
#     print "Dur: " + str(duration)
#     match = image_processor.findImage(search_source, template_source2)
#     print "Node Light: " + str(match)
#     
#     match = image_processor.findImage(search_source, template_source3)
#     print "Node Mid Cliff: " + str(match)
#     
#     match = image_processor.findImage(search_source, template_source4)
#     print "Node Mid River: " + str(match)
#     
#     match = image_processor.findImage(search_source, template_source4)
#     print "Node Arbor Call: " + str(match)
#     
#     match = image_processor.findImage(search_source, template_source4)
#     print "Node Arbor Call Light: " + str(match)
#     
#     match = image_processor.findImage(search_source, template_source4)
#     print "Node Mid Fate: " + str(match)
    duration = time.clock() - start
    print "Dur: " + str(duration)