#!/usr/bin/env python3
import struct, sys, pathlib, html

def u16(b,o): return struct.unpack_from('<H',b,o)[0]
def u32(b,o): return struct.unpack_from('<I',b,o)[0]
def i32(b,o): return struct.unpack_from('<i',b,o)[0]

def l8(b,o):
    x=b[o]; o+=1
    if x & 0x80:
        return ((x & 0x7f)<<8) | b[o], o+1
    return x,o

def l16(b,o):
    x=u16(b,o); o+=2
    if x & 0x8000:
        return ((x & 0x7fff)<<16) | u16(b,o), o+2
    return x,o

def parse_string_pool(b,off):
    typ,hs,size=u16(b,off),u16(b,off+2),u32(b,off+4)
    sc=u32(b,off+8); stc=u32(b,off+12); flags=u32(b,off+16); ss=u32(b,off+20)
    utf8=bool(flags & 0x100)
    offsets=[u32(b,off+hs+i*4) for i in range(sc)]
    base=off+ss
    out=[]
    for rel in offsets:
        p=base+rel
        try:
            if utf8:
                _,p=l8(b,p); bl,p=l8(b,p); raw=b[p:p+bl]; s=raw.decode('utf-8','replace')
            else:
                ln,p=l16(b,p); raw=b[p:p+ln*2]; s=raw.decode('utf-16le','replace')
        except Exception:
            s=''
        out.append(s)
    return out,size

def typed_value(strings,typ,data):
    if typ==0x00: return 'null'
    if typ==0x01: return f'@0x{data:08x}'
    if typ==0x02: return f'?0x{data:08x}'
    if typ==0x03: return strings[data] if data < len(strings) else f'<string#{data}>'
    if typ==0x04: return str(struct.unpack('<f',struct.pack('<I',data))[0])
    if typ==0x10: return str(struct.unpack('<i',struct.pack('<I',data))[0])
    if typ==0x11: return f'0x{data:x}'
    if typ==0x12: return 'true' if data else 'false'
    if typ in (0x1c,0x1d,0x1e,0x1f): return f'#{data:08x}'
    if typ in (0x05,0x06): return f'0x{data:08x}'
    return f'0x{data:08x}'

def qname(strings, ns_idx, name_idx, uri_to_prefix):
    name = strings[name_idx] if name_idx != 0xffffffff and name_idx < len(strings) else ''
    if ns_idx != 0xffffffff and ns_idx < len(strings):
        uri=strings[ns_idx]; p=uri_to_prefix.get(uri,'')
        if p: return f'{p}:{name}'
    return name

def dump(path):
    b=path.read_bytes()
    if len(b)<8 or u16(b,0)!=0x0003: raise ValueError('not Android binary XML')
    total=u32(b,4); off=u16(b,2)
    strings=[]; uri_to_prefix={}; pending_ns=[]; lines=[]; depth=0
    # XML starts with string pool
    while off < min(total,len(b)):
        typ=u16(b,off); hs=u16(b,off+2); size=u32(b,off+4)
        if size<=0: break
        if typ==0x0001:
            strings,_=parse_string_pool(b,off)
        elif typ==0x0100: # start namespace
            prefix_idx=u32(b,off+16); uri_idx=u32(b,off+20)
            prefix=strings[prefix_idx] if prefix_idx!=0xffffffff and prefix_idx<len(strings) else ''
            uri=strings[uri_idx] if uri_idx!=0xffffffff and uri_idx<len(strings) else ''
            uri_to_prefix[uri]=prefix
            pending_ns.append((prefix,uri))
        elif typ==0x0102: # start element
            ext=off+16
            ns_idx=u32(b,ext); name_idx=u32(b,ext+4)
            attr_start=u16(b,ext+8); attr_size=u16(b,ext+10); attr_count=u16(b,ext+12)
            tag=qname(strings,ns_idx,name_idx,uri_to_prefix)
            attrs=[]
            if pending_ns:
                for p,u in pending_ns:
                    attrs.append((f'xmlns:{p}' if p else 'xmlns',u))
                pending_ns.clear()
            abase=ext+attr_start
            for i in range(attr_count):
                a=abase+i*attr_size
                ans=u32(b,a); aname=u32(b,a+4); raw=u32(b,a+8)
                dtype=b[a+15]; data=u32(b,a+16)
                key=qname(strings,ans,aname,uri_to_prefix)
                if raw!=0xffffffff and raw < len(strings): val=strings[raw]
                else: val=typed_value(strings,dtype,data)
                attrs.append((key,val))
            ind='  '*depth
            if attrs:
                pieces=[f'{k}="{html.escape(v, quote=True)}"' for k,v in attrs]
                if len(' '.join(pieces))<100:
                    lines.append(ind+'<'+tag+' '+ ' '.join(pieces)+'>')
                else:
                    lines.append(ind+'<'+tag)
                    lines += [ind+'  '+p for p in pieces]
                    lines[-1] += '>'
            else:
                lines.append(ind+'<'+tag+'>')
            depth+=1
        elif typ==0x0103: # end element
            ext=off+16; ns_idx=u32(b,ext); name_idx=u32(b,ext+4); tag=qname(strings,ns_idx,name_idx,uri_to_prefix)
            depth=max(0,depth-1); lines.append('  '*depth+f'</{tag}>')
        elif typ==0x0104: # cdata
            data_idx=u32(b,off+16)
            if data_idx!=0xffffffff and data_idx<len(strings): lines.append('  '*depth+html.escape(strings[data_idx]))
        off += size
    return '<?xml version="1.0" encoding="utf-8"?>\n'+'\n'.join(lines)+'\n'

def main():
    src=pathlib.Path(sys.argv[1]); dst=pathlib.Path(sys.argv[2])
    try:
        txt=dump(src)
    except Exception as e:
        print(f'ERROR {src}: {e}',file=sys.stderr); sys.exit(2)
    dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(txt,encoding='utf-8')
if __name__=='__main__': main()
