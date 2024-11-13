import tkinter as tk
from tkinter import messagebox
import mysql.connector

class HotelManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("600x500")  # Set window size (width x height)

        # Add hotel name label
        tk.Label(root, text="Room Booking ", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        self.bookings = []
        
        # Labels and Entries for Booking
        tk.Label(root, text="Guest Name:").grid(row=1, column=0)
        self.guest_name_entry = tk.Entry(root)
        self.guest_name_entry.grid(row=1, column=1)
        
        tk.Label(root, text="Room Number:").grid(row=2, column=0)
        self.room_number_entry = tk.Entry(root)
        self.room_number_entry.grid(row=2, column=1)
        
        tk.Label(root, text="Number of Nights:").grid(row=3, column=0)
        self.nights_entry = tk.Entry(root)
        self.nights_entry.grid(row=3, column=1)
        
        tk.Label(root, text="City:").grid(row=4, column=0)
        self.city_entry = tk.Entry(root)
        self.city_entry.grid(row=4, column=1)
        
        tk.Label(root, text="Phone No:").grid(row=5, column=0)
        self.phone_entry = tk.Entry(root)
        self.phone_entry.grid(row=5, column=1)
        
        tk.Label(root, text="Email:").grid(row=6, column=0)
        self.email_entry = tk.Entry(root)
        self.email_entry.grid(row=6, column=1)
        
        # Buttons
        tk.Button(root, text="Book Room", command=self.book_room).grid(row=7, column=0, columnspan=2)

        # Text Widget for displaying all bookings
        self.booking_display = tk.Text(root, height=24, width=110)
        self.booking_display.grid(row=8, column=0, columnspan=2, pady=10)
        self.booking_display.config(state=tk.DISABLED)  # Make it read-only

        # Connect to the database
        self.db_connection = self.connect_to_database()
        self.db_cursor = self.db_connection.cursor()

        # Fetch existing bookings from the database
        self.update_booking_display()

    def connect_to_database(self):
        """Connect to the MySQL database."""
        try:
            connection = mysql.connector.connect(
                host="localhost",       # Change if your DB is hosted elsewhere
                user="root",            # MySQL username
                password="",
                database="hotel_management"  # Database name
            )
            return connection
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return None

    def book_room(self):
        guest_name = self.guest_name_entry.get()
        room_number = self.room_number_entry.get()
        nights = self.nights_entry.get()
        city = self.city_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        
        if not guest_name or not room_number or not nights or not city or not phone or not email:
            messagebox.showerror("Input Error", "Please fill in all fields")
            return
        
        try:
            nights = int(nights)
        except ValueError:
            messagebox.showerror("Input Error", "Number of nights must be a number")
            return

        # Insert the booking into the database
        self.insert_booking(guest_name, room_number, nights, city, phone, email)

        messagebox.showinfo("Success", f"Room {room_number} booked for {guest_name} for {nights} nights!")
        
        # Clear input fields
        self.guest_name_entry.delete(0, tk.END)
        self.room_number_entry.delete(0, tk.END)
        self.nights_entry.delete(0, tk.END)
        self.city_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

        self.update_booking_display()

    def insert_booking(self, guest_name, room_number, nights, city, phone, email):
        """Insert a new booking into the database."""
        try:
            query = """
                INSERT INTO bookings (guest_name, room_number, nights, city, phone, email)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.db_cursor.execute(query, (guest_name, room_number, nights, city, phone, email))
            self.db_connection.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error inserting booking: {err}")

    def update_booking_display(self):
        """Fetch and display bookings from the database."""
        self.booking_display.config(state=tk.NORMAL)
        self.booking_display.delete(1.0, tk.END)  # Clear the text area
        
        # Header for the columns
        header = f"{'Guest Name':<20} {'Room No.':<10} {'Nights':<7} {'City':<15} {'Phone':<15} {'Email'}"
        self.booking_display.insert(tk.END, header + "\n")
        self.booking_display.insert(tk.END, "-" * 80 + "\n")  # Separator line

        # Fetch all bookings from the database
        try:
            self.db_cursor.execute("SELECT guest_name, room_number, nights, city, phone, email FROM bookings")
            bookings = self.db_cursor.fetchall()

            if not bookings:
                self.booking_display.insert(tk.END, "No current bookings.")
            else:
                for b in bookings:
                    booking_info = (f"{b[0]:<20} {b[1]:<10} {b[2]:<7} {b[3]:<15} {b[4]:<15} {b[5]}")
                    self.booking_display.insert(tk.END, booking_info + "\n")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching bookings: {err}")

        self.booking_display.config(state=tk.DISABLED)  # Make it read-only again

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelManagementSystem(root)
    root.mainloop()
