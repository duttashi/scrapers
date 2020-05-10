#!/usr/bin/env python
# coding: utf-8

# In[2]:


# load required libraries
import urllib
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
import string
import itertools

# Reference:

# https://github.com/tlfvincent/political_liars/blob/master/scrape_politifact.py
# https://github.com/tlfvincent/political_liars/blob/master/analysis.R

# create custom functions to acquire the data
def get_page_source(page):
    '''get HTML content of page'''
    try:
        url = 'http://www.politifact.com/truth-o-meter/statements/?page={}'.format(page)
        response = urllib2.urlopen(url)
        page_source = response.read()
        soup = BeautifulSoup(page_source, "html.parser")
        return soup
    except:
        print ("Could not obtain data for page {}".format(page))
        return None

def extract_truth(table,
                  truth_meter,
                  image_source,
                  statement_text):
    '''extract statement text, image of candidate and truth of statement'''
    for truth in table:
        fact = [item['alt'] for item in truth.findAll("img")]
        images = [item['src'] for item in truth.findAll("img") if '.jpg' in item['src']]
        statement = [item.text.strip() for item in truth.findAll("a", {"class": "link"})]
        if fact[1] in truth_meter:
            truth_meter[fact[1]].append(fact[0])
            statement_text[fact[1]].append(statement[0])
        else:
            truth_meter[fact[1]] = []
            truth_meter[fact[1]].append(fact[0])
            statement_text[fact[1]] = []
            statement_text[fact[1]].append(statement[0])
            image_source[fact[1]] = images[0]
    return truth_meter, image_source, statement_text

def process_page_data(soup,
                      truth_meter,
                      image_source,
                      statement_text):
    try:
        table = soup.findAll("div", {'class': 'scoretable__item'})
        truth_meter, image_source, statement_text = extract_truth(table,
                                                                  truth_meter,
                                                                  image_source,
                                                                  statement_text)
        return truth_meter, image_source, statement_text
    except:
        return truth_meter, image_source, statement_text


def main():
    truth_meter, image_source, statement_text = {}, {}, {}
    for page in range(1, 198):
        print (page)
        soup = get_page_source(page)
        if soup is not None:
            truth_meter, image_source, statement_text = process_page_data(soup,
                                                                          truth_meter,
                                                                          image_source,
                                                                          statement_text)

    # process statement strings for R
    statement_text_processed = {}
    for k, val in statement_text.items():
        val_no_punctuation = ["".join(l for l in sent if l not in string.punctuation)                               for sent in val]
        val_lower = [sent.lower() for sent in val_no_punctuation]
        if len(val_lower) > 1:
            val_tokenized = ' '.join(val_lower).split(' ')
        else:
            val_tokenized = val_lower[0].split(' ')
        statement_text_processed[k] = val_tokenized

    with open('./data/politifact_statements.txt', 'w') as outfile:
        json.dump(truth_meter, outfile)

    with open('./data/politifact_statements_text.txt', 'w') as outfile:
        json.dump(statement_text_processed, outfile)

    df = pd.DataFrame.from_dict(image_source.items())
    df.to_csv('./data/politifact_image_source.csv', index=False, encoding='utf-8')

# Show time
if __name__ == '__main__':
    main()
