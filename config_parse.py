#!/usr/bin/python
#Class for parsing the config.txt file
import re

class ConfigParse:
   'Holds all information about the uut for the testbench'

   def __init__(self):
      self.uut_path = "root"
      self.uut_name = "mod"
      self.libraries = []
      self.submodules = []
      self.timescale = "ps"
      self.clocks = []
      self.resets = []
      self.runtime = ""
      return

   def parseConfig(self, filename):
      configfile = open(filename, "r")
      for line in configfile:
         line.strip('\n\r')
         if re.match('^U(?i)U(?i)T(?i):', line):
            path = re.findall('/\S+\.s*v', line)
            name = re.findall('/\S+/(\S+)\.s*v', line)
            #Throw error if wrong
            self.uut_path = path[0]
            self.uut_name = name[0]
         elif re.match('^[Ss]ub[a-z.]+: ',line):
            path = re.findall('/\S+\.s*v', line)
            name = re.findall('/\S+/(\S+)\.s*v', line)
            self.submodules.append((name[0],path[0]))
         elif re.match('^[Cc]lock:', line):
            name = re.findall('^[Cc]lock: (c\S+)', line)
            value = re.findall('^[Cc]lock: c\S+ ([0-9.]+)', line)
            clock_tup = (name[0], value[0])
            self.clocks.append(clock_tup)
         elif re.match('^[Rr]eset[a-z]*:', line):
            line = re.sub(re.compile('^[Rr]eset[a-z]*:'),"",line)
            rsts = re.findall('([a-zA-Z0-9_.]+)[,\n]', line)
            for rst in rsts:
               self.resets.append(rst)
         elif re.match('^[Ll]ibrar[a-z]+: ',line):
            line = re.sub(re.compile('^[Ll]ibrar[a-z]+: '),"",line)
            libs = re.findall('([a-zA-Z0-9_.]+)[,\n]',line)
            for lib in libs:
              self.libraries.append(lib)
         elif re.match('^[Tt]imescale:', line):
             time = re.findall('^[Tt]imescale: (.s)', line)
             self.timescale = time[0]
         elif re.match('^[Rr]untime:', line):
             run  = re.findall('^[Rr]untime: ([0-9.]+\Ss)', line)
             self.runtime = run[0]
         else:
            #Throw and error
            print "N/A"
      configfile.close()
      return
