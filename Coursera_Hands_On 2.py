http_status = 200

if http_status == 200 or http_status == 201:
  print("Correct")
elif http_status == 400:
  print("Bad Request")
elif http_status == 404:
  print("Not Found")
elif http_status == 500 or http_status == 501:
  print("Server Error")
else:
  print("Unknown Yagu Bagu Babu Error")

match http_status:
  case 200 | 201:
    print("Match Correct")
  case 400:
    print("Match Bad Request")
  case 404:
    print("Match Not Found")
  case 500 | 501:
    print("Match Server Error")
  case _:
    print("Match Unknown Yagu Bagu Babu Error")


