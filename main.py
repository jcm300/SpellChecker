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
        file = open(os.environ["HOME"]+f"/.pickle/spellcheck-pt-words-{n}.pkl", "rb")
    except:
        print(f"~/.pickle/spellcheck-pt-words-{n}.pkl: File not found... Build first!")
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
        try:
            regexs.append((aux[0],aux[1],aux[2],aux[3]))
        except:
            print("Error on configfile.... Syntax error!")
            sys.exit(1)

    return regexs

def get_words(text):
    text = clean_text(text)

    #separar por palavras
    words = re.split("\s+",text)

    #remove empty elems
    while "" in words:
        words.remove("")

    return words

def get_ngrams(words,i,n):
    if i == 0:
        ngrams = [" ".join(words[j:j+n]) for j in range(0,i+n-1)]
    elif i == len(words)-1:
        ngrams = [" ".join(words[j:j+n]) for j in range(i-n+1,len(words)-1)]
    else:
        ngrams = [" ".join(words[j:j+n]) for j in range(i-n+1,i+n-1)]

    while "" in ngrams:
        ngrams.remove("")

    return ngrams

def get_occur(ngrams, loaded_ngrams):
    occur = {}
    for ngram in ngrams:
        occur[ngram] = loaded_ngrams.get(ngram,0)

    return occur

def construct_regex(s,c,d):
    if c != "":
        if d != "":
            regex = r"("+c+r")"+s+r"("+d+r")"
        else:
            regex = r"("+c+r")"+s
    else:
        if d != "":
            regex = r""+s+r"("+d+r")"
        else:
            regex = r""+s

    return regex

def classify(filename,n):
    try:
        file = open(filename, "r")
    except:
        print("{filename}: File not found...")
        sys.exit(1)

    loaded_ngrams = load_ngrams(n)
    configfile = load_configfile()

    text = file.read() 
    words = get_words(text)
    print(words)
    
    for (a,b,c,d) in configfile:
        for i in range(len(words)):
            a_regex = construct_regex(a,c,d)
            b_regex = construct_regex(b,c,d)

            if re.match(a_regex,words[i]):
                a_ngrams = get_ngrams(words,i,n)
                occur_a = get_occur(a_ngrams,loaded_ngrams)
                sum_a = sum(occur_a.values())

                print(sum_a)
                #TODO: fazer o mesmo para o caso com b, mas para este caso em especifico, ou seja trocar nos ngrams o a_regex por b_regex

            elif re.match(b_regex,words[i]):
                b_ngrams = get_ngrams(words,i,n)
                occur_b = get_occur(b_ngrams,loaded_ngrams)
                sum_b = sum(occur_b.values())

                print(occur_b)
                #TODO: fazer o mesmo para o caso com a, mas para este caso em especifico, ou seja trocar nos ngrams o b_regex por a_regex
        
        #occur_a = {}
        #for ngram in a_ngrams:
        #    occur_a[ngram] = loaded_ngrams.get(ngram,0)

        #occur_b = {}
        #for ngram in b_ngrams:
        #    occur_b[ngram] = loaded_ngrams.get(ngram,0)

classify(args[0],int(args[1]))

    #TODO
    #for each line of config file:
        #filter ngrams, get only ngrams that contains one word that respect one of the regexs
        #for each case, get from load ngrams if are more cases with first regex or with the second regex. Maybe will be a problem, because is calculated ngrams for input so an occurence in the input file will appear more than one time, maybe can make the sommatory of all cases
