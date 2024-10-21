bill_total_str = input()
bill_total= int(bill_total_str)

discount1 = 14
discount2 = 28
if bill_total > 100 and bill_total <200:
  print("Bill Is Expensive Save Money!")
  bill_total = bill_total - discount1
elif bill_total > 200:
  print("Bill Is Greater Than 200")
  bill_total = bill_total - discount2
else:
  print("Bill Is Still Expensive Save More Money!")
x =input()

print("Total Bill:" + str(bill_total))
