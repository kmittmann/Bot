import ffxiv.game.Minimap as minimap
import util.Constants as const
import util.Keyboard as keyboard
import util.Mouse as mouse
import util.ImageProcessor as imaging

import win32api, win32con
import time

class Player(object):
     
    def __init__(self):
        '''constructor'''
        self.minimap = minimap.Minimap()
        self.keyboard = keyboard.Keyboard()
        self.image_processor = imaging.ImageProcessor()
        self.mouse = mouse.Mouse()
        self.cameraReset()
#        self.speed = self.__determineLinearSpeed()
        
    def abilityType(self, ability_str):
        self.keyboard.press(const.CHAT_BOX)
        self.keyboard.write(ability_str)
        self.keyboard.press(const.CHAT_BOX)
    
    def abilityKey(self, ability_key):
        self.keyboard.press(ability_key)
    
    def forwardRun(self, duration):
        """Run (default) character forward for duration milliseconds"""
        self.keyboard.pressAndHold(const.FORWARD)
        win32api.Sleep(duration)
        self.keyboard.release(const.FORWARD)

    def forwardWalk(self, duration):
        """Walk character forward for duration milliseconds"""
        self.keyboard.press(const.RUN_WALK)
        win32api.Sleep(100)
        self.keyboard.pressAndHold(const.FORWARD)
        win32api.Sleep(duration)
        self.keyboard.release(const.FORWARD)
        self.keyboard.press(const.RUN_WALK)
        
    def forwardSprint(self, duration):
        """Sprint character forward for duration milliseconds"""
        self.ability(const.ABILITY_SPRINT)
        win32api.Sleep(100)
        self.keyboard.pressAndHold(const.FORWARD)
        win32api.Sleep(duration)
        self.keyboard.release(const.FORWARD)
    
    def forwardLeftStrafe(self, duration):
        self.keyboard.pressAndHold(const.FORWARD)
        self.keyboard.pressAndHold(const.LEFT_STRAFE)
        win32api.Sleep(duration)
        self.keyboard.release(const.FORWARD)
        self.keyboard.pressAndHold(const.LEFT_STRAFE)
    
    def forwardRightStrafe(self, duration):
        self.keyboard.pressAndHold(const.FORWARD)
        self.keyboard.pressAndHold(const.RIGHT_STRAFE)
        win32api.Sleep(duration)
        self.keyboard.release(const.FORWARD)
        self.keyboard.pressAndHold(const.RIGHT_STRAFE)
    
    def callMount(self):
        """Calls Mount (Chocobo)"""
        self.abilityKey(const.ABILITY_CALL_MOUNT)
        win32api.Sleep(1000)
        
    def backwardWalk(self, duration):
        """Walk character backward for duration milliseconds"""
        self.keyboard.pressAndHold(const.BACKWARD)
        win32api.Sleep(duration)
        self.keyboard.release(const.BACKWARD)
    
    def leftTurn(self, duration):
        """Turn character left for duration milliseconds"""
        self.keyboard.pressAndHold(const.LEFT_TURN)
        win32api.Sleep(duration)
        self.keyboard.release(const.LEFT_TURN)
    
    def leftStrafe(self, duration):
        """Strafe Character left for duration milliseconds"""
        self.keyboard.pressAndHold(const.LEFT_STRAFE)
        win32api.Sleep(duration)
        self.keyboard.release(const.LEFT_STRAFE)
    
    def rightTurn(self, duration):
        """Turn character right for duration milliseconds"""
        self.keyboard.pressAndHold(const.RIGHT_TURN)
        win32api.Sleep(duration)
        self.keyboard.release(const.RIGHT_TURN)
    
    def rightStrafe(self, duration):
        """Strafe character right for duration milliseconds"""
        self.keyboard.pressAndHold(const.RIGHT_STRAFE)
        win32api.Sleep(duration)
        self.keyboard.release(const.RIGHT_STRAFE)
    
    def targetNearestNPC(self):
        """
        Targets nearest Non-Player-Character
        Includes Nodes, does not target enemies
        """
        self.abilityKey(const.TARGET_NPC)
    
    def faceTarget(self):
        """Positions character to face target"""
        #Note: can be paired with forward movement to direct camera towards 
        #target.
        self.abilityKey(const.FACE_TARGET)
    
    def lockOnTarget(self):
        self.abilityKey(const.LOCK_ON)
        
    def confirm(self):
        self.abilityKey(const.CONFIRM)
        
    def cancel(self):
        self.abilityKey(const.CANCEL)
    
    def cameraFirstPerson(self):
        """Toggle First Person"""
        self.keyboard.press(const.CAM_FIRST_PERSON)
        win32api.Sleep(700)
    
    def cameraReset(self):
        """Resets the camera to forward, third person"""
        self.keyboard.press(const.CAM_RESET)
    
    def cameraHoldReverse(self):
        """Reverse camera, call stop after"""
        self.keyboard.pressAndHold(const.CAM_REVERSE)
        
    def cameraTopDown(self):
        """Shift the camera to face downward"""
        self.keyboard.pressAndHold(const.CAM_UP)
        win32api.Sleep(1000)
        self.keyboard.release(const.CAM_UP)
        
    def cameraZoomIn(self, steps):
        """Zooms the camera in x steps (mouse wheel clicks)"""
        self.mouse.wheelUp(steps)
        
    def cameraZoomOut(self, steps):
        """Zooms the camera out x steps (mouse wheel clicks)"""
        self.mouse.wheelDown(steps)      
        
    def nonStopAction(self, action):
        """Perform action until stop method is manually called."""
        self.keyboard.pressAndHold(action)
   
    def stop(self):
        """Halt any actions"""
        self.keyboard.release(const.LEFT_TURN )
        self.keyboard.release(const.FORWARD)
        self.keyboard.release(const.RIGHT_TURN)
        self.keyboard.release(const.BACKWARD)
        self.keyboard.release(const.LEFT_STRAFE)
        self.keyboard.release(const.RIGHT_STRAFE)
        self.keyboard.release(const.CAM_REVERSE)
        
    def stopRun(self):
        self.keyboard.release(const.FORWARD)

 ###
#Implied Private Methods (Use at your own risk)
###          

    def _cameraDrag(self, x, y): 
        """
        Drag camera to point character to another point on the screen,
        making that point the new center.
        """ 
        x_dist, y_dist = self.distanceFromCenterScreen(x, y)
        x_center = self.image_processor.x_res / 2
        y_center = self.image_processor.y_res / 2
        
        print x_center
        print y_center
        print x_dist
        print y_dist
        self.mouse.clickAndDrag(x_center, y_center, 
                                x_dist, y_dist, 
                                'right', True)  

    def _determineRotationalSpeed(self):               
        '''
        Take a screencap of a small portion of the unlocked map, rotate
        the character until that portion of the screen matches a high threshold
        and record timing. 
        
        NOTE: Values in util.Constants class.  Should not need repeating. 
        '''
        self.minimap.minimapZoomIn(6)
        
        ip = imaging.ImageProcessor()
        test_x = self.minimap.x_char_pos - 15
        test_y = self.minimap.y_char_pos - 15
        ip.boundedScreenshot(test_x, test_y, 15, 15, const.IMG_DEFAULT_SCREENSHOT_PATH)
        
        best_times = []  
        rotation_time = 0
        
        start = time.clock()   
        self.keyboard.pressAndHold(const.RIGHT_TURN)
        current_val = 0 
        while rotation_time < 30:
            ip.boundedScreenshot(test_x, test_y, 15, 15, const.IMG_ALT_SCREENSHOT_PATH)
            current_val, loc = ip.findImage(const.IMG_DEFAULT_SCREENSHOT_PATH, const.IMG_ALT_SCREENSHOT_PATH)
            rotation_time = time.clock() - start
            if current_val > 0.9899 and rotation_time > 0.5:
                print current_val
                print rotation_time
                best_times.append((rotation_time, current_val))
        self.keyboard.release(const.RIGHT_TURN)
        print best_times
 
    def _determineLinearSpeed(self):
        '''
        Obtain location of node directly infront of user, move forward and 
        obtain new location. 
        Obtain distance traveled in pixels over time duration. 
        
        Most zoomed in minimap distance is checked first, then second most zoomed
        in is checked to determine scaling value. 
        
        NOTE: Values in util.Constants class. 
        Should not need repeating. If needed, manually align character 
        with closest node being in front. 
        '''
        self.minimap.minimapZoomOut(6)
        node_loc = self.minimap.findImageOnMinimap(const.IMG_GATHERING_NODE)
        node_loc_light = self.minimap.findImageOnMinimap(const.IMG_GATHERING_NODE_LIGHT)
        found_nodes = node_loc + node_loc_light
        #Iterate through found nodes finding node with shortest distance on minimap
        print found_nodes
        closest_node = found_nodes[0]
        closest_dist = self.minimap.minimapDistanceFromCharacter(closest_node[0], closest_node[1])
        for i in range(1, len(found_nodes)):
            curr_node = found_nodes[i]
            curr_dist = self.minimap.minimapDistanceFromCharacter(curr_node[0], curr_node[1])
            if curr_dist < closest_dist:
                closest_dist = curr_dist
                closest_node = curr_node
        
        print closest_node
        self.forwardRun(12000)
        node_loc = self.minimap.findImageOnMinimap(const.IMG_GATHERING_NODE)
        node_loc_light = self.minimap.findImageOnMinimap(const.IMG_GATHERING_NODE_LIGHT)
        found_nodes = node_loc + node_loc_light
        #Iterate through found nodes finding node with shortest distance on minimap
        print found_nodes
        closest_node = found_nodes[0]
        closest_dist = self.minimap.minimapDistanceFromCharacter(closest_node[0], closest_node[1])
        for i in range(1, len(found_nodes)):
            curr_node = found_nodes[i]
            curr_dist = self.minimap.minimapDistanceFromCharacter(curr_node[0], curr_node[1])
            if curr_dist < closest_dist:
                closest_dist = curr_dist
                closest_node = curr_node
        
        print closest_node       
   
if __name__ == '__main__':
    win32api.Sleep(5000)
    player = Player()
    win32api.Sleep(1000)
    player.forwardRun(2000)
#     player.rightStrafe(500)
#     player.forwardRun(4200)
#     player.leftTurn(650)
#     player.nonStopAction(const.FORWARD)
#     win32api.Sleep(2000)
#     player.abilityKey(const.JUMP)
#     win32api.Sleep(1000)
#     player.abilityKey(const.JUMP)
#     win32api.Sleep(1000)
#     player.abilityKey(const.JUMP)
#     win32api.Sleep(1000)
#     player.stop()