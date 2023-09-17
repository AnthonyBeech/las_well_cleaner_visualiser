import os
from wellcleaner import wellCleaner
from pathlib import Path


def list_las_files(directory):
    files_in_directory = os.listdir(directory)
    las_files = [file for file in files_in_directory if file.endswith(".las")]
    
    return las_files


# change dir to plae where .las files are stored
FLOC = str(Path(__file__).parent.parent) + "/tests/data"
os.chdir(FLOC)

las_files = list_las_files(FLOC)

for file in las_files:
    print(file)
    well = wellCleaner(file)
    well.calc()
    # wells.print_logs()
    well.write_las()
