import pygame
import copy
import json

class player:
    def __init__(self,co_ordinates_list,genes_list,brain,pygame_object,direction,co_ordinates_history_list,rect_co_ordinates_list):
        self.co_ordinates_list=co_ordinates_list
        self.genes_list=genes_list
        self.brain=brain
        self.pygame_object=pygame_object
        self.direction=direction
        self.co_ordinates_history_list=co_ordinates_history_list
        self.rect_co_ordinates_list=rect_co_ordinates_list
    def __deepcopy__(self):
        new_copy = self.__class__(
            copy.deepcopy(self.co_ordinates_list),
            copy.deepcopy(self.genes_list),
            copy.deepcopy(self.brain),
            copy.deepcopy(self.pygame_object),
            copy.deepcopy(self.direction),
            copy.deepcopy(self.co_ordinates_history_list),
            copy.deepcopy(self.rect_co_ordinates_list),
        )
        return new_copy
    def to_dict(self):
        di={"co_ordinates_list":self.co_ordinates_list,
            "genes_list":self.genes_list,
            "brain":self.brain,
            "pygame_object":self.pygame_object,
            "direction":self.direction,
            "co_ordinates_history_list":self.co_ordinates_history_list,
            "rect_co_ordinates_list":self.rect_co_ordinates_list}
        return di

class playerencoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, player):
            return obj.to_dict()
        return super().default(obj)
class env:
    def __init__(self,pygame_screen,players_dict,pheremones_list):
        self.pygame_screen=pygame_screen
        self.players_dict=players_dict
        self.pheremones_list=pheremones_list
    def update(self,activation_inputs_dict):
        return


class circle:
    def __init__(self,co_ordinates_list,color,radius=5):
        self.co_ordinates_list=co_ordinates_list
        self.radius=radius
        self.color=color
    def draw(self, screen):
        rect = pygame.Rect(0, 0, 2*self.radius, 2*self.radius)
        rect.center = (self.co_ordinates_list[0],self.co_ordinates_list[1])
        pygame.draw.rect(screen, self.color, rect)
        #pygame.draw.circle(screen, self.color, (self.co_ordinates_list[0], self.co_ordinates_list[1]), self.radius)
    def update_position_and_radius(self, dx, dy, dr=0):
        self.co_ordinates_list[0]+=dx
        self.co_ordinates_list[1]+=dy
        self.radius+=dr


players_num=1000
# new_player=player([1,2,3],[5,6,7],1,5,6,7,8)
# extremely_new_player=new_player.__deepcopy__()
# print(extremely_new_player.brain)
players_dict={}
#for i in range(players_num):
#players_dict[f'player{i}']=

