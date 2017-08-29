# JBS Problem

The root directory contains

- The original JBS Problem paper - `462.pdf`  
- A slightly modified DPOPagentJACOP file which FRODO uses - `DPOPagentJACOP.xml`  
- Results of the FRODO-DPOP for some problem instances - `NewProblemInstances.txt`  

### Constraint Generator for FRODO - `ConstraintGen`  
This directory contains the code for the constraint generator that generates an XML constraint file which can be used by a DCOP algorithm from the FRODO suite.  
To run: `python 1D_JBS_Gen.py`  
Takes the setting in `1DJBSInput.txt` as input and generates the constraints in the file `1DJBS.xml`.  
`1DJBSInput.txt` format:  
numofusers  
numofbs  
u(num)/b(num)  

### 1D Centralized 2 Approx Algorithm - `2Approx`
We use the `lpsolve` solver here, on Windows because of the GUI on offer.  
This is a pipeline:  
1. `python 2ApproxAlgo.py` - uses the setting from `1DJBSInput.txt` to generate the first stage output in `stage1.csv` and `endvars.csv`  
2. Proceed to find all the maximal cliques using the Bron Kerbosch algorithm `python maximal_cliques_alt.py` - uses `stage1.csv` and writes to `stage2.csv`  
3. Generate the constraints for lpsolve to use `python ConstraintGen.py` - uses `stage2.csv`, `1DJBSInput.txt` and `endvars.csv` for input and writes to `constraintfile.lp`  
4. `Double click` on the `constraintfile.lp` constraint file to use lpsolve to solve the LP. Export the result and save it as `constraintfile.lp.csv`  
5. Finally, `python coloring.py` - uses `constraintfile.lp.csv`, `1DJBSInput.txt` and `stage1.csv` as input and outputs the `optimal value for the relaxed LP solved using lpsolve` first and the `number of rounds` needed second, `on the terminal itself`. This `number of rounds` is within a factor of 2 of the optimal number of rounds needed and hence the name 2 approx algorithm  

### 1D Centralized DP algorithm for the special case of evenly spaced Base Stations - `temp-master`
This is `Chirag's` work.  
Contains code for generating settings which can be fed into `1DJBSInput.txt` and more importantly, contains code for the centralized DP algo which solves the special case of evenly spaced Base Stations.  

Credits for `Finding all maximal cliques` code goes to <https://gist.github.com/abhin4v/8304062>

