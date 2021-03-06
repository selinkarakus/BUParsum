import enum
import re
import sys
from collections import defaultdict 
import matplotlib.pyplot as plt
!pip install --upgrade matplotlib
from numpy import array
import pandas as pd
import seaborn as sns
import numpy as np


print(" [1] English \n [2] German \n [3] Turkish \n [4] French \n [5] Spanish \n [6] I will provide my own English text. ")
options = []
options = input ("Enter your options or options with commas in between: \n (e.g.: \"1\" or \"1, 2\") \n")
options = options.split(", ")

lang_dict = {1: 'English', 2:'German', 3:'Turkish', 4:'French', 5: 'Spanish'}

orig_input = input("Please enter the feature or features you would like to list with commas in between each feature:\n(ex.: \"DET\" or \"ADV, SUB\", etc.)\n")
temp_inp = orig_input.split(', ')

df = pd.DataFrame()


for option in options:
  input_list = []
  if option == '1':
    default_lang = '/content/en_partut-ud-dev.conllu'
    language = 'English'
  elif option == '2':
    default_lang = '/content/de_gsd-ud-dev.conllu'
    language = 'German'
  elif option == '3':
    default_lang = '/content/tr_boun-ud-dev.conllu'  
    language = 'Turkish'
  elif option == '4':
    default_lang = '/content/fr_partut-ud-dev.conllu'
    language = 'French'
  elif option == '5':
    default_lang = '/content/es_gsd-ud-dev.conllu'
    language = 'Spanish'
  elif option == '6':
    default_lang = []
    language = 'Your data'
  else:
    print("Invalid input.")
    #sys.exit()

  main_output = []

  #Some parts of this code was taken from a project by Karahan Sahin
  #https://github.com/karahan-sahin/Char-Level-Morphological-Parsing-with-Transformers

  def parser(file_names, output_name):
      """This function takes a language data file input that was written in line with the Universal Dependencies guidelines, parses it and returns the parsed data in txt format."""
      output = []

      for file_name in file_names:

          ud_file = open(f'{file_name}', 'r', encoding='utf-8').read()

          REGEX_BLOCK = '(\# sent_id = (.+?)\n# text = (.+?)\n)((.|\n)+?)\n(?=# sent_id)'

          parses = re.findall(REGEX_BLOCK, ud_file)

          pos_unique = set()

          for parse in parses:

              idt = parse[1]
              lines = parse[3].split('\n')

              sent = ""
              forms = []

              for line in lines[:-1]:

                  tokens = line.split('\t')

                  form = tokens[1]
                  lemma = tokens[2]
                  POS = tokens[3] 
                  features = tokens[5]

                  pos_unique.add(POS)

                  #print(line)

                  if lemma == "_" and len(forms) > 0:
                      forms[-1] = forms[-1] + form
                  
                  else:
                      forms.append(form) 

                  feature_find = '+'.join([i for i in features.split('|')])

                  features = '+'.join([i for i in features.split('|')])
                  
                  if lemma == "_":

                      sent += f"DB^{POS}+{features}"

                  else:

                      if POS == "PUNCT":

                            sent += f" {form}+{POS}"

                      else:

                          if features:

                              sent += f" {lemma}+{POS}+{features}"

                          else:

                              sent += f" {lemma}+{POS}"

              output.append((forms, sent.lstrip().split(), idt))

      with open(f"{output_name}.txt", "w+", encoding='utf-8') as f_out:

          for f, t, idt in output:

              for i, j in zip(f, t):

                  f_out.write(f"{i}\t{j}\t{idt}\n")

  parser([default_lang], "parse_datatest")

  with open('/content/parse_datatest.txt', 'r') as file:
      data = file.read().replace('\n','')
  
  for i in range(len(temp_inp)):
    input_list.append(temp_inp[i])

  output_dict = {}
  for element in input_list:
    output_dict[element] = len(re.findall(f".+?{element}", data))
  output_dict
  temp_df = pd.DataFrame({'x':list(output_dict.keys()),'y': list(output_dict.values())})
  temp_df['Language'] = language
  df=pd.concat([df, temp_df])

plt.figure(figsize=(8, 6))
splot=sns.barplot(x='x',y='y',data=df ,hue='Language')
plt.xlabel("Features", size=16)
plt.ylabel("Values", size=16)

for i in range(len(options)):
  plt.bar_label(splot.containers[i])

plt.savefig("visualized_data.png")
  
plt.show()
