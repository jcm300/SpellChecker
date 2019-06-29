# Installation of n-grams dictionary

- Unzip
```
cat spellcheck-pt-words-2.pkl.gz_aa spellcheck-pt-words-2.pkl.gz_ab spellcheck-pt-words-2.pkl.gz_ac spellcheck-pt-words-2.pkl.gz_ad > spellcheck-pt-words-2.pkl.gz
gunzip spellcheck-pt-words-2.pkl.gz

cat spellcheck-pt-words-3.pkl.gz_aa spellcheck-pt-words-3.pkl.gz_ab spellcheck-pt-words-3.pkl.gz_ac spellcheck-pt-words-3.pkl.gz_ad spellcheck-pt-words-3.pkl.gz_ae spellcheck-pt-words-3.pkl.gz_af spellcheck-pt-words-3.pkl.gz_ag spellcheck-pt-words-3.pkl.gz_ah spellcheck-pt-words-3.pkl.gz_ai spellcheck-pt-words-3.pkl.gz_aj spellcheck-pt-words-3.pkl.gz_ak spellcheck-pt-words-3.pkl.gz_al > spellcheck-pt-words-3.pkl.gz
gunzip spellcheck-pt-words-3.pkl.gz
```

- Create pickle folder
```
mkdir ~/.pickle
```

- Move corpus to pickle folder
```
mv spellcheck-pt-words-2.pkl spellcheck-pt-words-3.pkl ~/.pickle
```
