"""Read Addressables 2.9.1 binary catalog by its published serialization layout.

Offsets come from the Header -> KeyData -> ResourceLocation -> typed extra data,
never from byte searches or remembered offsets.
"""
import struct

class Catalog:
    def __init__(self, data):
        self.data = data
        magic, version = self.values(0, 2)
        if magic != 0x0DE38942 or version != 2:
            raise ValueError(f'Unsupported catalog {magic:x}, version {version}')

    def values(self, offset, count=1):
        if offset < 0 or offset + count*4 > len(self.data): raise ValueError('Out of bounds')
        return struct.unpack_from('<'+'I'*count, self.data, offset)

    def array(self, offset, width=1):
        if offset == 0xFFFFFFFF: return []
        size, = self.values(offset-4)
        if size % (width*4): raise ValueError('Invalid array size')
        return [self.values(i,width) for i in range(offset,offset+size,width*4)]

    def string(self, offset, sep):
        if offset == 0xFFFFFFFF: return None
        if offset & 0x40000000:
            parts=[]; seen=set()
            while offset != 0xFFFFFFFF:
                pos=offset & 0x3FFFFFFF
                if pos in seen: raise ValueError('String cycle')
                seen.add(pos)
                string_id, offset=self.values(pos,2)
                parts.append(self.string(string_id,''))
            return sep.join(reversed(parts))
        pos=offset & 0x3FFFFFFF
        length,=self.values(pos-4)
        return self.data[pos:pos+length].decode('utf-16-le' if offset & 0x80000000 else 'ascii')

    def bundles(self):
        keys,=self.values(8)
        locations={loc for _,arr in self.array(keys,2) for (loc,) in self.array(arr)}
        result=[]
        for loc in sorted(locations):
            primary,internal,provider,deps,dep_hash,extra,type_id=self.values(loc,7)
            provider_name=self.string(provider,'.')
            if not provider_name.endswith('AssetBundleProvider'): continue
            _,sd=self.values(extra,2)
            hash_id,name_id,crc,size,common=self.values(sd,5)
            result.append(dict(location=loc,internal_id=self.string(internal,'/'),
                               bundle_name=self.string(name_id,'_'), crc=crc,size=size,
                               crc_offset=sd+8,size_offset=sd+12,hash_offset=hash_id))
        return result


