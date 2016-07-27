#!/usr/bin/python
import sys
import re
from config_parse import *
from verilog_parse import *

def writeTestbench(cp, vp, tbfile):
   #write the timescale info
   tbfile.write("`timescale 1"+cp.timescale+"/1"+cp.timescale+"\n\n")
   #write the tb module name
   tbfile.write("module "+cp.uut_name+"_tb;\n\n")
   #write port input signal declarations
   for var in vp.inputs:
      if var[1] == '1':
         tbfile.write("logic "+var[0]+";\n")
      else:
         tbfile.write("logic ["+var[1]+":0] "+var[0]+";\n")
   tbfile.write("\n")
   #write port output signal declarations
   for var in vp.outputs:
      if var[1] == '1':
         tbfile.write("wire "+var[0]+";\n")
      else:
         tbfile.write("wire ["+var[1]+":0] "+var[0]+";\n")

   tbfile.write("\n")
   #write local clock params
   for clock in cp.clocks:
      tbfile.write("parameter half"+clock[0]+" = "+clock[1]+";\n")
   tbfile.write("\n")
   #write reset init statement
   for rst in cp.resets:
      tbfile.write("initial begin\n\t"+rst+" = 1'b0;\n\t#(1*half"+cp.clocks[0][0]+")\n")
      tbfile.write("\t"+rst+" = 1'b1;\n\t#(8*half"+cp.clocks[0][0]+")\n")
      tbfile.write("\t"+rst+" = 1'b0;\nend\n")
   #write init statements for clocks
   for clock in cp.clocks:
      tbfile.write("\ninitial begin\n\t"+clock[0]+" = 1'b0;\n\t")
      tbfile.write("forever #(half"+clock[0]+") "+clock[0]+" = ~"+clock[0]+";\nend\n")
   #write uut instantiation
   tbfile.write("\n"+cp.uut_name+" uut(\n")
   for var in vp.inputs:
      tbfile.write("\t."+var[0]+"("+var[0]+"),\n")
   for i in range(len(vp.outputs)):
      if i == (len(vp.outputs)-1):
         tbfile.write("\t."+vp.outputs[i][0]+"("+vp.outputs[i][0]+")\n")
      else:
         tbfile.write("\t."+vp.outputs[i][0]+"("+vp.outputs[i][0]+"),\n")
   tbfile.write(");\n")
   #write endmodule
   tbfile.write("\nTODO: STIMULUS GEN\n")
   tbfile.write("\nendmodule")
   return

def writeDoFile(cp, vp, dofile):
   #write the work lib
   dofile.write("vlib work\n\n")
   #write the compile statments
   dofile.write("vlog -work work "+cp.uut_path+"\n")
   dofile.write("vlog -work work "+cp.uut_name+"_tb.sv\n")
   #write vsim statement
   dofile.write("\nvsim -t 1"+cp.timescale+" novopt "+cp.uut_name+"_tb")
   if len(cp.libraries):
      dofile.write(" -L")
      for lib in cp.libraries:
         dofile.write(" "+lib) 
   dofile.write("\n\n")
   #write waves and signals
   dofile.write("view signals\nview wave\n\n")
   #write wave declarations
   for var in vp.inputs:
      label = re.sub('_',' ',var[0]).upper()
      if (int(var[1])+1) > 7 or (int(var[1])+1)%4 == 0:
         value = 'hexadecimal'
      else:
         value = 'binary'
      dofile.write("add wave -color Green -label {"+label+"} -radix "+value)
      dofile.write(" /"+cp.uut_name+"_tb/uut/"+var[0]+"\n")
   dofile.write("\n")
   for var in vp.internals:
      label = re.sub('_',' ',var[0]).upper()
      dofile.write("add wave -color Blue -label {"+label+"} -radix "+var[1])
      dofile.write(" /"+cp.uut_name+"_tb/uut/"+var[0]+"\n")
   dofile.write("\n")
   for var in vp.outputs:
      label = re.sub('_',' ',var[0]).upper()
      if (int(var[1])+1) > 7 or (int(var[1])+1)%4 == 0:
         value = 'hexadecimal'
      else:
         value = 'binary'
      dofile.write("add wave -color Yellow -label {"+label+"} -radix "+value)
      dofile.write(" /"+cp.uut_name+"_tb/uut/"+var[0]+"\n")
   #write run statement
   dofile.write("\nrun "+cp.runtime)
   return

#Main function
cp = ConfigParse()
cp.parseConfig(sys.argv[1])
vp = VerilogParse(cp.submodules)
vp.parseVerilog(cp.uut_path)

tbname = cp.uut_name + "_tb.sv"
tbfile = open(tbname, "w")
writeTestbench(cp, vp, tbfile)
tbfile.close()

doname = cp.uut_name + ".do"
dofile = open(doname, "w")
writeDoFile(cp, vp, dofile)
dofile.close()
