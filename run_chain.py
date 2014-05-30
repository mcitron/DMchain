import subprocess
import make_powheg
import argparse
import os
import shutil
from vectorwidth import vectorwidth

def parse_args():
 parser=argparse.ArgumentParser(
         formatter_class=argparse.ArgumentDefaultsHelpFormatter,
         fromfile_prefix_chars='@') 
 parser.add_argument('--outdir',required=True)
 parser.add_argument('--nevents',type=int,default=100)
 parser.add_argument('--cmenergy',type=int,default=8000)
 parser.add_argument('--DMmass',type=float,default=100)
 parser.add_argument('--DMlambda',type=float,default=1000)
 parser.add_argument('--spin',type=float,default=-1)
 parser.add_argument('--gv',type=float,default=0.0)
 parser.add_argument('--ga',type=float,default=0.0)
 parser.add_argument('--gaq',type=float,default=0.0)
 parser.add_argument('--powheginput',default="NAN")
 return parser.parse_args()
def run_chain(cmenergy,nevents,DMmass,DMlambda,outputdir,spin,gv,ga,gaq,userpow="NAN"):
#cmenergy=8000
#nevents=100
#DMmass=120
#DMlambda=1000
 #make sure to work with absolute paths
 powhegdir="/home/hep/mc3909/HEP_prog/POWHEG-BOX-V2/DMV/"
 delphesdir="/home/hep/mc3909/HEP_prog/Delphes-3.1.0/"
 pythiadir="/home/hep/mc3909/pythia-delphes/pythia8183/examples/"

 powhegdir=os.path.abspath(powhegdir)
 pythiadir=os.path.abspath(pythiadir)
 delphesdir=os.path.abspath(delphesdir)

 powheg_log=os.path.join(outputdir,'powheg-output.log')
 pythia_log=os.path.join(outputdir,'pythia-output.log')
 delphes_log=os.path.join(outputdir,'delphes-output.log')

 powheg_input=os.path.join(outputdir,'powheg.input')
 powheg_out=os.path.join(outputdir,'pwgevents.lhe')
 pythia_out=os.path.join(outputdir,'pythia-output.hepmc')
 delphes_out=os.path.join(outputdir,'delphes-output.root')
 #Remove current output
 if(os.path.isfile(powheg_out)):
  os.remove(powheg_out)
 if(os.path.isfile(delphes_out)):
  os.remove(delphes_out)
#Make output dir
 if not os.path.exists(outputdir):
  os.makedirs(outputdir)
#Check for user powheg_input
 if (userpow is "NAN"):
  DMwidth =  vectorwidth(DMlambda,DMmass,gv,ga,gaq,"False")
#DMlambda,DMmass,gv,ga,gaq,getcoupling,width
  print(DMwidth)
  phinput=make_powheg.make_powheg_input(cmenergy,nevents,DMmass,DMlambda,DMwidth,spin)
 else:
  with open(userpow,'r') as powin:
   phinput=powin.read()
   print(phinput)

 os.chdir(outputdir)   
 f = open(powheg_input,'w')
 f.write(phinput) 

 with open(powheg_log,'w') as f:
  subprocess.call([os.path.join(powhegdir,"pwhg_main")],stdout=f) 
 os.chdir(pythiadir)   
 with open(pythia_log,'w') as f:
  subprocess.call(["./mymain.exe",os.path.join(outputdir,"pwgevents.lhe"),pythia_out],stdout=f) 
 os.chdir(delphesdir)   
 with open(delphes_log,'w') as f:
  subprocess.call(["./DelphesHepMC","examples/delphes_card_CMS.tcl",os.path.join(outputdir,"delphes-output.root"),pythia_out],stdout=f) 

if __name__=="__main__":
 args=parse_args()
 outdir=os.path.abspath(args.outdir)
 nevents=args.nevents
 cmenergy=args.cmenergy
 spin=args.spin
 DMmass=args.DMmass
 DMlambda=args.DMlambda
 userpow=args.powheginput
 ga=args.ga
 gv=args.gv
 gaq=args.gaq
 print (userpow)
 run_chain(cmenergy,nevents,DMmass,DMlambda,outdir,spin,gv,ga,gaq,userpow)

