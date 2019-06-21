#!/usr/bin/env python3

from collections import Counter
import sys, re, pickle, os, getopt

opts, args = getopt.getopt(sys.argv[1:], "")
opts = dict(opts)

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[,.:;!?]",r"",text)
    text = text.lower()
    return text

def calc_ngrams(text,n):
    #separar por palavras
    ngrams = re.split("\s+",text)

    #remove empty elems
    while "" in ngrams:
        ngrams.remove("")

    #n grams of words
    ngrams = [" ".join(ngrams[i:i+n]) for i in range(len(ngrams)-(n-1))]
    occur = dict(Counter(ngrams))

    return occur

def build(file,n):
    text = open(file).read()
    text = clean_text(text)
    occur = calc_ngrams(text,n)

    print(occur)

    os.makedirs(os.environ["HOME"]+"/.pickle/", exist_ok=True)
    f = open(os.environ["HOME"]+f"/.pickle/spellcheck-pt-words-{n}.pkl", "wb")
    pickle.dump(occur, f, protocol = -1)

def load_ngrams(n):
    try:
        file = open(os.environ["HOME"]+"/.pickle/spellcheck-pt-{n}.pkl", "rb")
    except:
        print("~/.pickle/spellcheck-pt-{n}.pkl: File not found... Build first!")
        sys.exit(1)

    return pickle.load(file)

def load_configfile():
    try:
        file = open("configfile", "r")
    except:
        print("configfile: File not found... Define a config file!")
        sys.exit(1)

    text = file.read()
    lines = text.split("\n")
    
    #remove empty elems
    while "" in lines:
        lines.remove("")

    regexs = []
    for line in lines:
        aux = line.split(" ||| ")
        regexs.append((aux[0],aux[1]))

    return regexs

def classify(file,n):
    #TODO
    #load ngrams, and config file
    #calc ngrams for input file
    #for each line of config file:
        #filter ngrams, get only ngrams that contains one word that respect one of the regexs
        #for each case, get from load ngrams if are more cases with first regex or with the second regex. Maybe will be a problem, because is calculated ngrams for input so an occurence in the input file will appear more than one time, maybe can make the sommatory of all cases
