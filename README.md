# Split Network Interpreter

Welcome to the repository for the Split Network Interpreter (SNI). This tool can process a nexus file produced by [SplitsTree4](https://ab.inf.uni-tuebingen.de/software/splitstree4). Once the .nexus file is processed, the SNI will display the results on a window display. 

---
## How to run

 1. Download the project from this repository. 
 2. In the command line run `python3 split_network_interpreter.py`
 3. Push the upload button to upload a .nex or .nexus file. 
 4. Initalise your settings. 
 5. View the output. 

## Settings

 1. Top splits.
 2. Partition-Split similarity limit.
 3. Partition metric.
 4. Multithreading.
 5. Colourblind mode. 
---
#### Top splits
This will select the top weighted splits. The lower the number of splits, the faster it will run!

#### Partition-Split similarity limit.
The partition-similarity score will change score needed to associate a partition with a split.

#### Partition metric.
The two options are available. The Rand index and Jaccard index. These are very similar and may not affect the output much. 

#### Multithreading.
This will take advantage of any extra cores available on your PC to make the program run faster. 

#### Colourblind mode. 
The first 20 splits are distinct colours and are 95% accessible to all users. Following that the guarentee of accessible colours cannot be made as an algorithm will be used to generate as many colours as are needed.
