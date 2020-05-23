import torch
import util
from transformers import *
import numpy as np
from util import bold, red, yellow, green, white, pink, underline
from scipy.special import softmax

pretrained_weights = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(pretrained_weights)
model = BertForMaskedLM.from_pretrained(pretrained_weights)
MASKED_TOKEN = tokenizer.convert_tokens_to_ids(['[MASK]'])[0]

def bert_masked_lm(text):
    encoded = tokenizer.encode(text)
    masked_ids = [i for i, id_ in enumerate(encoded) if id_ == MASKED_TOKEN]
    input_ids = torch.tensor([encoded])
    pred = model(input_ids)[0][0].detach().numpy()
    res = [tokenizer.convert_ids_to_tokens([np.argmax(pred[i])])[0] for i in masked_ids]
    return res

MAX_RES = 15
MAX_PROB = 0.95

def bert_masked_lm_prob(text, word):
    encoded = tokenizer.encode(text)
    word_id = tokenizer.encode(word)[0]
    word_id_pos = encoded.index(word_id)
    input_ids = torch.tensor([encoded])
    pred = model(input_ids)[0][0].detach().numpy()[word_id_pos]
    pred = softmax(pred)
    top_ids = list(np.argsort(pred))
    top_ids.reverse()
    res = []
    tot_prob = 0
    for id_ in top_ids[:MAX_RES]:
        if tot_prob > MAX_PROB:
            break
        tot_prob += pred[id_]
        res.append((tokenizer.convert_ids_to_tokens([id_])[0], float(pred[id_])))
    return res

import json
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

def get_params(path):
    params_temp = parse_qs(urlparse(path).query)
    params = {}
    for param in params_temp:
        params[param] = params_temp[param][0]
    return params

def predict_handler(params):
    text = params['text']
    word = params['word']
    print(util.red(text), util.yellow(word))
    response = bert_masked_lm_prob(text, word)
    print(util.yellow(response))
    return json.dumps(response)


class testHTTPServer_RequestHandler(SimpleHTTPRequestHandler):

  # GET
  def do_GET(self):
        print(red(self.path))
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')

        self.end_headers()

        params = get_params(self.path)
        response = ''
        if 'predict' in params:
            response = predict_handler(params)

        # Write content as utf-8 data
        self.wfile.write(bytes(response, "utf8"))
        return

def run():
    print('starting server...')

    # Server settings
    # server_address = ('192.168.3.14', 8000)
    server_address = ('0.0.0.0', 8009)

    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()


run()

