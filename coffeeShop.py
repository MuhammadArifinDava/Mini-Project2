from prettytable import PrettyTable
from datetime import datetime

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
         print("Invalid location. Coffee not added.")

   def del_coffee(self, location=None):
      if location not in ['beginning', 'middle', 'end']:
         print("Invalid location. Please choose 'beginning', 'middle', or 'end'.")
         return

      if location == 'beginning':
         if self.coffee:
               deleted_coffee = self.coffee.pop(0)
               self.price.pop(0)
               self.stock.pop(0)
               print(f"Coffee '{deleted_coffee}' deleted successfully from the beginning.")
         else:
               print("No coffee found to delete.")
      elif location == 'end':
         if self.coffee:
               deleted_coffee = self.coffee.pop()
               self.price.pop()
               self.stock.pop()
               print(f"Coffee '{deleted_coffee}' deleted successfully from the end.")
         else:
               print("No coffee found to delete.")
      elif location == 'middle':
         if not self.coffee:
            print("No coffee found to delete.")
            return

         if len(self.coffee) == 1:
            print("There is only one coffee available. You cannot delete it from the middle.")
            return

         coffee_to_delete = input("Enter the coffee name to delete: ")
         if coffee_to_delete in self.coffee:
            index = self.coffee.index(coffee_to_delete)
            if index == 0 or index == len(self.coffee) - 1:
                  print(f"The coffee '{coffee_to_delete}' cannot be deleted from the middle.")
            else:
                  self.coffee.pop(index)
                  self.price.pop(index)
                  self.stock.pop(index)
                  print(f"Coffee '{coffee_to_delete}' deleted successfully.")
         else:
            print(f"Coffee '{coffee_to_delete}' not found.")





   def display_menu_and_stock(self):
      table = PrettyTable(["Menu", "Price", "Stock"])
      for coffee, price, stock in zip(self.coffee, self.price, self.stock):
         table.add_row([coffee, price, stock])
      print("Coffee Shop Menu and Stock")
      print(table)

   def update_menu_and_stock(self):
      self.display_menu_and_stock()
      item = input("Enter the item to update: ")
      if item in self.coffee:
         index = self.coffee.index(item)
         price = int(input("Enter the new price: "))
         quantity = int(input("Enter the new stock quantity: "))
         self.price[index] = price
         self.stock[index] = quantity
         print(f"Menu item '{item}' updated successfully.")
      else:
         print(f"Menu item '{item}' not found.")

   def place_order(self, customer_name, coffee_name, quantity):
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
            print(f"Order placed successfully. Total Bill: Rp. {total_bill:.2f}")
            self.total_income += total_bill
         else:
            print("Insufficient stock.")
      else:
         print("Invalid coffee selection.")

   def register_user(self, username, password):
      if username not in self.users:
         self.users[username] = {"password": password, "role": "customer", "balance": 0}
         print("Registration successful.")
      else:
         print("Username already exists. Please choose another username.")

   def login(self, username, password):
      if username in self.users and self.users[username]["password"] == password:
         return True
      return False

   def save_invoice_to_txt(self, customer_name, customer_order, total_bill):
      with open(f'{customer_name}_invoice.txt', 'w') as invoice_file:
         invoice_file.write("CoffeeShop Invoice\n")
         invoice_file.write(f"Customer Name: {customer_name}\n")
         for coffee, quantity in customer_order.items():
               invoice_file.write(f"{coffee}: {quantity}\n")
         invoice_file.write(f"Total Bill: Rp. {total_bill:.2f}\n")

   def generate_invoice(self, customer_name, customer_order, total_bill):
      invoice = PrettyTable()
      invoice.field_names = ["CoffeeShop", "Invoice"]
      invoice.add_row(["Customer Name:", customer_name])
      invoice.add_row(["Transaction Time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
      for coffee, quantity in customer_order.items():
         invoice.add_row([coffee, f"{quantity}"])
      invoice.add_row(["Total Bill:", f"Rp. {total_bill:.2f}"])
      print(invoice)
      self.save_invoice_to_txt(customer_name, customer_order, total_bill)

   def register(self):
      print("Welcome To Coffee Shop \nPlease Register First❤️")
      username = input("Enter your username: ")
      password = input("Enter your password: ")
      self.register_user(username, password)

   def login_screen(self):
      while True:
         print("Login Your Account✌️")
         username = input("Enter your username: ")
         password = input("Enter your password: ")
         if self.login(username, password):
               print(f"Welcome, {username}!")
               break
         else:
               print("Invalid username or password. Please try again.")

   def display_main_menu(self):
      main_menu = PrettyTable()
      main_menu.field_names = ["Features", "CoffeeShop Hanei"]
      main_menu.add_row(["1", "Display Menu"])
      main_menu.add_row(["2", "Add New Menu"])
      main_menu.add_row(["3", "Update Menu"])
      main_menu.add_row(["4", "Delete Coffee"])
      main_menu.add_row(["5", "Sort Menu by Price"])
      main_menu.add_row(["6", "Sort Menu by Stock"])
      main_menu.add_row(["7", "Input Orders"])
      main_menu.add_row(["8", "View Orders"])
      main_menu.add_row(["9", "Total Income"])
      main_menu.add_row(["0", "Exit"])
      print(main_menu)

   def display_total_income(self):
      print(f"Total Income: Rp. {self.total_income}")

   def display_orders(self):
      if not self.head:
         print("No orders yet.")
         return

      orders_table = PrettyTable(["Customer Name", "Order"])
      current = self.head
      while current:
            order_str = ", ".join([f"{coffee}: {quantity}" for coffee, quantity in current.order.items()])
            orders_table.add_row([current.customer_name, order_str])
            current = current.next
      print("All Orders")
      print(orders_table)

   def quick_sort(self, arr, key=None):
      if len(arr) <= 1:
         return arr
      else:
         pivot = arr[0]["price"] if key is None else key(arr[0])  
         less_than_pivot = [item for item in arr[1:] if (key(item) if key else item["price"]) <= pivot]
         greater_than_pivot = [item for item in arr[1:] if (key(item) if key else item["price"]) > pivot]

         return self.quick_sort(less_than_pivot, key) + [arr[0]] + self.quick_sort(greater_than_pivot, key)

   def sort_menu_by_price(self):
      sorted_items = sorted(zip(self.coffee, self.price, self.stock), key=lambda x: x[1])
      print("Sorted Menu by Price:")
      table = PrettyTable(["Menu", "Price", "Stock"])
      for coffee, price, stock in sorted_items:
         table.add_row([coffee, price, stock])
      print(table)

   def sort_menu_by_stock(self):
      sorted_items = sorted(zip(self.coffee, self.price, self.stock), key=lambda x: x[2])
      print("Sorted Menu by Stock:")
      table = PrettyTable(["Menu", "Price", "Stock"])
      for coffee, price, stock in sorted_items:
         table.add_row([coffee, price, stock])
      print(table)

   
   def run(self):
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
         elif choice == '6':
            self.sort_menu_by_stock()
         elif choice == '7':
            self.display_menu_and_stock()
            customer_name = input("Enter your name: ")
            coffee = input("Enter the coffee that been ordered: ")
            quantity = int(input("Enter the quantity: "))
            self.place_order(customer_name, coffee, quantity)
         elif choice == '8':
            self.display_orders()
         elif choice == '9':
            self.display_total_income()
         elif choice == '0':
            print("Thank you for using the Coffee Shop system.")
            break
         else:
            print("Invalid choice. Please try again.")



coffee_shop = CoffeeShop()
coffee_shop.run()