# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 11:50:56 2018

@author: poddo
"""

from Scripts.initialize import *

def alglist(string):
	
	string = string.lower()
	algs = QgsApplication.processingRegistry().algorithms()
	names = [alg.displayName() for alg in algs]
	
	indices = [i for i, s in enumerate(names) if string in s.lower()]
	
	if not indices:
		print("Algorithm not found")
	
	else:
		for ind in indices:
			print(f"'{algs[ind].id()}'", "->", algs[ind].displayName())


def alghelp(algorithm):
	processing.algorithmHelp(algorithm)
	
	
def get_coords(extent):
	ext = QgsVectorLayer(os.path.join('Layers', extent)).extent()
	rect = [ext.xMinimum(), ext.xMaximum(), ext.yMinimum(), ext.yMaximum()]
	rect = ['{:}'.format(x) for x in rect]
	out = ",".join(rect)
	return(out)
	
def cleanup(dir):
	for fname in os.listdir(dir):
		if 'final' not in fname:
			#delfile = str(os.path.join(dir, fname))
			os.remove(str(os.path.join(dir, fname)))
            
            