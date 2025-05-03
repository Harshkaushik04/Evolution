import hashlib
import random
import numpy as np
def encode_players_with_same_genes(genes_hexa_dict):
    colors_dict = {}
    seeds_list=[]
    seeds_set=set()
    for player_name, hexa_list in genes_hexa_dict.items():
        hexa_list = sorted(hexa_list)  #list and shuffles list should have same encoding
        hash_value = hashlib.md5(''.join(hexa_list).encode()).hexdigest()
        seed = int(hash_value, 16)%(2**32-1)
        seeds_list.append(seed)
        seeds_set.add(seed)
        np.random.seed(seed)
        colors_dict[player_name]=np.random.randint(1,255,3)
    numbers_list=[]
    for i in range(len(list(seeds_set))):
        numbers_list.append(0)
    for i in range(len(list((seeds_set)))):
        for j in range(len(seeds_list)):
            if list(seeds_set)[i]==seeds_list[j]:
                numbers_list[i]+=1
    max_value=max(numbers_list)
    print('max value:',max_value)
    for i in range(len(numbers_list)):
        if max_value==numbers_list[i]:
            another_index_value=i
            print('another_index_value:',i)
            break
    max_hash_value=list(seeds_set)[another_index_value]
    print('max hash value:',max_hash_value)
    for i in range(len(seeds_list)):
        if max_hash_value==seeds_list[i]:
            index_value=i
            print('index value:',index_value)
            break
    counter=0
    for player_name,gene in genes_hexa_dict.items():
        if counter==index_value:
            max_gene=genes_hexa_dict[player_name]
            print('max_gene:',max_gene)
        counter += 1
    return colors_dict,max_gene,max_value

genes_hexa_dict={'player1': ['a91b5b06', '4fb23d3c', '753b50ef', 'f4e1c1e2', 'c84a2ff1', 'f8725c20', 'aaf04d8b', 'c9c48280'],
'player2': ['4f83d11a', '28be7ef6', '4c8f589d', '8bb4d3d5', '547a3269', 'ae72c1cf', 'fa04b556', 'a15c947d'],
'player3': ['19b6d72c', '268fcd2d', 'bd1c9db1', '7c5d6c5b', '4e3cbbcc', '0c9813bc', 'c32d9f89', '4e6837c0'],
'player4': ['b5c6603d', '1d69e418', 'a8ee5a24', 'b37f745b', 'a86bf5c3', '8f6bb4ab', 'bcbcc8a5', 'eb0e3ab3'],
'player5': ['1836cd54', 'c4d21490', 'b2898d0b', 'a3c76aa3', 'e1a58e8f', 'c1c67fb9', 'f0677256', '5689ff8d'],
'player6': ['eec4b504', '2d4e08bb', 'c7d9da34', '3fb5a3c1', 'ee7c0b95', 'f7641d94', '26c5de45', '1c259ae6'],
'player7': ['a8ee5a24','b5c6603d', '1d69e418', 'b37f745b', 'a86bf5c3', '8f6bb4ab', 'bcbcc8a5', 'eb0e3ab3']
}

print(encode_players_with_same_genes(genes_hexa_dict))
