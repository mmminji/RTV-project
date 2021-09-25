
'''
Text Data Augmentation for 수시상황보고서 by KYS
'''
import re
import random
import glob
import pandas as pd
import os
from pathlib import Path
from tqdm import tqdm

class generate_01:
    def __init__(self, gold, iter_ratio, number): # Input : 보고서, 섞는 횟수, 몇개 생성할지
        
        self.sents = gold
        self.ratio = max(1, int(iter_ratio * len(gold)))
        self.number = number
    
    def split_sent(self, doc): 
        reObj = re.compile(r'[,!]') # ,와 !로 문장 split 
        temp_sents = reObj.split(doc)
        temp_sents[2:4] = ["".join(temp_sents[2:4])] # 문장이 섞이면 안되는 부분 붙혀줌
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
        for _ in range(self.number):
            shuf = self.random_swap(split_gold[1:-1], self.ratio)
            shuf.insert(0, split_gold[0]) # 맨 앞 OOO보고! 부분 앞에 붙히기
            shuf.append(split_gold[-1]) # OOO로 식별합니다 마지막에 붙힘.
            self.tot_shuf.append(shuf)

        
        return list(map(list,list(set(map(tuple,self.tot_shuf))))) # 마지막 중복해서 생성된 보고서 제거해서 return

if __name__ == "__main__":
    file_name = glob.glob('./txt_processed/비정형모의전장자료/1. 수시상황보고서/*')
    new_folder_summary = './txt_processed/비정형모의전장자료/generate_summary/1. 수시상황보고서'
    new_folder_generate = './RTV_data/정형모의전장자료/generate_CSV/'
    csv_file = pd.read_csv('./RTV_data/정형모의전장자료/new_CSV/T_AIRFORCE_DETECT.csv')

    Path(new_folder_summary).mkdir(parents=True, exist_ok=True)
    Path(new_folder_generate).mkdir(parents=True, exist_ok=True)

    new_csv = pd.DataFrame()

    print("Generate Start for 수시상황보고서")
    for idx, txt_file in enumerate(tqdm(file_name,leave = True)) :
        with open(txt_file, 'r', encoding = 'UTF-8') as f:
            tmp = f.read()
            gen_sum = generate_01(re.sub('\n','',tmp).strip(),0.2,100).shuf_gold() # 최대 24개의 조합이 나올 수 있다라고 하면 100번 정도 해야 모든 조합이 생성됨.
            for txt_idx, txt_content in enumerate(gen_sum):
                with open(os.path.join(new_folder_summary,os.path.basename(txt_file)[:-4] + "_" + str(txt_idx).zfill(2) + ".txt"), 'w', encoding = 'UTF-8') as f:                    
                    f.write('\t'.join(str(s) for s in txt_content) + '\n')
            for i in range(len(gen_sum)):
                new_csv = new_csv.append(csv_file.iloc[idx])

    print("Original length is " + str(len(file_name)) + "& Generated Csv dimension is " + str(new_csv.shape))
    new_csv.to_csv(os.path.join(new_folder_generate,'T_AIRFORCE_DETECT.csv'), index = False)
    