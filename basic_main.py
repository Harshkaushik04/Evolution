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

players_genes_hexa_list={"player0_genes_hexa_list": ["a8e3dcaf", "41adc125", "bd3ab6cd", "3f8a4d55"], "player1_genes_hexa_list": ["a8e3dcaf", "41adc125", "bd3ab6cd", "3f8a4d55"], "player2_genes_hexa_list": ["a8e3dcaf", "41adc125", "bd3ab6cd", "3f8a4d55"], "player3_genes_hexa_list": ["a8e3dcaf", "41adc125", "bd3ab6cd", "3f8a4d55"], "player4_genes_hexa_list": ["ca4c5f17", "e7827ce5", "2d6a1516", "4f654815"], "player5_genes_hexa_list": ["ca4c5f17", "e7827ce5", "2d6a1516", "4f654815"], "player6_genes_hexa_list": ["d14a2a1f", "f8acc7c7", "eb6d6257", "ca4dc68c"], "player7_genes_hexa_list": ["a98a8449", "c5794e39", "4ee2f118", "1635ffda"], "player8_genes_hexa_list": ["a98a8449", "c5794e39", "4ee2f118", "1635ffda"], "player9_genes_hexa_list": ["35928e62", "fcb1d196", "4cfbe7ab", "228edc4f"], "player10_genes_hexa_list": ["8a546e61", "fca5f7c5", "a3b6ba98", "d1c84aef"], "player11_genes_hexa_list": ["7e3482cd", "e16af238", "b1aefd36", "21fba31c"], "player12_genes_hexa_list": ["7e3482cd", "e16af238", "b1aefd36", "21fba31c"], "player13_genes_hexa_list": ["7e3482cd", "e16af238", "b1aefd36", "21fba31c"], "player14_genes_hexa_list": ["7e3482cd", "e16af238", "b1aefd36", "21fba31c"], "player15_genes_hexa_list": ["8c735a95", "b7c9bb27", "993baee9", "de497ced"], "player16_genes_hexa_list": ["7a62d8a4", "55ae8cd5", "324e5f79", "93df6ece"], "player17_genes_hexa_list": ["7a62d8a4", "55ae8cd5", "324e5f79", "93df6ece"], "player18_genes_hexa_list": ["7a62d8a4", "55ae8cd5", "324e5f79", "93df6ece"], "player19_genes_hexa_list": ["9cd2a878", "aedfe7df", "a49d1db5", "8da383b9"], "player20_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419"], "player21_genes_hexa_list": ["1bcdf7d4", "18aec48a", "5ee94f63", "56e14d9a"], "player22_genes_hexa_list": ["1bcdf7d4", "18aec48a", "5ee94f63", "56e14d9a"], "player23_genes_hexa_list": ["1bcdf7d4", "18aec48a", "5ee94f63", "56e14d9a"], "player24_genes_hexa_list": ["1bcdf7d4", "18aec48a", "5ee94f63", "56e14d9a"], "player25_genes_hexa_list": ["a8e3dcaf", "41adc125", "bd3ab6cd", "3f8a4d55"], "player26_genes_hexa_list": ["a8e3dcaf", "41adc125", "bd3ab6cd", "3f8a4d55"], "player27_genes_hexa_list": ["a8e3dcaf", "41adc125", "bd3ab6cd", "3f8a4d55"], "player28_genes_hexa_list": ["6dfbaa46", "42578e89", "8b8dfd59", "aff7cb2c"], "player29_genes_hexa_list": ["ca4c5f17", "e7827ce5", "2d6a1516", "4f654815"], "player30_genes_hexa_list": ["76381fdc", "b1673cae", "54bf5333", "9874d81f"], "player31_genes_hexa_list": ["76381fdc", "b1673cae", "54bf5333", "9874d81f"], "player32_genes_hexa_list": ["76381fdc", "b1673cae", "54bf5333", "9874d81f"], "player33_genes_hexa_list": ["eac32c59", "497bd955", "b71c7315", "2c176397"], "player34_genes_hexa_list": ["a37c5317", "46f42ba5", "722ecddf", "9d7172db"], "player35_genes_hexa_list": ["a37c5317", "46f42ba5", "722ecddf", "9d7172db"], "player36_genes_hexa_list": ["a37c5317", "46f42ba5", "722ecddf", "9d7172db"], "player37_genes_hexa_list": ["a37c5317", "46f42ba5", "722ecddf", "9d7172db"], "player38_genes_hexa_list": ["b8a87ffd", "9441ab6f", "9f923489", "84ab143f"], "player39_genes_hexa_list": ["325bae55", "47bb3b3c", "22318e98", "5e288be6"], "player40_genes_hexa_list": ["9b58ee24", "1717a5b9", "19475b73", "9c546ffb"], "player41_genes_hexa_list": ["9eed1b68", "a35bcdc1", "2c44df93", "c8ad78ba"], "player42_genes_hexa_list": ["1e55c5d7", "96237b79", "67372124", "9a99667b"], "player43_genes_hexa_list": ["1e55c5d7", "96237b79", "67372124", "9a99667b"], "player44_genes_hexa_list": ["54eeb994", "ceb87dd4", "f155bbfa", "67e4524e"], "player45_genes_hexa_list": ["54eeb994", "ceb87dd4", "f155bbfa", "67e4524e"], "player46_genes_hexa_list": ["1bcdf7d4", "18aec48a", "5ee94f63", "56e14d9a"], "player47_genes_hexa_list": ["1bcdf7d4", "18aec48a", "5ee94f63", "56e14d9a"], "player48_genes_hexa_list": ["443c4a97", "d14dccd1", "536e5bd5", "893ca16b"], "player49_genes_hexa_list": ["ec781d68", "7fbd5d75", "7cdbce37", "ce62631e"], "player50_genes_hexa_list": ["a8e3dcaf", "41adc125", "bd3ab6cd", "3f8a4d55"], "player51_genes_hexa_list": ["a8e3dcaf", "41adc125", "bd3ab6cd", "3f8a4d55"], "player52_genes_hexa_list": ["a8e3dcaf", "41adc125", "bd3ab6cd", "3f8a4d55"], "player53_genes_hexa_list": ["a98a8449", "c5794e39", "4ee2f118", "1635ffda"], "player54_genes_hexa_list": ["a98a8449", "c5794e39", "4ee2f118", "1635ffda"], "player55_genes_hexa_list": ["b8a87ffd", "9441ab6f", "9f923489", "84ab143f"], "player56_genes_hexa_list": ["b8a87ffd", "9441ab6f", "9f923489", "84ab143f"], "player57_genes_hexa_list": ["2443d79c", "4ff81d7a", "5e794419", "dcfcbc88"], "player58_genes_hexa_list": ["2443d79c", "4ff81d7a", "5e794419", "dcfcbc88"], "player59_genes_hexa_list": ["35928e62", "fcb1d196", "4cfbe7ab", "228edc4f"], "player60_genes_hexa_list": ["317b7818", "fdb2ed3a", "1253cd65", "22b9187d"], "player61_genes_hexa_list": ["a8e3dcaf", "41adc125", "bd3ab6cd", "3f8a4d55"], "player62_genes_hexa_list": ["a8e3dcaf", "41adc125", "bd3ab6cd", "3f8a4d55"], "player63_genes_hexa_list": ["a8e3dcaf", "41adc125", "bd3ab6cd", "3f8a4d55"], "player64_genes_hexa_list": ["2c4352bd", "fa499428", "386b6fca", "aa5c5b1b"], "player65_genes_hexa_list": ["5fcf43e2", "2926b713", "715f557d", "856f34b6"], "player66_genes_hexa_list": ["5fcf43e2", "2926b713", "715f557d", "856f34b6"], "player67_genes_hexa_list": ["5fcf43e2", "2926b713", "715f557d", "856f34b6"], "player68_genes_hexa_list": ["ca4c5f17", "e7827ce5", "2d6a1516", "4f654815"], "player69_genes_hexa_list": ["ca4c5f17", "e7827ce5", "2d6a1516", "4f654815"], "player70_genes_hexa_list": ["d14a2a1f", "f8acc7c7", "eb6d6257", "ca4dc68c"], "player71_genes_hexa_list": ["d14a2a1f", "f8acc7c7", "eb6d6257", "ca4dc68c"], "player72_genes_hexa_list": ["a98a8449", "c5794e39", "4ee2f118", "1635ffda"], "player73_genes_hexa_list": ["a98a8449", "c5794e39", "4ee2f118", "1635ffda"], "player74_genes_hexa_list": ["35928e62", "fcb1d196", "4cfbe7ab", "228edc4f"], "player75_genes_hexa_list": ["8a546e61", "fca5f7c5", "a3b6ba98", "d1c84aef"], "player76_genes_hexa_list": ["8a546e61", "fca5f7c5", "a3b6ba98", "d1c84aef"], "player77_genes_hexa_list": ["7e3482cd", "e16af238", "b1aefd36", "21fba31c"], "player78_genes_hexa_list": ["7e3482cd", "e16af238", "b1aefd36", "21fba31c"], "player79_genes_hexa_list": ["7e3482cd", "e16af238", "b1aefd36", "21fba31c"], "player80_genes_hexa_list": ["7e3482cd", "e16af238", "b1aefd36", "21fba31c"], "player81_genes_hexa_list": ["7e3482cd", "e16af238", "b1aefd36", "21fba31c"], "player82_genes_hexa_list": ["8c735a95", "b7c9bb27", "993baee9", "de497ced"], "player83_genes_hexa_list": ["7a62d8a4", "55ae8cd5", "324e5f79", "93df6ece"], "player84_genes_hexa_list": ["7a62d8a4", "55ae8cd5", "324e5f79", "93df6ece"], "player85_genes_hexa_list": ["7a62d8a4", "55ae8cd5", "324e5f79", "93df6ece"], "player86_genes_hexa_list": ["9cd2a878", "aedfe7df", "a49d1db5", "8da383b9"], "player87_genes_hexa_list": ["9cd2a878", "aedfe7df", "a49d1db5", "8da383b9"], "player88_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419"], "player89_genes_hexa_list": ["54eeb994", "ceb87dd4", "f155bbfa", "67e4524e"], "player90_genes_hexa_list": ["1bcdf7d4", "18aec48a", "5ee94f63", "56e14d9a"], "player91_genes_hexa_list": ["1bcdf7d4", "18aec48a", "5ee94f63", "56e14d9a"], "player92_genes_hexa_list": ["1bcdf7d4", "18aec48a", "5ee94f63", "56e14d9a"], "player93_genes_hexa_list": ["df75c5fe", "46456e33", "32753caa", "bc7335af"], "player94_genes_hexa_list": ["df75c5fe", "46456e33", "32753caa", "bc7335af"], "player95_genes_hexa_list": ["66e11c18", "6f4e7c17", "15fcdaff", "c3444395"], "player96_genes_hexa_list": ["a8e3dcaf", "41adc125", "bd3ab6cd", "3f8a4d55"], "player97_genes_hexa_list": ["d12c79bd", "cb4b17a4", "5bdd1edf", "8ac7d72a"], "player98_genes_hexa_list": ["6dfbaa46", "42578e89", "8b8dfd59", "aff7cb2c"], "player99_genes_hexa_list": ["6dfbaa46", "42578e89", "8b8dfd59", "aff7cb2c"], "player100_genes_hexa_list": ["ca4c5f17", "e7827ce5", "2d6a1516", "4f654815"], "player101_genes_hexa_list": ["76381fdc", "b1673cae", "54bf5333", "9874d81f"], "player102_genes_hexa_list": ["76381fdc", "b1673cae", "54bf5333", "9874d81f"], "player103_genes_hexa_list": ["eac32c59", "497bd955", "b71c7315", "2c176397"], "player104_genes_hexa_list": ["eac32c59", "497bd955", "b71c7315", "2c176397"], "player105_genes_hexa_list": ["a37c5317", "46f42ba5", "722ecddf", "9d7172db"], "player106_genes_hexa_list": ["a37c5317", "46f42ba5", "722ecddf", "9d7172db"], "player107_genes_hexa_list": ["a37c5317", "46f42ba5", "722ecddf", "9d7172db"], "player108_genes_hexa_list": ["2443d79c", "4ff81d7a", "5e794419", "dcfcbc88"]}
genes_hexa_dict=copy.deepcopy(players_genes_hexa_list)
for i in range(len(list(genes_hexa_dict.keys()))):
    genes_hexa_dict[f'player{i}']=genes_hexa_dict.pop(f'player{i}_genes_hexa_list')
restart_simulation(genes_hexa_dict,7,'test4.py',rf'D:\New_Evolution_4_improved_genome_length_images',200,200)