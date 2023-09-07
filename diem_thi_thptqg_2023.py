import requests
from bs4 import BeautifulSoup

# Get scores from: https://tienphong.vn/tra-cuu-scores-thi.tpo
def get_scores_tienphong(sbd):
    try:
        url = r'https://tienphong.vn/api/scoresthi/get/result?type=0&keyword=' + str(sbd)
        r = requests.get(url)
        json_response = r.json()['data']['results']
        soup = BeautifulSoup(json_response,'html.parser')
        td = soup.find_all('td', class_ = "point")
        scores = list()
        for i in td:
            scores.append(i.text)
        return ','.join(scores)
    except Exception as e:
        return 'error'

# Get scores from: https://dantri.com.vn/giao-duc/tuyen-sinh/tra-cuu-scores.htm
def get_scores_dantri(sbd):
    try:
        url = r'https://dantri.com.vn/thpt/1/0/99/' + str(sbd) + '/2023/0.2/search-gradle.htm'
        r = requests.get(url)
        scores = r.json()['student']
        data = f"{scores['sbd']},{scores['toan']},{scores['van']},{scores['ngoaiNgu']},{scores['vatLy']},{scores['hoaHoc']},{scores['sinhHoc']},{scores['lichSu']},{scores['diaLy']},{scores['gdcd']}"
        data = data.replace('None','')
        if data == ',,,,,,,,,':
            data = ''
        return data
    except Exception as e:
        return 'error'

# Get scores from: https://thptquocgia.edu.vn/
def get_scores_thptquocgia(sbd):
    try:
        url = r'https://thptquocgia.edu.vn/scoresthi/?sbd=' + str(sbd)
        r = requests.get(url)
        soup = BeautifulSoup(r.text,'html.parser')
        table = soup.find('div', class_="table-responsive")
        scores = table.find_all('td')
        data = [str(sbd)]
        for i in scores:
            data.append(i.text)
        data = data[:7] + data[8:11]
        return ','.join(data)
    except AttributeError:
        return ''
    except Exception as e:
        return 'error'
# Combine 3 websites
def get_scores(sbd):
    if sbd < 10000000:
        sbd = '0' + str(sbd)
    scores_tp = get_scores_tienphong(sbd)
    scores_dt = get_scores_dantri(sbd)
    scores_thptqg = get_scores_thptquocgia(sbd)
    if scores_tp != 'error':
        scores = scores_tp
    elif scores_dt != 'error':
        scores = scores_dt
    else:
        scores = scores_thptqg
    return scores

# Collect and write data to csv file
path = r'D:\Download\scores.csv'
header_scores = 'sbd,toan,ngu_van,ngoai_ngu,vat_li,hoa_hoc,sinh_hoc,lich_su,dia_li,gdcd'
with open(path, 'w') as thptqg:
    thptqg.write(header_scores + '\n')
    for ma_tinh in range(1,65):
        for sbd in range(ma_tinh * 1000000 + 1, (ma_tinh + 1) * 1000000):
            scores = get_scores(sbd)
            if scores == '':
                break
            else:
                thptqg.write(scores + '\n')
