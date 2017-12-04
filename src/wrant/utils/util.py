import requests
import json
import pickle
import csv
import time
import urllib
import operator
#

def get(url, sent=None, headers=None, json=True):
    # get params should be part of url
    if sent:
        url += urllib.parse.quote(sent)
    try:
        if headers:
            r = requests.get(url, headers=headers)
        else:
            r = requests.get(url)
    except Exception as e:
        print(e)

    if json:
        return r.json()
    else:
        return r.text

def post(url, data, headers=None):
    HEADERS={'Content-Type': 'application/json'}
    if headers:
        HEADERS.update(headers)
    # data is dict
    # get params should be part of url
    r = requests.post(url, data=json.dumps(data), headers=HEADERS)
    return r.json()

#############################

def read(filename, bin=False):
    if bin:
        f = open(filename, 'rb')
    else:
        f = open(filename, 'r')
    text = f.read()
    f.close()
    return text

def write(text, filename, bin=False):
    if bin:
        f = open(filename, 'wb')
    else:
        f = open(filename, 'w')
    f.write(text)
    f.close()

def readsents(filename):
    f = open(filename, 'r')
    sents = [x[:-1] for x in f.readlines()]
    f.close()
    return sents

def readcsv(filename, delimiter=',', quotes='"'):
    data = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotes)
        for row in reader:
            data.append(row)
    return data

def writecsv(data, filename, delimiter=',', quotes='"'):
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=delimiter, quotechar=quotes)
        for row in data:
            writer.writerow(row)

def readjson(filename):
    return json.load(open(filename))

def writejson(obj, filename):
    json.dump(obj, open(filename,'w'), indent=2)

#############################
def lapsed(start):
    return str(round((time.time() - start),2)) + 's'

def percent(i, tot):
    return str(round(100.0*i/tot,2)) + '%'

#############################
def sortdict(dic, rev=False):
    return sorted(dic.items(), key=operator.itemgetter(1), reverse=rev)

#############################
def save(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def load(filename):
    with open(filename, 'rb') as input:
        return pickle.load(input)

#############################
def red(s):
    return '\033[91m' + s + '\033[0m'

def yellow(s):
    return '\033[93m' + s + '\033[0m'

def green(s):
    return '\033[92m' + s + '\033[0m'

def blue(s):
    return '\033[94m' + s + '\033[0m'

def pink(s):
    return '\033[95m' + s + '\033[0m'

def lightblue(s):
    return '\033[96m' + s + '\033[0m'

def white(s):
    return '\033[97m' + s + '\033[0m'

def underline(s):
    return '\033[4m' + s + '\033[0m'

def bold(s):
    return '\033[1m' + s + '\033[0m'

def light(s):
    return '\033[2m' + s + '\033[0m'

def flash(s):
    return '\033[5m' + s + '\033[0m'
