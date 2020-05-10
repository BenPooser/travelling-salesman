===========================================================================

Ben Pooser
bpooser3@gatech.edu
4/13/20

===========================================================================

tsp-3510.py:
Python script containing the code for the travelling salesman algorithm
Contains previous work and brief comments for each section

README.txt:
File containing basic information, including name, email, date of 
submission, names and descriptions of submission files, instructions
for running the code, and any known bugs or limitations

mat-output.txt:
File that the program writes into after running the algorithm
First line contains cost of tour and second line contains the sequence
of node-IDs

algorithm.pdf:
A pdf document describing the algorithm in pseudocode and explaining the 
rationale behind its design

mat-output-10.txt
File that contains 10 runs from the mat-output.txt file, along with the
calculated mean and standard deviation

===========================================================================

Instructions for running program:

$ python3 tsp-3510.py <input-coordinates.txt>  <output-tour.txt> <time>


Example:

$ python3 tsp-3510.py mat-test.txt mat-output.txt 180

===========================================================================

Any known bugs or limitations:

N/A