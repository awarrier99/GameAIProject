import pygame

class Player:

    feet_walk = [pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_0.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_1.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_2.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_3.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_4.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_5.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_6.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_7.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_8.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_9.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_10.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_11.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_12.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_13.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_14.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_15.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_16.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_17.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_18.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_19.png')]
    rifle_walk = [pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_0.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_1.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_2.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_3.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_4.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_5.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_6.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_7.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_8.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_9.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_10.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_11.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_12.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_13.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_14.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_15.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_16.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_17.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_18.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_19.png'),]


    def __init__(self, location):
        #  init
        self.location = location
        self.direction = 0  # degrees: 0º is facing up
        self.health = 100


    def shoot(self, direction):
        pass
        #  shoot bullet






