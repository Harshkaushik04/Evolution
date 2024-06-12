import copy

from useful_functions import gene_to_unprocessed_data,unprocessed_data_to_processed_data,processed_data_to_brain,graph_visuals,genes_hexa_dict_generator,co_ordinates_initialize_dict,genes_to_brain,directions_dict_generator,sense_to_inputs_activations,update_activations,position_errors_resolve,change,back_to_normal,mutate,replicate,condition,check
from pygame_env import player,env,circle,playerencoder
from hashing_encoding_colors import encode_players_with_same_genes
import pygame
import json
# import logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
def main():
    player_size=4
    size_parameter=6
    num_neurons=[11,2,6] # [sensory_neurons,internal_neurons,output_neurons]
    env_width=600
    env_height=600
    population=300
    default_population=300
    steps_per_gen=120
    genome_length=12
    generations=500
    seed=0
    remaining_players_number=[]
    pygame.init()
    screen=pygame.display.set_mode((env_width,env_height),0,32)
    for generation in range(generations):
        if generation==0:
            genes_hexa_dict = genes_hexa_dict_generator(population, seed,genome_length)
            co_ordinates_dict,rect_co_ordinates_dict=co_ordinates_initialize_dict(env_width,env_height,population,size_parameter)
            #print(f'co_ordinates_dict:{co_ordinates_dict}')
            directions_dict=directions_dict_generator(population)
            colors_dict=encode_players_with_same_genes(genes_hexa_dict)
            activation_inputs_dict={}
            players_dict={}
            for i in range(num_neurons[0]): #for unused brain input activations
                activation_inputs_dict['S' + str(i)] = 0.0
            for i in range(population):
                flag = False
                # if i==10:
                #     flag=True
                genes_hexa_list=genes_hexa_dict['player'+str(i)]
                #print('genes_hexa_list:',genes_hexa_list)
                unused_brain=genes_to_brain(genes_hexa_list,activation_inputs_dict,num_neurons,show_graph=flag)
                # if i==10:
                #     genes_list=unused_brain.genes_list
                #     graph_visuals(unused_brain.genes_list)
                #print('unused_brain.genes_list:',unused_brain.genes_list)
                co_ordinates_list=co_ordinates_dict['player'+str(i)]
                rect_co_ordinates_list=rect_co_ordinates_dict['player'+str(i)]
                direction=directions_dict['player'+str(i)]
                color=colors_dict['player'+str(i)]
                pygame_object=circle(co_ordinates_list,color,radius=player_size//2)
                players_dict['player'+str(i)]=player(co_ordinates_list,unused_brain.genes_list,unused_brain,pygame_object,direction,[co_ordinates_list],rect_co_ordinates_list)
                #print('players_dict[player+str(i)].brain.genes_list:',players_dict['player'+str(i)].brain.genes_list)
        for step in range(steps_per_gen):
            print("step:",step)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
            screen.fill((255, 255, 255))
            for i in range(population):
                players_dict['player' + str(i)].pygame_object.draw(screen)
            # pygame.image.save(screen,rf'D:\Evolution\pygame_images_testing\images\image.png')
            pygame.display.flip()
            combined_activation_inputs_dict=sense_to_inputs_activations(screen,players_dict,step,steps_per_gen,size_parameter,seed=0)
            players_dict,stored_neurons_dict,stored_incoming_exhausted_dict=update_activations(players_dict,combined_activation_inputs_dict)
            players_dict=change(players_dict, screen, size_parameter, kill_neuron=False)
            players_dict=back_to_normal(players_dict,stored_neurons_dict,stored_incoming_exhausted_dict)
            pygame.image.save(screen, rf'D:\New_Evolution_16_genome_length_images\generation{generation+1}\image{step+generation*steps_per_gen+1}.png')
        players_dict,remaining_players_list=condition(players_dict,screen,inp=2)
        remaining_players_number.append(len(remaining_players_list))
        dicti = {}
        for i in range(len(remaining_players_list)):
            dicti[f'player{i}_genes_list'] = players_dict[remaining_players_list[i]].genes_list
        players_json = json.dumps(dicti, cls=playerencoder)
        with open('another_testing_file.py', 'w') as f:
            f.write('players_genes_list=' + players_json)
            f.write('\n')
            f.write('remaining_players_number=[')
            for i in range(len(remaining_players_number)):
                f.write(str(remaining_players_number[i])+',')
            f.write(']')
        players_dict,num_mutations=mutate(players_dict,num_neurons,remaining_players_list,mutation_prob=0.002)
        print('num_mutations:',num_mutations)
        print('num_players_after_mutation:',len(players_dict))
        players_dict,population=replicate(players_dict,env_width,env_height,size_parameter,remaining_players_list,player_size,default_population=default_population)
        print('num_players_after_replication:',default_population,' or ',len(players_dict))
    return players_dict,remaining_players_number

players_dict=main()
players_dict_copy=players_dict
print(players_dict_copy)
# def test():
#     genes_hexa_list = [
#         '3E2F1A4B', '7B9C0D8E', '5F4A7C1D', 'E9F8BBA6', '2C3D1E0F', '8A7B9C6D', '4F3E2D1C', '4B1A2C3D',
#         'D9E8F7A6', 'B7C6D5E4', '1A2B3C4D', '5E4F6A7B', '3C2D1E0F', '8B7A9C6D', '4D3E2F1C', '0E1F2C3D',
#         'F9E8D7C6', 'A7B6C5D4', '2B3A1C4D', '6F5E7A8B', '3D2C190F', '9B8A7C6D', '5C4D2F1E', '0D1E3C4F',
#         'E8F7D6C5', 'B6A5C4D3', '1B2A3D4C', '4E5F6A7B', '3A2B1E0D', '7B8C9D6E', '5D4E2F1C', '0C1D3A4E'
#     ]
#
#
#     activation_inputs_dict={'S0':0.1,
#                             'S1':0.3,
#                             'S2':0.8,
#                             'S3':0.5,
#                             'S4':0.9,
#                             'S5':1,
#                             'S6':0.4,
#                             'S7':0,
#                             'S8': 0.1,
#                             'S9': 0.3,
#                             'S10': 0.8,
#                             'S11': 0.5,
#                             'S12': 0.9,
#                             'S13': 1
#                             }
#     brain=genes_to_brain(genes_hexa_list,activation_inputs_dict,[14,4,9])
#     for edge in brain.edge_list:
#         print(f'{edge}:{brain.neurons_dict[edge].activation}')
#     print("==========================================")
#test()

# for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         game_over = True
            #     screen.fill((255, 255, 255))
            #     for i in range(population):
            #         players_dict['player' + str(i)].pygame_object.draw(screen)
            #     # pygame.image.save(screen,rf'D:\Evolution\pygame_images_testing\images\image.png')
            #     pygame.display.flip()

    # game_over = False
    # while not game_over:
    #     for event in pygame.event.get():
    #         if event.type==pygame.QUIT:
    #             game_over=True
    #         screen.fill((255,255,255))
    #         for i in range(population):
    #             players_dict['player' + str(i)].pygame_object.draw(screen)
    #         #pygame.image.save(screen,rf'D:\Evolution\pygame_images_testing\images\image.png')
    #         pygame.display.flip()