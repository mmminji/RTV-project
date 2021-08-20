# -*- coding: utf-8 -*-
import re, time, os
import pandas as pd
import numpy as np
import glob
from collections import Counter
import json
from sklearn.model_selection import train_test_split

def split_infobox():
    """
    extract box content, field type and position information from infoboxes from original_data
    *.box.val is the box content (token)
    *.box.lab is the field type for each token
    *.box.pos is the position counted from the begining of a field
    """
    bwfile = ["processed_data/train/train.box.val", 
              "processed_data/valid/valid.box.val", 
              "processed_data/test/test.box.val"]
    bffile = ["processed_data/train/train.box.lab", 
              "processed_data/valid/valid.box.lab", 
              "processed_data/test/test.box.lab"]
    bpfile = ["processed_data/train/train.box.pos", 
              "processed_data/valid/valid.box.pos", 
              "processed_data/test/test.box.pos"]
    boxes = ["original_data/train.box", "original_data/valid.box", "original_data/test.box"]
    
    mixb_word, mixb_label, mixb_pos = [], [], []
    ## fboxes = boxes[0]
    for fboxes in boxes:
        box = open(fboxes, "r", encoding='UTF8').read().strip().split('\n')
        box_word, box_label, box_pos = [], [], []
        ## ib = box[0]
        for ib in box:
            item = ib.split('\t')
            box_single_word, box_single_label, box_single_pos = [], [], []
            for it in item:
                ## it = item[3]
                if len(it.split(':')) > 2:
                    #continue
                    prefix = it.split(':')[0]
                    word = re.sub(' ','-',':'.join(it.split(':')[1:]))
                # print it
                else :
                    prefix, word = it.split(':')
                if '<none>' in word or word.strip()=='' or prefix.strip()=='':
                    continue
                new_label = re.sub("_[1-9]\d*$", "", prefix)
                if new_label.strip() == "":
                    continue
                box_single_word.append(word)
                box_single_label.append(new_label)
                if re.search("_[1-9]\d*$", prefix):
                    field_id = int(prefix.split('_')[-1])
                    box_single_pos.append(field_id if field_id<=30 else 30)
                else:
                    box_single_pos.append(1)
            box_word.append(box_single_word)
            box_label.append(box_single_label)
            box_pos.append(box_single_pos)
        mixb_word.append(box_word)
        mixb_label.append(box_label)
        mixb_pos.append(box_pos)
    for k, m in enumerate(mixb_word):  # len(mixb_word) = 3 : train/val/test  # word
        with open(bwfile[k], "w+", encoding='UTF8') as h:
            for items in m:
                for sens in items:
                    h.write(str(sens) + " ")
                h.write('\n')
    for k, m in enumerate(mixb_label):  # field
        with open(bffile[k], "w+", encoding='UTF8') as h:
            for items in m:
                for sens in items:
                    h.write(str(sens) + " ")
                h.write('\n')
    for k, m in enumerate(mixb_pos):  # position
        with open(bpfile[k], "w+", encoding='UTF8') as h:
            for items in m:
                for sens in items:
                    h.write(str(sens) + " ")
                h.write('\n')

def reverse_pos():
    # get the position counted from the end of a field
    bpfile = ["processed_data/train/train.box.pos", "processed_data/valid/valid.box.pos", "processed_data/test/test.box.pos"]
    bwfile = ["processed_data/train/train.box.rpos", "processed_data/valid/valid.box.rpos", "processed_data/test/test.box.rpos"]
    ## pos = bpfile[0]
    for k, pos in enumerate(bpfile):
        box = open(pos, "r").read().strip().split('\n')
        reverse_pos = []
        for bb in box:
            ## bb = box[0]
            pos = bb.split()
            tmp_pos = []
            single_pos = []
            for p in pos:
                ## p = pos[2]
                if int(p) == 1 and len(tmp_pos) != 0:
                    single_pos.extend(tmp_pos[::-1])
                    tmp_pos = []
                tmp_pos.append(p)
            single_pos.extend(tmp_pos[::-1])
            reverse_pos.append(single_pos)
        with open(bwfile[k], 'w+') as bw:
            for item in reverse_pos:
                bw.write(" ".join(item) + '\n')

def check_generated_box():
    ftrain = ["processed_data/train/train.box.val",
              "processed_data/train/train.box.lab",
              "processed_data/train/train.box.pos",
              "processed_data/train/train.box.rpos"]
    ftest  = ["processed_data/test/test.box.val", 
              "processed_data/test/test.box.lab",
              "processed_data/test/test.box.pos",
              "processed_data/test/test.box.rpos"]
    fvalid = ["processed_data/valid/valid.box.val", 
              "processed_data/valid/valid.box.lab", 
              "processed_data/valid/valid.box.pos",
              "processed_data/valid/valid.box.rpos"]
    for case in [ftrain, ftest, fvalid]:
        vals = open(case[0], 'r', encoding='UTF8').read().strip().split('\n')
        labs = open(case[1], 'r', encoding='UTF8').read().strip().split('\n')
        poses = open(case[2], 'r', encoding='UTF8').read().strip().split('\n')
        rposes = open(case[3], 'r', encoding='UTF8').read().strip().split('\n')
        assert len(vals) == len(labs)
        assert len(poses) == len(labs)
        assert len(rposes) == len(poses)
        for val, lab, pos, rpos in zip(vals, labs, poses, rposes):
            vval = val.strip().split(' ')
            llab = lab.strip().split(' ')
            ppos = pos.strip().split(' ')
            rrpos = rpos.strip().split(' ')
            if len(vval) != len(llab) or len(llab) != len(ppos) or len(ppos) != len(rrpos):
                print (case)
                print (val)
                print (len(vval))
                print (len(llab))
                print (len(ppos))
                print (len(rrpos))
            assert len(vval) == len(llab)
            assert len(llab) == len(ppos)
            assert len(ppos) == len(rrpos)


def split_summary_for_rouge():
    bpfile = ["original_data/test.summary", "original_data/valid.summary"]
    bwfile = ["processed_data/test/test_split_for_rouge/", "processed_data/valid/valid_split_for_rouge/"]
    for i, fi in enumerate(bpfile):
        ## fi = bpfile[0]
        fread = open(fi, 'r', encoding='UTF8')
        k = 0
        for line in fread:
            with open(bwfile[i] + 'gold_summary_' + str(k), 'w', encoding='UTF8') as sw:
                sw.write(line.strip() + '\n')
            k += 1
        fread.close()



class Vocab(object):
    """vocabulary for words and field types"""
    def __init__(self):
        vocab = dict()
        vocab['PAD'] = 0
        vocab['START_TOKEN'] = 1
        vocab['END_TOKEN'] = 2
        vocab['UNK_TOKEN'] = 3
        cnt = 4
        with open("original_data/word_vocab.txt", "r", encoding='UTF8') as v:
            for line in v:
                word = line.strip().split()[0]
                vocab[word] = cnt
                cnt += 1
        self._word2id = vocab
        self._id2word = {value: key for key, value in vocab.items()}

        key_map = dict()
        key_map['PAD'] = 0
        key_map['START_TOKEN'] = 1
        key_map['END_TOKEN'] = 2
        key_map['UNK_TOKEN'] = 3
        cnt = 4
        with open("original_data/field_vocab.txt", "r", encoding='UTF8') as v:
            for line in v:
                key = line.strip().split()[0]
                key_map[key] = cnt
                cnt += 1
        self._key2id = key_map
        self._id2key = {value: key for key, value in key_map.items()}

    def word2id(self, word):
        ans = self._word2id[word] if word in self._word2id else 3
        return ans

    def id2word(self, id):
        ans = self._id2word[int(id)]
        return ans

    def key2id(self, key):
        ans = self._key2id[key] if key in self._key2id else 3
        return ans

    def id2key(self, id):
        ans = self._id2key[int(id)]
        return ans

def table2id():
    fvals = ['processed_data/train/train.box.val',
             'processed_data/test/test.box.val',
             'processed_data/valid/valid.box.val']
    flabs = ['processed_data/train/train.box.lab',
             'processed_data/test/test.box.lab',
             'processed_data/valid/valid.box.lab']
    fsums = ['original_data/train.summary',
             'original_data/test.summary',
             'original_data/valid.summary']
    fvals2id = ['processed_data/train/train.box.val.id',
                'processed_data/test/test.box.val.id',
                'processed_data/valid/valid.box.val.id']
    flabs2id = ['processed_data/train/train.box.lab.id',
                'processed_data/test/test.box.lab.id',
                'processed_data/valid/valid.box.lab.id']
    fsums2id = ['processed_data/train/train.summary.id',
                'processed_data/test/test.summary.id',
                'processed_data/valid/valid.summary.id']
    vocab = Vocab()
    for k, ff in enumerate(fvals):
        fi = open(ff, 'r', encoding='UTF8')
        fo = open(fvals2id[k], 'w')
        for line in fi:
            items = line.strip().split(" ")
            fo.write(" ".join([str(vocab.word2id(word)) for word in items]) + '\n')
        fi.close()
        fo.close()
    for k, ff in enumerate(flabs):
        fi = open(ff, 'r', encoding='UTF8')
        fo = open(flabs2id[k], 'w')
        for line in fi:
            items = line.strip().split()
            fo.write(" ".join([str(vocab.key2id(key)) for key in items]) + '\n')
        fi.close()
        fo.close()
    for k, ff in enumerate(fsums):
        fi = open(ff, 'r', encoding='UTF8')
        fo = open(fsums2id[k], 'w')
        for line in fi:
            items = line.strip().split()
            fo.write(" ".join([str(vocab.word2id(word)) for word in items]) + '\n')
        fi.close()
        fo.close()


def preprocess():
    """
    We use a triple <f, p+, p-> to represent the field information of a token in the specific field. 
    p+&p- are the position of the token in that field counted from the begining and the end of the field.
    For example, for a field (birthname, Jurgis Mikelatitis) in an infoboxes, we represent the field as
    (Jurgis, <birthname, 1, 2>) & (Mikelatitis, <birthname, 2, 1>)
    """
    print("extracting token, field type and position info from original data ...")
    time_start = time.time()
    split_infobox() # word, field, position
    reverse_pos()  # 역방향 position
    duration = time.time() - time_start
    print("extract finished in %.3f seconds" % float(duration))

    print("spliting test and valid summaries for ROUGE evaluation ...")
    time_start = time.time()
    split_summary_for_rouge() # 전체파일을 하나씩 나눔 (test/valid)
    duration = time.time() - time_start
    print("split finished in %.3f seconds" % float(duration))

    print("turning words and field types to ids ...")
    time_start = time.time()
    table2id()
    duration = time.time() - time_start
    print("idlization finished in %.3f seconds" % float(duration))


def make_dirs():
    os.makedirs("results/", exist_ok=True)
    os.makedirs("results/res/", exist_ok=True)
    os.makedirs("results/evaluation/", exist_ok=True)
    os.makedirs("processed_data/", exist_ok=True)
    os.makedirs("processed_data/train/", exist_ok=True)
    os.makedirs("processed_data/test/", exist_ok=True)
    os.makedirs("processed_data/valid/", exist_ok=True)
    os.makedirs("processed_data/test/test_split_for_rouge/", exist_ok=True)
    os.makedirs("processed_data/valid/valid_split_for_rouge/", exist_ok=True)

if __name__ == '__main__':
    
    with open('mapping_dict.json', 'r') as f:
        mapping_dict = json.load(f)

    label_txt = []
    structure_all = pd.DataFrame()

    for idx, pth in enumerate(list(mapping_dict.values())):
        
        file_name = []
        
        if len(pth['csv_file']) == 1 :
            
            structure_all = structure_all.append(pd.read_csv(pth['csv_file'][0]), ignore_index = True)

            total = glob.glob(pth['summary']+"/*")
            for txt_file in total :
                with open(txt_file, 'r', encoding = 'UTF-8') as f:
                    tmp = f.read()
                    label_txt.append(re.sub('\n','',tmp).strip())

        else :
            for i, file in enumerate(pth['csv_file']):
                
                file_name.append(re.sub('.csv','',os.path.basename(file)))
                
                if i == 0:
                    concat_structure = pd.read_csv(file)
                else :
                    concat_structure = pd.merge(concat_structure, pd.read_csv(file),
                                        left_on = ['C' + file_name[i-1][1:] + "_" + s for s in pth['key'][i-1]],
                                        right_on = ['C' + file_name[i][1:] + "_" + s for s in pth['key'][i-1]],
                                        how = "inner")
            structure_all = structure_all.append(concat_structure, ignore_index = True)
            
            total = glob.glob(pth['summary']+"/*")
            for txt_file in total :
                with open(txt_file, 'r', encoding = 'UTF-8') as f:
                    tmp = f.read()
                    label_txt.append(re.sub('\n','',tmp).strip())

    structure_all = structure_all.replace({np.nan: '<none>'})

    train_struc, valid_struc, train_label, valid_label = train_test_split(structure_all, label_txt, test_size = 0.1, random_state = 0)
    train_struc, test_struc, train_label, test_label = train_test_split(train_struc, train_label, test_size = 0.1, random_state = 0)

    # train_end = int(len(label_txt)*0.8)
    # valid_end = int(len(label_txt)*0.9)

    # train_struc = structure_all[:train_end]
    # valid_struc = structure_all[train_end:valid_end]
    # test_struc = structure_all[valid_end:]

    # train_label = label_txt[:train_end]
    # valid_label = label_txt[train_end:valid_end]
    # test_label = label_txt[valid_end:]

    if not os.path.isdir('./original_data'):
        os.mkdir('./original_data')

    total_structure = {'./original_data/train.box' : train_struc,
                    './original_data/valid.box' : valid_struc,
                    './original_data/test.box' : test_struc}

    total_label = {'./original_data/train.summary' : train_label,
                    './original_data/valid.summary' : valid_label,
                    './original_data/test.summary' : test_label}


    for key, value in total_structure.items() :
        with open(key, "w", encoding = "UTF8") as h:
            for index , row in value.iterrows() :
                h.write("\t".join([m+':'+str(n) for m, n in zip(list(value.columns), list(row))]))
                h.write('\n')

    for key, value in total_label.items() :
        with open(key, "w", encoding = "UTF8") as h:
            for content in value :
                h.write(content+"\n")


    with open('./original_data/train.summary', 'r', encoding = 'UTF-8') as f :
        gold = f.readlines()
        for i , line in enumerate(gold):
            gold[i] = line.replace('\n','')
        
        f.close()

    tot_word = []
    for gold_row in gold :
        tot_word.extend(gold_row.split())        

    tot_word.extend([element for array in train_struc.values for element in array])

    word_count = Counter(tot_word).most_common()
    word_count = [x for x in word_count if x[1] > 0]

    with open('./original_data/word_vocab.txt', 'w', encoding = 'UTF-8') as f:
        for t in word_count:
            f.write('\t'.join(str(s) for s in t) + '\n')

    field_count = Counter(list(train_struc.columns) * len(train_struc)).most_common()

    with open('./original_data/field_vocab.txt', 'w', encoding = 'UTF-8') as f:
        for t in field_count:
            f.write('\t'.join(str(s) for s in t) + '\n')

    make_dirs()
    preprocess()
    check_generated_box()
    print("check done")
