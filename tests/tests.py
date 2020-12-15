#!/usr/bin/env python3
import csv
import sys
import unittest
from pathlib import Path

thisDir = Path(__file__).parent

sys.path.insert(0, str(thisDir.parent))

from collections import OrderedDict

dict = OrderedDict

from glossary import Glossary


class Tests(unittest.TestCase):
	def testReading(self):
		with Glossary(thisDir / "MOCK_DATA.csv") as p:
			for line in p:
				iD = tuple(csv.reader([line.decode("utf-8")]))[0]


if __name__ == "__main__":
	unittest.main()
