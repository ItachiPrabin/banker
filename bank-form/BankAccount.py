import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import webbrowser
import folium
import os


class BankAccountApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pyari Bot")
        self.geometry("1000x700")  # Increased window size
        
        self.steps = [
            'General Details',
            'Address Details',
            'Family Details',
            'Bank Details',
            'Depository Details',
            'Documents Upload',
            'User Agreement'
        ]
        
        self.current_step = 0
        self.create_widgets()

    def create_widgets(self):
        self.navbar_frame = tk.Frame(self, bg="white")
        self.navbar_frame.pack(side="top", fill="x", pady=20)
        
        self.content_frame = tk.Frame(self, bg="white")
        self.content_frame.pack(side="top", fill="both", expand=True)
        
        self.create_navbar()
        self.create_content()

    def create_navbar(self):
        self.step_buttons = []
        for index, step in enumerate(self.steps):
            btn = tk.Canvas(self.navbar_frame, width=50, height=50, highlightthickness=0)
            btn.create_oval(5, 5, 45, 45, fill="white", outline="gray")
            btn.create_text(25, 25, text=f"{index + 1}", fill="gray")
            btn.bind("<Button-1>", lambda e, idx=index: self.set_step(idx))
            btn.grid(row=0, column=index, padx=15, pady=5)  # Increased padding
            
            lbl = tk.Label(self.navbar_frame, text=step, bg="white", font=("Helvetica", 10))
            lbl.grid(row=1, column=index, padx=15, pady=5)  # Increased padding
            
            self.step_buttons.append((btn, lbl))
        
        self.update_navbar()

    def update_navbar(self):
        for index, (btn, lbl) in enumerate(self.step_buttons):
            if index == self.current_step:
                btn.itemconfig(1, fill="blue", outline="blue")
                btn.itemconfig(2, fill="white")
                lbl.config(fg="blue", font=("Helvetica", 10, "bold"))
            else:
                btn.itemconfig(1, fill="white", outline="gray")
                btn.itemconfig(2, fill="gray")
                lbl.config(fg="gray", font=("Helvetica", 10))

    def create_content(self):
        self.pages = {}
        for Page in (GeneralDetailsPage, AddressDetailsPage, FamilyDetailsPage,
                     BankDetailsPage, DepositoryDetailsPage, DocumentsPage, UserAgreementPage):
            page_name = Page.__name__
            page = Page(parent=self.content_frame, controller=self)
            self.pages[page_name] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show_page("GeneralDetailsPage")

    def show_page(self, page_name):
        page = self.pages[page_name]
        page.tkraise()

    def set_step(self, step):
        if step < 0 or step >= len(self.steps):
            return
        self.current_step = step
        self.update_navbar()
        page_name = self.steps[step].replace(" ", "") + "Page"
        self.show_page(page_name)

    def next_step(self):
        if self.current_step < len(self.steps) - 1:
            self.set_step(self.current_step + 1)

    def previous_step(self):
        if self.current_step > 0:
            self.set_step(self.current_step - 1)


class GeneralDetailsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        
        # Set a common font for the labels and entries
        label_font = ("Helvetica", 12)
        entry_font = ("Helvetica", 12)

        label = tk.Label(self, text="General Details", font=("Helvetica", 16, "bold"), bg="white")
        label.pack(side="top", fill="x", pady=10)
        
        form_frame = tk.Frame(self, bg="white")
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Full Name
        tk.Label(form_frame, text="Full Name", font=label_font, bg="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.full_name_entry = tk.Entry(form_frame, font=entry_font, width=50)
        self.full_name_entry.grid(row=2, column=1, padx=10, pady=5)

        # Sex
        tk.Label(form_frame, text="Sex", font=label_font, bg="white").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.sex_combobox = ttk.Combobox(form_frame, font=entry_font, values=["Select", "Male", "Female", "Other"], state="readonly")
        self.sex_combobox.current(0)
        self.sex_combobox.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Date of Birth
        tk.Label(form_frame, text="Date of Birth", font=label_font, bg="white").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.dob_entry = DateEntry(form_frame, font=entry_font, width=48, date_pattern="mm/dd/yyyy")
        self.dob_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # Email
        tk.Label(form_frame, text="Email", font=label_font, bg="white").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.email_entry = tk.Entry(form_frame, font=entry_font, width=50)
        self.email_entry.grid(row=5, column=1, padx=10, pady=5)

        # Phone
        tk.Label(form_frame, text="Phone", font=label_font, bg="white").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.phone_entry = tk.Entry(form_frame, font=entry_font, width=50)
        self.phone_entry.grid(row=6, column=1, padx=10, pady=5)

        self.create_navigation_buttons()

    def create_navigation_buttons(self):
        nav_frame = tk.Frame(self, bg="white")
        nav_frame.pack(side="bottom", fill="x", pady=10)

        next_btn = tk.Button(nav_frame, text="Next", command=self.controller.next_step)
        next_btn.pack(side="right", padx=5, pady=5)


class AddressDetailsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        # Set a common font for the labels and entries
        label_font = ("Helvetica", 12)
        entry_font = ("Helvetica", 12)

        # Create a canvas and a vertical scrollbar
        self.canvas = tk.Canvas(self, bg="white")
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        # Create a frame to hold the form
        self.form_frame = tk.Frame(self.canvas, bg="white")

        # Add the frame to the canvas
        self.canvas.create_window((0, 0), window=self.form_frame, anchor="nw")
        self.form_frame.bind("<Configure>", self.on_frame_configure)
        
        # Pack the canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Configure the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Permanent Address Section
        perm_address_label = tk.Label(self.form_frame, text="Permanent Address", font=("Helvetica", 14, "bold"), bg="white")
        perm_address_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        tk.Label(self.form_frame, text="Country of Residence", font=label_font, bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.country_entry = tk.Entry(self.form_frame, font=entry_font, width=50)
        self.country_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.form_frame, text="District", font=label_font, bg="white").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.district_entry = tk.Entry(self.form_frame, font=entry_font, width=50)
        self.district_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self.form_frame, text="Municipality", font=label_font, bg="white").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.municipality_entry = tk.Entry(self.form_frame, font=entry_font, width=50)
        self.municipality_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(self.form_frame, text="Ward No.", font=label_font, bg="white").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.ward_no_entry = tk.Entry(self.form_frame, font=entry_font, width=50)
        self.ward_no_entry.grid(row=5, column=1, padx=10, pady=5)

        # Checkbox for "Same as Permanent Address"
        self.same_address_var = tk.IntVar()
        same_address_check = tk.Checkbutton(self.form_frame, text="Same as Permanent Address", font=label_font, bg="white", variable=self.same_address_var, command=self.copy_permanent_address)
        same_address_check.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Temporary Address Section with Permanent Address labels
        temp_address_label = tk.Label(self.form_frame, text="Temporary Address", font=("Helvetica", 14, "bold"), bg="white")
        temp_address_label.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        tk.Label(self.form_frame, text="Country of Residence", font=label_font, bg="white").grid(row=8, column=0, padx=10, pady=5, sticky="w")
        self.temp_country_entry = tk.Entry(self.form_frame, font=entry_font, width=50)
        self.temp_country_entry.grid(row=8, column=1, padx=10, pady=5)

        tk.Label(self.form_frame, text="District", font=label_font, bg="white").grid(row=9, column=0, padx=10, pady=5, sticky="w")
        self.temp_district_entry = tk.Entry(self.form_frame, font=entry_font, width=50)
        self.temp_district_entry.grid(row=9, column=1, padx=10, pady=5)

        tk.Label(self.form_frame, text="Municipality", font=label_font, bg="white").grid(row=10, column=0, padx=10, pady=5, sticky="w")
        self.temp_municipality_entry = tk.Entry(self.form_frame, font=entry_font, width=50)
        self.temp_municipality_entry.grid(row=10, column=1, padx=10, pady=5)

        tk.Label(self.form_frame, text="Ward No.", font=label_font, bg="white").grid(row=11, column=0, padx=10, pady=5, sticky="w")
        self.temp_ward_no_entry = tk.Entry(self.form_frame, font=entry_font, width=50)
        self.temp_ward_no_entry.grid(row=11, column=1, padx=10, pady=5)

        # Button to Open Map
        self.map_btn = tk.Button(self.form_frame, text="Open Map", font=entry_font, command=self.open_map)
        self.map_btn.grid(row=12, column=0, columnspan=2, padx=10, pady=10)

        self.create_navigation_buttons()

    def on_frame_configure(self, event):
        # Update the scroll region of the canvas to encompass the form frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def copy_permanent_address(self):
        if self.same_address_var.get():
            self.temp_country_entry.delete(0, tk.END)
            self.temp_country_entry.insert(0, self.country_entry.get())

            self.temp_district_entry.delete(0, tk.END)
            self.temp_district_entry.insert(0, self.district_entry.get())

            self.temp_municipality_entry.delete(0, tk.END)
            self.temp_municipality_entry.insert(0, self.municipality_entry.get())

            self.temp_ward_no_entry.delete(0, tk.END)
            self.temp_ward_no_entry.insert(0, self.ward_no_entry.get())

    def open_map(self):
        # Generate a map centered at Kathmandu
        map_center = [27.7172, 85.3240]  # Coordinates for Kathmandu
        map_obj = folium.Map(location=map_center, zoom_start=13)

        # Add a marker for user location
        marker = folium.Marker(location=map_center, popup="Your Location", draggable=True)
        marker.add_to(map_obj)

        # Save map as HTML
        map_html_path = 'map.html'
        map_obj.save(map_html_path)

        # Open the map in the default web browser
        webbrowser.open(f'file://{os.path.abspath(map_html_path)}')

    def create_navigation_buttons(self):
        nav_frame = tk.Frame(self, bg="white")
        nav_frame.pack(side="bottom", fill="x", pady=10)

        prev_btn = tk.Button(nav_frame, text="Previous", font=("Helvetica", 12), command=self.controller.previous_step)
        prev_btn.pack(side="left", padx=5, pady=5)

        next_btn = tk.Button(nav_frame, text="Next", font=("Helvetica", 12), command=self.controller.next_step)
        next_btn.pack(side="right", padx=5, pady=5)


class FamilyDetailsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        label_font = ("Helvetica", 12)
        entry_font = ("Helvetica", 12)

        label = tk.Label(self, text="Family Details", font=("Helvetica", 16, "bold"), bg="white")
        label.pack(side="top", fill="x", pady=10)

        form_frame = tk.Frame(self, bg="white")
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(form_frame, text="Father's Name", font=label_font, bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.father_name_entry = tk.Entry(form_frame, font=entry_font, width=50)
        self.father_name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Mother's Name", font=label_font, bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.mother_name_entry = tk.Entry(form_frame, font=entry_font, width=50)
        self.mother_name_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="GrandFather's Name", font=label_font, bg="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.spouse_name_entry = tk.Entry(form_frame, font=entry_font, width=50)
        self.spouse_name_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="GrandMother's Name", font=label_font, bg="white").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.spouse_name_entry = tk.Entry(form_frame, font=entry_font, width=50)
        self.spouse_name_entry.grid(row=3, column=1, padx=10, pady=5)

        self.create_navigation_buttons()

    def create_navigation_buttons(self):
        nav_frame = tk.Frame(self, bg="white")
        nav_frame.pack(side="bottom", fill="x", pady=10)

        prev_btn = tk.Button(nav_frame, text="Previous", command=self.controller.previous_step)
        prev_btn.pack(side="left", padx=5, pady=5)

        next_btn = tk.Button(nav_frame, text="Next", command=self.controller.next_step)
        next_btn.pack(side="right", padx=5, pady=5)


class BankDetailsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        label_font = ("Helvetica", 12)
        entry_font = ("Helvetica", 12)

        label = tk.Label(self, text="Bank Details", font=("Helvetica", 16, "bold"), bg="white")
        label.pack(side="top", fill="x", pady=10)

        form_frame = tk.Frame(self, bg="white")
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(form_frame, text="Bank Name", font=label_font, bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.bank_name_entry = tk.Entry(form_frame, font=entry_font, width=50)
        self.bank_name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Account Number", font=label_font, bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.account_number_entry = tk.Entry(form_frame, font=entry_font, width=50)
        self.account_number_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="IFSC Code", font=label_font, bg="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.ifsc_code_entry = tk.Entry(form_frame, font=entry_font, width=50)
        self.ifsc_code_entry.grid(row=2, column=1, padx=10, pady=5)

        self.create_navigation_buttons()

    def create_navigation_buttons(self):
        nav_frame = tk.Frame(self, bg="white")
        nav_frame.pack(side="bottom", fill="x", pady=10)

        prev_btn = tk.Button(nav_frame, text="Previous", command=self.controller.previous_step)
        prev_btn.pack(side="left", padx=5, pady=5)

        next_btn = tk.Button(nav_frame, text="Next", command=self.controller.next_step)
        next_btn.pack(side="right", padx=5, pady=5)


class DepositoryDetailsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        label_font = ("Helvetica", 12)
        entry_font = ("Helvetica", 12)

        label = tk.Label(self, text="Depository Details", font=("Helvetica", 16, "bold"), bg="white")
        label.pack(side="top", fill="x", pady=10)

        form_frame = tk.Frame(self, bg="white")
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(form_frame, text="Depository Participant", font=label_font, bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.dp_entry = tk.Entry(form_frame, font=entry_font, width=50)
        self.dp_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="DP ID", font=label_font, bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.dp_id_entry = tk.Entry(form_frame, font=entry_font, width=50)
        self.dp_id_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Client ID", font=label_font, bg="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.client_id_entry = tk.Entry(form_frame, font=entry_font, width=50)
        self.client_id_entry.grid(row=2, column=1, padx=10, pady=5)

        self.create_navigation_buttons()

    def create_navigation_buttons(self):
        nav_frame = tk.Frame(self, bg="white")
        nav_frame.pack(side="bottom", fill="x", pady=10)

        prev_btn = tk.Button(nav_frame, text="Previous", command=self.controller.previous_step)
        prev_btn.pack(side="left", padx=5, pady=5)

        next_btn = tk.Button(nav_frame, text="Next", command=self.controller.next_step)
        next_btn.pack(side="right", padx=5, pady=5)


class DocumentsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        label_font = ("Helvetica", 12)
        entry_font = ("Helvetica", 12)

        label = tk.Label(self, text="Documents Upload", font=("Helvetica", 16, "bold"), bg="white")
        label.pack(side="top", fill="x", pady=10)

        form_frame = tk.Frame(self, bg="white")
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(form_frame, text="Passport Size Photo", font=label_font, bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.passport_photo_label = tk.Label(form_frame, bg="white")
        self.passport_photo_label.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Citizenship Front", font=label_font, bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.citizenship_front_label = tk.Label(form_frame, bg="white")
        self.citizenship_front_label.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Citizenship Back", font=label_font, bg="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.citizenship_back_label = tk.Label(form_frame, bg="white")
        self.citizenship_back_label.grid(row=2, column=1, padx=10, pady=5)

        self.create_navigation_buttons()

        # Load and display the images
        self.load_images()

    def load_images(self):
        # Placeholder method to load images from database
        # Replace this method with actual database fetching logic
        passport_photo_path = "path_to_passport_photo.jpg"
        citizenship_front_path = "path_to_citizenship_front.jpg"
        citizenship_back_path = "path_to_citizenship_back.jpg"

        self.display_image(passport_photo_path, self.passport_photo_label)
        self.display_image(citizenship_front_path, self.citizenship_front_label)
        self.display_image(citizenship_back_path, self.citizenship_back_label)

    def display_image(self, image_path, label):
        try:
            image = Image.open(image_path)
            image = image.resize((150, 150), Image.ANTIALIAS)  # Resize the image to fit the label
            photo = ImageTk.PhotoImage(image)
            label.config(image=photo)
            label.image = photo  # Keep a reference to avoid garbage collection
        except Exception as e:
            print(f"Error loading image: {e}")

    def create_navigation_buttons(self):
        nav_frame = tk.Frame(self, bg="white")
        nav_frame.pack(side="bottom", fill="x", pady=10)

        prev_btn = tk.Button(nav_frame, text="Previous", command=self.controller.previous_step)
        prev_btn.pack(side="left", padx=5, pady=5)

        next_btn = tk.Button(nav_frame, text="Next", command=self.controller.next_step)
        next_btn.pack(side="right", padx=5, pady=5)



class UserAgreementPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        label_font = ("Helvetica", 12)
        entry_font = ("Helvetica", 12)

        label = tk.Label(self, text="User Agreement", font=("Helvetica", 16, "bold"), bg="white")
        label.pack(side="top", fill="x", pady=10)

        form_frame = tk.Frame(self, bg="white")
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(form_frame, text="Terms and Conditions", font=label_font, bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.terms_text = tk.Text(form_frame, font=entry_font, width=70, height=20, wrap="word", bg="lightgrey")
        self.terms_text.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
        self.terms_text.insert(tk.END, self.get_terms_and_conditions())
        self.terms_text.config(state=tk.DISABLED)

        self.terms_var = tk.IntVar()
        terms_check = tk.Checkbutton(form_frame, text="I have read and agree to the terms and conditions", font=label_font, bg="white", variable=self.terms_var)
        terms_check.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        self.create_navigation_buttons()

    def create_navigation_buttons(self):
        nav_frame = tk.Frame(self, bg="white")
        nav_frame.pack(side="bottom", fill="x", pady=10)

        prev_btn = tk.Button(nav_frame, text="Previous", font=("Helvetica", 12), command=self.controller.previous_step)
        prev_btn.pack(side="left", padx=5, pady=5)

        next_btn = tk.Button(nav_frame, text="Next", font=("Helvetica", 12), command=self.next_step)
        next_btn.pack(side="right", padx=5, pady=5)

    def next_step(self):
        if not self.terms_var.get():
            messagebox.showwarning("Warning", "You must agree to the terms and conditions before proceeding.")
        else:
            self.controller.next_step()

    def get_terms_and_conditions(self):
        return (
            "1. Introduction\n"
            "Welcome to XYZ Bank. These terms and conditions outline the rules and regulations for the use of XYZ Bank's services.\n\n"
            "2. Acceptance of Terms\n"
            "By accessing this service, you accept these terms and conditions in full. Do not continue to use XYZ Bank's services if you do not accept all of the terms and conditions stated on this page.\n\n"
            "3. Services\n"
            "XYZ Bank offers a range of financial services including savings accounts, loans, and investment options. The specific terms and conditions of each service will be provided when you sign up for that service.\n\n"
            "4. User Responsibilities\n"
            "As a user, you are responsible for maintaining the confidentiality of your account information, including your username and password. You agree to notify us immediately of any unauthorized use of your account or any other breach of security.\n\n"
            "5. Privacy Policy\n"
            "We are committed to protecting your privacy. Our privacy policy, which sets out how we will use your information, can be found on our website. By using our services, you consent to the processing described therein.\n\n"
            "6. Limitation of Liability\n"
            "XYZ Bank will not be liable for any indirect, incidental, special, consequential, or punitive damages, or any loss of profits or revenues, whether incurred directly or indirectly, or any loss of data, use, goodwill, or other intangible losses, resulting from (i) your use or inability to use the service; (ii) any unauthorized access to or use of our servers and/or any personal information stored therein.\n\n"
            "7. Changes to the Terms\n"
            "XYZ Bank reserves the right to revise these terms and conditions at any time. By using our services, you agree to be bound by the current version of these terms and conditions.\n\n"
            "8. Governing Law\n"
            "These terms and conditions are governed by and construed in accordance with the laws of [Your Country], and you irrevocably submit to the exclusive jurisdiction of the courts in that location.\n\n"
            "9. Contact Us\n"
            "If you have any questions about these terms and conditions, please contact us at support@xyzbank.com.\n\n"
            "Thank you for choosing XYZ Bank.\n"
        )
        self.create_navigation_buttons()

    def create_navigation_buttons(self):
        nav_frame = tk.Frame(self, bg="white")
        nav_frame.pack(side="bottom", fill="x", pady=10)

        prev_btn = tk.Button(nav_frame, text="Previous", command=self.controller.previous_step)
        prev_btn.pack(side="left", padx=5, pady=5)

if __name__ == "__main__":
    app = BankAccountApp()
    app.mainloop()
