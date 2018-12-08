# -*- coding: utf-8 -*-

from __future__ import nested_scopes
from __future__ import generators
from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

import argparse
from collections import defaultdict
import codecs
import random
import re
import string

# def debuglog(s): print('DEBUG', s)
def debuglog(s): pass

class ProbabilityDistribution(object):
  def __init__(self, element_counts, smoothing_count=0.0, vocab_size=-1):
    self._element_counts = element_counts
    self._smoothing_count = smoothing_count
    self._total_count = sum(element_counts.values())
    self._vocab_size = vocab_size if vocab_size >= 0 else len(element_counts)

  def probability(self, element):
    element_count = self._element_counts.get(element, 0.0) + self._smoothing_count
    total_count = self._total_count + (self._smoothing_count * self._vocab_size)
    return element_count / total_count

  def __getitem__(self, element):
    return self.probability(element)

  def sample(self, smooth=False):
    total_count = self._total_count
    if smooth:
      total_count += self._vocab_size * self._smoothing_count
    random_count = random.random() * total_count
    count_accumulation = 0.0
    for e,c in self._element_counts.items():
      count_accumulation += (c + self._smoothing_count)
      if count_accumulation >= random_count:
        return e
    return None

class NGramModel(object):
  def __init__(self, lines, order, smoothing_count=0.0, backoff_exponent=3, buffer_symbol='<buffer>'):
    vocab_size = len(set(element for line in lines for element in line))
    self._conditional_prob_dists = dict()
    n_counts = dict()
    for n in range(order,0,-1):
      self._conditional_prob_dists[n] = dict()
      n_counts[n] = n**backoff_exponent
      conditional_counts = defaultdict(lambda: defaultdict(int))
      for line in lines:
        buffered_line = ([buffer_symbol] * (n-1)) + list(line) + [buffer_symbol]
        for i in range(len(line) + 1):
          context = tuple(buffered_line[i:i+n-1])
          element = buffered_line[i+n-1]
          conditional_counts[context][element] += 1
      for context, element_counts in conditional_counts.items():
        self._conditional_prob_dists[n][context] = \
            ProbabilityDistribution(element_counts, smoothing_count, vocab_size)

    self._dist_of_conditional_dists = ProbabilityDistribution(n_counts)
    self._order = order
    self._buffer_symbol = buffer_symbol

  def probability(self, context, element):
    total_prob = 0.0
    for n in range(self._order,0,-1):
      total_prob += self._dist_of_conditional_dists.probability(n) * \
                        self._conditional_prob_dists[n][context].probability(element)

  def generate(self, stop_symbols=set(), max_length=-1):
    output = [self._buffer_symbol] * (self._order-1)
    while True:
      if (max_length >= 0 and len(output)-(self._order-1) >= max_length) \
             or (len(output) > 0 and output[-1] in stop_symbols):
        return output[self._order-1:]
      debuglog('Generate_next_element')
      for n in range(self._dist_of_conditional_dists.sample(),0,-1):
        context = tuple(output[-n+1:]) if n > 1 else tuple()
        debuglog('  n=%s,  context=%s'%(n, ' '.join(context)))
        if context not in self._conditional_prob_dists[n]: continue
        element = self._conditional_prob_dists[n][context].sample()
        debuglog('  element=%s'%(element))
        if element == self._buffer_symbol:
          return output[self._order-1:]
        output.append(element)
        break
    return output

def read_corpus(files, chars=False, remove_newlines=False):
  output_lines = []
  for filename in files:
    with codecs.open(filename, 'r', encoding='utf-8') as f:
      data = f.read()
      if remove_newlines:
        data = re.sub('[\n\r\t]', ' ', data)
      for punc in set('!"#$%&()*+,./:;<=>?@[\\]^_`{|}~–—“”…'):
        data = data.replace(punc, ' ' + punc + ' ')
      for line in data.split('\n'):
        if not line: continue
        if chars:
          line = re.sub('\\s+', ' ', line)
        else:
          line = line.split()
        output_lines.append(line)
  return output_lines

if __name__ == "__main__":
  # pd = ProbabilityDistribution({'a': 100, 'b': 50, 'c': 30},
  #                              smoothing_count=1, vocab_size=5)
  # print('%-5s %.4f' % ('a', pd['a']))  # (100+1) / (180+1*5)
  # print('%-5s %.4f' % ('b', pd['b']))  #  (50+1) / (180+1*5)
  # print('%-5s %.4f' % ('c', pd['c']))  #  (30+1) / (180+1*5)
  # print('%-5s %.4f' % ('d', pd['d']))  #   (0+1) / (180+1*5)
  # print('%-5s %.4f' % ('e', pd['e']))
  # print('%-5s %.4f' % ('total', pd['a']+pd['b']+pd['c']+pd['z']*(5-3)))
  # print()
  # d = defaultdict(float)
  # for _ in range(100000):
  #   d[pd.sample()] += 1/100000
  # for e,p in sorted(d.items()):
  #   print('%-5s %.4f' % (e, p))
  # print('%-5s %.4f' % (None, d[None]))
  # print('%-5s %.4f' % ('total', sum(d.values())))
  # print()
  # d = defaultdict(float)
  # for _ in range(1000000):
  #   d[pd.sample(smooth=True)] += 1/1000000
  # for e,p in sorted(d.items()):
  #   if e is not None:
  #     print('%-5s %.4f %.4f' % (e,       p,         (p-pd[e])))
  # print(    '%-5s %.4f %.4f' % (None,    d[None]/2, (d[None]/2-pd[None])))
  # print(    '%-5s %.4f'      % ('total', sum(d.values())))
  # print()

  parser = argparse.ArgumentParser(description='Generate text in the style of the text in the given files.')
  parser.add_argument('files', metavar='FILE', nargs='+',
                      help="The files to use for language model training.")
  parser.add_argument('--lines', dest='lines', type=int, default=10,
                      help="The number of lines of text to generate. Default: 10")
  parser.add_argument('--order', dest='order', type=int, default=4,
                      help="The order of the n-gram model (the maximum 'n'). Default: 4")
  parser.add_argument('--chars', dest='chars', default='false',
                      help="Use a character-based model instead of a word-based model. Default: false")
  parser.add_argument('--stop_symbols', dest='stop_symbols', default='',
                      help="Symbols that will stop the generation of a single text. This is optional, but an example might be --stop_symbols=\".?!\"")
  parser.add_argument('--backoff_exponent', dest='backoff_exponent', type=float, default=3,
                      help="A higher exponent means that the model will be less likely to randomly use shorter contexts. Default: 3")
  args = parser.parse_args()
  chars = (len(args.chars) and args.chars.lower()[:1] in 'ty')

  # chars = False; order = 4; stop_symbols = ''
  # chars = True;  order = 7; stop_symbols = ''

  debuglog('Reading Corpus')
  corpus = read_corpus(args.files, chars=chars, remove_newlines=False)
  debuglog('Constructing NGramModel')
  model = NGramModel(corpus, order=args.order, smoothing_count=1.0, backoff_exponent=args.backoff_exponent)
  debuglog('Generating Texts')
  for _ in range(args.lines):
    separator = '' if chars else ' '
    text = separator.join(model.generate(stop_symbols=set(args.stop_symbols), max_length=-1))
    text = re.sub('[“”]', '"', text)
    text = re.sub('[‘’]', "'", text)
    text = re.sub('^ ', '', text)
    text = re.sub(' ([.,?!:;\\)’”])', '\\1', text)
    text = re.sub('([\\(‘“]) ', '\\1', text)
    text = re.sub('" ([^"]+) "', '"\\1"', text)
    text = re.sub('_ ([^_]+) _', '_\\1_', text)
    text = re.sub('- - - -', '----', text)
    text = re.sub('- -', '--', text)
    text = re.sub(' - ', '-', text)
    print(text, '\n')
