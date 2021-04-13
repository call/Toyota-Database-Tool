import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams.update({'font.size': 6})


with open("C:/Users/schro/Downloads/CS3435/Project v2/Analysis_Output") as f:
    lines = f.read().splitlines()


g = []

def graph(input):
    x = {}
    for f in input:
        x[f[1] + str(f[3])] = float(f[2].replace("'",""))


    data = {input[0][0]: x}
    df = pd.DataFrame(data)
    df.plot(kind='bar')
    g.append(plt)


formatted_lines = []
current_make = "'4Runner'"


for l in lines:
    a = l.replace("[","").replace("]","").replace("\"","").split(", ")
    formatted_lines.append(a)
    if a[0] != current_make:
        print(a[0])
        current_make = a[0]
        graph(formatted_lines)
        formatted_lines = []

# print(*formatted_lines, sep="\n")
plt.show(g)