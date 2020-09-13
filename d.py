d = {3:[5,5],4:[0,55],1:[2,15]}
for w in sorted(d, key=d.get):
    print(w, d[w])
