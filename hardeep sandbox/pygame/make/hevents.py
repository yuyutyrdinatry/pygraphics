import pygame

#===============================================================================
# EVENT Constants
#===============================================================================
H_EVENT_MOUSE_DOWN = pygame.MOUSEBUTTONDOWN
H_EVENT_MOUSE_MOVE = pygame.MOUSEMOTION
H_EVENT_FRAME_UPDATE = -1
H_EVENT_INIT_PHYSICS = -2
#    QUIT         none
#    ACTIVEEVENT         gain, state
#    KEYDOWN         unicode, key, mod
#    KEYUP         key, mod
#    MOUSEMOTION         pos, rel, buttons
#    MOUSEBUTTONUP    pos, button
#    MOUSEBUTTONDOWN  pos, button
#    JOYAXISMOTION    joy, axis, value
#    JOYBALLMOTION    joy, ball, rel
#    JOYHATMOTION     joy, hat, value
#    JOYBUTTONUP      joy, button
#    JOYBUTTONDOWN    joy, button
#    VIDEORESIZE      size, w, h
#    VIDEOEXPOSE      none
#    USEREVENT        code