# import sys,string,os,linecache
import os
import time

def getMinusAndStr(n):
    return str(-n)        








n = int(input("nを入力してください: "))
if n < 4:
    print("4以上の整数にしてください")
    exit()


conditionlist = []
#行にかならず一つクイーンあり
for i in range(0,n):
    conditionlist.append([i*n+m+1 for m in range(n)])

# 同じ行に二つない
for m in range(0,n):
    for i in range(0,n):
        for j in range(i+1,n):
            conditionlist.append([-(i+m*n+1), -(j+m*n+1)])

# 同じ列に二つない
for m in range(0,n):
    for i in range(0,n):
        for j in range(i+1,n):
            conditionlist.append([-(i*n+m+1), -(j*n+m+1)])

# 北西->南東、上三角+対角線
for m in range(0,n-1):
    for i in range(m,n-1):
        for j in range(1,n-i):
            conditionlist.append([-(i+m*n+1), -(i+m*n+1+j*(n+1))])

# 北西->南東、下三角
for m in range(0,n-1):
    for i in range(0,m):
        for j in range(1,n-m):
            conditionlist.append([-(i+m*n+1), -(i+m*n+1+j*(n+1))])

# 北東->南西、上三角+対角線
for m in range(0,n):
    for i in range(0,n-m):
        for j in range(1,i+1):
            conditionlist.append([-(i+n*m+1), -(i+n*m+1+j*(n-1))])

# 北東->南西、下三角
for m in range(0,n):
    for i in range(n-m,n):
        for j in range(1,n-m):
            conditionlist.append([-(i+n*m+1), -(i+n*m+1+j*(n-1))])


# write input text
with open("input.txt", "w", encoding="utf8") as inputfile:
    inputfile.write("p cnf {} {}\n".format(n*n, len(conditionlist)))
    for ct in conditionlist:
        inputfile.write(" ".join([str(c) for c in ct] + ["0"]))
        inputfile.write("\n")

# # write ans header
# with open("ans.txt", "w", encoding="utf8") as ansfile:
#     ansfile.write(str(n)+"queen\n\n")

# write ans header
with open("time.txt", "w", encoding="utf8") as timefile:
    timefile.write(str(n)+"queen\n\n")

# with open("ans.txt", "w", encoding="utf8") as ansfile:
#     ansfile.write(str(n)+"queen\n\n")

count = 0

time_start = time.time()

while True:
    os.system("/usr/bin/minisat input.txt output.txt")   
    # UNSAT かどうか判断して終了->nqueen
    # ans.txtに出力しないようにして
    # 解を吐き出す速度を知りたいから、1000この生成速度、ans.txt
    # 1000こごとの時刻を調べる
    ansDisplay = [0]*n*n
    ansIndex = []

    # get output from output.txt
    with open("output.txt") as outputfile:
        if outputfile.readline() == "UNSAT\n":
            time_finish = time.time()
            break
        ans = outputfile.readline()
        # ans = -1 -2 3 -4 -5 -6 -7 -8 -9 -10 -11 ......
        for i,x in enumerate(ans.split(" ")[:-1]): # 最後の1つは区切り文字
            x_int = int(x)
            if x_int < 0:
                continue
            ansDisplay[i] = 1
            ansIndex.append(i+1) 
    count += 1

    if(count % 1000 == 0):
        time_current = time.time()
        # write time
        with open("time.txt", "a", encoding="utf8") as timefile:
            timefile.write("time at " + str(count) + ": " + str(time_current - time_start) + "\n\n")        
    # print(ans)
    print(ansIndex)

    # write(append) answer to ans.txt
    # with open("ans.txt", "a", encoding="utf8") as ansfile:
    #     for i in range(len(ansDisplay)):
    #         ansfile.write(str(ansDisplay[i]))
    #         if(i % n) == n-1:
    #             ansfile.write("\n")
    #     ansfile.write("\n\n")

    # write(append) answer condition to input.txt
    with open("input.txt", "a", encoding="utf8") as inputfile:
        inputfile.write(" ".join([(" ".join(map(getMinusAndStr, ansIndex)))] + ["0"]))
        inputfile.write("\n")

print(count)
print(time_finish - time_start)
# write time_process
with open("time.txt", "a", encoding="utf8") as timefile:
    timefile.write("process time: " + str(time_finish - time_start) + "\n\n")
    timefile.write("the number of solution: " + str(count) + "\n\n")
