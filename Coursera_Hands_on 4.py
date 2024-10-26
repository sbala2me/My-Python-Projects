import time
start_time = time.time()

#Outer Loop
for i in range(100):
    #inner loop
    for j in range(100):
        print(0, end = "")
    print()

print(round(time.time() - start_time, 2))

