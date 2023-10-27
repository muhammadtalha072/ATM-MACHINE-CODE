import os
# Take a tuple of available denominations of bills
bills = (100, 50, 20, 10, 5, 1)

# Define a dictionary of available denominations and their respective quantities
quantities = {100: 10, 50: 10, 20: 10, 10: 10, 5: 10, 1: 10}

# A list of the user's available account balances
balances = [1000, 500]

# Define a set of allowed transaction types
transactions = {"withdraw", "deposit", "transfer"}
correct_pin = "1234"
pin = None
def process_transaction(transaction_type, amount, from_account=None, to_account=None):
  if from_account is None:
      from_account = 0
  if to_account is None:
      to_account = 1
      
  pin = input("Enter your pin number: ")
  
  # Check if the pin number is correct
  if pin != correct_pin:
    print("Incorrect pin number")
    return "Try again"
  if transaction_type not in transactions:
    return "Invalid transaction type"
  if transaction_type == "withdraw":
    if amount > balances[from_account]:
      return "Insufficient balance"
    balances[from_account] -= amount
    try:
      
      with open("transactions.txt", "a") as f:
        f.write("Transaction type: Withdraw\n")
        f.write(f"From account: {from_account}\n")
        f.write(f"Amount: {amount}\n")
        f.write(f"Amount remaining: {balances[from_account]}\n")
      print(f"Withdrawal amount: {amount}")
      print(f"Remaining balance: {balances[from_account]}")

    except IOError:
      print("Error opening transactions.txt for writing")
      raise
      
    withdraw_bills = {}
    for bill in bills:
      if bill <= amount:
        withdraw_bills[bill] = amount // bill
        amount = amount % bill
    for bill, quantity in withdraw_bills.items():
      if quantities[bill] < quantity:
        return "Insufficient quantities of bills"
    for bill, quantity in withdraw_bills.items():
      quantities[bill] -= quantity
    # Write to the transactions file
    try:
      
      with open("transactions.txt", "a") as f:
      
        f.write("Denominations: \n")
        for bill, quantity in withdraw_bills.items():
          f.write(f"{bill}: {quantity}\n")
        f.write("\n")
     
    except IOError:
      print("Error opening transactions.txt for writing")
      raise
    except FileNotFoundError:
      print("Error: transactions.txt file not found")
      raise
    except PermissionError:
      print("Error: insufficient permissions to access transactions.txt")
      raise


    
  elif transaction_type == "deposit":
    balances[to_account] += amount
    try:
      with open("transactions.txt", "a") as f:
        f.write("Transaction type: Deposit\n")

        f.write(f"To account: {to_account}\n")

        f.write(f"Amount: {amount}\n")
        f.write(f"New balance: {balances[to_account]}\n")
      print(f"Deposited amount: {amount}")
    except IOError:
      print("Error opening transactions.txt for writing")
    

    # Calculate the number of each note in the deposit
    deposit_bills = {}
    for bill in bills:
      if bill <= amount:
        deposit_bills[bill] = amount // bill
        amount = amount % bill
    for bill, quantity in deposit_bills.items():
      quantities[bill] += quantity
    try:
      with open("transactions.txt", "a") as f:
        f.write("Denominations: \n")
        for bill, quantity in deposit_bills.items():
            f.write(f"{bill}: {quantity}\n")
        f.write("\n")
      print(f"New balance: {balances[to_account]}")
    except IOError:
      print("Error opening transactions.txt for writing")
      raise
    except FileNotFoundError:
      print("Error: transactions.txt file not found")
      raise
    except PermissionError:
      print("Error: insufficient permissions to access transactions.txt")
      raise
  elif transaction_type == "transfer":
    if amount > balances[from_account]:
      return "Insufficient balance"
  # Transfer the amount from the specified account to the other account
    balances[from_account] -= amount
    balances[to_account] += amount
  # Write to the transactions file
    with open("transactions.txt", "a") as f:
        f.write("Transaction type: Transfer\n")
        f.write(f"Amount: {amount}\n")
        f.write(f"From account: {from_account}\n")
        f.write(f"To account: {to_account}\n")
        f.write(f"Remaining balance in source account: {balances[from_account]}\n")
        f.write(f"Remaining balance in destination account: {balances[to_account]}\n")
        f.write("\n")
        
    print("Success")
    print(f"Remaining balance in source account: {balances[from_account]}")
    print(f"Balance in destination account: {balances[to_account]}")

  
  return "Transaction processed successfully"
def read_file():
  with open("transactions.txt","r") as a:
    return a.read()

def print_balances():
  print("Your available account balances are:")
  for i, balance in enumerate(balances):
    print(f"Account {i}: {balance}")


def get_input(prompt):
  return input(prompt).strip()
def menu():
  print("Welcome to the ATM")
  print_balances() 

  while True:
    print("Please select an option:")
    print("1. Withdraw")
    print("2. Deposit")
    print("3. Transfer")
    print("4. Exit")
    selection = get_input("Enter your selection: ")
    if selection == "1":
      while True:
        try:
          account = int(input("Enter the account number: "))
          break
        except ValueError:
          print("Invalid input. Please enter a number.")
      if account not in [0, 1]:
        print("Invalid account number")
        continue
      
      while True:
        try:
          amount = int(input("Enter the amount in numbers to withdraw: "))
          break
        except ValueError:
          print("Invalid input. Please enter a number.")


      result = process_transaction("withdraw",amount, from_account=account)
      print(result)
    elif selection == "2":
      while True:
        try:
          account = int(input("Enter the account number: "))
          break
        except ValueError:
          print("Invalid input. Please enter a number.")
      if account not in [0, 1]:
        print("Invalid account number")
        continue
      while True:
        try:
          amount = int(input("Enter the amount in numbers to deposit: "))
          break
        except ValueError:
          print("Invalid input. Please enter a number.")
      result = process_transaction("deposit", amount, to_account=account)
      print(result)
    elif selection == "3":
      while True:

        try:
          from_account = int(get_input("Enter the account number to transfer from: "))
          break
        except ValueError:
          print("Invalid input. Please enter a number.")
      if from_account not in [0, 1]:
        print("Invalid account number")
        continue
      while True:
        try:
          to_account = int(get_input("Enter the account number to transfer to: "))
          break
        except ValueError:
          print("Invalid input. Please enter a number.")
      if to_account not in [0, 1]:
        print("Invalid account number")
        continue
      while True:
        try:
          amount = int(input("Enter the amount in numbers to withdraw: "))
          break
        except ValueError:
          print("Invalid input. Please enter a number.")
      result = process_transaction("transfer", amount, from_account=from_account, to_account=to_account)
      print(result)
    elif selection == "4":
      break
    else:
      print("Invalid selection")

  while True:
    
    print("If you want to read the transaction data file,Please select one of the options: ")
    print("1.yes")
    print("2.no")
    answer  = int(get_input("Enter your selection: "))
    try:
      if answer == 1:
        receipt = read_file()
        print(receipt)
        os.remove("transactions.txt")
      else:
        print("have a nice day:)")
        
    except Exception as e:
      print("Error:", e)
    else:
      break
    
    
      





# Call the menu function to start the program
menu()
print_balances() 
