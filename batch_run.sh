OUTDIR=/vols/cms04/mc3909/DM/140530/$SGE_TASK_ID/
COM=8000
NEVENTS=10000
i=0
cd /home/hep/mc3909/DMchain/
source setup.sh
while read DMmin DMlin
do
i=$(($i+1))

DMmass[$i]=$DMmin
DMlambda[$i]=$DMlin

done < input_masses.txt
echo Running for $i samples
python run_chain.py --outdir=$OUTDIR --DMmass=${DMmass[$SGE_TASK_ID]} --DMlambda=${DMlambda[$SGE_TASK_ID]} --cmenergy=$COM --nevents=$NEVENTS --spin=-2 --ga=1.0 --gaq=0.3 --gv=0.0
