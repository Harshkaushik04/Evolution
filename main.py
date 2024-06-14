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
    population=300
    default_population=300
    steps_per_gen=120
    genome_length=12
    generations=500
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
            # for i in range(len(list(players_dict.keys()))):
                # if step%2==0:
                #     print(f'player{i} co_ordinates history::',players_dict['player'+str(i)].co_ordinates_history_list)
                #     print(f'player{i} rect co ordinates:', players_dict['player' + str(i)].co_ordinates_history_list)
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
            pygame.image.save(screen, rf'D:\New_Evolution_improved_12_genome_length_images\generation{generation+1}\image{step+generation*steps_per_gen+1}.png')
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
        with open('another_testing_file.py', 'w') as f:
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

players_genes_hexa_list={"player0_genes_hexa_list": ["1c2a1f74", "371aeadd", "5d53b896", "f2e37438", "eed8dfc7", "62f35ba4", "d8219341", "ad3d2ad5", "83f1ddf2", "f21cdfa5", "8df3a12d", "fea48f3c"], "player1_genes_hexa_list": ["1c2a1f74", "371aeadd", "5d53b896", "f2e37438", "eed8dfc7", "62f35ba4", "d8219341", "ad3d2ad5", "83f1ddf2", "f21cdfa5", "8df3a12d", "fea48f3c"], "player2_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player3_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player4_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player5_genes_hexa_list": ["33fe356a", "4a9a6439", "d8bca62d", "d19ffdba", "9bd79f58", "daa7c5c6", "ca79ee9e", "bf171fa2", "d2ae3886", "19a52933", "399fe738", "3be52d4d"], "player6_genes_hexa_list": ["33fe356a", "4a9a6439", "d8bca62d", "d19ffdba", "9bd79f58", "daa7c5c6", "ca79ee9e", "bf171fa2", "d2ae3886", "19a52933", "399fe738", "3be52d4d"], "player7_genes_hexa_list": ["33fe356a", "4a9a6439", "d8bca62d", "d19ffdba", "9bd79f58", "daa7c5c6", "ca79ee9e", "bf171fa2", "d2ae3886", "19a52933", "399fe738", "3be52d4d"], "player8_genes_hexa_list": ["33fe356a", "4a9a6439", "d8bca62d", "d19ffdba", "9bd79f58", "daa7c5c6", "ca79ee9e", "bf171fa2", "d2ae3886", "19a52933", "399fe738", "3be52d4d"], "player9_genes_hexa_list": ["33fe356a", "4a9a6439", "d8bca62d", "d19ffdba", "9bd79f58", "daa7c5c6", "ca79ee9e", "bf171fa2", "d2ae3886", "19a52933", "399fe738", "3be52d4d"], "player10_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player11_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player12_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player13_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player14_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player15_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player16_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player17_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player18_genes_hexa_list": ["1e55c5d7", "96237b79", "67372124", "9a99667b", "3c1a3c4c", "5afe362b", "be5316f9", "e8b6f63e", "1281b6ba", "e2a9661d", "c68955f7", "2611cd54"], "player19_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player20_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player21_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player22_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player23_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player24_genes_hexa_list": ["f497c16e", "7fefe5d2", "c42fd8e9", "7b7aa2fc", "b51df5a4", "37a8d3f5", "4cef14a8", "451a8a5e", "bf6f7b6e", "11881ee8", "99de4ebb", "583613c8"], "player25_genes_hexa_list": ["f497c16e", "7fefe5d2", "c42fd8e9", "7b7aa2fc", "b51df5a4", "37a8d3f5", "4cef14a8", "451a8a5e", "bf6f7b6e", "11881ee8", "99de4ebb", "583613c8"], "player26_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player27_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player28_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player29_genes_hexa_list": ["d7aeaeba", "21453dbd", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player30_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player31_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player32_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player33_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player34_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player35_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player36_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player37_genes_hexa_list": ["f497c16e", "7fefe5d2", "c42fd8e9", "7b7aa2fc", "b51df5a4", "37a8d3f5", "4cef14a8", "451a8a5e", "bf6f7b6e", "11881ee8", "99de4ebb", "583613c8"], "player38_genes_hexa_list": ["f497c16e", "7fefe5d2", "c42fd8e9", "7b7aa2fc", "b51df5a4", "37a8d3f5", "4cef14a8", "451a8a5e", "bf6f7b6e", "11881ee8", "99de4ebb", "583613c8"], "player39_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player40_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player41_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player42_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player43_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player44_genes_hexa_list": ["d7aeaeba", "21453d5d", "d72eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player45_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player46_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player47_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player48_genes_hexa_list": ["d7aeaeba", "21453dbd", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player49_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player50_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player51_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player52_genes_hexa_list": ["f497c16e", "7fefe5d2", "c42fd8e9", "7b7aa2fc", "b51df5a4", "37a8d3f5", "4cef14a8", "451a8a5e", "bf6f7b6e", "11881ee8", "99de4ebb", "583613c8"], "player53_genes_hexa_list": ["f497c16e", "7fefe5d2", "c42fd8e9", "7b7aa2fc", "b51df5a4", "37a8d3f5", "4cef14a8", "451a8a5e", "bf6f7b6e", "11881ee8", "99de4ebb", "583613c8"], "player54_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player55_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player56_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player57_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player58_genes_hexa_list": ["33fe356a", "4a9a6439", "d8bca62d", "d19ffdba", "9bd79f58", "daa7c5c6", "ca79ee9e", "bf171fa2", "d2ae3886", "19a52933", "399fe738", "3be52d4d"], "player59_genes_hexa_list": ["33fe356a", "4a9a6439", "d8bca62d", "d19ffdba", "9bd79f58", "daa7c5c6", "ca79ee9e", "bf171fa2", "d2ae3886", "19a52933", "399fe738", "3be52d4d"], "player60_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player61_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player62_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player63_genes_hexa_list": ["33fe356a", "4a9a6439", "d8bca62d", "d19ffdba", "9bd79f58", "daa7c5c6", "ca79ee9e", "bf171fa2", "d2ae3886", "19a52933", "399fe738", "3be52d4d"], "player64_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player65_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player66_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player67_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player68_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"]}
genes_hexa_dict=copy.deepcopy(players_genes_hexa_list)
for i in range(len(list(genes_hexa_dict.keys()))):
    genes_hexa_dict[f'player{i}']=genes_hexa_dict.pop(f'player{i}_genes_hexa_list')
restart_simulation(genes_hexa_dict,16)