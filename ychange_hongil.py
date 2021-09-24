#%%
import glob
import re
from eunjeon import Mecab 
mecab = Mecab() 
#%%

def delete_josa(text):    
    token=mecab.pos(text)
    # 조사 제거
    token=[t[0] for t in token if t[1][0]=='J']

    for i in range(len(token)):
        text=re.sub(token[i],'',text).strip()
    ##
    text=re.sub('으','',text).strip()
    text=re.sub('()','',text).strip()
    text=re.sub('[#/\?^$@*\"※~&%ㆍ』\\‘|\(\)\[\]\<\>`\'…》]', '', text).strip() # 특수문자 제거
    
    # 시, 분, 초로 변경
    sbc=re.compile('.{2}:.{2}:.{2}')
    sibuncho=sbc.findall(text)[0]
    sbc=list(sibuncho)
    sbc[2]='시 '
    sbc[5]='분 '
    sbc[-1]=sbc[-1]+'초'
    change_sibuncho=''.join(sbc)
    text=text.replace(sibuncho,change_sibuncho)

    return text
#%%
# pth = list(before_mapping_dict.values())[0]
# total = glob.glob(pth['summary']+"/*")
# with open(total[0], 'r', encoding = 'UTF-8') as f:
#     txt1 = f.read()  

# pth = list(before_mapping_dict.values())[2]
# total = glob.glob(pth['summary']+"/*")
# with open(total[0], 'r', encoding = 'UTF-8') as f:
#     txt2 = f.read()

# pth = list(before_mapping_dict.values())[1]
# total = glob.glob(pth['summary']+"/*")
# with open(total[0], 'r', encoding = 'UTF-8') as f:
#     txt3 = f.read()

# path='./txt_processed/1. 수시상황보고서'
# total=glob.glob(path+'/*')
# with open(total[0], 'r', encoding = 'UTF-8') as f:
#     change1 = f.read() 

# path='./txt_processed/2. 적기 공격 임박 보고서'
# total=glob.glob(path+'/*')
# with open(total[0], 'r', encoding = 'UTF-8') as f:
#     change2 = f.read()

# path='./txt_processed/3. 지대공 미사일 사격 보고서'
# total=glob.glob(path+'/*')
# with open(total[0], 'r', encoding = 'UTF-8') as f:
#     change3 = f.read()  
#%%
# delete_josa(txt1)
# #%%
# print(txt1)

# #%%
# print(change1)
# #%%
# print(txt2)
# #%%
# print(change2)
# #%%
# print(txt3)
# #%%
# print(change3)
#%%
before_mapping_dict = {'1': {'csv_file': ['./RTV_data/정형모의전장자료/new_CSV/T_AIRFORCE_DETECT.csv'],
  'summary': './RTV_data/비정형모의전장자료/1. 수시상황보고서',
  'key': [],
  'threshold': {}},
 '2': {'csv_file': ['./RTV_data/정형모의전장자료/new_CSV/T_AIRFORCE_FIRE_SAM.csv',
   './RTV_data/정형모의전장자료/new_CSV/T_AIRFORCE_DETONATION_SAM.csv'],
  'summary': './RTV_data/비정형모의전장자료/3. 지대공 미사일 사격 보고서',
  'key': [['SIMULATIONID', 'TARGET_MSN_NO']],
  'threshold': {}},
 '3': {'csv_file': ['./RTV_data/정형모의전장자료/new_CSV/T_AIRFORCE_DETECT.csv'],
  'summary': './RTV_data/비정형모의전장자료/2. 적기 공격 임박 보고서',
  'key': [],
  'threshold': {'C_AIRFORCE_DETECT_TARGET_RANGE': 30}}}


# 수시상황보고서
pth = list(before_mapping_dict.values())[0]
total = glob.glob(pth['summary']+"/*")
for txt_file in total :
    with open(txt_file, 'r', encoding = 'UTF-8') as f:
        tmp = f.read()
        tmp = tmp[3:]
        tmp = re.sub('\n','',tmp).strip()  # \n 제거
        tmp = re.sub('Z','',tmp).strip()  # Z 제거
        tmp = tmp.replace('도', ' 도')  # 도 앞에 띄어쓰기
        tmp = tmp.replace('기가', ' 기가')  # 기가 앞에 띄어쓰기
        tmp = tmp.replace('오전', ' 오전 ')  # 오전 앞뒤 띄어쓰기 
        tmp = tmp.replace('오후', ' 오후 ')  # 오후 앞뒤 띄어쓰기 
        tmp = tmp.replace('오후4', '오후04')  # 04시로 변경
        tmp = tmp.replace('속 도로', '속도로')  # 속 도 띄어쓰기 제거
        tmp = tmp.replace('(으)로', ' (으)로')  # (으)로 앞에 띄어쓰기
        tmp = tmp.replace(',', ' ,')  # , 앞에 띄어쓰기
        tmp = delete_josa(tmp) # 조사 제거 함수 적용
        
    ff = open('./txt_processed/1. 수시상황보고서/{}'.format(txt_file.split('\\')[1]), 'wt', encoding = 'UTF-8')
    ff.write(tmp)
    ff.close()

# 지대공 미사일 사격 보고서
pth = list(before_mapping_dict.values())[1]
total = glob.glob(pth['summary']+"/*")
for txt_file in total :
    with open(txt_file, 'r', encoding = 'UTF-8') as f:
        tmp = f.read()
        tmp = tmp[3:]
        tmp = re.sub('\n','',tmp).strip()  # \n 제거
        tmp = tmp.replace('발', ' 발')  # 발 앞에 띄어쓰기
        tmp = tmp.replace('오전', ' 오전 ')  # 오전 앞뒤 띄어쓰기 
        tmp = tmp.replace('오후', ' 오후 ')  # 오후 앞뒤 띄어쓰기 
        tmp = tmp.replace('오후4', '오후04')  # 04시로 변경
        tmp = tmp.replace('(으)로', ' (으)로')  # (으)로 앞에 띄어쓰기
        tmp = tmp.replace('에', ' 에')  # 에 앞에 띄어쓰기
        tmp = tmp.replace(',', ' ,')  # , 앞에 띄어쓰기
        tmp = delete_josa(tmp) # 조사 제거 함수 적용
    ff = open('./txt_processed/3. 지대공 미사일 사격 보고서/{}'.format(txt_file.split('\\')[1]), 'wt', encoding = 'UTF-8')
    ff.write(tmp)
    ff.close()

# 적기 공격 임박 보고서
pth = list(before_mapping_dict.values())[2]
total = glob.glob(pth['summary']+"/*")
for txt_file in total :
    with open(txt_file, 'r', encoding = 'UTF-8') as f:
        tmp = f.read()
        tmp = tmp[3:]
        tmp = re.sub('\n','',tmp).strip()  # \n 제거
        tmp = tmp.replace('대', ' 대')  # 발 앞에 띄어쓰기
        tmp = tmp.replace('오전', ' 오전 ')  # 오전 앞뒤 띄어쓰기 
        tmp = tmp.replace('오후', ' 오후 ')  # 오후 앞뒤 띄어쓰기 
        tmp = tmp.replace('오후4', '오후04')  # 04시로 변경
        tmp = tmp.replace('(으)로', ' (으)로')  # (으)로 앞에 띄어쓰기
        tmp = tmp.replace(',', ' ,')  # , 앞에 띄어쓰기
        tmp = delete_josa(tmp) # 조사 제거 함수 적용
    ff = open('./txt_processed/2. 적기 공격 임박 보고서/{}'.format(txt_file.split('\\')[1]), 'wt', encoding = 'UTF-8')
    ff.write(tmp)
    ff.close()
# %%
