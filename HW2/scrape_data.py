a = [1,2,3]
b = [4,5,6]
[print((x,y)) for (x,y) in zip(a,b) if x != 1]

def month_avg(df):
    print("\nExercise 6:")
    if (len(df['date']) != len(df['cost'])):
        print("Incorrect Comparison")
    for k in range(1,2):
        df["monthy"] = [print(y) for (x,y) in zip(df['date'], df['cost']) if x != 0 and x.month == k]
        print(df["monthy"])
    print(df["monthy"].mean())