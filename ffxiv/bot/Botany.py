import util.Constants as const
import util.ImageProcessor as imaging
import util.MathExtended as math_ext
import util.Mouse
import ffxiv.game.Player as player

import os
import cv2
import math
import time
import win32api

'''
Created on Sep 26, 2013

@author: Karl
'''
class Botany(object):
    
    def __init__(self, farm_mat):
        """
        constructor
        """
        self.farm_mat = farm_mat
        self.player = player.Player()
        self.minimap = self.player.minimap
        self.image_processor = imaging.ImageProcessor()
        self.mouse = util.Mouse.Mouse()
          
          
    def run(self):
        """
        Start botany bot.
        """
#         self.findNextNode()
        result = self.findNextNodeRecursive()
        if not result:
            win32api.Sleep(2000)
            self.player.abilityKey(const.ABILITY_ARBOR_CALL)
            win32api.Sleep(750)
            result = self.findNextNodeRecursive()
    
        success = self.openGatherWindow()
        if success:
            success = self.gatherMaterials()
        else:
            self.player.cancel()
            self.player.cancel()
        return success
        
    def findNextNodeRecursive(self):
        """Find next node, recursive method"""
        self.player.cameraReset()
        self.player.callMount()
        
        nodes = self.findAllMinimapNodes()
        if not nodes:
            if self.isMounted():
                self.player.callMount()
            return None
        closest_dist, closest_node = self.findClosestMinimapNode(nodes)
        self.faceMinimapNode(closest_node)
        #Begin navigation towards nodes
        distance = self.minimap.distanceFromCharacter(closest_node[0], closest_node[1]) 
        #Approximate distance traveled on minimap after 1 second at a given level
        one_sec_dist = self.minimap.determinePixelsPerSec('mount')
        run_time_sec = (distance / one_sec_dist)    
        run_time_ms = int(1000 * (run_time_sec)) 
        self.avoidanceRun(run_time_ms * (0.75))  
#       self.runJump(current_time)
        self.findNextNodeRecursiveHelper(run_time_ms)
        win32api.Sleep(150)
        if self.isMounted():
            self.player.callMount()
        return True
        
    def findNextNodeRecursiveHelper(self, run_time_ms):
        """Recursive method."""
        self.player.targetNearestNPC()
        win32api.Sleep(200)
        detail = self.findDetailedNodeBar()
        if detail:
            return True
        else:
            self.player.cancel()
        
        nodes = self.findAllMinimapNodes(7, self.minimap.minimap_level)
        if nodes:
            closest_dist, closest_node = self.findClosestMinimapNode(nodes)
            self.faceMinimapNode(closest_node)
            distance = self.minimap.distanceFromCharacter(closest_node[0], closest_node[1]) 
            one_sec_dist = self.minimap.determinePixelsPerSec('mount')
            run_time_sec = (distance / one_sec_dist)   
            prev_time_ms = run_time_ms  
            run_time_ms = int(1000 * (run_time_sec))         
            self.avoidanceRun(run_time_ms / 2) 
            
            if prev_time_ms > run_time_ms:
                return self.findNextNodeRecursiveHelper(run_time_ms)
            elif prev_time_ms == run_time_ms:
                self.unstickCharacter()
                return self.findNextNodeRecursiveHelper(run_time_ms)
        return True
    
    def findNextNode(self):
        #Find all nodes at most zoomed in minimap level
        self.player.callMount()
        nodes = self.findAllMinimapNodes()
        closest_dist, closest_node = self.findClosestMinimapNode(nodes)
        self.faceMinimapNode(closest_node)
        
        #Begin navigation towards nodes
        #First Chunk, largest step
        distance = self.minimap.distanceFromCharacter(closest_node[0], closest_node[1]) 
        #Approximate distance traveled on minimap after 1 second at a given level
        one_sec_dist = self.minimap.determinePixelsPerSec('mount')
        run_duration = (distance / one_sec_dist)    
        current_time = int(1000 * (run_duration))  
        previous_time = current_time
        current_time = current_time / 2
#         self.runJump(current_time)
        self.mountRunTest(current_time)    
        
        #Second Chunk, smaller step
        nodes = self.findAllMinimapNodes()
        closest_dist, closest_node = self.findClosestMinimapNode(nodes)
        distance = self.minimap.distanceFromCharacter(closest_node[0], closest_node[1]) 
        #Approximate distance traveled on minimap after 1 second at a given level
        one_sec_dist = self.minimap.determinePixelsPerSec('mount')
        run_duration = (distance / one_sec_dist)    
        print run_duration
        current_time = int(1000 * (run_duration)  * 0.75) 
        while previous_time > current_time:
            print "Previous: " + str(previous_time)
            print "current: " + str(current_time)
            

            self.faceMinimapNode(closest_node)
#             self.runJump(current_time)           
            self.mountRunTest(current_time)
            #Second Chunk, smaller step
            nodes = self.findAllMinimapNodes(7, self.minimap.minimap_level)
            if nodes:
                closest_dist, closest_node = self.findClosestMinimapNode(nodes)
                distance = self.minimap.distanceFromCharacter(closest_node[0], closest_node[1]) 
                #Approximate distance traveled on minimap after 1 second at a given level
                one_sec_dist = self.minimap.determinePixelsPerSec('mount')
                run_duration = (distance / one_sec_dist)    
                previous_time = current_time
                current_time = int(1000 * (run_duration) / 2)
            else:
                break
        self.player.callMount()
        
    def openGatherWindow(self):
        self.player.targetNearestNPC()
        win32api.Sleep(200)
        detail = self.findDetailedNodeBar()

        #Partial run, checking to see if node has been found (align if so)
        if not detail:
            self.player.cancel()
            self.sideApproach()
            self.player.targetNearestNPC()
            win32api.Sleep(200)
            detail = self.findDetailedNodeBar()
        
        if not detail:
            self.player.cancel()
            self.player.rightTurn(int(const.ROTATION_TIME / 4))
            self.player.targetNearestNPC()
            win32api.Sleep(200)
            detail = self.findDetailedNodeBar()
        
        if not detail:
            self.player.cancel()
            self.player.leftStrafe(750)
            self.player.targetNearestNPC()
            win32api.Sleep(200)
            detail = self.findDetailedNodeBar()
        
        if not detail:
            self.player.cancel()
            self.player.rightTurn(int(const.ROTATION_TIME / 4))
            self.player.targetNearestNPC()
            win32api.Sleep(200)
            detail = self.findDetailedNodeBar()
            
        if not detail:
            self.player.cancel()
            self.player.cameraFirstPerson()
            self.player.targetNearestNPC()
            win32api.Sleep(200)
            detail = self.findDetailedNodeBar()
            self.player.cameraFirstPerson()
        
        if not detail:
            self.player.cancel()
            return False
        
        #Node has been found, narrow in
        self.player.lockOnTarget()
        self.player.confirm()
        success = self.findGatheringWindow()
        
        if not success:
            self.player.abilityKey(const.ABILITY_SPRINT)
        
        total_time = 0
        self.player.nonStopAction(const.FORWARD)
        while not success and total_time < 10000:
            #Attempt to gather from selected node, up to 3 attempts
#             self.strafeRun(2000)
            case = total_time / 250 % 4
            if case == 0:
                self.player.stop()
                self.player.nonStopAction(const.FORWARD)
                self.player.nonStopAction(const.LEFT_STRAFE)
            elif case == 1:
                self.player.stop()
                self.player.nonStopAction(const.FORWARD)
                self.player.nonStopAction(const.RIGHT_STRAFE)
            else:
                self.player.stop()
                self.player.nonStopAction(const.FORWARD) 
                self.player.abilityKey(const.JUMP)          
            
            if total_time == 6000:
                self.player.stop()
                self.player.leftStrafe(2000)
            
            self.player.confirm()
            success = self.findGatheringWindow()
            if success:
                self.player.stopRun()
                self.player.stop()
                break
            win32api.Sleep(250)
            total_time += 250

        self.player.stopRun()
        self.player.stop() 
        
        return success
        
    def findGatheringWindow(self):
        """Looks to see if the gathering window is open"""
        alt_template = const.IMG_GATHERING_MENU
        search_source = const.IMG_DEFAULT_SCREENSHOT_PATH
        x = 0
        y = 0
        width = self.image_processor.x_res / 3
        height = self.image_processor.y_res / 2
    #     image_processor.boundedScreenshot(100, 100, 600, 600, search_source)
        self.image_processor.boundedScreenshot(x, y, width, height, search_source)
        val, loc = self.image_processor.findImage(search_source, alt_template)
#         print "Gathering Window match val: " + str(val)
        if val > 0.98:
            return True
        return False
    
    def gatherMaterials(self):
        """Gather materials from node"""
        self.mouse.move(0,0)
        win32api.Sleep(200)
        template_source = const.IMG_GATHERING_TREE
        alt_template_source = const.IMG_GATHERING_VEG
        search_source = const.IMG_DEFAULT_SCREENSHOT_PATH
        x = 0
        y = 0
        width = self.image_processor.x_res / 5
        height = self.image_processor.y_res / 2
    #     image_processor.boundedScreenshot(100, 100, 600, 600, search_source)
        self.image_processor.boundedScreenshot(x, y, width, height, search_source)
        val, loc = self.image_processor.findImage(search_source, template_source)
        val2, loc2 = self.image_processor.findImage(search_source, alt_template_source)
        

        #Account for lag when first looking for material
        if val < 0.95 and val2 < 0.95:
            total_time = 0
            while total_time < 5000:
                self.image_processor.boundedScreenshot(x, y, width, height, search_source)
                val, loc = self.image_processor.findImage(search_source, template_source)
                val2, loc2 = self.image_processor.findImage(search_source, alt_template_source)
    #             print "Value: " + str(val)
                if val > 0.9:
                    break
                win32api.Sleep(150)
                total_time += 150
        
        castWard = True
        if val2 > val:
            val = val2
            loc = loc2
            template_source = alt_template_source
            castWard = False
            
        if val < 0.95:                
            print "Unable to find materials: " + str(val)
            self.player.cancel()
            self.player.cancel()
            return False
        
        if castWard:
            self.player.abilityKey(const.ABILITY_MENPHINAS_WARD)
            
        win32api.Sleep(1000)
        self.mouse.leftClick(loc[0], loc[1])
        win32api.Sleep(1000)
        total_time = 0
        while total_time < 20000:
            self.image_processor.boundedScreenshot(x, y, width, height, search_source)
            val, loc = self.image_processor.findImage(search_source, template_source)
#             print "Value: " + str(val)
            if val < 0.9:
                break
            if val > 0.99: 
                self.mouse.leftClick(loc[0], loc[1])
#                 self.player.confirm()  
                win32api.Sleep(1000)  
            win32api.Sleep(150)
            total_time += 150
        self.player.cancel()
        self.player.cancel()
        return True
    
###################################
#         Minimap Nodes           #  
###################################

    def findAllMinimapNodes(self, max_zoom_lvl = 7, min_zoom_lvl = 1):
        """
        Finds all non-centered nodes on minimap.
        """
        self.minimap.setZoomLevel(max_zoom_lvl)
        nodes = None
        for i in range(max_zoom_lvl, min_zoom_lvl - 1,-1):
            nodes = self.findNodesAtMinimapLevel()
            if nodes:
                return nodes
            self.minimap.zoomOut(1)
        return nodes   
    
    
    def findClosestMinimapNode(self, nodes):
        """
        Returns tuple (x,y) of closest node on minimap that character is not
        centered on.
        """
        if not nodes:
            return
        #Iterate through found nodes finding node with shortest distance on minimap
        closest_node = nodes[0]
        closest_dist = self.minimap.distanceFromCharacter(closest_node[0], closest_node[1])
        for i in range(1, len(nodes)):
            curr_node = nodes[i]
            curr_dist = self.minimap.distanceFromCharacter(curr_node[0], curr_node[1])
            if curr_dist < closest_dist:
                closest_dist = curr_dist
                closest_node = curr_node
        return (closest_dist, closest_node)
    
    
    def findNodesAtMinimapLevel(self):
        """
        Finds minimap nodes at a specific level
        """
        start = time.clock()
        nodes = []
        template_dir = const.IMG_TEMPLATE_DIR
        for fn in os.listdir(template_dir):
            template_source = template_dir + fn
            loc = self.minimap.findImageOnMinimap(template_source)
            if loc:
                nodes += loc
#         if not nodes:
#             print "No nearby nodes found."
        return nodes    
    
    
    def faceMinimapNode(self, node_loc):
        """
        Turn character to face point on minimap
        """  
        #Determine angle of triangle formed between character position
        #Node location, and ideal forward postion. 
        x1 = self.minimap.x_char_pos
        y1 = self.minimap.y_char_pos
        x2 = node_loc[0]
        y2 = node_loc[1]
        x3 = x1
        y3 = y1 - math_ext.distance(x1, y1, x2, y2)
        angle = math_ext.triangleAngle(x1, y1, x2, y2, x3, y3)
        turn_duration = (angle / (2 * math.pi)) * const.ROTATION_TIME
        if x1 > x2:
            self.player.leftTurn(int(turn_duration))
        else:
            self.player.rightTurn(int(turn_duration))
        return (x3, y3)
    
###################################
# Node Bars - Object Health       #  
###################################
    
    def findDetailedNodeBar(self):
        """Returns the location of a detailed node bar if found"""
        template_source = const.IMG_NODE_HEALTH
        alt_template = const.IMG_NODE_HEALTH_FULL_DETAIL
        search_source = const.IMG_DEFAULT_SCREENSHOT_PATH
        x = self.image_processor.x_res / 4
        y = 0
        width = self.image_processor.x_res / 2
        height = self.image_processor.y_res / 10
    #     image_processor.boundedScreenshot(100, 100, 600, 600, search_source)
        self.image_processor.boundedScreenshot(x, y, width, height, search_source)
        val, loc = self.image_processor.findImage(search_source, alt_template)
        print "Detailed Node match val: " + str(val)
        if val > 0.98:
            return loc
        return None


    def searchForNodeBar(self):
        """
        Searches the screen for a node health bar, returns if 
        the result meets the threshold
        """
        template_source = const.IMG_NODE_HEALTH
        alt_template = const.IMG_NODE_HEALTH_PARTIAL
        search_source = const.IMG_DEFAULT_SCREENSHOT_PATH
    #     image_processor.boundedScreenshot(100, 100, 600, 600, search_source)
        self.image_processor.screenshot(search_source)
        val, loc = self.image_processor.findImage(search_source, alt_template) 
        if val > 0.99:
            print val
            return loc
        #Not found
        return None
    
    
    def findCenteredNodeBar(self):
        """Returns the location of a detailed node bar if found"""
        template_source = const.IMG_NODE_HEALTH
        search_source = const.IMG_DEFAULT_SCREENSHOT_PATH
        x = self.image_processor.x_res / 4
        y = 0
        width = self.image_processor.x_res / 2
        height = self.image_processor.y_res / 2
        #     image_processor.boundedScreenshot(100, 100, 600, 600, search_source)
        self.image_processor.boundedScreenshot(x, y, width, height, search_source)
        val, loc = self.image_processor.findImage(search_source, template_source)
        print "Local Node val: " + str(val)
        if val > 0.98:
            return loc
        return None

################################
# Miscellaneous Helper Methods #
################################ 

    def isMounted(self):
        template_source = const.IMG_MOUNTED_BUFF
        search_source = const.IMG_DEFAULT_SCREENSHOT_PATH
        x = self.image_processor.x_res / 4
        y = (self.image_processor.y_res / 4) * 3
        width = x * 2
        height = self.image_processor.y_res / 4 - 30
    #     image_processor.boundedScreenshot(100, 100, 600, 600, search_source)
        self.image_processor.boundedScreenshot(x, y, width, height, search_source)
        val, loc = self.image_processor.findImage(search_source, template_source)
        #     image_processor.boundedScreenshot(100, 100, 600, 600, search_source)
#         self.image_processor.screenshot(search_source)
#         val, loc = self.image_processor.findImage(search_source, template_source)
        print "Mounted: " + str(val)
        if val > 0.98:
            return True
        return False
    
    def runJump(self, duration):
        """Weaves running and jumping to avoid environmental collision"""
        self.player.nonStopAction(const.FORWARD)
        total_time = 0
        while total_time < duration:
            win32api.Sleep(100)
            if total_time % 500 == 0:
                self.player.abilityKey(const.JUMP)
            total_time += 100
        self.player.stop()
    
    def strafeRunJump(self, duration):
        """Unintelligently avoid obstacles"""
        self.player.nonStopAction(const.FORWARD)
        total_time = 0
        while total_time < duration:
            win32api.Sleep(1000)           
            if total_time % 3000 == 0:
                self.player.stop()
                self.player.nonStopAction(const.FORWARD)
            elif total_time % 2000 == 0:
                self.player.stop()
                self.player.nonStopAction(const.FORWARD)
                self.player.nonStopAction(const.RIGHT_STRAFE)
            else:
                self.player.stop()
                self.player.nonStopAction(const.FORWARD)
                self.player.nonStopAction(const.LEFT_STRAFE)
            if total_time % 6000 == 0:
                self.player.abilityKey(const.JUMP)
            total_time += 1000
        self.player.stop()
    
    def mountRunTest(self, duration): 
        self.player.nonStopAction(const.FORWARD)
        total_time = 0
        while total_time < duration:
            win32api.Sleep(250) 
            case = total_time / 250 % 11
            if case is 2 or case is 3 or case is 4:# or case is 2 or case is 3:
                self.player.stop()
                self.player.nonStopAction(const.FORWARD)
                self.player.nonStopAction(const.LEFT_STRAFE)
            elif case is 6 or case is 7 or case is 8:# or case is 6 or case is 7:
                self.player.stop()
                self.player.nonStopAction(const.FORWARD)                
                self.player.nonStopAction(const.RIGHT_STRAFE)
            else:
                self.player.stop()
                self.player.nonStopAction(const.FORWARD)
                if total_time + 500 < duration:
                    self.player.abilityKey(const.JUMP)

            total_time += 250
        self.player.stop()
    
    def avoidanceRun(self, duration):
        if self.farm_mat == 'ice':
            self.player.nonStopAction(const.FORWARD)
            total_time = 0
            while total_time < duration:
                win32api.Sleep(250) 
                case = total_time / 250 % 11
                if case is 2 or case is 3 or case is 4:# or case is 2 or case is 3:
                    self.player.stop()
                    self.player.nonStopAction(const.FORWARD)
                    self.player.nonStopAction(const.LEFT_STRAFE)
                elif case is 6 or case is 7 or case is 8:# or case is 6 or case is 7:
                    self.player.stop()
                    self.player.nonStopAction(const.FORWARD)                
                    self.player.nonStopAction(const.RIGHT_STRAFE)
                else:
                    self.player.stop()
                    self.player.nonStopAction(const.FORWARD)
                    if total_time + 500 < duration:
                        self.player.abilityKey(const.JUMP)
    
                total_time += 250
            self.player.stop()
        elif self.farm_mat == 'wind':
            self.player.nonStopAction(const.FORWARD)
            total_time = 0
            while total_time < duration:
                win32api.Sleep(500)  
                case = total_time / 500 % 4         
                if case is 0 or case is 1:
                    self.player.stop()
                    self.player.nonStopAction(const.FORWARD)
                    if total_time + 500 < duration:
                        self.player.abilityKey(const.JUMP)
                elif case is 2:
                    self.player.stop()
                    self.player.nonStopAction(const.FORWARD)
                    self.player.nonStopAction(const.RIGHT_STRAFE)
                else:
                    self.player.stop()
                    self.player.nonStopAction(const.FORWARD)
                    self.player.nonStopAction(const.LEFT_STRAFE)
                total_time += 1000
            self.player.stop()
        else:
            self.mountRunTest(duration)
            
    
    def unstickCharacter(self):
        """
        Character is stuck?! WHAT DO? Spaz out.
        """
        self.player.backwardWalk(300)
        self.player.rightStrafe(700)
        self.player.forwardRun(1000)
    
    def sideApproach(self):
        self.player.backwardWalk(700)
        self.player.leftStrafe(900)
        self.player.forwardRun(1000)
        
    def circleObject(self):
        """
        Character is on the wrong side of an object, bring character around to 
        other side (at least try to)
        """
        self.unstickCharacter()
        self.player.rightStrafe(700)
        self.player.rightTurn(const.ROTATION_TIME / 2)


    def distanceFromCenterScreen(self, node_loc):
        """
        Returns the distance from the center of the screen
        """
        center_x = self.image_processor.x_res / 2
        print "node_loc: " + str(node_loc)
        return (node_loc[0] - center_x)

        
if __name__ == '__main__':
    const.IMG_GATHERING_TREE = 'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\Materials\\ice_shard.png'
    const.IMG_TEMPLATE_DIR = 'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\Oak\\'
    const.IMG_GATHERING_VEG = 'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\Materials\\ice_shard.png'
    win32api.Sleep(5000)
    bot = Botany('ice')
    
    mouse = bot.mouse  
    total_time = 0
#     bot.findNodesAtMinimapLevel()
    iterations = 0
    failures = 0
    while iterations < 1200 and failures < 5 :
        start = time.clock()
        success = bot.run()
        print "Iteration: " + str(iterations) + " : " + str(success)
        if success is False:
            failures += 1
        else:
            total_time += (time.clock() - start)
            print "Total for " + str(iterations) + " Iterations: " + str(total_time)
            iterations += 1
            failures = 0
        
        
    if bot.isMounted():
        bot.player.callMount()
#     
#     
#     if failures < 5:
#         const.IMG_GATHERING_TREE = 'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\Materials\\earth_shard.png'
#         const.IMG_TEMPLATE_DIR = 'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\Earth\\'
#         const.IMG_GATHERING_VEG = 'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\Materials\\earth_shard.png'
#         win32api.Sleep(10000)
#         bot.player.backwardWalk(2000)
#         bot.player.rightTurn(1000)
#         bot.player.forwardRun(3000)
#         iterations = 0
#         failures = 0
#         while iterations < 800 and failures < 5 : 
#             success = bot.run()
#             print "Round 2: Iteration: " + str(iterations) + " : " + str(success)
#             if success is False:
#                 failures += 1
#             else:
#                 iterations += 1
#                 failures = 0