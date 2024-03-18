#Nama : Muhammad Arifin Dava 
#NIM  : 2309116059

import math
from prettytable import PrettyTable
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

class Node:
   def __init__(self, customer_name, order, next=None):
      self.customer_name = customer_name
      self.order = order
      self.next = next

class CoffeeShop:
   def __init__(self):
      self.coffee = ["Espresso", "Latte", "Cappuccino", "Mocha", "Macchiato"]
      self.price = [15000, 17000, 16000, 26500, 25500]
      self.stock = [150, 120, 100, 320, 80]
      self.users = {}
      self.head = None
      self.total_income = 0

   def add_new_coffee(self, coffee_name, price, stock, location):
      try:
         if location == 'beginning':
               self.coffee.insert(0, coffee_name)
               self.price.insert(0, price)
               self.stock.insert(0, stock)
         elif location == 'end':
               self.coffee.append(coffee_name)
               self.price.append(price)
               self.stock.append(stock)
         elif location == 'middle':
               middle_index = len(self.coffee) // 2
               self.coffee.insert(middle_index, coffee_name)
               self.price.insert(middle_index, price)
               self.stock.insert(middle_index, stock)
         else:
               raise ValueError("Invalid location. Coffee not added.")
      except ValueError as e:
         print(Fore.RED + str(e))

   def del_coffee(self, location=None):
      try:
         if location not in ['beginning', 'middle', 'end']:
               raise ValueError("Invalid location. Please choose 'beginning', 'middle', or 'end'.")

         if location == 'beginning':
               if self.coffee:
                  deleted_coffee = self.coffee.pop(0)
                  self.price.pop(0)
                  self.stock.pop(0)
                  print(Fore.GREEN + f"Coffee '{deleted_coffee}' deleted successfully from the beginning.")
               else:
                  print(Fore.YELLOW + "No coffee found to delete.")
         elif location == 'end':
               if self.coffee:
                  deleted_coffee = self.coffee.pop()
                  self.price.pop()
                  self.stock.pop()
                  print(Fore.GREEN + f"Coffee '{deleted_coffee}' deleted successfully from the end.")
               else:
                  print(Fore.YELLOW + "No coffee found to delete.")
         elif location == 'middle':
               if not self.coffee:
                  print(Fore.YELLOW + "No coffee found to delete.")
                  return

               if len(self.coffee) == 1:
                  print(Fore.YELLOW + "There is only one coffee available. You cannot delete it from the middle.")
                  return

               coffee_to_delete = input("Enter the coffee name to delete: ")
               if coffee_to_delete in self.coffee:
                  index = self.coffee.index(coffee_to_delete)
                  if index == 0 or index == len(self.coffee) - 1:
                     print(Fore.RED + f"The coffee '{coffee_to_delete}' cannot be deleted from the middle.")
                  else:
                     self.coffee.pop(index)
                     self.price.pop(index)
                     self.stock.pop(index)
                     print(Fore.GREEN + f"Coffee '{coffee_to_delete}' deleted successfully.")
               else:
                  print(Fore.RED + f"Coffee '{coffee_to_delete}' not found.")
      except ValueError as e:
         print(Fore.RED + str(e))

   def display_menu_and_stock(self):
      try:
         table = PrettyTable(["Menu", "Price", "Stock"])
         for coffee, price, stock in zip(self.coffee, self.price, self.stock):
               table.add_row([coffee, price, stock])
         print(Fore.CYAN + "Coffee Shop Menu and Stock")
         print(table)
      except Exception as e:
         print(Fore.RED + str(e))

   def update_menu_and_stock(self):
      try:
         self.display_menu_and_stock()
         item = input("Enter the item to update: ")
         if item in self.coffee:
               index = self.coffee.index(item)
               price = int(input("Enter the new price: "))
               quantity = int(input("Enter the new stock quantity: "))
               self.price[index] = price
               self.stock[index] = quantity
               print(Fore.GREEN + f"Menu item '{item}' updated successfully.")
         else:
               raise ValueError(f"Menu item '{item}' not found.")
      except ValueError as e:
         print(Fore.RED + str(e))

   def place_order(self, customer_name, coffee_name, quantity):
      try:
         if coffee_name in self.coffee:
               index = self.coffee.index(coffee_name)
               if self.stock[index] >= quantity:
                  total_bill = self.price[index] * quantity
                  self.stock[index] -= quantity
                  if not self.head:
                     self.head = Node(customer_name, {coffee_name: quantity})
                  else:
                     current = self.head
                     while current.next:
                           current = current.next
                     current.next = Node(customer_name, {coffee_name: quantity})
                  print(Fore.GREEN + f"Order placed successfully. Total Bill: Rp. {total_bill:.2f}")
                  self.total_income += total_bill
               else:
                  print(Fore.RED + "Insufficient stock.")
         else:
               raise ValueError("Invalid coffee selection.")
      except ValueError as e:
         print(Fore.RED + str(e))

   def register_user(self, username, password):
      try:
         if username not in self.users:
               self.users[username] = {"password": password, "role": "customer", "balance": 0}
               print(Fore.GREEN + "Registration successful.")
         else:
               raise ValueError("Username already exists. Please choose another username.")
      except ValueError as e:
         print(Fore.RED + str(e))

   def login(self, username, password):
      try:
         if username in self.users and self.users[username]["password"] == password:
               return True
         else:
               raise ValueError("Invalid username or password. Please try again.")
      except ValueError as e:
         print(Fore.RED + str(e))
         return False

   def save_invoice_to_txt(self, customer_name, customer_order, total_bill):
      try:
         with open(f'{customer_name}_invoice.txt', 'w') as invoice_file:
               invoice_file.write("CoffeeShop Invoice\n")
               invoice_file.write(f"Customer Name: {customer_name}\n")
               for coffee, quantity in customer_order.items():
                  invoice_file.write(f"{coffee}: {quantity}\n")
               invoice_file.write(f"Total Bill: Rp. {total_bill:.2f}\n")
      except Exception as e:
         print(Fore.RED + str(e))

   def generate_invoice(self, customer_name, customer_order, total_bill):
      try:
         invoice = PrettyTable()
         invoice.field_names = ["CoffeeShop", "Invoice"]
         invoice.add_row(["Customer Name:", customer_name])
         invoice.add_row(["Transaction Time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
         for coffee, quantity in customer_order.items():
               invoice.add_row([coffee, f"{quantity}"])
         invoice.add_row(["Total Bill:", f"Rp. {total_bill:.2f}"])
         print(invoice)
         self.save_invoice_to_txt(customer_name, customer_order, total_bill)
      except Exception as e:
         print(Fore.RED + str(e))

   def register(self):
      try:
         print(Fore.BLUE + "Welcome To Coffee Shop \nPlease Register First❤️")
         username = input("Enter your username: ")
         password = input("Enter your password: ")
         self.register_user(username, password)
      except ValueError as e:
         print(Fore.RED + str(e))

   def login_screen(self):
      try:
         while True:
               print(Fore.BLUE + "Login Your Account✌️")
               username = input("Enter your username: ")
               password = input("Enter your password: ")
               if self.login(username, password):
                  print(Fore.GREEN + f"Welcome, {username}!")
                  break
      except ValueError as e:
         print(Fore.RED + str(e))

   def display_main_menu(self):
      try:
         main_menu = PrettyTable()
         main_menu.field_names = [Fore.YELLOW + "Features", Fore.YELLOW + "CoffeeShop Hanei" + Fore.CYAN]
         main_menu.add_row([Fore.CYAN + "1",  "Display Menu"])
         main_menu.add_row([Fore.CYAN + "2", "Add New Menu"])
         main_menu.add_row([Fore.CYAN + "3", "Update Menu"])
         main_menu.add_row([Fore.CYAN + "4", "Delete Coffee"])
         main_menu.add_row([Fore.CYAN + "5" , "Sort Menu by Price"])
         main_menu.add_row([Fore.CYAN + "6",  "Sort Menu by Stock"])
         main_menu.add_row([Fore.CYAN + "7",  "Search Menu by Price"])
         main_menu.add_row([Fore.CYAN + "8",  "Search Menu by Stock"])
         main_menu.add_row([Fore.CYAN + "9", "Input Orders"])  
         main_menu.add_row([Fore.CYAN + "10", "View Orders"])
         main_menu.add_row([Fore.CYAN + "11",  "Total Income"])
         main_menu.add_row([Fore.CYAN + "0", "Exit"])
         print(Fore.YELLOW + str(main_menu))

      except Exception as e:
         print(Fore.RED + str(e))

   def display_total_income(self):
      try:
         print(Fore.CYAN + f"Total Income: Rp. {self.total_income}")
      except Exception as e:
         print(Fore.RED + str(e))

   def display_orders(self):
      try:
         if not self.head:
               print(Fore.YELLOW + "No orders yet.")
               return

         orders_table = PrettyTable(["Customer Name", "Order"])
         current = self.head
         while current:
               order_str = ", ".join([f"{coffee}: {quantity}" for coffee, quantity in current.order.items()])
               orders_table.add_row([current.customer_name, order_str])
               current = current.next
         print(Fore.CYAN + "All Orders")
         print(orders_table)
      except Exception as e:
         print(Fore.RED + str(e))

   def quick_sort(self, arr, key=None):
      try:
         if len(arr) <= 1:
               return arr
         else:
               pivot = arr[0]["price"] if key is None else key(arr[0])
               less_than_pivot = [item for item in arr[1:] if (key(item) if key else item["price"]) <= pivot]
               greater_than_pivot = [item for item in arr[1:] if (key(item) if key else item["price"]) > pivot]

               return self.quick_sort(less_than_pivot, key) + [arr[0]] + self.quick_sort(greater_than_pivot, key)
      except Exception as e:
         print(Fore.RED + str(e))
         return []

   def sort_menu_by_price(self):
      try:
         sorted_items = sorted(zip(self.coffee, self.price, self.stock), key=lambda x: x[1])
         print(Fore.GREEN + "Sorted Menu by Price:")
         table = PrettyTable(["Menu", "Price", "Stock"])
         for coffee, price, stock in sorted_items:
               table.add_row([coffee, price, stock])
         print(table)
      except Exception as e:
         print(Fore.RED + str(e))

   def sort_menu_by_stock(self):
      try:
         sorted_items = sorted(zip(self.coffee, self.price, self.stock), key=lambda x: x[2])
         print(Fore.GREEN + "Sorted Menu by Stock:")
         table = PrettyTable(["Menu", "Price", "Stock"])
         for coffee, price, stock in sorted_items:
               table.add_row([coffee, price, stock])
         print(table)
      except Exception as e:
         print(Fore.RED + str(e))

   def search_menu_by_price(self):
      try:
         target_price = int(input("Enter the price to search for: "))
         found = False
         for index, price in enumerate(self.price):
               if price == target_price:
                  found = True
                  print(Fore.GREEN + f"Price {target_price} found at index {index}.")
                  print(Fore.CYAN + "Corresponding Menu and Stock:")
                  print(f"Menu: {self.coffee[index]}, Stock: {self.stock[index]}, Price: {self.price[index]}")
         if not found:
               print(Fore.RED + f"Price {target_price} not found in the menu.")
      except ValueError:
         print(Fore.RED + "Please enter a valid price.")


   def search_menu_by_stock(self):
      try:
         target_stock = int(input("Enter the stock quantity to search for: "))
         found = False
         for index, stock in enumerate(self.stock):
               if stock == target_stock:
                  found = True
                  print(Fore.GREEN + f"Stock {target_stock} found at index {index}.")
                  print(Fore.CYAN + "Corresponding Menu and Price:")
                  print(f"Menu: {self.coffee[index]}, Price: {self.price[index]}, Stock: {self.stock[index]}")
         if not found:
               print(Fore.RED + f"Stock {target_stock} not found in the menu.")
      except ValueError:
         print(Fore.RED + "Please enter a valid stock quantity.")


   def jump_search(self, arr, x):
      try:
         n = len(arr)
         step = int(math.sqrt(n))
         prev = 0

         while arr[min(step, n) - 1] < x:
            prev = step
            step += int(math.sqrt(n))
            if prev >= n:
               return -1

         while arr[prev] < x:
            prev += 1
            if prev == min(step, n):
               return -1

         if arr[prev] == x:
            return prev
         return -1
      except Exception as e:
         print(Fore.RED + str(e))
         return -1

   def run(self):
      try:
         self.register()
         self.login_screen()

         while True:
               self.display_main_menu()
               choice = input("Enter your choice: ")

               if choice == '1':
                  self.display_menu_and_stock()
               elif choice == '2':
                  coffee_name = input("Enter new coffee name: ")
                  price = int(input("Enter price: "))
                  stock = int(input("Enter stock: "))
                  location = input("Enter location (beginning, middle, or end): ")
                  self.add_new_coffee(coffee_name, price, stock, location)
               elif choice == '3':
                  self.update_menu_and_stock()
               elif choice == '4':
                  self.display_menu_and_stock()
                  location = input("Enter location (beginning, middle, or end): ")
                  self.del_coffee(location)
               elif choice == '5':
                  self.sort_menu_by_price()
               elif choice == '7':
                  self.search_menu_by_price()
               elif choice == '8':
                  self.search_menu_by_stock()   
               elif choice == '8':
                  self.display_menu_and_stock()
                  customer_name = input("Enter your name: ")
                  coffee = input("Enter the coffee that been ordered: ")
                  quantity = int(input("Enter the quantity: "))
                  self.place_order(customer_name, coffee, quantity)
               elif choice == '9':
                  self.display_orders()
               elif choice == '10':
                  self.display_total_income()
               elif choice == '0':
                  print(Fore.BLUE + "Thank you for using the Coffee Shop system.")
                  break
               else:
                  print(Fore.RED + "Invalid choice. Please try again.")
      except Exception as e:
         print(Fore.RED + str(e))

coffee_shop = CoffeeShop()
coffee_shop.run()
