#!/usr/bin/env python

p1 = -0.57812754047966752
p2 = 0.45325732769386157
steps = 8

p = p1
for i in range(steps):
   p = ((steps - i)*p1 + i*p2) / steps
   print p
