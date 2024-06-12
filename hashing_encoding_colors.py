import hashlib
import random
import numpy as np

def encode_players_with_same_genes(genes_hexa_dict):
    colors_dict = {}
    for player, hexa_list in genes_hexa_dict.items():
        hexa_list = sorted(hexa_list)  #list and shuffles list should have same encoding
        hash_value = hashlib.md5(''.join(hexa_list).encode()).hexdigest()
        seed = int(hash_value, 16)%(2**32-1)
        np.random.seed(seed)
        colors_dict[player]=np.random.randint(1,255,3)
    return colors_dict

genes_hexa_dict={'player1': ['a91b5b06', '4fb23d3c', '753b50ef', 'f4e1c1e2', 'c84a2ff1', 'f8725c20', 'aaf04d8b', 'c9c48280'],
'player2': ['4f83d11a', '28be7ef6', '4c8f589d', '8bb4d3d5', '547a3269', 'ae72c1cf', 'fa04b556', 'a15c947d'],
'player3': ['19b6d72c', '268fcd2d', 'bd1c9db1', '7c5d6c5b', '4e3cbbcc', '0c9813bc', 'c32d9f89', '4e6837c0'],
'player4': ['b5c6603d', '1d69e418', 'a8ee5a24', 'b37f745b', 'a86bf5c3', '8f6bb4ab', 'bcbcc8a5', 'eb0e3ab3'],
'player5': ['1836cd54', 'c4d21490', 'b2898d0b', 'a3c76aa3', 'e1a58e8f', 'c1c67fb9', 'f0677256', '5689ff8d'],
'player6': ['eec4b504', '2d4e08bb', 'c7d9da34', '3fb5a3c1', 'ee7c0b95', 'f7641d94', '26c5de45', '1c259ae6'],
'player7': ['a8ee5a24','b5c6603d', '1d69e418', 'b37f745b', 'a86bf5c3', '8f6bb4ab', 'bcbcc8a5', 'eb0e3ab3']
}

#print(encode_players_with_same_genes(genes_hexa_dict))
