#define _GNU_SOURCE
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MAXNUM 100
char num[0x8];

unsigned long read_num() {
  puts(">>");
  read(STDIN_FILENO, num, 0x4);
  return atoll(num);
}

char *chunk_pointer[MAXNUM];
int chunk_size[MAXNUM];

void allocate_chunk() {
  puts("index:");
  unsigned long index = read_num();
  puts("size:");
  unsigned long size = read_num();
  void *allocated_pointer = malloc(size);
  chunk_pointer[index] = allocated_pointer;
  chunk_size[index] = size;
  puts("malloc done");
}

void calloc_chunk() {
  puts("index:");
  unsigned long index = read_num();
  puts("size:");
  unsigned long size = read_num();
  void *allocated_pointer = calloc(0x1, size);
  chunk_pointer[index] = allocated_pointer;
  chunk_size[index] = size;
  puts("calloc done");
}

void free_chunk() {
  puts("index:");
  unsigned long index = read_num();
  if (!chunk_pointer[index]) {
    puts("there is no such chunk");
    return;
  }
  free(chunk_pointer[index]);
  puts("free done");
}

void edit_chunk() {
  puts("index");
  unsigned long index = read_num();
  read(STDIN_FILENO, chunk_pointer[index], chunk_size[index]);
  puts("edit done");
}

void view_chunk() {
  puts("index");
  unsigned long index = read_num();
  write(STDOUT_FILENO, chunk_pointer[index], chunk_size[index]);
  puts("view done");
}

void menu() {
  puts("1.malloc");
  puts("2.calloc");
  puts("3.free");
  puts("4.edit");
  puts("5.view");
}

int main() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
  while (true) {
    menu();
    unsigned long index = read_num();
    if (index == 0x1)
      allocate_chunk();
    if (index == 0x2)
      calloc_chunk();
    if (index == 0x3)
      free_chunk();
    if (index == 0x4)
      edit_chunk();
    if (index == 0x5)
      view_chunk();
  }
}
