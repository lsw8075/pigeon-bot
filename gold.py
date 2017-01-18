from urllib.request import urlopen
import re

cp = re.compile('class="tx_r"><em>(.*)</em> <img src=')

def getgold() :
  with urlopen('https://search.naver.com/search.naver?where=nexearch&query=%EA%B8%88%EA%B0%92&sm=top_hty&fbm=1&ie=utf8') as f:
    a = f.read().decode('utf-8')
    m = re.search(cp, a)
    return m.group(1)


