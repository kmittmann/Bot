
'''
Created on Sep 25, 2013

@author: Karl
'''

LATENCY_BUFFER =        200  #Account for latency when starting movement
ROTATION_TIME =         2660 #2.667 Seconds for full rotation
MINIMAP_PIX_WALK =      5    #11 Minimap Pixels traveled over 2 seconds at max Zoom 
MINIMAP_PIX_RUN =       13   #27 Minimap Pixels traveled over 2 seconds at max Zoom. (3.5 at min Zoom)
MINIMAP_PIX_MOUNT =     20   #40 Minimp Pixels traveled over 2 seconds at max Zoom
MINIMAP_PIX_SCALE =     0.90 #Each level on the minimap is 85% of next level

###IMAGES
IMG_TEMPLATE_DIR =              'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\Walnut\\'
#Default location for screenshot captures
IMG_DEFAULT_SCREENSHOT_PATH =   'E:\\Users\\Karl\\Documents\\workspace\\Bot\\ffxiv\\images\\test.png'
IMG_ALT_SCREENSHOT_PATH =       'E:\\Users\\Karl\\Documents\\workspace\\Bot\\ffxiv\\images\\test2.png'
IMG_FATE =                      'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\fate.png'
IMG_GATHERING_NODE_FATE =       'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\fate_node.png'
IMG_GATHERING_NODE_FATE_LIGHT = 'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\fate_node_light.png'
IMG_GATHERING_NODE_BROWN =      'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\botany_node_brown.png'
IMG_GATHERING_NODE =            'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\botany_node.png'
IMG_GATHERING_NODE_LIGHT =      'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\botany_node_light.png'
IMG_GATHERING_MENU =            'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\gathering_menu.png'
IMG_GATHERING_TREE =            'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\Materials\\oak.png'
IMG_GATHERING_VEG =             'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\Materials\\wildfowl_feather.png' 
IMG_NODE_HEALTH_FULL_DETAIL =   'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\full_detail_node_health.png'
IMG_NODE_HEALTH =               'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\node_health.png'
IMG_NODE_HEALTH_PARTIAL =       'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\node_health_partial.png'
IMG_MINIMAP =                   'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\minimap.png'  
IMG_MINIMAP_CHARACTER =         'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\minimap_character.png' 
IMG_MINIMAP_LOCK =              'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\minimap_lock.png'       
IMG_MINIMAP_ZOOM_IN =           'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\minimap_zoom_in.png'
IMG_MINIMAP_ZOOM_OUT =          'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\minimap_zoom_out.png'
IMG_MOUNTED_BUFF =              'E:\\Users\\Karl\\Pictures\\FFXIV_Script_Images\\mount_active.png'

###CONTROLS###
###MOVEMENT
LEFT_TURN =     'a'
RIGHT_TURN =    'd'
FORWARD =       'w'
BACKWARD =      's'
LEFT_STRAFE =   'q'
RIGHT_STRAFE =  'e'
JUMP =          'spacebar'
RUN_WALK =      'divide_key'
FACE_TARGET =   'f'
TARGET_NPC =    'F12'
LOCK_ON =       'numpad_5'
CONFIRM =       'numpad_0'
CANCEL =        'decimal_key'
RETURN =        'r'
###GENERAL INTERFACE
CAM_RESET =         'end'
CAM_FIRST_PERSON =  'home'
CAM_REVERSE =       'v'
CAM_UP =     'down_arrow'

MAP_OPEN =          'm'
CHAT_BOX = 'enter'

#LOGS
LOG_GATHERING =         'b'
LOG_CRAFTING =          'n'

#ABILITIES
ABILITY_CALL_MOUNT =    '9'
ABILITY_ARBOR_CALL =    '7'
ABILITY_SPRINT=         '0'
ABILITY_LEAF_TURN  =    '6'
ABILITY_LEAF_TURN_II =  '/ac Leaf Turn II <me>'
ABILITY_STEALTH =       '/ac Stealth <me>'
ABILITY_STEALTH_BOUND = '5'
ABILITY_MENPHINAS_WARD ='8'
ABILITY_FIELD_MASTERY_II = '3'
###CARPENTRY
ABILITY_BASIC_SYNTH =    '/ac "Basic Synth" <me>'
ABILITY_STANDARD_SYNTH = '/ac "Standard Synth" <me>'
ABILITY_BASIC_TOUCH =    '/ac "Basic Touch" <me>'
ABILITY_STANDARD_TOUCH = '/ac "Standard Synth" <me>'
ABILITY_GREAT_STRIDES =  '/ac "Great Strides" <me>'
ABILITY_STEADY_HAND =    '/ac "Steady Hand" <me>'