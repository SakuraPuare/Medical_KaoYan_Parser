
import httpx
from bs4 import BeautifulSoup
import pathlib
import time

httpx._config.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

url = [
    'https://m.eol.cn/kaoyan/zyk/zyk_2/201606/t20160601_1405065.shtml',
    'https://m.eol.cn/kaoyan/zyk/zyk_2/201606/t20160601_1405010.shtml',
    'https://m.eol.cn/kaoyan/zyk/zyk_2/201606/t20160601_1404966.shtml',
    'https://m.eol.cn/kaoyan/zyk/zyk_2/201606/t20160601_1404942.shtml',
    'https://m.eol.cn/kaoyan/zyk/zyk_2/201606/t20160601_1404913.shtml',
    'https://m.eol.cn/kaoyan/zyk/zyk_2/201606/t20160601_1404873.shtml',
    'https://m.eol.cn/kaoyan/zyk/zyk_2/201606/t20160601_1405393.shtml',
    'https://m.eol.cn/kaoyan/zyk/zyk_2/201606/t20160601_1405384.shtml',
    'https://m.eol.cn/kaoyan/zyk/zyk_2/201606/t20160601_1405360.shtml',
    'https://m.eol.cn/kaoyan/zyk/zyk_2/201606/t20160601_1405331.shtml',
    'https://m.eol.cn/kaoyan/zyk/zyk_2/201606/t20160601_1405307.shtml',
    'https://m.eol.cn/kaoyan/zyk/zyk_2/201606/t20160601_1405275.shtml',
    'https://m.eol.cn/kaoyan/zyk/zyk_2/201606/t20160601_1405267.shtml',
    'https://m.eol.cn/kaoyan/zyk/zyk_2/201606/t20160601_1405249.shtml',
    'https://m.eol.cn/kaoyan/zyk/zyk_2/201606/t20160601_1405243.shtml',
    'https://m.eol.cn/kaoyan/zyk/zyk_2/201606/t20160601_1405238.shtml',
    'https://m.eol.cn/kaoyan/zyk/zyk_2/201606/t20160601_1405223.shtml',
    'https://m.eol.cn/kaoyan/zyk/zyk_2/201606/t20160601_1405220.shtml',
    'https://m.eol.cn/kaoyan/zyk/zyk_2/201606/t20160601_1405218.shtml',
    'https://m.eol.cn/kaoyan/zyk/zyk_2/201606/t20160601_1405200.shtml',
    'https://m.eol.cn/kaoyan/zyk/zyk_2/201606/t20160601_1405190.shtml',
    'https://m.eol.cn/kaoyan/zyk/zyk_2/201606/t20160601_1405171.shtml',
    'https://m.eol.cn/kaoyan/zyk/zyk_2/201606/t20160601_1405115.shtml',
    'https://m.eol.cn/kaoyan/zyk/zyk_2/201606/t20160601_1405102.shtml',
    'https://m.eol.cn/kaoyan/zyk/zyk_2/201606/t20160601_1405088.shtml',
]

base_url = 'https://m.eol.cn/kaoyan/zyk/zyk_2/201606/'

_PAGE_COUNT = ""
_PAGE_NAME = ""

data_path = pathlib.Path('data')
data_path.mkdir(exist_ok=True)

def get(url: str) -> str:
    with httpx.Client(verify=False, follow_redirects=True) as client:
        resp = client.get(url)
        return resp.text


def main():
    for i in url:
        data = get(i)
        soup = BeautifulSoup(data, 'html.parser')
        nav = soup.find('div', id='pagenav').find('script').text

        exec(nav.replace('var ', ''), globals())
        content = soup.find_all('div', id='mcontent')[0].text
        content = content.replace('\u3000', ' ')
        for i in range(1, int(_PAGE_COUNT)):
        # for i in range(1, 2):
            url_ = base_url + f'{_PAGE_NAME}_{i}.shtml'
            data = get(url_)
            soup = BeautifulSoup(data, 'html.parser')
            content += soup.find_all('div', id='mcontent')[0].text
            time.sleep(0.5)

        with open(data_path / f'{_PAGE_NAME}.txt', 'w') as f:
            f.write(content)


if __name__ == "__main__":
    main()
