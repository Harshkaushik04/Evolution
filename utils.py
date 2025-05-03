# input is 8 digit hexadecimal number converted to 32 digit binary
import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
import copy
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set the desired logging level

# Create a logger
logger = logging.getLogger(__name__)
def hexadecimal_to_binary(hex_value,binary_length=32):
    binary_value = bin(int(hex_value, 16))[2:].zfill(binary_length)
    return binary_value
# state_at_error={}
# l=[4,5,6,7,0,1]
# checkpoint = {}
# for i in range(6):
#     try:
#         result=1
#         # Some critical operation
#         result+=1/l[i]
#         # Save checkpoint
#         checkpoint = {'i': i, 'result': result}
#     except Exception as e:
#         logger.error(f"Error occurred at iteration {i}: {e}")
#         # Recover state from the last checkpoint
#         i = checkpoint['i']
#         result = checkpoint['result']
#         #print(checkpoint['result'])
#         break  # Exit the loop or handle the error appropriately

mutation_prob=0.5
decider=[0,1]
# inp=random.choices(decider,weights=[1-mutation_prob,mutation_prob])
# print(inp==[1])
# s=['a']

# change_decider=['1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
# char_to_change=random.choices(change_decider,weights=np.ones(15)/15)
# print(char_to_change)
# dict={'wow':[2,3]}
# dict['wow']=[5,6]
# print(type(dict.keys()))
# l=list(dict.keys())
# print(type(l))
# print(l)

# for i in range(1,14):
#     print(f'{i}. S{i}:')
# class wow:
#     def __init__(self,l,dicti):
#         self.l=l
#         self.dicti=dicti
#
#
# hi1=wow(5,{'wow':3})
# hi2=wow([4,5,6],{})
#
# new1=copy.deepcopy(hi1.l)
# new2=copy.deepcopy(hi1.dicti)

# hi1.l=1
# hi1.dicti['wow']=9
# print(new1)
# print(new2)
# #print(hi1!=hi2)
# new_var=hi1.new
# new_var=4
# print(hi1.new)
#print(pow(11,2))
# hi=wow(new=2)
# l=[hi,'wow']
# for i in l[:]:
#     l.remove(i)
# print(l)
# a=1
# b=2
# c=3
# print(min(a,b,c))
# x=1
# y='abc'
# z=5
# l=[x,y,z]
# l[0]=2
# print(x)

# l1=[1,2,3]
# l2=l1
# l1=[5,6,7]
# l3=[100,120]
# l3=l1
# print(l2)
# print(l3)

#print(type(hexadecimal_to_binary('f1351fe3')))

# dicti={'hi1':hi1,'hi2':hi2}
# print(type(dicti))
# assert(type(dicti)==dict)
# #for player_name,player in dicti.items():
#     #del dicti[player_name]  #gives error
# print(dicti)
# l=[1,2,3]
# new=random.choices(l,weights=np.ones(3)/3)
# # print(new,type(new))
# print(5 not in [i for i in range(5)])
# x={'wow':6}
# del x
# x={'wow':7}
# print(x)
# print(1)
# print('\n')
# print(2)
players=[]
players_genes_hexa_list={"player0_genes_hexa_list": ["1c2a1f74", "371aeadd", "5d53b896", "f2e37438", "eed8dfc7", "62f35ba4", "d8219341", "ad3d2ad5", "83f1ddf2", "f21cdfa5", "8df3a12d", "fea48f3c"], "player1_genes_hexa_list": ["1c2a1f74", "371aeadd", "5d53b896", "f2e37438", "eed8dfc7", "62f35ba4", "d8219341", "ad3d2ad5", "83f1ddf2", "f21cdfa5", "8df3a12d", "fea48f3c"], "player2_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player3_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player4_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player5_genes_hexa_list": ["33fe356a", "4a9a6439", "d8bca62d", "d19ffdba", "9bd79f58", "daa7c5c6", "ca79ee9e", "bf171fa2", "d2ae3886", "19a52933", "399fe738", "3be52d4d"], "player6_genes_hexa_list": ["33fe356a", "4a9a6439", "d8bca62d", "d19ffdba", "9bd79f58", "daa7c5c6", "ca79ee9e", "bf171fa2", "d2ae3886", "19a52933", "399fe738", "3be52d4d"], "player7_genes_hexa_list": ["33fe356a", "4a9a6439", "d8bca62d", "d19ffdba", "9bd79f58", "daa7c5c6", "ca79ee9e", "bf171fa2", "d2ae3886", "19a52933", "399fe738", "3be52d4d"], "player8_genes_hexa_list": ["33fe356a", "4a9a6439", "d8bca62d", "d19ffdba", "9bd79f58", "daa7c5c6", "ca79ee9e", "bf171fa2", "d2ae3886", "19a52933", "399fe738", "3be52d4d"], "player9_genes_hexa_list": ["33fe356a", "4a9a6439", "d8bca62d", "d19ffdba", "9bd79f58", "daa7c5c6", "ca79ee9e", "bf171fa2", "d2ae3886", "19a52933", "399fe738", "3be52d4d"], "player10_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player11_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player12_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player13_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player14_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player15_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player16_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player17_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player18_genes_hexa_list": ["1e55c5d7", "96237b79", "67372124", "9a99667b", "3c1a3c4c", "5afe362b", "be5316f9", "e8b6f63e", "1281b6ba", "e2a9661d", "c68955f7", "2611cd54"], "player19_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player20_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player21_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player22_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player23_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player24_genes_hexa_list": ["f497c16e", "7fefe5d2", "c42fd8e9", "7b7aa2fc", "b51df5a4", "37a8d3f5", "4cef14a8", "451a8a5e", "bf6f7b6e", "11881ee8", "99de4ebb", "583613c8"], "player25_genes_hexa_list": ["f497c16e", "7fefe5d2", "c42fd8e9", "7b7aa2fc", "b51df5a4", "37a8d3f5", "4cef14a8", "451a8a5e", "bf6f7b6e", "11881ee8", "99de4ebb", "583613c8"], "player26_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player27_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player28_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player29_genes_hexa_list": ["d7aeaeba", "21453dbd", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player30_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player31_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player32_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player33_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player34_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player35_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player36_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player37_genes_hexa_list": ["f497c16e", "7fefe5d2", "c42fd8e9", "7b7aa2fc", "b51df5a4", "37a8d3f5", "4cef14a8", "451a8a5e", "bf6f7b6e", "11881ee8", "99de4ebb", "583613c8"], "player38_genes_hexa_list": ["f497c16e", "7fefe5d2", "c42fd8e9", "7b7aa2fc", "b51df5a4", "37a8d3f5", "4cef14a8", "451a8a5e", "bf6f7b6e", "11881ee8", "99de4ebb", "583613c8"], "player39_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player40_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player41_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player42_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player43_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player44_genes_hexa_list": ["d7aeaeba", "21453d5d", "d72eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player45_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player46_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player47_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player48_genes_hexa_list": ["d7aeaeba", "21453dbd", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player49_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player50_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player51_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player52_genes_hexa_list": ["f497c16e", "7fefe5d2", "c42fd8e9", "7b7aa2fc", "b51df5a4", "37a8d3f5", "4cef14a8", "451a8a5e", "bf6f7b6e", "11881ee8", "99de4ebb", "583613c8"], "player53_genes_hexa_list": ["f497c16e", "7fefe5d2", "c42fd8e9", "7b7aa2fc", "b51df5a4", "37a8d3f5", "4cef14a8", "451a8a5e", "bf6f7b6e", "11881ee8", "99de4ebb", "583613c8"], "player54_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player55_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player56_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"], "player57_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player58_genes_hexa_list": ["33fe356a", "4a9a6439", "d8bca62d", "d19ffdba", "9bd79f58", "daa7c5c6", "ca79ee9e", "bf171fa2", "d2ae3886", "19a52933", "399fe738", "3be52d4d"], "player59_genes_hexa_list": ["33fe356a", "4a9a6439", "d8bca62d", "d19ffdba", "9bd79f58", "daa7c5c6", "ca79ee9e", "bf171fa2", "d2ae3886", "19a52933", "399fe738", "3be52d4d"], "player60_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player61_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player62_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player63_genes_hexa_list": ["33fe356a", "4a9a6439", "d8bca62d", "d19ffdba", "9bd79f58", "daa7c5c6", "ca79ee9e", "bf171fa2", "d2ae3886", "19a52933", "399fe738", "3be52d4d"], "player64_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player65_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player66_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player67_genes_hexa_list": ["d7aeaeba", "21453d5d", "472eddb6", "46d823fe", "23db7e2e", "2ac3fb26", "3fadb5ef", "46387622", "2bcf7551", "d1b914d8", "cb7b2bbf", "bcfc27c1"], "player68_genes_hexa_list": ["2a345da9", "1c6d41d4", "752ddf6f", "7b2e5419", "8afee823", "f7dba5e4", "7fc797b6", "bba943c5", "a5375494", "cbb2f8e3", "9ff18519", "1aeefc37"]}
for i in range(len(players_genes_hexa_list)):
    players_genes_hexa_list[f'player{i}']=players_genes_hexa_list.pop(f'player{i}_genes_hexa_list')
print(players_genes_hexa_list)