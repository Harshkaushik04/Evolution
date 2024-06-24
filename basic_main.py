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
    population=200
    default_population=200
    steps_per_gen=120
    genome_length=4
    generations=100
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
            pygame.image.save(surface, rf'D:\New_Evolution_4_improved_genome_length_images\generation{generation+1}\image{step+generation*steps_per_gen+1}.png')
        players_dict,remaining_players_list=condition(players_dict,surface,inp=1)
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
        with open('test4.py', 'w') as f:
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

# players_dict=main()
# players_dict_copy=players_dict
# print(players_dict_copy)

players_genes_hexa_list={"player0_genes_hexa_list": ["a37c5317", "46f42ba5", "722ecddf", "9d7172db", "95f3a87b", "575fed1f", "fd8f7511", "12149333"], "player1_genes_hexa_list": ["655d8b2c", "93a531f7", "eb5aacfb", "d73b33da", "3aa443eb", "8127c769", "edb38a8e", "2d5a1e84"], "player2_genes_hexa_list": ["66e11c18", "6f4e7c17", "15fcdaff", "c3444395", "c433433e", "96c543a3", "999bb7c9", "717bfc7b"], "player3_genes_hexa_list": ["66e11c18", "6f4e7c17", "15fcdaff", "c3444395", "c433433e", "96c543a3", "999bb7c9", "717bfc7b"], "player4_genes_hexa_list": ["66e11c18", "6f4e7c17", "15fcdaff", "c3444395", "c433433e", "96c543a3", "999bb7c9", "717bfc7b"], "player5_genes_hexa_list": ["66e11c18", "6f4e7c17", "15fcdaff", "c3444395", "c433433e", "96c543a3", "999bb7c9", "717bfc7b"], "player6_genes_hexa_list": ["2399cdab", "163fd45e", "5dd45ffb", "25fdfa9d", "ae2d47a4", "b6e3b96c", "3794a6c5", "73844af6"], "player7_genes_hexa_list": ["317b7818", "fdb2ed3a", "1253cd65", "22b9187d", "ba9ff64c", "162525ce", "c9a637b1", "1c5bce76"], "player8_genes_hexa_list": ["317b7818", "fdb2ed3a", "1253cd65", "22b9187d", "ba9ff64c", "162525ce", "c9a637b1", "1c5bce76"], "player9_genes_hexa_list": ["317b7818", "fdb2ed3a", "1253cd65", "22b9187d", "ba9ff64c", "162525ce", "c9a637b1", "1c5bce76"], "player10_genes_hexa_list": ["317b7818", "fdb2ed3a", "1253cd65", "22b9187d", "ba9ff64c", "162525ce", "c9a637b1", "1c5bce76"], "player11_genes_hexa_list": ["317b7818", "fdb2ed3a", "1253cd65", "22b9187d", "ba9ff64c", "162525ce", "c9a637b1", "1c5bce76"], "player12_genes_hexa_list": ["317b7818", "fdb2ed3a", "1253cd65", "22b9187d", "ba9ff64c", "162525ce", "c9a637b1", "1c5bce76"], "player13_genes_hexa_list": ["317b7818", "fdb2ed3a", "1253cd65", "22b9187d", "ba9ff64c", "162525ce", "c9a637b1", "1c5bce76"], "player14_genes_hexa_list": ["317b7818", "fdb2ed3a", "1253cd65", "22b9187d", "ba9ff64c", "162525ce", "c9a637b1", "1c5bce76"], "player15_genes_hexa_list": ["b16a5f36", "9834a471", "5571cb9b", "9ace65a6", "db7e173d", "2cd35ea5", "7333db25", "914b5612"], "player16_genes_hexa_list": ["b16a5f36", "9834a471", "5571cb9b", "9ace65a6", "db7e173d", "2cd35ea5", "7333db25", "914b5612"], "player17_genes_hexa_list": ["b16a5f36", "9834a471", "5571cb9b", "9ace65a6", "db7e173d", "2cd35ea5", "7333db25", "914b5612"], "player18_genes_hexa_list": ["b16a5f36", "9834a471", "5571cb9b", "9ace65a6", "db7e173d", "2cd35ea5", "7333db25", "914b5612"], "player19_genes_hexa_list": ["b16a5f36", "9834a471", "5571cb9b", "9ace65a6", "db7e173d", "2cd35ea5", "7333db25", "914b5612"], "player20_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622"], "player21_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622"], "player22_genes_hexa_list": ["dee7394b", "4c2764f6", "5ee997c5", "55e1471c", "8b9eebb9", "6f25bf22", "7f9f63bb", "b5f315ec"], "player23_genes_hexa_list": ["8b5beb45", "52f259d4", "d6d1b557", "8fbf987d", "a8184823", "ff2d2b93", "b4e7e1cb", "faf5dfa9"], "player24_genes_hexa_list": ["8b5beb45", "52f259d4", "d6d1b557", "8fbf987d", "a8184823", "ff2d2b93", "b4e7e1cb", "faf5dfa9"], "player25_genes_hexa_list": ["1bcdf7d4", "18aec48a", "5ee94f63", "56e14d9a", "f7122fb2", "1566ec52", "ca9c8e59", "27e8bb9a"], "player26_genes_hexa_list": ["1bcdf7d4", "18aec48a", "5ee94f63", "56e14d9a", "f7122fb2", "1566ec52", "ca9c8e59", "27e8bb9a"], "player27_genes_hexa_list": ["1bcdf7d4", "18aec48a", "5ee94f63", "56e14d9a", "f7122fb2", "1566ec52", "ca9c8e59", "27e8bb9a"], "player28_genes_hexa_list": ["fbf46cf5", "3656be94", "b99ed5ab", "fefaa48d", "d9c8dad4", "7a3279f7", "cfe1feb2", "9d969e21"], "player29_genes_hexa_list": ["a37c5317", "46f42ba5", "722ecddf", "9d7172db", "95f3a87b", "575fed1f", "fd8f7511", "12149333"], "player30_genes_hexa_list": ["a37c5317", "46f42ba5", "722ecddf", "9d7172db", "95f3a87b", "575fed1f", "fd8f7511", "12149333"], "player31_genes_hexa_list": ["a37c5317", "46f42ba5", "722ecddf", "9d7172db", "95f3a87b", "575fed1f", "fd8f7511", "12149333"], "player32_genes_hexa_list": ["66e11c18", "6f4e7ce7", "15fcdaff", "c3444395", "c433433e", "96c543a3", "999bb7c9", "717bfc7b"], "player33_genes_hexa_list": ["66e11c18", "6f4e7c17", "15fcdaff", "c3444395", "c433433e", "96c543a3", "999bb7c9", "717bfc7b"], "player34_genes_hexa_list": ["66e11c18", "6f4e7c17", "15fcdaff", "c3444395", "c433433e", "96c543a3", "999bb7c9", "717bfc7b"], "player35_genes_hexa_list": ["66e11c18", "6f4e7c17", "15fcdaff", "c3444395", "c433433e", "96c543a3", "999bb7c9", "717bfc7b"], "player36_genes_hexa_list": ["66e11c18", "6f4e7c17", "15fcdaff", "c3444395", "c433433e", "96c543a3", "999bb7c9", "717bfc7b"], "player37_genes_hexa_list": ["66e11c18", "6f4e7c17", "15fcdaff", "c3444395", "c433433e", "96c543a3", "999bb7c9", "717bfc7b"], "player38_genes_hexa_list": ["66e11c18", "6f4e7c17", "15fcdaff", "c3444395", "c433433e", "96c543a3", "999bb7c9", "717bfc7b"], "player39_genes_hexa_list": ["8b5beb45", "52f259d4", "d6d1b557", "8fbf987d", "a8184823", "ff2d2b93", "b4e7e1cb", "faf5dfa9"], "player40_genes_hexa_list": ["8b5beb45", "52f259d4", "d6d1b557", "8fbf987d", "a8184823", "ff2d2b93", "b4e7e1cb", "faf5dfa9"], "player41_genes_hexa_list": ["8b5beb45", "52f259d4", "d6d1b557", "8fbf987d", "a8184823", "ff2d2b93", "b4e7e1cb", "faf5dfa9"], "player42_genes_hexa_list": ["dee7394b", "4c2764f6", "5ee997c5", "55e1471c", "8b9eebb9", "6f25bf22", "7f9f63bb", "b5f315ec"], "player43_genes_hexa_list": ["dee7394b", "4c2764f6", "5ee997c5", "55e1471c", "8b9eebb9", "6f25bf22", "7f9f63bb", "b5f315ec"], "player44_genes_hexa_list": ["dee7394b", "4c2764f6", "5ee997c5", "55e1471c", "8b9eebb9", "6f25bf22", "7f9f63bb", "b5f315ec"], "player45_genes_hexa_list": ["dee7394b", "4c2764f6", "5ee997c5", "55e1471c", "8b9eebb9", "6f25bf22", "7f9f63bb", "b5f315ec"], "player46_genes_hexa_list": ["dee7394b", "4c2764f6", "5ee997c5", "55e1471c", "8b9eebb9", "6f25bf22", "7f9f63bb", "b5f315ec"], "player47_genes_hexa_list": ["fbf46cf5", "3656be94", "b99ed5ab", "fefaa48d", "d9c8dad4", "7a3279f7", "cfe1feb2", "9d969e21"], "player48_genes_hexa_list": ["a37c5317", "46f42ba5", "722ecddf", "9d7172db", "95f3a87b", "575fed1f", "fd8f7511", "12149333"], "player49_genes_hexa_list": ["dee7394b", "4c2764f6", "5ee997c5", "55e1471c", "8b9eebb9", "6f25bf22", "7f9f63bb", "b5f315ec"], "player50_genes_hexa_list": ["dee7394b", "4c2764f6", "5ee997c5", "55e1471c", "8b9eebb9", "6f25bf22", "7f9f63bb", "b5f315ec"], "player51_genes_hexa_list": ["dee7394b", "4c2764f6", "5ee997c5", "55e1471c", "8b9eebb9", "6f25bf22", "7f9f63bb", "b5f315ec"], "player52_genes_hexa_list": ["a37c5317", "46f42ba5", "722ecddf", "9d7172db", "95f3a87b", "575fed1f", "fd8f7511", "12149333"], "player53_genes_hexa_list": ["a37c5317", "46f42ba5", "722ecddf", "9d7172db", "95f3a87b", "575fed1f", "fd8f7511", "12149333"], "player54_genes_hexa_list": ["a37c5317", "46f42ba5", "722ecddf", "9d7172db", "95f3a87b", "575fed1f", "fd8f7511", "12149333"], "player55_genes_hexa_list": ["a37c5317", "46f42ba5", "722ecddf", "9d7172db", "95f3a87b", "575fed1f", "fd8f7511", "12149333"], "player56_genes_hexa_list": ["655d8b2c", "93a531f7", "eb5aacfb", "d73b33da", "3aa443eb", "8127c769", "edb38a8e", "2d5a1e84"], "player57_genes_hexa_list": ["66e11c18", "6f4e7c17", "15fcdaff", "c3444395", "c433433e", "96c543a3", "999bb7c9", "717bfc7b"], "player58_genes_hexa_list": ["66e11c18", "6f4e7c17", "15fcdaff", "c3444395", "c433433e", "96c543a3", "999bb7c9", "717bfc7b"], "player59_genes_hexa_list": ["66e11c18", "6f4e7c17", "15fcdaff", "c3444395", "c433433e", "96c543a3", "999bb7c9", "717bfc7b"], "player60_genes_hexa_list": ["317b7818", "fdb2ed3a", "1253cd65", "22b9187d", "ba9ff64c", "162525ce", "c9a637b1", "1c5bce76"], "player61_genes_hexa_list": ["a37c5317", "46f42ba5", "722ecddf", "9d7172db", "95f3a87b", "575fed1f", "fd8f7511", "12149333"], "player62_genes_hexa_list": ["66e11c18", "6f4e7c17", "15fcdaff", "c3444395", "c433433e", "96c543a3", "999bb7c9", "717bfc7b"], "player63_genes_hexa_list": ["66e11c18", "6f4e7c17", "15fcdaff", "c3444395", "c433433e", "96c543a3", "999bb7c9", "717bfc7b"], "player64_genes_hexa_list": ["317b7818", "fdb2ed3a", "1253cd65", "22b9187d", "ba9ff64c", "162525ce", "c9a637b1", "1c5bce76"], "player65_genes_hexa_list": ["317b7818", "fdb2ed3a", "1253cd65", "22b9187d", "ba9ff64c", "162525ce", "c9a637b1", "1c5bce76"], "player66_genes_hexa_list": ["317b7818", "fdb2ed3a", "1253cd65", "22b9187d", "ba9ff64c", "162525ce", "c9a637b1", "1c5bce76"]}
genes_hexa_dict=copy.deepcopy(players_genes_hexa_list)
for i in range(len(list(genes_hexa_dict.keys()))):
    genes_hexa_dict[f'player{i}']=genes_hexa_dict.pop(f'player{i}_genes_hexa_list')
restart_simulation(genes_hexa_dict,54,r'D:\Evolution\test4_continued.py',rf'D:\New_Evolution_4_improved_genome_length_images(improvised)',200,200)