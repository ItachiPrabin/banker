import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

class BankAccountApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bank Account Application")
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
                     BankDetailsPage, DepositoryDetailsPage, DocumentsUploadPage, UserAgreementPage):
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
        label = tk.Label(self, text="General Details", font=("Helvetica", 16, "bold"), bg="white")
        label.pack(side="top", fill="x", pady=10)
        
        form_frame = tk.Frame(self, bg="white")
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Branch
        tk.Label(form_frame, text="Branch", bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.branch_entry = tk.Entry(form_frame, width=50)
        self.branch_entry.grid(row=0, column=1, padx=10, pady=5)

        # Purpose of Creating Bank Account
        tk.Label(form_frame, text="Purpose of Creating Bank Account", bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.purpose_entry = tk.Entry(form_frame, width=50)
        self.purpose_entry.grid(row=1, column=1, padx=10, pady=5)

        # Full Name
        tk.Label(form_frame, text="Full Name", bg="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.full_name_entry = tk.Entry(form_frame, width=50)
        self.full_name_entry.grid(row=2, column=1, padx=10, pady=5)

        # Sex
        tk.Label(form_frame, text="Sex", bg="white").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.sex_combobox = ttk.Combobox(form_frame, values=["Select", "Male", "Female", "Other"], state="readonly")
        self.sex_combobox.current(0)
        self.sex_combobox.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Date of Birth
        tk.Label(form_frame, text="Date of Birth", bg="white").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.dob_entry = DateEntry(form_frame, width=48, date_pattern="mm/dd/yyyy")
        self.dob_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # Email
        tk.Label(form_frame, text="Email", bg="white").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.email_entry = tk.Entry(form_frame, width=50)
        self.email_entry.grid(row=5, column=1, padx=10, pady=5)

        # Phone
        tk.Label(form_frame, text="Phone", bg="white").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.phone_entry = tk.Entry(form_frame, width=50)
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
        label = tk.Label(self, text="Address Details", font=("Helvetica", 16), bg="white")
        label.pack(side="top", fill="x", pady=10)

        form_frame = tk.Frame(self, bg="white")
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(form_frame, text="Address Line 1", bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.address1_entry = tk.Entry(form_frame, width=50)
        self.address1_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Address Line 2", bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.address2_entry = tk.Entry(form_frame, width=50)
        self.address2_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="City", bg="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.city_entry = tk.Entry(form_frame, width=50)
        self.city_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="State", bg="white").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.state_entry = tk.Entry(form_frame, width=50)
        self.state_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Zip Code", bg="white").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.zip_entry = tk.Entry(form_frame, width=50)
        self.zip_entry.grid(row=4, column=1, padx=10, pady=5)

        self.create_navigation_buttons()

    def create_navigation_buttons(self):
        nav_frame = tk.Frame(self, bg="white")
        nav_frame.pack(side="bottom", fill="x", pady=10)

        prev_btn = tk.Button(nav_frame, text="Previous", command=self.controller.previous_step)
        prev_btn.pack(side="left", padx=5, pady=5)

        next_btn = tk.Button(nav_frame, text="Next", command=self.controller.next_step)
        next_btn.pack(side="right", padx=5, pady=5)

class FamilyDetailsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        label = tk.Label(self, text="Family Details", font=("Helvetica", 16), bg="white")
        label.pack(side="top", fill="x", pady=10)

        form_frame = tk.Frame(self, bg="white")
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(form_frame, text="Father's Name", bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.father_name_entry = tk.Entry(form_frame, width=50)
        self.father_name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Mother's Name", bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.mother_name_entry = tk.Entry(form_frame, width=50)
        self.mother_name_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Spouse's Name", bg="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.spouse_name_entry = tk.Entry(form_frame, width=50)
        self.spouse_name_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Number of Dependents", bg="white").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.dependents_entry = tk.Entry(form_frame, width=50)
        self.dependents_entry.grid(row=3, column=1, padx=10, pady=5)

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
        label = tk.Label(self, text="Bank Details", font=("Helvetica", 16), bg="white")
        label.pack(side="top", fill="x", pady=10)

        form_frame = tk.Frame(self, bg="white")
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(form_frame, text="Account Type", bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.account_type_entry = tk.Entry(form_frame, width=50)
        self.account_type_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Branch Name", bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.branch_name_entry = tk.Entry(form_frame, width=50)
        self.branch_name_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="IFSC Code", bg="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.ifsc_code_entry = tk.Entry(form_frame, width=50)
        self.ifsc_code_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Account Number", bg="white").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.account_number_entry = tk.Entry(form_frame, width=50)
        self.account_number_entry.grid(row=3, column=1, padx=10, pady=5)

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
        label = tk.Label(self, text="Depository Details", font=("Helvetica", 16), bg="white")
        label.pack(side="top", fill="x", pady=10)

        form_frame = tk.Frame(self, bg="white")
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(form_frame, text="Depository Participant Name", bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.dp_name_entry = tk.Entry(form_frame, width=50)
        self.dp_name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="DP ID", bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.dp_id_entry = tk.Entry(form_frame, width=50)
        self.dp_id_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Client ID", bg="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.client_id_entry = tk.Entry(form_frame, width=50)
        self.client_id_entry.grid(row=2, column=1, padx=10, pady=5)

        self.create_navigation_buttons()

    def create_navigation_buttons(self):
        nav_frame = tk.Frame(self, bg="white")
        nav_frame.pack(side="bottom", fill="x", pady=10)

        prev_btn = tk.Button(nav_frame, text="Previous", command=self.controller.previous_step)
        prev_btn.pack(side="left", padx=5, pady=5)

        next_btn = tk.Button(nav_frame, text="Next", command=self.controller.next_step)
        next_btn.pack(side="right", padx=5, pady=5)

class DocumentsUploadPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        label = tk.Label(self, text="Documents Upload", font=("Helvetica", 16), bg="white")
        label.pack(side="top", fill="x", pady=10)

        form_frame = tk.Frame(self, bg="white")
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(form_frame, text="Upload Photo", bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.upload_photo_btn = tk.Button(form_frame, text="Browse", command=self.upload_photo)
        self.upload_photo_btn.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        tk.Label(form_frame, text="Upload Signature", bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.upload_signature_btn = tk.Button(form_frame, text="Browse", command=self.upload_signature)
        self.upload_signature_btn.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        tk.Label(form_frame, text="Upload ID Proof", bg="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.upload_id_proof_btn = tk.Button(form_frame, text="Browse", command=self.upload_id_proof)
        self.upload_id_proof_btn.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        self.create_navigation_buttons()

    def upload_photo(self):
        pass

    def upload_signature(self):
        pass

    def upload_id_proof(self):
        pass

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
        label = tk.Label(self, text="User Agreement", font=("Helvetica", 16), bg="white")
        label.pack(side="top", fill="x", pady=10)

        form_frame = tk.Frame(self, bg="white")
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(form_frame, text="I agree to the terms and conditions", bg="white").pack(side="top", fill="x", pady=5)
        self.agreement_var = tk.IntVar()
        self.agreement_check = tk.Checkbutton(form_frame, variable=self.agreement_var, bg="white")
        self.agreement_check.pack(side="top", pady=5)

        self.create_navigation_buttons()

    def create_navigation_buttons(self):
        nav_frame = tk.Frame(self, bg="white")
        nav_frame.pack(side="bottom", fill="x", pady=10)

        prev_btn = tk.Button(nav_frame, text="Previous", command=self.controller.previous_step)
        prev_btn.pack(side="left", padx=5, pady=5)

        submit_btn = tk.Button(nav_frame, text="Submit", command=self.submit_form)
        submit_btn.pack(side="right", padx=5, pady=5)

    def submit_form(self):
        if self.agreement_var.get() == 1:
            print("Form submitted!")
        else:
            print("Please agree to the terms and conditions.")

if __name__ == "__main__":
    app = BankAccountApp()
    app.mainloop()

