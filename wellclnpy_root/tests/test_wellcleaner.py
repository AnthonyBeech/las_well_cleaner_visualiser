from wellclnpy.wellcleaner import wellCleaner
from pathlib import Path
import os


FLOC = str(Path(__file__).parent.parent) + "/tests/data"
os.chdir(FLOC)
LAS = "test.las"

def test_class():
    test_well = wellCleaner(LAS)
    assert test_well.NM == "test"
