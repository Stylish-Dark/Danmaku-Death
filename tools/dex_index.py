#!/usr/bin/env python3
import struct, sys, pathlib, csv


def u32(b,o): return struct.unpack_from('<I',b,o)[0]
def u16(b,o): return struct.unpack_from('<H',b,o)[0]
def uleb(b,o):
    v=0; s=0
    while True:
        x=b[o]; o+=1
        v |= (x & 0x7f) << s
        if x < 0x80: return v,o
        s += 7

def read_mutf8(b,o):
    _,o=uleb(b,o)
    end=b.find(b'\x00',o)
    raw=b[o:end]
    return raw.decode('utf-8','replace')

def parse(path):
    b=path.read_bytes()
    if not b.startswith(b'dex\n'): raise ValueError('not dex')
    string_ids_size=u32(b,0x38); string_ids_off=u32(b,0x3c)
    type_ids_size=u32(b,0x40); type_ids_off=u32(b,0x44)
    proto_ids_size=u32(b,0x48); proto_ids_off=u32(b,0x4c)
    field_ids_size=u32(b,0x50); field_ids_off=u32(b,0x54)
    method_ids_size=u32(b,0x58); method_ids_off=u32(b,0x5c)
    class_defs_size=u32(b,0x60); class_defs_off=u32(b,0x64)
    strings=[]
    for i in range(string_ids_size):
        off=u32(b,string_ids_off+i*4); strings.append(read_mutf8(b,off))
    types=[strings[u32(b,type_ids_off+i*4)] for i in range(type_ids_size)]
    protos=[]
    for i in range(proto_ids_size):
        o=proto_ids_off+i*12
        shorty_idx=u32(b,o); ret_idx=u32(b,o+4); params_off=u32(b,o+8)
        params=[]
        if params_off:
            n=u32(b,params_off)
            for j in range(n): params.append(types[u16(b,params_off+4+j*2)])
        protos.append((strings[shorty_idx],types[ret_idx],params))
    methods=[]
    for i in range(method_ids_size):
        o=method_ids_off+i*8
        cls_idx=u16(b,o); proto_idx=u16(b,o+2); name_idx=u32(b,o+4)
        shorty,ret,params=protos[proto_idx]
        methods.append((types[cls_idx],strings[name_idx],ret,params))
    classes=[]
    for i in range(class_defs_size):
        o=class_defs_off+i*32
        cls_idx=u32(b,o); access=u32(b,o+4); super_idx=u32(b,o+8); interfaces_off=u32(b,o+12); source_idx=u32(b,o+16)
        cls=types[cls_idx]; sup=types[super_idx] if super_idx != 0xffffffff else ''
        src=strings[source_idx] if source_idx != 0xffffffff else ''
        classes.append((cls,sup,src,access))
    return strings, types, methods, classes

def main():
    p=pathlib.Path(sys.argv[1]); out=pathlib.Path(sys.argv[2]); out.mkdir(parents=True,exist_ok=True)
    strings,types,methods,classes=parse(p)
    (out/'strings.txt').write_text('\n'.join(f'{i:05d}\t{s}' for i,s in enumerate(strings)),encoding='utf-8')
    (out/'classes.tsv').write_text('class\tsuper\tsource\taccess_flags\n' + '\n'.join(f'{c}\t{s}\t{src}\t0x{a:x}' for c,s,src,a in classes),encoding='utf-8')
    with (out/'methods.tsv').open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f,delimiter='\t'); w.writerow(['class','method','return','params'])
        for c,n,r,ps in methods: w.writerow([c,n,r,','.join(ps)])
    pkg=[c for c,_,_,_ in classes if 'jakiganicsystems/danmakudeath' in c]
    (out/'game_classes.txt').write_text('\n'.join(pkg),encoding='utf-8')
    print(f'{p.name}: {len(strings)} strings, {len(classes)} classes, {len(methods)} methods; game classes={len(pkg)}')
if __name__=='__main__': main()
