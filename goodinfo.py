from bs4 import BeautifulSoup
import os
import requests

os.system('CLS')
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}
# stkno = '6208'
stkno = input("標的 => ")
url = "https://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID="+stkno
response = requests.post(url, headers = headers)
response.encoding = 'utf-8'

# soup = BeautifulSoup(response.text, 'html.parser')
soup = BeautifulSoup(response.text, 'lxml')
def checkIncludes(number):
    # 5 or 6 => 當天交易資料
    # 15 16 => 法人買賣情況
    # 17 18 => 資券變化
    # 39 => 股利政策
    # 40 41 => 近期月營收狀況
    # 45 46 => 個別獲利狀況
    # 48 49 => 合併獲利狀況
    # 51 52 => 個別資產負債
    # 54 55 => 合併資產負債
    # 57 58 => 個別現金流量
    # 60 61 => 合併現金流量
    return {
        5: '當天交易資料',
        6: '當天交易資料',
        16: '法人買賣情況',
        18: '資券變化',
        39: '股利政策',
        41: '近期月營收狀況',
        46: '個別獲利狀況',
        49: '合併獲利狀況',
        52: '個別資產負債',
        55: '合併資產負債',
        58: '個別現金流量',
        61: '合併現金流量',
    }.get(number, '')
needCheck = soup.findAll('table')[5].find_all('table')
dict = {}
for i in range(len(needCheck)):
    if len(checkIncludes(i)) != 0:
        dict[checkIncludes(i)] = needCheck[i]
        
data_array = []
td_index = 0
for res in dict['當天交易資料'].find_all('tr'):
    for td in res.find_all('td'):
        if td_index > 0:
            res = td.get_text()
            data_array.append(" ".join(res.split()))
        td_index += 1

# print('\n array => ', data_array)

res_dict = {}
res_dict['stkno'] = data_array[0].split()[0]
res_dict['name'] = data_array[0].split()[1]
res_dict['date'] = data_array[3].split(': ')[1]

first_column = data_array.index("成交價")
for i in range(first_column, first_column+8):
    res_dict[data_array[i]] = data_array[i+8]

second_column = data_array.index("成交張數")
for i in range(second_column, second_column+8):
    res_dict[data_array[i]] = data_array[i+8]

third_column = data_array.index("昨日張數")
for i in range(third_column, third_column+6):
    res_dict[data_array[i]] = data_array[i+6]

print('\n\nres dict =>', res_dict)
print('\n\n name =>', res_dict['name'])
print('\n\n')