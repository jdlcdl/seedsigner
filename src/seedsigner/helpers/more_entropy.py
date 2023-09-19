"""
reversible operations on bip-39 entropy bytes before finalizing a seed
"""

def xor_bytes(a, b):
    assert type(a) == type(b) == bytes and len(a) == len(b)
    return bytes(i^j for i,j in zip(a,b))

def inv_bits(b):
    assert type(b) == bytes
    return xor_bytes(b'\xff'*len(b), b)

def rev_bits(b):
    assert type(b) == bytes
    binstr = '{:0{width}b}'.format(int.from_bytes(b, 'big'), width=len(b)*8)
    return int(binstr[::-1], 2).to_bytes(len(b), 'big')

def rev_nibbles(b):
    assert type(b) == bytes
    return bytes.fromhex(''.join(reversed([x for x in b.hex()])))

def rev_bytes(b):
    assert type(b) == bytes
    return b[::-1]
