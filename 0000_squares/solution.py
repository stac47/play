#!/usr/bin/env python3
import sys

n = int(input())

l = sorted([int(input()) for _ in range(n)])
print(l, file=sys.stderr, flush=True)
print(" ".join([str(i ** 2) for i in l]))
