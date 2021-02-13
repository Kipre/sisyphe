import unittest
import csv
import tempfile
from .. import sisyphe

features = {
    2: 'Thanks for your feedback God bless you',
    4: 'EARN $110,000.00 96 HOURS INVESTMENT I',
    6: 'When your payment is due, send your name',
    32: 'Amount (USD) $4,481.33 BITBRON successfully paid',
    43: 'Во Владимирской области объявили оранжевый уровень опасности',
    54: 'Общее число инфицированных коронавирусом жителей – 24 390 человек',
    23: 'Who's the best defender in Champions League history?'
}

categories = ['Russian', 'English']

render = lambda x: f'<span style="color: red">{x}</span>'
csvfile = tempfile.TemporaryFile()

def save_callback(labels):
    writer = csv.DictWriter(csvfile, fieldnames=['id', 'label'])
    writer.writeheader()
    for key in labels:
        writer.writerow({'id': key, 'label': labels[key]})

sisyphe = Sisyphe(features, categories, save_callback, render)

example = sysiphe.get()

