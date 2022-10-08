

alphabet = {}

alphabet['a'] = '''
 █████
██   ██
███████
██   ██
██   ██
'''

alphabet['b'] = '''
█████
██   ██
█████
██   ██
█████
'''

alphabet['c'] = '''
 █████
██   ██
██
██   ██
 █████
'''

alphabet['d'] = '''
█████
██   ██
██   ██
██   ██
█████
'''

alphabet['e'] = '''
███████
██     
█████  
██     
███████
'''

alphabet['f'] = '''
███████
██     
█████  
██     
██
'''

alphabet['g'] = '''
 ██████ 
██      
██   ██ 
██    ██
██████  
'''

alphabet['h'] = '''
██   ██
██   ██
███████
██   ██
██   ██
'''

alphabet['i'] = '''
   ██

   ██
   ██
   ██
'''

alphabet['j'] = '''
   ██

   ██
█   █
 ███
'''

alphabet['k'] = '''
██    ██
██  ██
████
██  ██
██    ██
'''

alphabet['l'] = '''
██
██
██
██   ██
██████
'''

alphabet['m'] = '''
███    ███
██ █  █ ██
██  ██  ██
██      ██
██      ██
'''

alphabet['n'] = '''
███     ██
██ ██   ██
██  ██  ██
██   ██ ██
██     ███
'''

alphabet['o'] = '''
 ██████
██    ██
██    ██
██    ██
 ██████
'''

alphabet['p'] = '''
███████
██    ██
███████
██    
██
'''

alphabet['p'] = '''
███████
██    ██
███████
██
██
'''

alphabet['r'] = '''
███████
██    ██
███████
██  ██
██    ██
'''


alphabet['s'] = '''
 ██████
██     
 █████ 
     ██
██████ 
'''

alphabet['t'] = '''
████████
   ██   
   ██   
   ██   
   ██   
'''

alphabet['u'] = '''
██    ██
██    ██
██    ██
██    ██
 ██████
'''

alphabet['v'] = '''
█    █
█    █
 █  █
 █  █
  ██
'''


alphabet['w'] = '''
█       █
█       █
 █  █  █
 █  █  █
  ██ ██
'''

alphabet['x'] = '''
██    ██
 ██  ██
   ██
 ██  ██
██    ██
'''


alphabet['y'] = '''
██    ██
 ██  ██
  ████
   ██
   ██
'''

alphabet['z'] = '''
████████
     ██
   ██
 ██
████████
'''

alphabet[' '] = '''
       
       
         
        
        
'''


word = "forums"


out = ""
for line in range(0, 6):
    for letter in word:
        asc_ii = alphabet[letter]

        asc_ii_list = str(asc_ii).split("\n")
        # выравниваем по ширине
        max_width = 0
        for w in asc_ii_list:
            if len(w) > max_width:
                max_width = len(w)
        current = str(asc_ii_list[line]).ljust(max_width)
        out += current + "   "
    out += "\n"


print(out)


