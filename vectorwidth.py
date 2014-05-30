#!/usr/bin/python
# This script is for calculating the width of a vector or pseudo-vector into 
# quarks and dark matter, needed for monojet calculations.  MJD, July 2013.

import math
import argparse
import numpy as np 

# Quark masses
mt = 173.3
mb = 4.2
mc = 1.27
ms = 0.104
mu = 0.0024
md = 0.0048

quarks=[md,mu,ms,mc,mb,mt]
#quarks=[md,mu]

def fermion_width(mzp,mq,gv,ga,Nc):
    """Calculates the partial width of a Zprime into quarks.
    Should read in (mzp,mq,gv,ga,Nc). 
    """
    if mzp > 2 * mq:
        return (Nc*mzp/(12*math.pi)) * math.sqrt(1-(2*mq/mzp)**2) * (gv**2 + ga**2 + (mq/mzp)**2 *(2 * gv**2 - 4 * ga**2))
#        return (Nc*mzp/(12*math.pi)) * math.sqrt(1-np.power(2*mq/mzp,2)) * np.power(gv,2) + np.power(ga,2) + np.power(mq/mzp,2) *(2 * np.power(gv,2) - 4 * np.power(ga,2))
#        return  (Nc*mzp/(12*math.pi))
    else:
        return 0



def chiwidth(mzp,mchi,gv,ga):
    """Calculates the partial width of a Zprime into dark matter.
       Should read in (mzp,chi,gv,ga)
    """
    if mzp > 2 * mchi:
        return (mzp/(12*math.pi)) * math.sqrt(1-(2*mchi/mzp)**2) * (gv**2 + ga**2 + (mchi/mzp)**2 *(2 * gv**2 - 4 * ga**2))
#        return (mzp/(12*math.pi)) * math.sqrt(1-np.power((2*mchi/mzp),2)) * np.power(gv,2)+ np.power(ga,2) + np.power((mchi/mzp),2) *(2 * np.power(gv,2) - 4 * np.power(ga,2))
#        return (mzp/(12*math.pi)) * math.sqrt(1-(2*mchi/mzp)**2) * gv
    else:
        return 0


def threshfunc(mzp,m):
    if mzp > 2 * m:
        return math.pow((1-(2*m/mzp)**2),1.5)
    else:
        return 0



def calccoupling(mzp,mchi,width):
    """ Calculates the couplings g given the width Gamma/mmed"""
    quarkcont=0
    for q in quarks:
        quarkcont+=3*threshfunc(mzp,q)
    
    dmcont=threshfunc(mzp,mchi)
    
    coupling=width * pow(1/(12*math.pi)*(quarkcont+dmcont),-1)

    return math.sqrt(coupling)


def vectorwidth(mzp,mchi,gv,ga,gaq,getcoupling,width=0.0):
 # Code to read in program arguments
 quark_partials= [] 
 
 if getcoupling == "True":
     coupling=calccoupling(mzp,mchi,width)
 #    print coupling
 elif getcoupling == "False":
     totalwidth=chiwidth(mzp,mchi,gv,ga)
     for q in quarks:
         totalwidth+=fermion_width(mzp,q,gv,gaq,3)    
     return("%.1f" % totalwidth)
     #print totalwidth
 else:
     exit
 
