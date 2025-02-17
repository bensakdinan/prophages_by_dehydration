prophages_by_dehydration.py Description

This script is designed to retrieve any prophages present in any sample (from
an output of PropagAtE), and the corresponding prophage read:host 
read depth ratios of that prophage in a given sample it is present in.
This script was written to analyze data for my MSc project "Exploring how 
phage predation, prophage induction, and antibiotic exposure inform 
cholera disease severity" as part of my 2nd aim bioinformatic workflow

This script is designed to work on output data from PropagAtE, a tool to identify
actively replicating prophages (prophage induction).
    Kieft, K., and Anantharaman, K. (2022). Deciphering active prophages from metagenomes. 
    mSystems, 7 (2), e00084-22.

Dependencies:
- Pandas >= 0.24.2
- Python >= 3
  - Was written with Python/3.11

Required command line input arguments:
- all_prophages_names.txt
  - A text file that contains all the prophage names on a new line
- all/prophages/file/path.csv
  - .csv file that contains:
    - 'Prophage','Sample',prophage-host_ratio
- metadata/file/path.csv
  - .csv file that contains metadata for each **Sample** 
  - Can contain any metadata, but **Must** include:
    - 'Sample','Dehydration_Status'
- output/csv/path.csv
  - Path to output file
- Example call python prophages_by_dehydration.py all_prophages_names.txt all/prophages/file/path.csv metadata/file/path.csv output/csv/path.csv

Output:
- The output file is a .csv file that contains every prophage (by row)
  - 3 columns, 'Mild', 'Moderate', 'Severe', that contain Python lists
    of any and all prophage:host read ratios at the given dehydration status

    ![image](https://github.com/user-attachments/assets/1c844c2b-1ec1-4c0b-bc8c-5482b1b224cb)

