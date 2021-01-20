import pandas as pd

csv1 = pd.read_csv("status_1.csv")

print(csv1)
val_list = csv1.values.tolist()
# yes_count = val_list.count('Yes')
yes_count = 0
# yes_count = 5
for x in range(len(val_list)):
    if val_list[x][1]=='Yes':
        yes_count+=1
        print(yes_count)
print(yes_count)
print(val_list[0][1])
print(type(val_list))
