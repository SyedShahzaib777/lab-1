import tkinter as tk
from tkinter import messagebox
from datetime import datetime

THIS IS THE V2 OF MAIN.
menu = {
    'Chicken karahi': 350,
    'Chicken tikka': 300,
    'Malai Chicken tikka': 350,
    'Roti': 15,
    'Nan': 20,
    'Paratha': 80,
    'Zinger Burger' : 250
}

class BillGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Bill Generator")
        
        self.items = []
        self.quantities = []
        self.prices = []
        self.table_number = None
        
        # Create a frame to hold the table selection
        self.table_frame = tk.LabelFrame(root, text="Table Number")
        self.table_frame.pack(padx=10, pady=10)
        
        # Create buttons for table numbers
        for i in range(1, 6):
            button = tk.Button(self.table_frame, text=f"Table {i}", command=lambda table=i: self.select_table(table))
            button.pack(side=tk.LEFT, padx=5)
        
        # Create a frame to hold the menu items
        self.menu_frame = tk.LabelFrame(root, text="Menu")
        self.menu_frame.pack(padx=10, pady=10)
        
        # Create buttons for each menu item
        for item in menu:
            button = tk.Button(self.menu_frame, text=item, command=lambda item=item: self.add_item(item))
            button.pack(anchor=tk.W)
        
        # Create a frame to hold the order items and quantity entries
        self.order_frame = tk.LabelFrame(root, text="Order")
        self.order_frame.pack(padx=10, pady=10)
        
        # Create a listbox to display the order items and quantities
        self.order_listbox = tk.Listbox(self.order_frame, width=50)
        self.order_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        
        # Create a scrollbar for the order listbox
        self.scrollbar = tk.Scrollbar(self.order_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure the scrollbar to work with the listbox
        self.order_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.order_listbox.yview)
        
        # Create a frame to hold the delete and quantity entries
        self.modify_frame = tk.Frame(self.order_frame)
        self.modify_frame.pack(side=tk.RIGHT)
        
        # Create a delete button
        self.delete_button = tk.Button(self.modify_frame, text="Delete", command=self.delete_item)
        self.delete_button.pack()
        
        self.quantity_entries = {}
        
        # Create labels and entries for quantities
        for item in menu:
            label = tk.Label(self.modify_frame, text=item + ":")
            label.pack(anchor=tk.W)
            
            entry = tk.Entry(self.modify_frame)
            entry.pack()
            
            self.quantity_entries[item] = entry
        
        # Create a button to generate the bill
        self.bill_button = tk.Button(root, text="Generate Bill", command=self.generate_bill)
        self.bill_button.pack(pady=10)
        
        # Create a button to clear the order
        self.clear_button = tk.Button(root, text="Clear Order", command=self.clear_order)
        self.clear_button.pack(pady=5)
    
    def select_table(self, table):
        self.table_number = table
        messagebox.showinfo("Table Selected", f"You selected Table {table}.")
    
    def add_item(self, item):
        quantity_entry = self.quantity_entries[item]
        quantity = quantity_entry.get()
        
        # Check if a quantity is provided
        if quantity:
            try:
                quantity = int(quantity)
                if quantity > 0:
                    self.items.append(item)
                    self.quantities.append(quantity)
                    self.prices.append(menu[item])
                    
                    # Clear the order listbox
                    self.order_listbox.delete(0, tk.END)
                    
                    # Display the selected items and quantities in the order listbox
                    for i in range(len(self.items)):
                        self.order_listbox.insert(tk.END, f"{self.items[i]} ({self.quantities[i]})")
                else:
                    messagebox.showerror("Error", "Quantity must be greater than zero!")
            except ValueError:
                messagebox.showerror("Error", "Invalid quantity! Please enter a valid number.")
        else:
            messagebox.showerror("Error", "Quantity cannot be empty!")
    
    def delete_item(self):
        selected_indices = self.order_listbox.curselection()
        
        if selected_indices:
            # Delete the selected item from the order
            index = selected_indices[0]
            del self.items[index]
            del self.quantities[index]
            del self.prices[index]
            
            # Clear the order listbox
            self.order_listbox.delete(0, tk.END)
            
            # Display the updated order in the listbox
            for i in range(len(self.items)):
                self.order_listbox.insert(tk.END, f"{self.items[i]} ({self.quantities[i]})")
        else:
            messagebox.showerror("Error", "No item selected!")
    
    def generate_bill(self):
        if len(self.items) == 0:
            messagebox.showerror("Error", "No items selected!")
            return
        
        total = sum([self.prices[i] * self.quantities[i] for i in range(len(self.items))])
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        bill_text = f"Table Number: {self.table_number}\n"
        bill_text += f"Time and Date: {current_time}\n\n"
        bill_text += "Item                Price        Quantity\n"
        bill_text += "---------------------------------------\n"
        
        for i in range(len(self.items)):
            item = self.items[i]
            quantity = self.quantities[i]
            price = self.prices[i]
            item_line = f"{item:20} Rs{price:6.2f}   {quantity:6}\n"
            bill_text += item_line
        
        bill_text += "\n"
        bill_text += f"Total Amount: Rs{total:.2f}"
        
        messagebox.showinfo("Bill", bill_text)
        
        # Append the order details to the file
        with open("orders.txt", "a") as file:
            file.write(bill_text + "\n\n")
        
        self.clear_order()
    
    def clear_order(self):
        self.items = []
        self.quantities = []
        self.prices = []
        self.table_number = None
        
        self.order_listbox.delete(0, tk.END)
        for entry in self.quantity_entries.values():
            entry.delete(0, tk.END)

# Create the main window
root = tk.Tk()

# Create an instance of the BillGenerator class
bill_generator = BillGenerator(root)

# Run the application
root.mainloop()
