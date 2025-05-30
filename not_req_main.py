import copy

from useful_functions import gene_to_unprocessed_data,unprocessed_data_to_processed_data,processed_data_to_brain,graph_visuals,genes_hexa_dict_generator,co_ordinates_initialize_dict,genes_to_brain,directions_dict_generator,sense_to_inputs_activations,update_activations,position_errors_resolve,change,back_to_normal,mutate,replicate,condition,check,genes_hexa_list_to_genes_list,restart_simulation
from pygame_env import player,env,circle,playerencoder
from hashing_encoding_colors import encode_players_with_same_genes
import pygame
import json
import os
# import logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


PLAYER_DATA_SAVE_PATH='Saves/new_req.py'
IMAGES_SAVE_PATH='Simulations/not_req'
def main():
    size_parameter=5
    num_neurons=[11,2,6] # [sensory_neurons,internal_neurons,output_neurons]
    env_width=250
    env_height=250
    population=30
    default_population=30
    steps_per_gen=40
    genome_length=10
    generations=1000
    seed=0
    remaining_players_number=[]
    pygame.init()
    screen=pygame.display.set_mode((env_width,env_height),0,32)
    max_genes_list_combined=[]
    for generation in range(generations):
        if generation==0:
            genes_hexa_dict = genes_hexa_dict_generator(population, seed,genome_length)
            co_ordinates_dict,rect_co_ordinates_dict=co_ordinates_initialize_dict(env_width,env_height,population,size_parameter)
            #print(f'co_ordinates_dict:{co_ordinates_dict}')
            directions_dict=directions_dict_generator(population)
            colors_dict,max_gene,max_value=encode_players_with_same_genes(genes_hexa_dict)
            max_genes_list_combined.append(copy.deepcopy(max_gene))
            activation_inputs_dict={}
            players_dict={}
            for i in range(num_neurons[0]): #for unused brain input activations
                activation_inputs_dict['S' + str(i)] = 0.0
            for i in range(population):
                flag = False
                # if i==10:
                #     flag=True
                genes_hexa_list=genes_hexa_dict['player'+str(
                    i)]
                #print('genes_hexa_list:',genes_hexa_list)
                unused_brain=genes_to_brain(genes_hexa_list,activation_inputs_dict,num_neurons,show_graph=flag)
                # if i==10:
                #     genes_list=unused_brain.genes_list
                #     graph_visuals(unused_brain.genes_list)
                #print('unused_brain.genes_list:',unused_brain.genes_list)
                co_ordinates_list=co_ordinates_dict['player'+str(i)]
                rect_co_ordinates_list=rect_co_ordinates_dict['player'+str(i)]
                #print(rect_co_ordinates_list)
                direction=directions_dict['player'+str(i)]
                color=colors_dict['player'+str(i)]
                pygame_object=circle(co_ordinates_list,color,radius=size_parameter//2)
                co_ordinates_history_list=[copy.deepcopy(co_ordinates_list)]
                players_dict['player'+str(i)]=player(co_ordinates_list,unused_brain.genes_list,unused_brain,pygame_object,direction,co_ordinates_history_list,rect_co_ordinates_list)
                #print(players_dict['player'+str(i)].rect_co_ordinates_list)
                #print('players_dict[player+str(i)].brain.genes_list:',players_dict['player'+str(i)].brain.genes_list)
        for step in range(steps_per_gen):
            print('generation:',generation,' step:',step)
            # for i in range(len(list(players_dict.keys()))):
                # if step%2==0:
                #     print(f'player{i} co_ordinates history::',players_dict['player'+str(i)].co_ordinates_history_list)
                #     print(f'player{i} rect co ordinates:', players_dict['player' + str(i)].co_ordinates_history_list)
            print("step:",step)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
            screen.fill((255, 255, 255))
            print("this:",len(players_dict.keys()))
            for i in range(population):
                players_dict['player' + str(i)].pygame_object.draw(screen)
            # pygame.image.save(screen,rf'D:\Evolution\pygame_images_testing\images\image.png')
            pygame.display.flip()
            combined_activation_inputs_dict=sense_to_inputs_activations(screen,players_dict,step,steps_per_gen,size_parameter,seed=0)
            players_dict,stored_neurons_dict,stored_incoming_exhausted_dict=update_activations(players_dict,combined_activation_inputs_dict)
            players_dict=change(players_dict, screen, size_parameter, kill_neuron=False)
            players_dict=back_to_normal(players_dict,stored_neurons_dict,stored_incoming_exhausted_dict)
            pygame.image.save(screen, os.path.join(IMAGES_SAVE_PATH,rf'generation{generation+1}/image{step+generation*steps_per_gen+1}.png'))
        players_dict,remaining_players_list=condition(players_dict,screen,inp=2)
        remaining_players_number.append(len(remaining_players_list))
        dicti = {}
        another_dicti={}
        for i in range(len(remaining_players_list)):
            dicti[f'player{i}_genes_list'] = players_dict[remaining_players_list[i]].genes_list
            another_dicti[f'player{i}_genes_hexa_list']=players_dict[remaining_players_list[i]].brain.genes_hexa_list
        players_json = json.dumps(dicti)
        players_another_json=json.dumps(another_dicti)
        list_json=json.dumps(remaining_players_number)
        max_gene_json=json.dumps(max_gene)
        max_genes_list_combined_json=json.dumps(max_genes_list_combined)
        with open(PLAYER_DATA_SAVE_PATH, 'w') as f:
            f.write('players_genes_list=' + players_json)
            f.write('\n')
            f.write('players_genes_hexa_list='+players_another_json)
            f.write('\n')
            f.write('remaining_players_number='+list_json)
            f.write('\n')
            f.write('num_neurons=[11,2,6]')
            f.write('\n')
            f.write('max_genes_list_combined='+max_genes_list_combined_json)
            f.write('\n')
            f.write('max_gene='+max_gene_json)
            f.write('\n')
            f.write('max_number_of_same_genes='+str(max_value))
            f.write('\n')
            f.write('from useful_functions import graph_visuals,genes_hexa_list_to_genes_list')
            f.write('\n')
            f.write('max_genes_list=genes_hexa_list_to_genes_list(max_gene,num_neurons)')
            f.write('\n')
            f.write('graph_visuals(max_genes_list)')
        players_dict,num_mutations=mutate(players_dict,num_neurons,remaining_players_list,mutation_prob=0.008)
        print('num_mutations:',num_mutations)
        print('num_players_after_mutation:',len(players_dict))
        players_dict,population,max_gene,max_value=replicate(players_dict,env_width,env_height,size_parameter,remaining_players_list,default_population=default_population)
        max_genes_list_combined.append(copy.deepcopy(max_gene))
        print('num_players_after_replication:',default_population,' or ',len(players_dict))
    return players_dict,remaining_players_number

players_dict,remaining_players_number=main()
players_dict_copy=players_dict
print(players_dict_copy)

# players_genes_hexa_list={"player0_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player1_genes_hexa_list": ["9137fb1a", "671f44d3", "9a48d87a", "e2566ed5", "37cdd3d3", "4b2639ca", "af93cdd3", "4fa616f4", "bf9884ae", "83b75d86", "74824669", "ca45cea7"], "player2_genes_hexa_list": ["e9ad32c7", "6cb325ae", "a7fdce21", "b9df89c9", "c93cfed5", "2ee71112", "d687571f", "649e946c", "6779e4c9", "4967815e", "f7d52eb2", "bb3ef296"], "player3_genes_hexa_list": ["e9ad32c7", "6cb325ae", "a7fdce21", "b9df89c9", "c93cfed5", "2ee71112", "d687571f", "649e946c", "6779e4c9", "4967815e", "f7d52eb2", "bb3ef296"], "player4_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player5_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player6_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player7_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player8_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player9_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player10_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player11_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player12_genes_hexa_list": ["73531932", "34f1f32f", "dbbc42c6", "9f83aef3", "d661481f", "2d2c5d37", "5c1d5444", "da6cc372", "dd7e21c3", "67dfecb9", "eaa1ecdc", "9983378c"], "player13_genes_hexa_list": ["73531932", "34f1f32f", "dbbc42c6", "9f83aef3", "d661481f", "2d2c5d37", "5c1d5444", "da6cc372", "dd7e21c3", "67dfecb9", "eaa1ecdc", "9983378c"], "player14_genes_hexa_list": ["73531932", "34f1f32f", "dbbc42c6", "9f83aef3", "d661481f", "2d2c5d37", "5c1d5444", "da6cc372", "dd7e21c3", "67dfecb9", "eaa1ecdc", "9983378c"], "player15_genes_hexa_list": ["73531932", "34f1f32f", "dbbc42c6", "9f83aef3", "d661481f", "2d2c5d37", "5c1d5444", "da6cc372", "dd7e21c3", "67dfecb9", "eaa1ecdc", "9983378c"], "player16_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player17_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player18_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player19_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player20_genes_hexa_list": ["e9ad32c7", "6cc325ae", "a7fdce21", "b9df89c9", "c93cfed5", "2ee71112", "d687571f", "649e946c", "6779e4c9", "4967815e", "f7d52eb2", "bb3ef296"], "player21_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player22_genes_hexa_list": ["4e115536", "4f541dae", "5ed4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player23_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d", "77e3bb42", "4ebb7244", "3f4ec3e2", "aa57ceb8", "f659fe26", "731cf4fc"], "player24_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player25_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player26_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab4ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player27_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player28_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player29_genes_hexa_list": ["e9ad32c7", "6cc325ae", "a7fdce21", "b9df89c9", "c93cfed5", "2ee71112", "d687571f", "649e946c", "6779e4c9", "4967815e", "f7d52eb2", "bb3ef296"], "player30_genes_hexa_list": ["e9ad32c7", "6cc325ae", "a7fdce21", "b9df89c9", "c93cfed5", "2ee71112", "d687571f", "649e946c", "6779e4c9", "4967815e", "f7d52eb2", "bb3ef296"], "player31_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player32_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player33_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player34_genes_hexa_list": ["54eeb994", "ceb87dd4", "f155bbfa", "67e4524e", "daffdea6", "96863e9d", "91ac5124", "ad1b3eaf", "598caafa", "ac1ebe81", "d9e24c2a", "478f9ea8"], "player35_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player36_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player37_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player38_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player39_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player40_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player41_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d", "77e3bb42", "4ebb7244", "3f4ec3e2", "aa57ceb8", "f659fe26", "731cf4fc"], "player42_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player43_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player44_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player45_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player46_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player47_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player48_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player49_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player50_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player51_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player52_genes_hexa_list": ["e9ad32c7", "6cc325ae", "a7fdce21", "b9df89c9", "c93cfed5", "2ee71112", "d687571f", "649e946c", "6779e4c9", "4967815e", "f7d52eb2", "bb3ef296"], "player53_genes_hexa_list": ["e9ad32c7", "6cc325ae", "a7fdce21", "b9df89c9", "c93cfed5", "2ee71112", "d687571f", "649e946c", "6779e4c9", "4967815e", "f7d52eb2", "bb3ef296"], "player54_genes_hexa_list": ["e9ad32c7", "6cc325ae", "a7fdce21", "b9df89c9", "c93cfed5", "2ee71412", "d687571f", "649e946c", "6779e4c9", "4967815e", "f7d52eb2", "bb3ef296"], "player55_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d", "77e3bb42", "4ebb7244", "3f4ec3e2", "aa57ceb8", "f659fe26", "731cf4fc"], "player56_genes_hexa_list": ["e9ad32c7", "6cc325ae", "a7fdce21", "b9df84c9", "c93cfed5", "2ee71112", "d687571f", "649e946c", "6779e4c9", "4967815e", "f7d52eb2", "bb3ef296"], "player57_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player58_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player59_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player60_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player61_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player62_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player63_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player64_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player65_genes_hexa_list": ["54eeb994", "ceb87dd4", "f155bbfa", "67e4524e", "daffdea6", "96863e9d", "91ac5124", "ad1b3eaf", "598caafa", "ac1ebe81", "d9e24c2a", "478f9ea8"], "player66_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player67_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player68_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player69_genes_hexa_list": ["e9ad32c7", "6cc325ae", "a7fdce21", "b9df89c9", "c93cfed5", "2ee71112", "d687571f", "649e946c", "6779e4c9", "4967815e", "f7d52eb2", "bb3ef296"], "player70_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player71_genes_hexa_list": ["e9ad32c7", "6cc325ae", "a7fdce21", "b9df89c9", "c93cfed5", "2ee71112", "d687571f", "649e946c", "6779e4c9", "4967815e", "f7d52eb2", "bb3ef296"], "player72_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d", "77e3bb42", "4ebb7244", "3f4ec3e2", "aa57ceb8", "f659fe26", "731cf4fc"], "player73_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d", "77e3bb42", "4ebb7244", "3f4ec3e2", "aa57ceb8", "f659fe26", "731cf4fc"], "player74_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d", "77e3bb42", "4ebb7244", "3f4ec3e2", "aa57ceb8", "f659fe26", "731cf4fc"], "player75_genes_hexa_list": ["c4dff7ac", "ab151d6b", "4616f45e", "11ae1cd2", "a88f14b5", "5be4746a", "c2b93243", "eb4992d7", "338bfe82", "e64e3499", "f72c4376", "f3db22f3"], "player76_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player77_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player78_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player79_genes_hexa_list": ["9137fb1a", "671f44d3", "9a48d87a", "e2566ed5", "37cdd3d3", "4b2639ca", "af93cdd3", "4fa616f4", "bf9884ae", "83b75d86", "74824669", "ca45cea7"], "player80_genes_hexa_list": ["e9ad32c7", "6cb325ae", "a7fdce21", "b9df89c9", "c93cfed5", "2ee71112", "d687571f", "649e946c", "6779e4c9", "4967815e", "f7d52eb2", "bb3ef296"], "player81_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player82_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player83_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player84_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player85_genes_hexa_list": ["54eeb994", "ceb87dd4", "f155bbfa", "67e4524e", "daffdea6", "96863e9d", "91ac5124", "ad1b3eaf", "598caafa", "ac1ebe81", "d9e24c2a", "478f9ea8"], "player86_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player87_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player88_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player89_genes_hexa_list": ["e9ad32c7", "6cc325ae", "a7fdce21", "b9df89c9", "c93cfed5", "2ee71112", "d687571f", "649e946c", "6779e4c9", "4967815e", "f7d52eb2", "bb3ef296"], "player90_genes_hexa_list": ["e9ad32c7", "6cc325ae", "a7fdce21", "b9df89c9", "c93cfed5", "2ee71112", "d687571f", "649e946c", "6779e4c9", "4967815e", "f7d52eb2", "bb3ef296"], "player91_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player92_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player93_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player94_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d", "77e3bb42", "4ebb7244", "3f4ec3e2", "aa57ceb8", "f659fe26", "731cf4fc"], "player95_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player96_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player97_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player98_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player99_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player100_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player101_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player102_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player103_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player104_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player105_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player106_genes_hexa_list": ["54eeb994", "ceb87dd4", "f155bbfa", "67e4524e", "daffdea6", "96863e9d", "91ac5124", "ad1b3eaf", "598caafa", "ac1ebe81", "d9e24c2a", "478f9ea8"], "player107_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"]}
# genes_hexa_dict=copy.deepcopy(players_genes_hexa_list)
# for i in range(len(list(genes_hexa_dict.keys()))):
#     genes_hexa_dict[f'player{i}']=genes_hexa_dict.pop(f'player{i}_genes_hexa_list')
# restart_simulation(genes_hexa_dict,27,r'test_3_continued_part_2.py',rf'D:\New_Evolution_best_12_genome_length_images',350,350,inp=2)