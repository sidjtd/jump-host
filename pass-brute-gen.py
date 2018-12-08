#!/usr/bin/env python
# RUN THE COMMAND LIKE SO:
# python2.7 jump-host.py -c config.cfg 

import optparse
import ConfigParser
import itertools

def all_perms(itemList):
  perms = []
  n = len(itemList)

  for i in range (1,n+1):
    for perm in itertools.permutations(itemList,i):
      for connector in connectors:
          str = ''
          str += connector.join(perm)
          perms.append(str)
  return perms

def leetify(l): # Medico -> M3d1c0
  leeted = []
  aux = l
  v = len(replacements)
  for i in replacements:
    aux = [w.replace(i[0], i[1]) for w in aux]
    leeted.extend([w.replace(i[0], i[1]) for w in l])
  leeted.extend(aux)
  return leeted
  
def to_file(filename, wordlist):
  f = open ( filename, 'w' )
  wordlist = sorted(list(set(wordlist)))
  f.write ('\n'.join(wordlist))
  f = open ( filename, 'r' )
  lines = 0
  for line in f:
    lines += 1
  f.close()
  print "Saving wordlist ("+str(lines)+" words) to "+filename+"."

Config = ConfigParser.ConfigParser()

parser = optparse.OptionParser("usage %prog "+\
		"-c <configfile> -o <outputfile>")
parser.add_option('-c', dest='confname', type='string',\
			help='specify config filename')
parser.add_option('-o', dest='outputname', type='string',\
			help='specify output filename')
(options, arg) = parser.parse_args()
if (options.confname == None) | (options.outputname == None):
	confname = 'config.cfg'
	Config.read(confname)
	outputname = Config.get('Files', 'output')
else:
	confname = options.confname
	outputname = options.outputname
	Config.read(confname)

replacements = Config.items('Replacements');
items = list(Config.get('Params','keywords').split(','))
connectors = list(Config.get('Params','connectors').split(','))
num_tails = list(Config.get('Params','num_tails').split(','))
tails = list(Config.get('Params','tails').split(','))
min_lenght = Config.get('Options','min_length')
max_lenght = Config.get('Options','max_length')
output = outputname

m = len(items)
result = []

result.extend(all_perms(items))

if (Config.getboolean('Options','abbreviation')):
  # Abbr by element T[ab,cd,ef] -> t[a,cd,ef],t[ab,c,ef],t[ab,cd,e]
  abbr_items = list(items)
  for i in range(0,m):
    abbr_items = list(items)
    abbr_items[i] = abbr_items[i][0]
    result.extend(all_perms(abbr_items))

  # Abbr acum forward T[ab,cd,ef] -> t[a,cd,ef],t[a,c,ef],t[a,c,e]
  abbr_items = list(items)
  for i in range(0,m):
    abbr_items[i] = abbr_items[i][0]
    result.extend(all_perms(abbr_items))

  # Abbr acum backward T[ab,cd,ef] -> t[ab,cd,e],t[ab,c,e],t[a,c,e]
  abbr_items = list(items)
  for i in range(0,m):
    k = m-i-1
    abbr_items[k] = abbr_items[k][0]
    result.extend(all_perms(abbr_items))

if (Config.getboolean('Options','reverse')):
  # Reverse by element T[ab,cd,ef] -> t[ba,cd,ef],t[ba,dc,ef],t[ba,dc,fe]
  inv_items = list(items)
  for i in range(0,m):
    inv_items = list(items)
    inv_items[i] = inv_items[i][::-1]
    result.extend(all_perms(inv_items))
    
  # Reverse acum forward T[ab,cd,ef] -> t[ba,cd,ef],t[ba,dc,ef],t[ba,dc,fe]
  inv_items = list(items)
  for i in range(0,m):
    inv_items[i] = inv_items[i][::-1]
    result.extend(all_perms(inv_items))
    
  # Reverse acum backward T[ab,cd,ef] -> t[ab,cd,fe],t[ab,dc,fe],t[ba,cd,ef]
  inv_items = list(items)
  for i in range(0,m):
    k = m-i-1
    inv_items[k] = inv_items[k][::-1]
    result.extend(all_perms(inv_items))
  
result = sorted(list(set(result)))

if (Config.getboolean('Options','string_replacements')):
  result.extend(leetify(result))

# Add pretails and tails
aux = []
for item in result:
  for tail in tails:
    for pretail in num_tails:
      if "-" in pretail:
        limits = pretail.split('-')
        for x in range(int(limits[0]),int(limits[1])+1):
          aux.append(item+str(x)+tail)
      else:
        aux.append(item+pretail+tail)
        
result.extend(aux)

# Tolowercase
if (Config.getboolean('Options','to_lower')):
  aux = []
  for item in result:
    aux.append(item.lower())
  result.extend(aux)

# Filter by length
result = [elem for elem in result if (len(elem) > int(min_lenght) and len(elem) < int(max_lenght))]

to_file(output, result)