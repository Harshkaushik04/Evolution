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
    population=350
    default_population=350
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
            pygame.image.save(screen, rf'D:\New_Evolution_best_12_genome_length_images\generation{generation+1}\image{step+generation*steps_per_gen+1}.png')
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
        with open('test3.py', 'w') as f:
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

players_genes_hexa_list={"player0_genes_hexa_list": ["7197754a", "55a8383c", "d8d28172", "29424684", "a886c93b", "f8e6977c", "9f926d71", "42ffdac3", "5861f785", "46dc61c5", "91a68769", "f251ca47"], "player1_genes_hexa_list": ["18833474", "263ef1b9", "eb9b6bd7", "fdf38fad", "f34eec67", "a887e3bb", "e1aa7113", "c3368bd5", "e1636787", "444b7987", "c95f43a8", "329528a1"], "player2_genes_hexa_list": ["18833474", "263ef1b9", "eb9b6bd7", "fdf38fad", "f34eec67", "a887e3bb", "e1aa7113", "c3368bd5", "e1636787", "444b7987", "c95f43a8", "329528a1"], "player3_genes_hexa_list": ["c4dff7ac", "ab151d6b", "4616f45e", "11ae1cd2", "a88f14b5", "5be4746a", "c2b93243", "eb4992d7", "338bfe82", "e64e3499", "f72c4376", "f3db22f3"], "player4_genes_hexa_list": ["c4dff7ac", "ab151d6b", "4616f45e", "11ae1cd2", "a88f14b5", "5be4746a", "c2b93243", "eb4992d7", "338bfe82", "e64e3499", "f72c4376", "f3db22f3"], "player5_genes_hexa_list": ["c4dff7ac", "ab151d6b", "4616f45e", "11ae1cd2", "a88f14b5", "5be4746a", "c2b93243", "eb4992d7", "338bfe82", "e64e3499", "f72c4376", "f3db22f3"], "player6_genes_hexa_list": ["58cce358", "c3395c55", "fe98a9f3", "fab5acae", "ea5b5297", "9d26fef1", "ec423cfc", "3828332a", "f868fa6f", "c1f655a8", "5f75d7b7", "c125a16b"], "player7_genes_hexa_list": ["58cce358", "c3395c55", "fe98a9f3", "fab5acae", "ea5b5297", "9d26fef1", "ec423cfc", "3828332a", "f868fa6f", "c1f655a8", "5f75d7b7", "c125a16b"], "player8_genes_hexa_list": ["58cce358", "c3395c55", "fe98a9f3", "fab5acae", "ea5b5297", "9d26fef1", "ec423cfc", "3828332a", "f868fa6f", "c1f655a8", "5f75d7b7", "c125a16b"], "player9_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d", "77e3bb42", "4ebb7244", "3f4ec3e2", "aa57ceb8", "f659fe26", "731cf4fc"], "player10_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d", "77e3bb42", "4ebb7244", "3f4ec3e2", "aa57ceb8", "f659fe26", "731cf4fc"], "player11_genes_hexa_list": ["baf3d634", "a1fe9341", "467474b7", "954431a8", "4836f413", "86a7368d", "77e3bb42", "4ebb7244", "3f4ec3e2", "aa57ceb8", "f659fe26", "731cf4fc"], "player12_genes_hexa_list": ["1e55c5d7", "96237b79", "67372124", "9a99667b", "3c1a3c4c", "5afe362b", "be5316f9", "e8b6f63e", "1281b6ba", "e2a9661d", "c68955f7", "2611cd54"], "player13_genes_hexa_list": ["1e55c5d7", "96237b79", "67372124", "9a99667b", "3c1a3c4c", "5afe362b", "be5316f9", "e8b6f63e", "1281b6ba", "e2a9661d", "c68955f7", "2611cd54"], "player14_genes_hexa_list": ["5d6c9421", "bbbc25c5", "8357855b", "4b7668f8", "b62b7752", "7d373213", "42e9fe66", "ad78392f", "f5c5f5b7", "79917b1b", "48967141", "327cba4b"], "player15_genes_hexa_list": ["b95c8266", "6267e5df", "7bf7b5fb", "124edad9", "8a3f388d", "fb712173", "41da85b1", "53264146", "86a77556", "651b39b3", "d3bb97bf", "5355aef5"], "player16_genes_hexa_list": ["b8d1d951", "f1cc68e6", "f82d495d", "d4a27234", "8241e93e", "918add4f", "74964efd", "7bd27afb", "a4535bf1", "51ebde38", "98bd42a4", "d7b62534"], "player17_genes_hexa_list": ["9b5b9d35", "688e36d6", "842291ac", "439e878f", "d3886297", "ed2b6a5f", "5d9bf27e", "b56ca4f7", "b5a66168", "668143db", "38c576f9", "e3522ab5"], "player18_genes_hexa_list": ["9b5b9d35", "688e36d6", "842291ac", "439e878f", "d3886297", "ed2b6a5f", "5d9bf27e", "b56ca4f7", "b5a66168", "668143db", "38c576f9", "e3522ab5"], "player19_genes_hexa_list": ["3b477a94", "3b882614", "949dd7be", "534d1431", "4ddef121", "e47adfc1", "df8f7c83", "fe16212e", "de48a157", "4675d5bd", "74564588", "6c912dbb"], "player20_genes_hexa_list": ["813c927b", "b8e232a2", "7e2a4e22", "b484c6fa", "6ae49743", "817d64fc", "f23b837b", "8b565b34", "338546fb", "8bedfd55", "b1b8a837", "ed7bcdb5"], "player21_genes_hexa_list": ["813c927b", "b8e232a2", "7e2a4e22", "b484c6fa", "6ae49743", "817d64fc", "f23b837b", "8b565b34", "338546fb", "8bedfd55", "b1b8a837", "ed7bcdb5"], "player22_genes_hexa_list": ["813c927b", "b8e232a2", "7e2a4e22", "b484c6fa", "6ae49743", "817d64fc", "f23b837b", "8b565b34", "338546fb", "8bedfd55", "b1b8a837", "ed7bcdb5"], "player23_genes_hexa_list": ["813c927b", "b8e232a2", "7e2a4e22", "b484c6fa", "6ae49743", "817d64fc", "f23b837b", "8b565b34", "338546fb", "8bedfd55", "b1b8a837", "ed7bcdb5"], "player24_genes_hexa_list": ["e9ad32c7", "6cc325ae", "a7fdce21", "b9df89c9", "c93cfed5", "2ee71112", "d687571f", "649e946c", "6779e4c9", "4967815e", "f7d52eb2", "bb3ef296"], "player25_genes_hexa_list": ["655d8b2c", "93a531f7", "eb5aacfb", "d73b33da", "3aa443eb", "8127c769", "edb38a8e", "2d5a1e84", "d9565ed4", "47acfe48", "781617de", "d8324ce1"], "player26_genes_hexa_list": ["655d8b2c", "93a531f7", "eb5aacfb", "d73b33da", "3aa443eb", "8127c769", "edb38a8e", "2d5a1e84", "d9565ed4", "47acfe48", "781617de", "d8324ce1"], "player27_genes_hexa_list": ["63ace596", "13eb8b43", "9c97c7df", "d23d53f1", "1439152b", "a2429755", "6da2b625", "74fabc12", "fdd82cab", "8cf153f9", "c425442b", "9768a424"], "player28_genes_hexa_list": ["63ace596", "13eb8b43", "9c97c7df", "d23d53f1", "1439152b", "a2429755", "6da2b625", "74fabc12", "fdd82cab", "8cf153f9", "c425442b", "9768a424"], "player29_genes_hexa_list": ["59469ea7", "2f2fdf3d", "f589f76a", "5db13a7f", "aa15d2fd", "6bdeb38c", "d429548f", "8e125396", "2b6e91d8", "b8e1e13d", "fc72d51b", "4d1bd613"], "player30_genes_hexa_list": ["59469ea7", "2f2fdf3d", "f589f76a", "5db13a7f", "aa15d2fd", "6bdeb38c", "d429548f", "8e125396", "2b6e91d8", "b8e1e13d", "fc72d51b", "4d1bd613"], "player31_genes_hexa_list": ["59469ea7", "2f2fdf3d", "f589f76a", "5db13a7f", "aa15d2fd", "6bdeb38c", "d429548f", "8e125396", "2b6e91d8", "b8e1e13d", "fc72d51b", "4d1bd613"], "player32_genes_hexa_list": ["244ca37d", "8854e323", "da722e1f", "db539185", "e94e1191", "8965af13", "e98131ca", "364df13b", "d97a518d", "1d56ed4b", "f6965fb9", "13771a6e"], "player33_genes_hexa_list": ["851a3bdb", "a8744357", "159828bf", "daee5fea", "459dd257", "8969bcae", "654ba51b", "918bcfd7", "ecd743c2", "3e2d873b", "caf7d21b", "6f2c35f9"], "player34_genes_hexa_list": ["73531932", "34f1f32f", "dbbc42c6", "9f83aef3", "d661481f", "2d2c5d37", "5c1d5444", "da6cc372", "dd7e21c3", "67dfecb9", "eaa1ecdc", "9983378c"], "player35_genes_hexa_list": ["73531932", "34f1f32f", "dbbc42c6", "9f83aef3", "d661481f", "2d2c5d37", "5c1d5444", "da6cc372", "dd7e21c3", "67dfecb9", "eaa1ecdc", "9983378c"], "player36_genes_hexa_list": ["73531932", "34f1f32f", "dbbc42c6", "9f83aef3", "d661481f", "2d2c5d37", "5c1d5444", "da6cc372", "dd7e21c3", "67dfecb9", "eaa1ecdc", "9983378c"], "player37_genes_hexa_list": ["73531932", "34f1f32f", "dbbc42c6", "9f83aef3", "d661481f", "2d2c5d37", "5c1d5444", "da6cc372", "dd7e21c3", "67dfecb9", "eaa1ecdc", "9983378c"], "player38_genes_hexa_list": ["73531932", "34f1f32f", "dbbc42c6", "9f83aef3", "d661481f", "2d2c5d37", "5c1d5444", "da6cc372", "dd7e21c3", "67dfecb9", "eaa1ecdc", "9983378c"], "player39_genes_hexa_list": ["73531932", "34f1f32f", "dbbc42c6", "9f83aef3", "d661481f", "2d2c5d37", "5c1d5444", "da6cc372", "dd7e21c3", "67dfecb9", "eaa1ecdc", "9983378c"], "player40_genes_hexa_list": ["73531932", "34f1f32f", "dbbc42c6", "9f83aef3", "d661481f", "2d2c5d37", "5c1d5444", "da6cc372", "dd7e21c3", "67dfecb9", "eaa1ecdc", "9983378c"], "player41_genes_hexa_list": ["73531932", "34f1f32f", "dbbc42c6", "9f83aef3", "d661481f", "2d2c5d37", "5c1d5444", "da6cc372", "dd7e21c3", "67dfecb9", "eaa1ecdc", "9983378c"], "player42_genes_hexa_list": ["9137fb1a", "671f44d3", "9a48d87a", "e2566ed5", "37cdd3d3", "4b2639ca", "af93cdd3", "4fa616f4", "bf9884ae", "83b75d86", "74824669", "ca45cea7"], "player43_genes_hexa_list": ["9137fb1a", "671f44d3", "9a48d87a", "e2566ed5", "37cdd3d3", "4b2639ca", "af93cdd3", "4fa616f4", "bf9884ae", "83b75d86", "74824669", "ca45cea7"], "player44_genes_hexa_list": ["9137fb1a", "671f44d3", "9a48d87a", "e2566ed5", "37cdd3d3", "4b2639ca", "af93cdd3", "4fa616f4", "bf9884ae", "83b75d86", "74824669", "ca45cea7"], "player45_genes_hexa_list": ["9137fb1a", "671f44d3", "9a48d87a", "e2566ed5", "37cdd3d3", "4b2639ca", "af93cdd3", "4fa616f4", "bf9884ae", "83b75d86", "74824669", "ca45cea7"], "player46_genes_hexa_list": ["9137fb1a", "671f44d3", "9a48d87a", "e2566ed5", "37cdd3d3", "4b2639ca", "af93cdd3", "4fa616f4", "bf9884ae", "83b75d86", "74824669", "ca45cea7"], "player47_genes_hexa_list": ["9137fb1a", "671f44d3", "9a48d87a", "e2566ed5", "37cdd3d3", "4b2639ca", "af93cdd3", "4fa616f4", "bf9884ae", "83b75d86", "74824669", "ca45cea7"], "player48_genes_hexa_list": ["9137fb1a", "671f44d3", "9a48d87a", "e2566ed5", "37cdd3d3", "4b2639ca", "af93cdd3", "4fa616f4", "bf9884ae", "83b75d86", "74824669", "ca45cea7"], "player49_genes_hexa_list": ["9137fb1a", "671f44d3", "9a48d87a", "e2566ed5", "37cdd3d3", "4b2639ca", "af93cdd3", "4fa616f4", "bf9884ae", "83b75d86", "74824669", "ca45cea7"], "player50_genes_hexa_list": ["9137fb1a", "671f44d3", "9a48d87a", "e2566ed5", "37cdd3d3", "4b2639ca", "af93cdd3", "4fa616f4", "bf9884ae", "83b75d86", "74824669", "ca45cea7"], "player51_genes_hexa_list": ["4774e31f", "b8f6263f", "e877b4a3", "42f19bfd", "8562935d", "66b18bc4", "5393d816", "a372b666", "18e3d5cd", "ef7b5c78", "c37eb579", "f9f349af"], "player52_genes_hexa_list": ["54eeb994", "ceb87dd4", "f155bbfa", "67e4524e", "daffdea6", "96863e9d", "91ac5124", "ad1b3eaf", "598caafa", "ac1ebe81", "d9e24c2a", "478f9ea8"], "player53_genes_hexa_list": ["5fcf43e2", "2926b713", "715f557d", "856f34b6", "7b248222", "5edc8e52", "385519b7", "34c66cec", "6797dd25", "7aa8611c", "37d79177", "5a436a69"], "player54_genes_hexa_list": ["5fcf43e2", "2926b713", "715f557d", "856f34b6", "7b248222", "5edc8e52", "385519b7", "34c66cec", "6797dd25", "7aa8611c", "37d79177", "5a436a69"], "player55_genes_hexa_list": ["1e55c5d7", "96237b79", "67372124", "9a99667b", "3c1a3c4c", "5afe362b", "be5316f9", "e8b6f63e", "1281b6ba", "e2a9661d", "c68955f7", "2611cd54"], "player56_genes_hexa_list": ["1e55c5d7", "96237b79", "67372124", "9a99667b", "3c1a3c4c", "5afe362b", "be5316f9", "e8b6f63e", "1281b6ba", "e2a9661d", "c68955f7", "2611cd54"], "player57_genes_hexa_list": ["e817b31b", "e319c486", "a8b51e2c", "c931afbf", "d4368586", "ff5868ba", "98772b3f", "d7e557aa", "5fe555dd", "95124119", "d3628ba8", "24622eba"], "player58_genes_hexa_list": ["e9ad32c7", "6cc325ae", "a7fdce21", "b9df89c9", "c93cfed5", "2ee71112", "d687571f", "649e946c", "6779e4c9", "4967815e", "f7d52eb2", "bb3ef296"], "player59_genes_hexa_list": ["e9ad32c7", "6cc325ae", "a7fdce21", "b9df89c9", "c93cfed5", "2ee71112", "d687571f", "649e946c", "6779e4c9", "4967815e", "f7d52eb2", "bb3ef296"], "player60_genes_hexa_list": ["e9ad32c7", "6cc325ae", "a7fdce21", "b9df89c9", "c93cfed5", "2ee71112", "d687571f", "649e946c", "6779e4c9", "4967815e", "f7d52eb2", "bb3ef296"], "player61_genes_hexa_list": ["ae3a2348", "3d78bd8c", "6b7b1215", "16a356bf", "f85b3282", "b7c392b1", "48531919", "1aaa5a67", "15c7644a", "f69fcdf4", "76f5896c", "f228ce73"], "player62_genes_hexa_list": ["ae3a2348", "3d78bd8c", "6b7b1215", "16a356bf", "f85b3282", "b7c392b1", "48531919", "1aaa5a67", "15c7644a", "f69fcdf4", "76f5896c", "f228ce73"], "player63_genes_hexa_list": ["8c95d556", "2fcfab5e", "a6822241", "2dcdb294", "8229f74f", "e52d536f", "b8e9ccae", "c19fc417", "1f42e9cc", "9e81ac65", "baaac772", "32bd2b3d"], "player64_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player65_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player66_genes_hexa_list": ["4e115536", "4f541dae", "51d4c321", "d2eab9ef", "8691d9cb", "ccf63a7e", "32254e93", "b7f99e2a", "27a9f6fc", "c46bbce1", "17db59df", "7636dea5"], "player67_genes_hexa_list": ["63ace596", "13eb8b43", "9c97c7df", "d23d53f1", "1439152b", "a2429755", "6da2b625", "74fabc12", "fdd82cab", "8cf153f9", "c425442b", "9768a424"], "player68_genes_hexa_list": ["63ace596", "13eb8b43", "9c97c7df", "d23d53f1", "1439152b", "a2429755", "6da2b625", "74fabc12", "fdd82cab", "8cf153f9", "c425442b", "9768a424"], "player69_genes_hexa_list": ["18833474", "263ef1b9", "eb9b6bd7", "fdf38fad", "f34eec67", "a887e3bb", "e1aa7113", "c3368bd5", "e1636787", "444b7987", "c95f43a8", "329528a1"], "player70_genes_hexa_list": ["18833474", "263ef1b9", "eb9b6bd7", "fdf38fad", "f34eec67", "a887e3bb", "e1aa7113", "c3368bd5", "e1636787", "444b7987", "c95f43a8", "329528a1"], "player71_genes_hexa_list": ["18833474", "263ef1b9", "eb9b6bd7", "fdf38fad", "f34eec67", "a887e3bb", "e1aa7113", "c3368bd5", "e1636787", "444b7987", "c95f43a8", "329528a1"], "player72_genes_hexa_list": ["c4dff7ac", "ab151d6b", "4616f45e", "11ae1cd2", "a88f14b5", "5be4746a", "c2b93243", "eb4992d7", "338bfe82", "e64e3499", "f72c4376", "f3db22f3"], "player73_genes_hexa_list": ["c4dff7ac", "ab151d6b", "4616f45e", "11ae1cd2", "a88f14b5", "5be4746a", "c2b93243", "eb4992d7", "338bfe82", "e64e3499", "f72c4376", "f3db22f3"], "player74_genes_hexa_list": ["b8d1d951", "f1cc68e6", "f82d495d", "d4a27234", "8241e93e", "918add4f", "74964efd", "7bd27afb", "a4535bf1", "51ebde38", "98bd42a4", "d7b62534"], "player75_genes_hexa_list": ["b8d1d951", "f1cc68e6", "f82d495d", "d4a27234", "8241e93e", "918add4f", "74964efd", "7bd27afb", "a4535bf1", "51ebde38", "98bd42a4", "d7b62534"], "player76_genes_hexa_list": ["e9ad32c7", "6cc325ae", "a7fdce21", "b9df89c9", "c93cfed5", "2ee71112", "d687571f", "649e946c", "6779e4c9", "4967815e", "f7d52eb2", "bb3ef296"], "player77_genes_hexa_list": ["e9ad32c7", "6cc325ae", "a7fdce21", "b9df89c9", "c93cfed5", "2ee71112", "d687571f", "649e946c", "6779e4c9", "4967815e", "f7d52eb2", "bb3ef296"], "player78_genes_hexa_list": ["2e83b87d", "b592c4a5", "f679f9be", "31f2da85", "37793b8e", "eaa1d36a", "2f3d529a", "667625d3", "18723352", "c9e9e8a2", "1b6331c5", "c9e77ec2"], "player79_genes_hexa_list": ["ae3a2348", "3d78bd8c", "6b7b1215", "16a356bf", "f85b3282", "b7c392b1", "48531919", "1aaa5a67", "15c7644a", "f69fcdf4", "76f5896c", "f228ce73"], "player80_genes_hexa_list": ["ae3a2348", "3d78bd8c", "6b7b1215", "16a356bf", "f85b3282", "b7c392b1", "48531919", "1aaa5a67", "15c7644a", "f69fcdf4", "76f5896c", "f228ce73"], "player81_genes_hexa_list": ["63ace596", "13eb8b43", "9c97c7df", "d23d53f1", "1439152b", "a2429755", "6da2b625", "74fabc12", "fdd82cab", "8cf153f9", "c425442b", "9768a424"], "player82_genes_hexa_list": ["244ca37d", "8854e323", "da722e1f", "db539185", "e94e1191", "8965af13", "e98131ca", "364df13b", "d97a518d", "1d56ed4b", "f6965fb9", "13771a6e"], "player83_genes_hexa_list": ["7cfe242d", "ef6bd5f8", "14d65a34", "5f9921dd", "976c973f", "b8ba917e", "6faecbf3", "bdf63a19", "92e4ec78", "cacb8dc3", "98a4cc77", "41595fd1"], "player84_genes_hexa_list": ["9137fb1a", "671f44d3", "9a48d87a", "e2566ed5", "37cdd3d3", "4b2639ca", "af93cdd3", "4fa616f4", "bf9884ae", "83b75d86", "74824669", "ca45cea7"], "player85_genes_hexa_list": ["9137fb1a", "671f44d3", "9a48d87a", "e2566ed5", "37cdd3d3", "4b2639ca", "af93cdd3", "4fa616f4", "bf9884ae", "83b75d86", "74824669", "ca45cea7"], "player86_genes_hexa_list": ["ec781d68", "7fbd5d75", "7cdbce37", "ce62631e", "c2b98ab2", "87d6625e", "8432cc93", "b14dd6cd", "9c77831f", "f1f93598", "e4fae7bf", "5a3619c8"], "player87_genes_hexa_list": ["18833474", "263ef1b9", "eb9b6bd7", "fdf38fad", "f34eec67", "a887e3bb", "e1aa7113", "c3368bd5", "e1636787", "444b7987", "c95f43a8", "329528a1"]}
genes_hexa_dict=copy.deepcopy(players_genes_hexa_list)
for i in range(len(list(genes_hexa_dict.keys()))):
    genes_hexa_dict[f'player{i}']=genes_hexa_dict.pop(f'player{i}_genes_hexa_list')
restart_simulation(genes_hexa_dict,4,'test3.py',rf'D:\New_Evolution_best_12_genome_length_images',350,350)