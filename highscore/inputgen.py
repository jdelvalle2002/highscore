import random
a = open("random_input.txt", "w")
pos_lugares = ["a1","a2","a3","a4","a5","b1","b2","b3","b4","b5", 
"c1", "c2", "c3", "c4", "c5", "d1", "d2", "d3", "d4", "d5", "e1", "e2", "e3", "e4", "e5"]
new = random.sample(pos_lugares, 25)
for x in new:
    a.write(x)
    if x != new[-1]:
        a.write("\n")
a.close()    