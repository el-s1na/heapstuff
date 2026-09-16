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















io.interactive()
