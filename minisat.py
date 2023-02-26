import os

# ユニット（計27)
UNITS = []
for i in range(9):
    UNITS.append([9*i+j for j in range(9)]) # 行
    # UNITS[0] = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    UNITS.append([i+9*j for j in range(9)]) # 列
for i in [0,3,6,27,30,33,54,57,60]:
    UNITS.append([i+j for j in [0,1,2,9,10,11,18,19,20]]) # 四角

# 命題変数 (729=81*9個)
def varOf(i,m):
    """セルiに数mが入るかを格納する命題変数番号(1,2,...)を返す"""
    return i*9+m+1
def invVar(n):
    return ((n-1)//9, (n-1)%9)

conditionText = []

# 各セル
for i in range(81):
    # どれか一つの値が入っているべき
    conditionText.append([varOf(i,m) for m in range(9)])
    # 任意の二つの数m,nに対して同時にフラグが立たない
    # ¬(var(i,m)⋀var(i,n)) 変形して ¬var(i,m)⋁¬var(i,n)
    for m in range(9):
        for n in range(m+1,9):
            conditionText.append([-varOf(i,m), -varOf(i,n)])

# 各ユニット
for u in UNITS:
    for m in range(9):
        # 数mがユニットに含まれているべき
        conditionText.append([varOf(i,m) for i in u])
        # 任意の二つのマスi,jが同じ値をもたない すなわち
        # ¬(var(m,i)⋀var(m,j)) 変形して ¬var(m,i)⋁¬var(m,j)
        for i in range(9):
            for j in (range(i+1,9)):
                conditionText.append([-varOf(i,m), -varOf(j,m)])

# 初期盤面
# initialBoard = '85...24..72......9..4.........1.7..23.5...9...4...........8..7..17..........36.4.'
# initialBoard = '.4.5...21...1.....82..3..6.2..4.58...1....2.359............2385..3...91.....8....'
initialBoard = input()
for i, m in enumerate(initialBoard):
    if m not in "123456789":
        continue
    conditionText.append([varOf(i, int(m)-1)]) # -1 to 0-indexed

# inputにかきこみ
with open("input.txt", "w", encoding="utf8") as ofh:
    ofh.write("p cnf {} {}\n".format(729, len(conditionText)))
    for ct in conditionText:
        ofh.write(" ".join([str(c) for c in ct] + ["0"]))
        ofh.write("\n")

os.system("/usr/bin/minisat input.txt output.txt")

# outputから答えを入手
with open("output.txt") as ifh:
    if ifh.readline() != "SAT\n":
        raise Exception("ouch")
    ans = ifh.readline()
    # ans = -1 -2 3 -4 -5 -6 -7 -8 -9 -10 -11 ......
    data = [0]*81
    for x in ans.split(" ")[:-1]: # 最後の1つは区切り文字
        n = int(x)
        if n < 0:
            continue
        i, m = invVar(n)
        data[i] = m+1

# ANS="859612437723854169164379528986147352375268914241593786432981675617425893598736241"
# if "".join(map(str, data)) == ANS:
#     print("seems good.")
#     print("".join(map(str, data)))

# 答えの表示
[print("".join(map(str, data))[i*9:(i*9)+9]) for i in range(9)]