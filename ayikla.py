read = open("eng.txt").readlines()

k = ""
write = open("yeni.txt",mode="r+")


for i in read:
    i = i.strip("\n")
    i = i.split("\t")
    k = i[0] + "\t" + i[1] + "\n"
    write.write(k)

