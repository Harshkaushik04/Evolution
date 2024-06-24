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
    genome_length=6
    generations=500
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
            pygame.image.save(surface, rf'D:\New_Evolution_left_final\generation{generation+1}\image{step+generation*steps_per_gen+1}.png')
        players_dict,remaining_players_list=condition(players_dict,surface,inp=1)
        remaining_players_number.append(len(remaining_players_list))
        dicti,another_dicti = {},{}
        for i in range(len(remaining_players_list)):
            dicti[f'player{i}_genes_list'] = players_dict[remaining_players_list[i]].genes_list
            another_dicti[f'player{i}_genes_hexa_list']=players_dict[remaining_players_list[i]].brain.genes_hexa_list
        players_json = json.dumps(dicti)
        players_another_json=json.dumps(another_dicti)
        list_json=json.dumps(remaining_players_number)
        max_gene_json=json.dumps(max_gene)
        max_genes_list_combined_json=json.dumps(max_genes_list_combined)
        with open('left_test_part_2.py', 'w') as f:
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

players_genes_hexa_list={"player0_genes_hexa_list": ["58cce358", "c3395c55", "fe98a9f3", "fab5acae", "ea5b5297", "9d26fef1"], "player1_genes_hexa_list": ["2c9765b6", "5c926f83", "1baea497", "398fff42", "4b3d68af", "2c691ecb"], "player2_genes_hexa_list": ["af6ab244", "7dc64174", "9249f4a8", "52df94a3", "e9b5c26a", "738a9dff"], "player3_genes_hexa_list": ["655d8b2c", "93a531f7", "eb5aacfb", "d73b33da", "3aa443eb", "8127c769"], "player4_genes_hexa_list": ["a6a3f6f4", "97398cf2", "3f44acb1", "e59618d6", "886c6956", "4b4569ed"], "player5_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d"], "player6_genes_hexa_list": ["813c927b", "b8e232a2", "7e2a4e22", "b484c6fa", "6ae49743", "817d64fc"], "player7_genes_hexa_list": ["af6ab244", "7dc64174", "9249f4a8", "52df94a3", "e9b5c26a", "738a9dff"], "player8_genes_hexa_list": ["b926c83d", "ff3f41fe", "536857d9", "df52c3bf", "27d3ccb2", "1a4f91ba"], "player9_genes_hexa_list": ["336b34c9", "882d51be", "89aa613e", "2622221c", "17f46153", "27f1f223"], "player10_genes_hexa_list": ["2c9765b6", "5c926f83", "1baea497", "398fff42", "4b3d68af", "2c691ecb"], "player11_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d"], "player12_genes_hexa_list": ["f739ab2c", "5cca7fe3", "99be1326", "df583ec3", "691da1d7", "1769fec7"], "player13_genes_hexa_list": ["3c491ee1", "f35afd18", "98c3c132", "5b8d5bb5", "6fafcd77", "7f3f7776"], "player14_genes_hexa_list": ["45525ba8", "faf265be", "219b1762", "c38a12c3", "9b8874e2", "8c6cc5b3"], "player15_genes_hexa_list": ["af6ab244", "7dc64174", "9249f4a8", "52df94a3", "e9b5c26a", "738a9dff"], "player16_genes_hexa_list": ["58cce358", "c3395c55", "fe98a9f3", "fab5acae", "ea5b5297", "9d26fef1"], "player17_genes_hexa_list": ["9ba97a7e", "f6c89e22", "1dcefc7c", "2a3f874c", "791aaafb", "67b1bb42"], "player18_genes_hexa_list": ["c1ac843c", "32bf18da", "b5eb936b", "77a8aad8", "e5252d1a", "9d3d6c5e"], "player19_genes_hexa_list": ["487d365b", "4d19dc31", "cfb5cb6a", "79b2efbc", "13ec8288", "51721bd2"], "player20_genes_hexa_list": ["58cce358", "c3395c55", "fe98a9f3", "fab5acae", "ea5b5297", "9d26fef1"], "player21_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d"], "player22_genes_hexa_list": ["43eb8eb8", "cf8f886f", "47d64851", "5c447f6e", "66719135", "e548ad6d"], "player23_genes_hexa_list": ["f91eaf29", "ef8adaae", "e6ab51f2", "87c515d7", "f31369a8", "42fbc7d1"], "player24_genes_hexa_list": ["af6ab244", "7dc64174", "9249f4a8", "52df94a3", "e9b5c26a", "738a9dff"], "player25_genes_hexa_list": ["8cff3354", "42279313", "3f97f687", "8d729359", "bee3f9f4", "7bc37d16"], "player26_genes_hexa_list": ["5aac8ffd", "43a9af6d", "b922e926", "6171b16d", "e5233ff2", "42b313ea"], "player27_genes_hexa_list": ["eac32c59", "497bd955", "b71c7315", "2c176397", "1d53a266", "7fb5ec45"], "player28_genes_hexa_list": ["f91eaf29", "ef8adaae", "e6ab51f2", "87c515d7", "f31369a8", "42fbc7d1"], "player29_genes_hexa_list": ["af6ab244", "7dc64174", "9249f4a8", "52df94a3", "e9b5c26a", "738a9dff"], "player30_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d"], "player31_genes_hexa_list": ["af6ab244", "7dc64174", "9249f4a8", "52df94a3", "e9b5c26a", "738a9dff"], "player32_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d"], "player33_genes_hexa_list": ["d4214aca", "6252a458", "be2bf99c", "d2e9b513", "3a7f744d", "b4bdcc44"], "player34_genes_hexa_list": ["af6ab244", "7dc64174", "9249f4a8", "52df94a3", "e9b5c26a", "738a9dff"], "player35_genes_hexa_list": ["eac32c59", "497bd955", "b71c7315", "2c176397", "1d53a266", "7fb5ec45"], "player36_genes_hexa_list": ["2c9765b6", "5c926f83", "1baea497", "398fff42", "4b3d68af", "2c691ecb"], "player37_genes_hexa_list": ["c1ac843c", "32bf18da", "b5eb936b", "77a8aad8", "e5252d1a", "9d3d6c5e"], "player38_genes_hexa_list": ["2b9679b3", "287f747a", "9caa63c6", "a5217bc4", "ae42d16b", "d722bc56"], "player39_genes_hexa_list": ["af6ab244", "7dc64174", "9249f4a8", "52df94a3", "e9b5c26a", "738a9dff"], "player40_genes_hexa_list": ["af6ab244", "7dc64174", "9249f4a8", "52df94a3", "e9b5c26a", "738a9dff"], "player41_genes_hexa_list": ["8cff3354", "42279313", "3f97f687", "8d729359", "bee3f9f4", "7bc37d16"], "player42_genes_hexa_list": ["eac32c59", "497bd955", "b71c7315", "2c176397", "1d53a266", "7fb5ec45"], "player43_genes_hexa_list": ["2c9765b6", "5c926f83", "1baea497", "398fff42", "4b3d68af", "2c691ecb"], "player44_genes_hexa_list": ["af6ab244", "7dc64174", "9249f4a8", "52df94a3", "e9b5c26a", "738a9dff"], "player45_genes_hexa_list": ["a6a3f6f4", "97398cf2", "3f44acb1", "e59618d6", "886c6956", "4b4569ed"], "player46_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d"], "player47_genes_hexa_list": ["813c927b", "b8e232a2", "7e2a4e22", "b484c6fa", "6ae49743", "817d64fc"], "player48_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d"], "player49_genes_hexa_list": ["af6ab244", "7dc64174", "9249f4a8", "52df94a3", "e9b5c26a", "738a9dff"], "player50_genes_hexa_list": ["a6a3f6f4", "97398cf2", "3f44acb1", "e59618d6", "886c6956", "4b4569ed"], "player51_genes_hexa_list": ["af6ab244", "7dc64174", "9249f4a8", "52df94a3", "e9b5c26a", "738a9dff"], "player52_genes_hexa_list": ["58cce358", "c3395c55", "fe98a9f3", "fab5acae", "ea5b5297", "9d26fef1"], "player53_genes_hexa_list": ["f91eaf29", "ef8adaae", "e6ab51f2", "87c515d7", "f31369a8", "42fbc7d1"], "player54_genes_hexa_list": ["af6ab244", "7dc64174", "9249f4a8", "52df94a3", "e9b5c26a", "738a9dff"], "player55_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d"], "player56_genes_hexa_list": ["d2c66a67", "8bf7724f", "f1a4a37e", "4ad39332", "47cfd681", "b2ebdbbe"], "player57_genes_hexa_list": ["af6ab244", "7dc64174", "9249f4a8", "52df94a3", "e9b5c26a", "738a9dff"], "player58_genes_hexa_list": ["b926c83d", "ff3f41fe", "536857d9", "df52c3bf", "27d3ccb2", "1a4f91ba"], "player59_genes_hexa_list": ["a37c5317", "46f42ba5", "722ecddf", "9d7172db", "95f3a87b", "575fed1f"], "player60_genes_hexa_list": ["af6ab244", "7dc64174", "9249f4a8", "52df94a3", "e9b5c26a", "738a9dff"], "player61_genes_hexa_list": ["c2151529", "3ee8522d", "c61e8cd3", "8e439f75", "c39a9818", "5b8dbf19"], "player62_genes_hexa_list": ["58cce358", "c3395c55", "fe98a9f3", "fab5acae", "ea5b5297", "9d26fef1"], "player63_genes_hexa_list": ["eac32c59", "497bd955", "b71c7315", "2c176397", "1d53a266", "7fb5ec45"], "player64_genes_hexa_list": ["af6ab244", "7dc64174", "9249f4a8", "52df94a3", "e9b5c26a", "738a9dff"], "player65_genes_hexa_list": ["655d8b2c", "93a531f7", "eb5aacfb", "d73b33da", "3aa443eb", "8127c769"], "player66_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d"], "player67_genes_hexa_list": ["58cce358", "c3395c55", "fe98a9f3", "fab5acae", "ea5b5297", "9d26fef1"], "player68_genes_hexa_list": ["dee7394b", "4c2764f6", "5ee997c5", "55e1471c", "8b9eebb9", "6f25bf22"], "player69_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d"], "player70_genes_hexa_list": ["3c491ee1", "f35afd18", "98c3c132", "5b8d5bb5", "6fafcd77", "7f3f7776"], "player71_genes_hexa_list": ["a6a3f6f4", "97398cf2", "3f44acb1", "e59618d6", "886c6956", "4b4569ed"], "player72_genes_hexa_list": ["45525ba8", "faf265be", "219b1762", "c38a12c3", "9b8874e2", "8c6cc5b3"], "player73_genes_hexa_list": ["58cce358", "c3395c55", "fe98a9f3", "fab5acae", "ea5b5297", "9d26fef1"], "player74_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d"], "player75_genes_hexa_list": ["2c9765b6", "5c926f83", "1baea497", "398fff42", "4b3d68af", "2c691ecb"], "player76_genes_hexa_list": ["487d365b", "4d19dc31", "cfb5cb6a", "79b2efbc", "13ec8288", "51721bd2"], "player77_genes_hexa_list": ["58cce358", "c3395c55", "fe98a9f3", "fab5acae", "ea5b5297", "9d26fef1"], "player78_genes_hexa_list": ["43eb8eb8", "cf8f886f", "47d64851", "5c447f6e", "66719135", "e548ad6d"], "player79_genes_hexa_list": ["af6ab244", "7dc64174", "9249f4a8", "52df94a3", "e9b5c26a", "738a9dff"], "player80_genes_hexa_list": ["8cff3354", "42279313", "3f97f687", "8d729359", "bee3f9f4", "7bc37d16"], "player81_genes_hexa_list": ["a37c5317", "46f42ba5", "722ecddf", "9d7172db", "95f3a87b", "575fed1f"], "player82_genes_hexa_list": ["eac32c59", "497bd955", "b71c7315", "2c176397", "1d53a266", "7fb5ec45"], "player83_genes_hexa_list": ["f91eaf29", "ef8adaae", "e6ab51f2", "87c515d7", "f31369a8", "42fbc7d1"], "player84_genes_hexa_list": ["2c9765b6", "5c926f83", "1baea497", "398fff42", "4b3d68af", "2c691ecb"], "player85_genes_hexa_list": ["af6ab244", "7dc64174", "9249f4a8", "52df94a3", "e9b5c26a", "738a9dff"], "player86_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d"], "player87_genes_hexa_list": ["2c9765b6", "5c926f83", "1baea497", "398fff42", "4b3d68af", "2c691ecb"], "player88_genes_hexa_list": ["af6ab244", "7dc64174", "9249f4a8", "52df94a3", "e9b5c26a", "738a9dff"], "player89_genes_hexa_list": ["b926c83d", "ff3f41fe", "536857d9", "df52c3bf", "27d3ccb2", "1a4f91ba"], "player90_genes_hexa_list": ["af6ab244", "7dc64174", "9249f4a8", "52df94a3", "e9b5c26a", "738a9dff"], "player91_genes_hexa_list": ["58cce358", "c3395c55", "fe98a9f3", "fab5acae", "ea5b5297", "9d26fef1"], "player92_genes_hexa_list": ["af6ab244", "7dc64174", "9249f4a8", "52df94a3", "e9b5c26a", "738a9dff"], "player93_genes_hexa_list": ["a6a3f6f4", "97398cf2", "3f44acb1", "e59618d6", "886c6956", "4b4569ed"], "player94_genes_hexa_list": ["655d8b2c", "93a531f7", "eb5aacfb", "d73b33da", "3aa443eb", "8127c769"], "player95_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d"], "player96_genes_hexa_list": ["2c9765b6", "5c926f83", "1baea497", "398fff42", "4b3d68af", "21691ecb"], "player97_genes_hexa_list": ["813c927b", "b8e232a2", "7e2a4e22", "b484c6fa", "6ae49743", "817d64fc"], "player98_genes_hexa_list": ["af6ab244", "7dc64174", "9249f4a8", "52df94a3", "e9b5c26a", "738a9dff"], "player99_genes_hexa_list": ["c2151529", "3ee8522d", "c61e8cd3", "8e439f75", "c39a9818", "5b8dbf19"], "player100_genes_hexa_list": ["b926c83d", "ff3f41fe", "536857d9", "df52c3bf", "27d3ccb2", "1a4f91ba"], "player101_genes_hexa_list": ["7545d2a5", "bbc1e45f", "3fc43862", "61ce92d8", "e37dfae4", "a54926ad"], "player102_genes_hexa_list": ["2c9765b6", "5c926f83", "1baea497", "398fff42", "4b3d68af", "2c691ecb"], "player103_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d"], "player104_genes_hexa_list": ["dee7394b", "4c2764f6", "5ee997c5", "55e1471c", "8b9eebb9", "6f25bf22"], "player105_genes_hexa_list": ["a6a3f6f4", "97398cf2", "3f44acb1", "e59618d6", "886c6956", "4b4569ed"], "player106_genes_hexa_list": ["15b1415a", "592e238d", "cfc67b5d", "ec835557", "94cbd5aa", "67dae8dd"], "player107_genes_hexa_list": ["2222c691", "78dd5f12", "798cb6cf", "bc93efac", "83e631d4", "534c1279"], "player108_genes_hexa_list": ["c1ac843c", "32bf18da", "b5eb936b", "77a8aad8", "e5252d1a", "9d3d6c5e"], "player109_genes_hexa_list": ["487d365b", "4d19dc31", "cfb5cb6a", "79b2efbc", "13ec8288", "51721bd2"], "player110_genes_hexa_list": ["58cce358", "c3395c55", "fe98a9f3", "fab5acae", "ea5b5297", "9d26fef1"], "player111_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d"], "player112_genes_hexa_list": ["f91eaf29", "ef8adaae", "e6ab51f2", "87c515d7", "f31369a8", "42fbc7d1"], "player113_genes_hexa_list": ["af6ab244", "7dc64174", "9249f4a8", "52df94a3", "e9b5c26a", "738a9dff"], "player114_genes_hexa_list": ["8cff3354", "42279313", "3f97f687", "8d729359", "bee3f9f4", "7bc37d16"], "player115_genes_hexa_list": ["a37c5317", "46f42ba5", "722ecddf", "9d7172db", "95f3a87b", "575fed1f"], "player116_genes_hexa_list": ["c1ac843c", "32bf18da", "b5eb936b", "77a8aad8", "e5252d1a", "9d3d6c5e"], "player117_genes_hexa_list": ["eac32c59", "497bd955", "b71c7315", "2c176397", "1d53a266", "7fb5ec45"], "player118_genes_hexa_list": ["f91eaf29", "ef8adaae", "e6ab51f2", "87c515d7", "f31369a8", "42fbc7d1"], "player119_genes_hexa_list": ["af6ab244", "7dc64174", "9249f4a8", "52df94a3", "e9b5c26a", "738a9dff"], "player120_genes_hexa_list": ["c1ac843c", "32bf18da", "b5eb936b", "77a8aad8", "e5252d1a", "9d3d6c5e"], "player121_genes_hexa_list": ["a6a3f6f4", "97398cf2", "3f44acb1", "e59618d6", "886c6956", "4b4569ed"], "player122_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d"], "player123_genes_hexa_list": ["2c9765b6", "5c926f83", "1baea497", "398fff42", "4b3d68af", "2c691ecb"], "player124_genes_hexa_list": ["af6ab244", "7dc64174", "9249f4a8", "52df94a3", "e9b5c26a", "738a9dff"], "player125_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d"], "player126_genes_hexa_list": ["b16a5f36", "9834a471", "5571cb9b", "9ace65a6", "db7e173d", "2cd35ea5"], "player127_genes_hexa_list": ["af6ab244", "7dc64174", "9249f4a8", "52df94a3", "e9b5c26a", "738a9dff"], "player128_genes_hexa_list": ["eac32c59", "497bd955", "b71c7315", "2c176397", "1d53a266", "7fb5ec45"], "player129_genes_hexa_list": ["2c9765b6", "5c926f83", "1baea497", "398fff42", "4b3d68af", "2c691ecb"], "player130_genes_hexa_list": ["813c927b", "b8e232a2", "7e2a4e22", "b484c6fa", "6ae49743", "817d64fc"], "player131_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d"], "player132_genes_hexa_list": ["8883d5cd", "14bdc898", "53644781", "fdccff28", "c5b3d7a5", "b6437ec5"], "player133_genes_hexa_list": ["af6ab244", "7dc64174", "9249f4a8", "52df94a3", "e9b5c26a", "738a9dff"], "player134_genes_hexa_list": ["af6ab244", "7dc64174", "9249f4a8", "52df94a3", "e9b5c26a", "738a9dff"], "player135_genes_hexa_list": ["8cff3354", "42279313", "3f97f687", "8d729359", "bee3f9f4", "7bc37d16"], "player136_genes_hexa_list": ["eac32c59", "497bd955", "b71c7315", "2c176397", "1d53a266", "7fb5ec45"], "player137_genes_hexa_list": ["2c9765b6", "5c926f83", "1baea497", "398fff42", "4b3d68af", "2c691ecb"], "player138_genes_hexa_list": ["af6ab244", "7dc64174", "9249f4a8", "52df94a3", "e9b5c26a", "738a9dff"]}
genes_hexa_dict=copy.deepcopy(players_genes_hexa_list)
for i in range(len(list(genes_hexa_dict.keys()))):
    genes_hexa_dict[f'player{i}']=genes_hexa_dict.pop(f'player{i}_genes_hexa_list')
restart_simulation(genes_hexa_dict,8,r'left_test_part_2.py',rf'D:\New_Evolution_left_final',200,200,inp=1)