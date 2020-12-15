# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class GlossaryIndex(KaitaiStruct):
    """'glossary' is a tool written in Rust to index flat files delimited by line breaks.
    In fact the index can be used for any binary files.
    
    .. seealso::
       Source - https://github.com/waltonseymour/glossary/blob/7cfc390d20afd7373749aa94e0b4ce0f30709f97/src/write.rs
    """
    def __init__(self, index_io, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self.index_io = index_io
        self._read()

    def _read(self):
        self.records = []
        i = 0
        while not self._io.is_eof():
            self.records.append(GlossaryIndex.RecordDescriptor(self._io, self, self._root))
            i += 1


    class RecordDescriptor(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.size = self._io.read_u8le()
            self.offset = self._io.read_u8le()

        class Record(KaitaiStruct):
            def __init__(self, size, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self.size = size
                self._read()

            def _read(self):
                self.key = self._io.read_bytes(self.size)
                self.offset = self._io.read_u8le()


        @property
        def record(self):
            if hasattr(self, '_m_record'):
                return self._m_record if hasattr(self, '_m_record') else None

            io = self._root.index_io
            _pos = io.pos()
            io.seek(self.offset)
            self._m_record = GlossaryIndex.RecordDescriptor.Record(self.size, io, self, self._root)
            io.seek(_pos)
            return self._m_record if hasattr(self, '_m_record') else None



