#Class to parse verilog and systemverilog files
import re

class VerilogParse:
   'Hold all information about the uut verilog file'

   def __init__(self, submodules):
      self.parameters = []
      self.inputs = []
      self.outputs = []
      self.internals = []
      self.submodules = submodules
      return

   def parseVerilog(self, filename):
      verilogfile = open(filename, "r")
      for line in verilogfile:
         line.strip('\r')
         if re.search('P(?i)arameter\s+\S+', line):
            line = re.sub(re.compile('//.*?\n'),"",line) #Removes comments
            param_tup = re.findall('P(?i)arameter (\S+) = ([0-9.]+)', line)
            self.parameters.append(param_tup[0])
         #Still need to fix comment on same line problem
         elif re.search('^\s+I(?i)nput\s+\S+', line):
            line = re.sub(re.compile('//.*?\n'),"",line) #Removes comments
            name = re.findall('([a-zA-Z0-9_.]+)[,\n]', line)
            value = re.findall('\[([a-zA-Z0-9]\S*):[a-zA-Z0-9]\S*\]', line)
            if len(value): #Resolve params to defaults
               for i in range(len(self.parameters)):
                  if value[0] == (self.parameters[i][0] + '-1'):
                     value[0] = self.parameters[i][1]
            else:
               value = '1'
            for var in name:
               self.inputs.append((var,value[0]))
         elif re.search('^\s+O(?i)utput\s+\S+', line):
            line = re.sub(re.compile('//.*?\n'),"",line) #Removes comments
            name = re.findall('([a-zA-Z0-9_.]+)[,\n]', line)
            value = re.findall('\[([a-zA-Z0-9]\S*):([a-zA-Z0-9]\S*)\]', line)
            if len(value): #Resovle params to defaults
               for i in range(len(self.parameters)):
                  if value[0] == (self.parameters[i][0] + '-1'):
                     value[0] = self.parameters[i][1]
            else:
               value = '1'
            for var in name:
               self.outputs.append((var,value[0]))
         elif re.search('^\s+reg\s+\S+',line):
            line = re.sub(re.compile('//.*?\n'),"",line) #Removes comments
            name = re.findall('([a-zA-Z0-9_.]+)[,;]', line)
            value = re.findall('\[([a-zA-Z0-9]\S*):[a-zA-Z0-9]\S*\]', line)
            if len(value): #Resovle params to defaults
               for i in range(len(self.parameters)):
                  if value[0] == (self.parameters[i][0] + '-1'):
                     value[0] = self.parameters[i][1]
            else:
               value = '1'
            for var in name:
               if len(value):
                  if (int(value[0])+1) > 7 or (int(value[0])+1)%4 == 0:
                     self.internals.append((var,'hexadecimal'))
                  else:
                     self.internals.append((var,'binary'))
               else:
                  self.internals.append((var,'binary'))
         elif re.search('^\s+logic\s+\S+',line):
            line = re.sub(re.compile('//.*?\n'),"",line) #Removes comments
            name = re.findall('([a-zA-Z0-9_.]+)[,;]', line)
            value = re.findall('\[([a-zA-Z0-9]\S*):[a-zA-Z0-9]\S*\]', line)
            if len(value): #Resovle params to defaults
               for i in range(len(self.parameters)):
                  if value[0] == (self.parameters[i][0] + '-1'):
                     value[0] = self.parameters[i][1]
            else:
               value = '1'
            for var in name:
               if len(value):
                  if (int(value[0])+1) > 7 or (int(value[0])+1)%4 == 0:
                     self.internals.append((var,'hexadecimal'))
                  else:
                     self.internals.append((var,'binary'))
               else:
                  self.internals.append((var,'binary'))
         elif re.search('^\s+wire\s+\S+',line):
            line = re.sub(re.compile('//.*?\n'),"",line) #Removes comments
            name = re.findall('([a-zA-Z0-9_.]+)[,;]', line)
            value = re.findall('\[([a-zA-Z0-9]\S*):([a-zA-Z0-9]\S*)\]', line)
            if len(value): #Resovle params to defaults
               for i in range(len(self.parameters)):
                  if value[0] == (self.parameters[i][0] + '-1'):
                     value[0] = self.parameters[i][1]
            else:
               value = '1'
            for var in name:
               if len(value):
                  if (int(value[0])+1) > 7 or (int(value[0])+1)%4 == 0:
                     self.internals.append((var,'hexadecimal'))
                  else:
                     self.internals.append((var,'binary'))
               else:
                  self.internals.append((var,'binary'))
         elif re.search('//[A-Z_.]+?\n',line):
            name = re.findall('([A-Z_.]+?)\n',line)
            name = name[0].lower()
            for sub in self.submodules:
               if sub[0] == name:
                  vp = VerilogParse(self.submodules)
                  vp.parseVerilog(sub[1])
                  for signal in vp.internals:
                     self.internals.append(signal)
               else:
                  pass
         else:
            pass
      verilogfile.close()
      return
