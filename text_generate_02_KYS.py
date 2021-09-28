

'''
Text Data Augmentation for 적기공격임박보고서 by KYS
'''
import re
import random
import glob
import pandas as pd
import os
from pathlib import Path
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--ratio', type=float, default=0.2, help='Shuffle ratio')

args = parser.parse_args()

class generate_02:
    def __init__(self, gold, iter_ratio): # Input : 보고서, 섞는 횟수, 몇개 생성할지
        
        self.sents = gold
        self.ratio = max(1, int(iter_ratio * len(gold)))
    
    def split_sent(self, doc):
        reObj = re.compile(r'[,!]') # ,와 !로 문장 split 
        temp_sents = reObj.split(doc)[:-1]
        #temp_sents[2:4] = ["".join(temp_sents[2:4])]
        temp_sents[0] = temp_sents[0] + "!" # 첫 번째 문장 ! 붙혀줌
        return temp_sents
 
    def random_swap(self, words, n): # 섞는 부분
        new_words = words.copy()
        for _ in range(n):
            new_words = self.swap_word(new_words)

        return new_words

    def swap_word(self, new_words):
        random_idx_1 = random.randint(0, len(new_words)-1)
        random_idx_2 = random_idx_1
        counter = 0

        while random_idx_2 == random_idx_1:
            random_idx_2 = random.randint(0, len(new_words)-1)
            counter += 1
            if counter > 3:
                return new_words

        new_words[random_idx_1], new_words[random_idx_2] = new_words[random_idx_2], new_words[random_idx_1]
        return new_words        

    def shuf_gold(self): # 동작 코드
        self.tot_shuf = []
        split_gold = self.split_sent(self.sents)

        shuf = self.random_swap(split_gold[1:], self.ratio)
        shuf.insert(0, split_gold[0]) # 맨 앞 OOO보고! 부분 앞에 붙히기
        self.tot_shuf.append(shuf)

        return list(map(list,list(set(map(tuple,self.tot_shuf)))))

if __name__ == "__main__":
    file_name = glob.glob('./txt_processed/비정형모의전장자료/2. 적기 공격 임박 보고서/*')
    new_folder_summary = './txt_processed/비정형모의전장자료/generate_summary/2. 적기 공격 임박 보고서'

    Path(new_folder_summary).mkdir(parents=True, exist_ok=True)

    print("Generate Start for 적기 공격 임박 보고서")
    for idx, txt_file in enumerate(tqdm(file_name,leave = True)) :
        with open(txt_file, 'r', encoding = 'UTF-8') as f:
            tmp = f.read()
        gen_sum = generate_02(re.sub('\n','',tmp).strip(),args.ratio).shuf_gold()
        
        with open(os.path.join(new_folder_summary,os.path.basename(txt_file)[:-4] + ".txt"), 'w', encoding = 'UTF-8') as f:                    
            f.write('\t'.join(str(s) for s in gen_sum[0]) + '\n')
    