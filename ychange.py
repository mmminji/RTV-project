import glob
import re

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
        tmp = tmp.replace(' 오전 ', '오전')  # 오전 앞뒤 띄어쓰기 제거
        tmp = tmp.replace(' 오후 ', '오후')  # 오후 앞뒤 띄어쓰기 제거
        tmp = tmp.replace('속 도로', '속도로')  # 속 도 띄어쓰기 제거
        tmp = tmp.replace('(으)로', ' (으)로')  # (으)로 앞에 띄어쓰기
        tmp = tmp.replace(',', ' ,')  # , 앞에 띄어쓰기

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
        tmp = tmp.replace(' 오전 ', '오전')  # 오전 앞뒤 띄어쓰기 제거
        tmp = tmp.replace(' 오후 ', '오후')  # 오후 앞뒤 띄어쓰기 제거
        tmp = tmp.replace('로', ' 로')  # (으)로 앞에 띄어쓰기
        tmp = tmp.replace('에', ' 에')  # 에 앞에 띄어쓰기
        tmp = tmp.replace(',', ' ,')  # , 앞에 띄어쓰기

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
        tmp = tmp.replace(' 오전 ', '오전')  # 오전 앞뒤 띄어쓰기 제거
        tmp = tmp.replace(' 오후 ', '오후')  # 오후 앞뒤 띄어쓰기 제거
        tmp = tmp.replace('로', ' 로')  # (으)로 앞에 띄어쓰기
        tmp = tmp.replace(',', ' ,')  # , 앞에 띄어쓰기

    ff = open('./txt_processed/2. 적기 공격 임박 보고서/{}'.format(txt_file.split('\\')[1]), 'wt', encoding = 'UTF-8')
    ff.write(tmp)
    ff.close()