import copy

from useful_functions import gene_to_unprocessed_data,unprocessed_data_to_processed_data,processed_data_to_brain,graph_visuals,genes_hexa_dict_generator,co_ordinates_initialize_dict,genes_to_brain,directions_dict_generator,sense_to_inputs_activations,update_activations,position_errors_resolve,change,back_to_normal,mutate,replicate,condition,check,genes_hexa_list_to_genes_list,restart_simulation
from pygame_env import player,env,circle,playerencoder
from hashing_encoding_colors import encode_players_with_same_genes
import pygame
import json
# import logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
def main():
    size_parameter=5
    num_neurons=[11,2,6] # [sensory_neurons,internal_neurons,output_neurons]
    env_width=500
    env_height=500
    population=250
    default_population=250
    steps_per_gen=120
    genome_length=10
    generations=200
    seed=0
    remaining_players_number=[]
    pygame.init()
    surface = pygame.Surface((env_width, env_height))
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
            # for i in range(len(list(players_dict.keys()))):
                # if step%2==0:
                #     print(f'player{i} co_ordinates history::',players_dict['player'+str(i)].co_ordinates_history_list)
                #     print(f'player{i} rect co ordinates:', players_dict['player' + str(i)].co_ordinates_history_list)
            print("step:",step)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
            surface.fill((255, 255, 255))
            for i in range(population):
                players_dict['player' + str(i)].pygame_object.draw(surface)
            # pygame.image.save(screen,rf'D:\Evolution\pygame_images_testing\images\image.png')
            #pygame.display.flip()
            combined_activation_inputs_dict=sense_to_inputs_activations(surface,players_dict,step,steps_per_gen,size_parameter,seed=0)
            players_dict,stored_neurons_dict,stored_incoming_exhausted_dict=update_activations(players_dict,combined_activation_inputs_dict)
            players_dict=change(players_dict, surface, size_parameter, kill_neuron=False)
            players_dict=back_to_normal(players_dict,stored_neurons_dict,stored_incoming_exhausted_dict)
            pygame.image.save(surface, rf'D:\New_Evolution_10_genome_length_images\generation{generation+1}\image{step+generation*steps_per_gen+1}.png')
        players_dict,remaining_players_list=condition(players_dict,surface,inp=3)
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
        with open('testing_left_again.py', 'w') as f:
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
        players_dict,num_mutations=mutate(players_dict,num_neurons,remaining_players_list,mutation_prob=0.002)
        print('num_mutations:',num_mutations)
        print('num_players_after_mutation:',len(players_dict))
        players_dict,population,max_gene,max_value=replicate(players_dict,env_width,env_height,size_parameter,remaining_players_list,default_population=default_population)
        max_genes_list_combined.append(copy.deepcopy(max_gene))
        print('num_players_after_replication:',default_population,' or ',len(players_dict))
    return players_dict,remaining_players_number

players_dict=main()
players_dict_copy=players_dict
print(players_dict_copy)

# players_genes_hexa_list={"player0_genes_hexa_list": ["8ce15f85", "94d691b4", "e6cce258", "b4ba35e2", "c1bc7f73", "6b615f57", "cf3424f4", "287caa39", "2377c253", "89a47829"], "player1_genes_hexa_list": ["8ce15f85", "94d691b4", "e6cce258", "b4ba35e2", "c1bc7f73", "6b615f57", "cf3424f4", "277caa39", "2377c253", "89a47829"], "player2_genes_hexa_list": ["5832caa9", "16f1de1a", "9985596c", "7331b53d", "9293b27e", "c2fabce3", "cdd16788", "2f199f32", "e1ccee54", "5b2bdbc6"], "player3_genes_hexa_list": ["76d89b42", "6e77338d", "6eada295", "9d18ade7", "6336f6ee", "16f8f31f", "a476769b", "9578d265", "b4211c93", "9d975a74"], "player4_genes_hexa_list": ["76d89b42", "6e77338d", "6eada295", "9d18ade7", "6336f6ee", "16f8f31f", "a476769b", "9578d265", "b4211c93", "9d975a74"], "player5_genes_hexa_list": ["8ce15f85", "94d691b4", "e6cce258", "b4ba35e2", "c1bc7f73", "6b615f57", "cf3424f4", "287caa39", "2377c253", "89a47829"], "player6_genes_hexa_list": ["8ce15f85", "94d691b4", "e6cce258", "b4ba35e2", "c1bc7f73", "6b615f57", "cf3424f4", "287caa39", "2377c253", "89a47829"], "player7_genes_hexa_list": ["8ce15f85", "94d691b4", "e6cce258", "b4ba35e2", "c1bc7f73", "6b615f57", "cf3424f4", "287caa39", "2377c253", "89a47829"], "player8_genes_hexa_list": ["8ce15f85", "94d691b4", "e6cce258", "b4ba35e2", "c1bc7f73", "6b615f57", "cf3424f4", "287caa39", "2377c253", "89a47829"], "player9_genes_hexa_list": ["8ce15f85", "94d691b4", "e6cce258", "b4ba35e2", "c1bc7f73", "6b615f57", "cf3424f4", "287caa39", "2377c253", "89a47829"], "player10_genes_hexa_list": ["8ce15f85", "94d691b4", "e6cce258", "b4ba35e2", "c1bc7f73", "6b615f57", "cf3424f4", "287caa39", "2377c253", "89a47829"], "player11_genes_hexa_list": ["8ce15f85", "94d691b4", "e6cce258", "b4ba35e2", "c1bc7f73", "6b615f57", "cf3424f4", "287caa39", "2377c253", "89a47829"], "player12_genes_hexa_list": ["8ce15f85", "94d691b4", "e6cce258", "b4ba35e2", "c1bc7f73", "6b615f57", "cf3424f4", "287caa39", "2377c253", "89a47829"], "player13_genes_hexa_list": ["8ce15f85", "94d691b4", "e6cce258", "b4ba35e2", "c1bc7f73", "6b615f57", "cf3424f4", "287caa39", "2377c253", "89a47829"], "player14_genes_hexa_list": ["5cebceb5", "5b9ffd5b", "183ef26e", "e299e849", "b74a8766", "79eb534c", "a1139b85", "56636a5f", "9d97a6fa", "658f8d86"], "player15_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d", "77e3bb42", "4ebb7244", "3f4ec3e2", "aa57ceb8"], "player16_genes_hexa_list": ["8ce15f85", "94d691b4", "e6cce258", "b4ba35e2", "c1bc7f73", "6b615f57", "cf3424f4", "287caa39", "2377c253", "89a47829"], "player17_genes_hexa_list": ["8ce15f85", "94d691b4", "e6cce258", "b4ba35e2", "c1bc7f73", "6b615f57", "cf3424f4", "287caa39", "2377c253", "89a47829"], "player18_genes_hexa_list": ["8ce15f85", "94d691b4", "e6cce258", "b4ba35e2", "c1bc7f73", "6b615f57", "cf3424f4", "287caa39", "2377c253", "89a47829"], "player19_genes_hexa_list": ["8ce15f85", "94d691b4", "e6cce258", "b4ba35e2", "c1bc7f73", "6b615f57", "cf3424f4", "287caa39", "2377c253", "89a47829"], "player20_genes_hexa_list": ["a6a3f6f4", "97398cf2", "3f44acb1", "e59618d6", "886c6956", "4b4569ed", "31c46dd8", "d6147b57", "db59a93a", "831f4166"], "player21_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d", "77e3bb42", "4ebb7244", "3f4ec3e2", "aa57ceb8"], "player22_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d", "77e3bb42", "4ebb7244", "3f4ec3e2", "aa57ceb8"], "player23_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d", "77e3bb42", "4ebb7244", "3f4ec3e2", "aa57ceb8"], "player24_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d", "77e3bb42", "4ebb7244", "3f4ec3e2", "aa57ceb8"], "player25_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d", "77e3bb42", "4ebb7244", "3f4ec3e2", "aa57ceb8"], "player26_genes_hexa_list": ["8ce15f85", "94d691b4", "e6cce258", "b4ba35e2", "c1bc7f73", "6b615f57", "cf3424f4", "287caa39", "2377c253", "89a47829"], "player27_genes_hexa_list": ["8ce15f85", "94d691b4", "e6cce258", "b4ba35e2", "c1bc7f73", "6b615f57", "cf3424f4", "287caa39", "2377c253", "89a47829"], "player28_genes_hexa_list": ["8ce15f85", "94d691b4", "e6cce258", "b4ba35e2", "c1bc7f73", "6b615f57", "cf3424f4", "287caa39", "2377c253", "89a47829"], "player29_genes_hexa_list": ["8ce15f85", "94d691b4", "e6cce258", "b4ba35e2", "c1bc7f73", "6b615f57", "cf3424f4", "287caa39", "2377c253", "89a47829"], "player30_genes_hexa_list": ["5832caa9", "16f1de1a", "9945596c", "7331b53d", "9293b27e", "c2fabce3", "cdd16788", "2f199f32", "e1ccee54", "5b2bdbc6"], "player31_genes_hexa_list": ["5832caa9", "16f1de1a", "9945596c", "7331b53d", "9293b27e", "c2fabce3", "cdd16788", "2f199f32", "e1ccee54", "5b2bdbc6"], "player32_genes_hexa_list": ["5832caa9", "16f1de1a", "9945596c", "7331b53d", "9293b27e", "c2fabce3", "cdd16788", "2f199f32", "e1ccee54", "5b2bdbc6"], "player33_genes_hexa_list": ["5832caa9", "16f1de1a", "9985596c", "7331b53d", "9293b27e", "c2fabce3", "cdd16788", "2f199f32", "e1ccee54", "5b2bdbc6"], "player34_genes_hexa_list": ["5832caa9", "16f1de1a", "9985596c", "7331b53d", "9293b27e", "c2fabce3", "cdd16788", "2f199f32", "e1ccee54", "5b2bdbc6"], "player35_genes_hexa_list": ["76d89b42", "6e77338d", "6eada295", "9d18ade7", "6336f6ee", "16f8f31f", "a476769b", "9578d265", "b4211c93", "9d975a74"], "player36_genes_hexa_list": ["76d89b42", "6e77338d", "6eada295", "9d18ade7", "6336f6ee", "16f8f31f", "a476769b", "9578d265", "b4211c93", "9d975a74"], "player37_genes_hexa_list": ["76d89b42", "6e77338d", "6eada295", "9d18ade7", "6336f6ee", "16f8f31f", "a476769b", "9578d265", "b4211c93", "9d975a74"], "player38_genes_hexa_list": ["76d89b42", "6e77338d", "6eada295", "9d18ade7", "6336f6ee", "16f8f31f", "a476769b", "9578d265", "b4211c93", "9d975a74"], "player39_genes_hexa_list": ["76d89b42", "6e77338d", "6eada295", "9d18ade7", "6336f6ee", "16f8f31f", "a476769b", "9578d265", "b4211c93", "9d975a74"], "player40_genes_hexa_list": ["8ce15f85", "94d691b4", "e6cce258", "b4ba35e2", "c1bc7f73", "6b615f57", "cf3424f4", "287caa39", "2377c253", "89a47829"], "player41_genes_hexa_list": ["8ce15f85", "94d691b4", "e6cce258", "b4ba35e2", "c1bc7f73", "6b615f57", "cf3424f4", "287caa39", "2377c253", "89a47829"], "player42_genes_hexa_list": ["8ce15f85", "94d691b4", "e6cce258", "b4ba35e2", "c1bc7f73", "6b615f57", "cf3424f4", "287caa39", "2377c253", "89a47829"], "player43_genes_hexa_list": ["8ce15f85", "94d691b4", "e6cce258", "b4ba35e2", "c1bc7f73", "6b615f57", "cf3424f4", "287caa39", "2377c253", "89a47829"], "player44_genes_hexa_list": ["a6a3f6f4", "97398cf2", "3f44acb1", "e59618d6", "886c6956", "4b4569ed", "31c46dd8", "d6147b57", "db59a93a", "831f4166"], "player45_genes_hexa_list": ["a6a3f6f4", "97398cf2", "3f44acb1", "e59618d6", "886c6956", "4b4569ed", "31c46dd8", "d6147b57", "db59a93a", "831f4166"], "player46_genes_hexa_list": ["5cebceb5", "5b9ffd5b", "183ef26e", "e299e849", "b74a8766", "79eb534c", "a1139b85", "56636a5f", "9d97a6fa", "658f8d86"], "player47_genes_hexa_list": ["5cebceb5", "5b9ffd5b", "183ef26e", "e299e849", "b74a8766", "79eb534c", "a1139b85", "56636a5f", "9d97a6fa", "658f8d86"], "player48_genes_hexa_list": ["5cebceb5", "5b9ffd5b", "183ef26e", "e299e849", "b74a8766", "79eb534c", "a1139b85", "56636a5f", "9d97a6fa", "658f8d86"], "player49_genes_hexa_list": ["5cebceb5", "5b9ffd5b", "183ef26e", "e299e849", "b74a8766", "79eb534c", "a1139b85", "56636a5f", "9d97a6fa", "658f8d86"], "player50_genes_hexa_list": ["8ce15f85", "94d691b4", "e6cce258", "b4ba35e2", "c1bc7f73", "6b615f57", "cf3424f4", "287caa39", "2377c253", "89a47829"], "player51_genes_hexa_list": ["8ce15f85", "94d691b4", "e6cce258", "b4ba35e2", "c1bc7f73", "6b615f57", "cf3424f4", "287caa39", "2377c253", "89a47829"], "player52_genes_hexa_list": ["8ce15f85", "94d691b4", "e6cce258", "b4ba35e2", "c1bc7f73", "6b615f57", "cf3424f4", "287caa39", "2377c253", "89a47829"], "player53_genes_hexa_list": ["8ce15f85", "94d691b4", "e6cce258", "b4ba35e2", "c1bc7f73", "6b615f57", "cf3424f4", "287caa39", "2377c253", "89a47829"], "player54_genes_hexa_list": ["8ce15f85", "94d691b4", "e6cce258", "b4ba35e2", "c1bc7f73", "6b615f57", "cf3424f4", "277caa39", "2377c253", "89a47829"], "player55_genes_hexa_list": ["76d89b42", "6e77338d", "6eada295", "9d18ade7", "6336f6ee", "16f8f31f", "a476769b", "9578d265", "b4211c93", "9d975a74"], "player56_genes_hexa_list": ["8ce15f85", "94d691b4", "e6cce258", "b4ba35e2", "c1bc7f73", "6b615f57", "cf3424f4", "287caa39", "2377c253", "89a47829"]}
# genes_hexa_dict=copy.deepcopy(players_genes_hexa_list)
# for i in range(len(list(genes_hexa_dict.keys()))):
#     genes_hexa_dict[f'player{i}']=genes_hexa_dict.pop(f'player{i}_genes_hexa_list')
# restart_simulation(genes_hexa_dict,33,r'D:Evolution\testing_left_again_continued.py',rf'D:\New_Evolution_10_genome_length_images',250,250,inp=3)