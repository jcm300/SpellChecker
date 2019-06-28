#!/usr/bin/env python3

from collections import Counter
import sys, re, pickle, os, getopt, gc

def clean_text(lines):
    for i in range(len(lines)):
        lines[i] = re.sub(r"\s+", " ", lines[i])
        lines[i] = re.sub(r"[,.:;!?]",r"",lines[i])
        lines[i] = lines[i].lower()
    return lines

def calc_ngrams(lines,n):
    #separar por palavras
    words_a = []
    for line in lines:
        aux = re.split("\s+",line)

        #remove empty elems
        while "" in aux:
            aux.remove("")

        words_a.append(aux)

    words = []
    for wl in words_a:
        words.extend(wl)

    #release memory
    del words_a
    gc.collect()

    #n grams of words
    ngrams = [" ".join(words[i:i+n]) for i in range(len(words)-(n-1))]

    #release memory
    del words
    gc.collect()

    occur = dict(Counter(ngrams))
    return occur

def build(file,n):
    text = open(file).read()
    lines = text.split("\n")
    lines = clean_text(lines)
    occur = calc_ngrams(lines,n)

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

    words = re.split("(\s+|[,.:;!?])",text)

    while "" in words:
        words.remove("")

    words_backup = words.copy()
    
    i = 0
    length = len(words)
    while i < length:
        if re.match("\s+|[,.:;!?]",words[i]):
            del words[i]
            length -= 1
        else:
            words[i] = words[i].lower()
            i += 1
    
    return (words,words_backup)

def get_ngrams_aux(words):
    ngrams = [" ".join(words[j:j+n]) for j in range(0,len(words)-n+1)]

    while "" in ngrams:
        ngrams.remove("")

    return ngrams

def get_ngrams(words,i,n):
    if i == 0:
        if i == len(words)-1:
            words_used = [words[i]]
        else:
            words_used = words[i:i+n]
    else:
        if i == len(words)-1:
            words_used = words[i-n+1:i+1]
        else:
            words_used = words[i-n+1:i+n]

    ngrams = get_ngrams_aux(words_used)
    return ngrams

def get_ngrams_sub(words,new_word,i,n):
    if i == 0:
        if i == len(words)-1:
            words_used = [new_word]
        else:
            words_used = [new_word]+words[i+1:i+n]
    else:
        if i == len(words)-1:
            words_used = words[i-n+1:i]+[new_word]
        else:
            words_used = words[i-n+1:i]+[new_word]+words[i+1:i+n]

    ngrams = get_ngrams_aux(words_used)
    return ngrams

def get_occur(ngrams, loaded_ngrams):
    occur = {}
    for ngram in ngrams:
        occur[ngram] = loaded_ngrams.get(ngram,0)

    return occur

def construct_regex(s,c,d):
    if c != "":
        if d != "":
            regex = r"^("+c+r")"+s+r"("+d+r")$"
        else:
            regex = r"^("+c+r")"+s+r"$"
    else:
        if d != "":
            regex = r"^"+s+r"("+d+r")$"
        else:
            regex = r"^"+s+r"$"

    return regex

def get_match_group(match,n):
    try:
        group = match.group(n)
    except:
        group = None

    return group

def get_regex_sub(match,c):
    group1 = get_match_group(match,1)
    group2 = get_match_group(match,2)

    if group1!=None:
        if group2!=None:
            regex_sub = r'' + group1 + c + group2
        else:
            regex_sub = r'' + group1 + c
    else:
        if group2!=None:
            regex_sub = r'' + c + group2
        else:
            regex_sub = r'' + c

    return regex_sub

def sub(words, i, n, loaded_ngrams, match, c):
    ngrams = get_ngrams(words,i,n)
    occur = get_occur(ngrams,loaded_ngrams)
    sum_r = sum(occur.values())

    regex_sub = get_regex_sub(match, c)

    ngrams_sub = get_ngrams_sub(words,regex_sub,i,n)
    occur_sub = get_occur(ngrams_sub,loaded_ngrams)
    sum_sub = sum(occur_sub.values())

    if sum_sub > sum_r:
        words[i] = regex_sub

def recover_text(words, words_backup):
    i = 0
    j = 0
    len_b = len(words_backup)
    len_w = len(words)
    while i < len_b and j < len_w:
        if not re.match("\s+|[,.:;!?]",words_backup[i]):
            words_backup[i] = words[j]
            j += 1
        i += 1

    text_spell_checked = "".join(words_backup)
    return text_spell_checked

def spell_check(filename,n):
    try:
        file = open(filename, "r")
    except:
        print(f"{filename}: File not found...")
        sys.exit(1)

    loaded_ngrams = load_ngrams(n)
    configfile = load_configfile()

    text = file.read() 
    #words only have words and words backup have words and other symbols that are not words to recovery later the text
    (words, words_backup) = get_words(text)
    
    for (a,b,c,d) in configfile:
        for i in range(len(words)):
            a_regex = construct_regex(a,c,d)
            b_regex = construct_regex(b,c,d)

            a_match = re.match(a_regex,words[i])
            b_match = re.match(b_regex,words[i])

            if a_match:
                sub(words, i, n, loaded_ngrams, a_match, b)
            elif b_match:
                sub(words, i, n, loaded_ngrams, b_match, a)

    text_spell_checked = recover_text(words, words_backup)
    return text_spell_checked
        
def printHelp():
    print("Usage: ./main.py [OPTIONS] [FILENAME] [N-GRAM-SIZE]")
    print("Default behaviour: output spell checked file content")
    print("\nOptions:")
    print("  -b\tBuild N-Grams dataset")
    print("  -o\tOutput filename of default behaviour")
    print("  -h\tHelp")
    print("\nExample: ./main.py text.txt 2")

try:
    opts, args = getopt.getopt(sys.argv[1:], "bho:")
    opts = dict(opts)
except:
    printHelp()
    sys.exit(1)

b = opts.get('-b',None)
h = opts.get('-h',None)
o = opts.get('-o',None)

if h!=None:
    printHelp()
    sys.exit(1)
else:
    try:
        n = int(args[1])
    except:
        printHelp()
        sys.exit(1)

    if b!=None:
        build(args[0],n)
    else:
        if o!=None:
            out = open(o,"w")
        else:
            out = sys.stdout

        out.write(spell_check(args[0],n))
