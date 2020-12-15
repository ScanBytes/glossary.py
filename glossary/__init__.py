from pathlib import Path
import typing

import kaitaistruct
from fsutilz import MMap

from glossary.kaitai.glossary_index import GlossaryIndex

from .kaitai.glossary_index import GlossaryIndex


class Glossary:
	__slots__ = ("path", "indexDir", "iF", "gIF", "map", "index")

	DEFAULT_SUBDIR = ".glossary"
	DEFAULT_METAINDEX_FILE_NAME = "top_index.bin"
	DEFAULT_INDEX_FILE_NAME = "index.bin"

	def __init__(self, path: Path, indexDir: typing.Optional[Path] = None) -> None:
		self.path = path
		if indexDir is None:
			indexDir = path.parent / self.__class__.DEFAULT_SUBDIR
		self.indexDir = indexDir
		self.iF = None
		self.gIF = None
		self.map = None
		self.index = None

	def __exit__(self, *args, **kwargs) -> None:
		self.index = None
		if self.iF is not None:
			self.iF.__exit__(*args, **kwargs)
			self.iF = None

		if self.gIF is not None:
			self.gIF.__exit__(*args, **kwargs)
			self.gIF = None

		if self.map is not None:
			self.map.__exit__(*args, **kwargs)
			self.map = None

	def parseMetaIndex(self) -> None:
		globalIdxFile = self.indexDir / self.__class__.DEFAULT_METAINDEX_FILE_NAME
		self.gIF = MMap(globalIdxFile).__enter__()
		self.index = GlossaryIndex(kaitaistruct.KaitaiStream(self.iF), kaitaistruct.KaitaiStream(self.gIF))
		self.gIF.__exit__(None, None, None)
		self.gIF = None

	def __enter__(self) -> "Glossary":
		idxFile = self.indexDir / self.__class__.DEFAULT_INDEX_FILE_NAME
		self.iF = MMap(idxFile).__enter__()
		self.parseMetaIndex()
		self.map = MMap(self.path).__enter__()
		return self

	def getLine(self, rec_descriptor: GlossaryIndex.RecordDescriptor) -> bytes:
		line = self.map[rec_descriptor.record.offset :]
		l = line.find(b"\n")
		if l >= 0:
			line = line[:l]
		return line

	def __iter__(self) -> typing.Iterator[bytes]:
		for rec in self.index.records:
			yield self.getLine(rec)
