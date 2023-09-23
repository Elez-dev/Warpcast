import requests
import time

auto = ''

header = {
    'accept': '*/*',
    'authorization': auto,
    'origin': 'https://warpcast.com',
    'referer': 'https://warpcast.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}


def get_profile(retry=0):
    try:
        url = 'https://client.warpcast.com/v2/suggested-users?limit=100&randomized=false'
        fid_arr = []
        data = requests.get(url=url, headers=header)
        json_data = data.json()
        users = json_data['result']['users']
        for user in users:
            fid = user['fid']
            fid_arr.append(fid)
        return fid_arr
    except Exception as error:
        print(error)
        retry += 1
        if retry > 10:
            raise ValueError('Не удалось получить profile id')
        time.sleep(15)
        get_profile()


def follow(fid, retry=0):
    try:
        js = {
            'targetFid': fid
        }
        url = 'https://client.warpcast.com/v2/follows'
        data = requests.put(url=url, data=js, headers=header)
        json_data = data.json()
        if 'result' in json_data:
            if json_data['result']['success'] is True:
                print(f'Успешынй follow, fid - {fid}')
            else:
                print(f'Неудачный follow, fid - {fid}')
                print(f'{data.text}\n')
        else:
            print('Неудачный follow')
            print(f'{data.text}\n')
        time.sleep(0.1)

    except Exception as error:
        print(error)
        retry += 1
        if retry > 5:
            raise ValueError('Не удалось сделать follow')
        time.sleep(15)
        follow(fid)


if __name__ == '__main__':
    for _ in range(100):
        arr_fid = get_profile()
        if len(arr_fid) == 0:
            break
        for pid in arr_fid:
            follow(pid)
