import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

PRIMARY = "#2c3e50"
ACCENT = "#3498db"
SUCCESS = "#2ecc71"
DANGER = "#e74c3c"
TEXT = "#ecf0f1"

stock_data = []

root = tk.Tk()
root.title("Stock Management System")
root.geometry("700x500")

# ===== โหลดรูป =====
try:
    original = Image.open("bg.jpg").convert("RGB")
except:
    original = Image.new("RGB", (100, 100), color=PRIMARY)

# ===== Notebook =====
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# =========================
# LOGO TAB
# =========================
tab_logo = tk.Frame(notebook, bg=PRIMARY)
notebook.add(tab_logo, text="Logo")

tk.Label(tab_logo, text="📦 STOCK SYSTEM",
         bg=PRIMARY, fg=TEXT,
         font=("Segoe UI", 28, "bold")).pack(expand=True)

tk.Button(tab_logo, text="เข้าสู่เมนู",
          command=lambda: notebook.select(1)).pack(pady=20)

# =========================
# MENU TAB
# =========================
tab_menu = tk.Frame(notebook)
notebook.add(tab_menu, text="Menu")

canvas = tk.Canvas(tab_menu)
canvas.pack(fill="both", expand=True)
bg_image = None

def resize_bg(event):
    global bg_image
    w, h = event.width, event.height
    resized = original.resize((w, h), Image.LANCZOS)
    bg_image = ImageTk.PhotoImage(resized)
    canvas.delete("bg")
    canvas.create_image(0, 0, image=bg_image, anchor="nw", tags="bg")
    canvas.create_rectangle(0, 0, w, h, fill="#000000", stipple="gray25")

canvas.bind("<Configure>", resize_bg)

# =========================
# EFFECT
# =========================
def add_hover_effect(btn, color, hover):
    btn.bind("<Enter>", lambda e: btn.config(bg=hover))
    btn.bind("<Leave>", lambda e: btn.config(bg=color))

# =========================
# REGISTER
# =========================
def open_register():
    form = tk.Toplevel(root)
    form.title("ลงทะเบียนสินค้า")
    form.geometry("420x600")

    card = tk.Frame(form, bg=PRIMARY)
    card.pack(fill="both", expand=True)

    tk.Label(card, text="ลงทะเบียนสินค้า",
             bg=PRIMARY, fg=TEXT,
             font=("Segoe UI", 16, "bold")).pack(pady=10)

    prefix = {
        "Resistor":"R","Capacitor":"C","Inductor":"L",
        "Diode":"D","Transistor":"T","IC":"IC"
    }

    type_short = {
        "Carbon Film":"CF","Metal Film":"MF","Wirewound":"WW",
        "Ceramic":"CER","Electrolytic":"EL",
        "Rectifier":"REC","Zener":"ZN","LED":"LED",
        "BJT":"BJT","MOSFET":"MOS",
        "Logic IC":"LOG","Microcontroller":"MCU"
    }

    types = {
        "Resistor": ["Carbon Film","Metal Film","Wirewound"],
        "Capacitor": ["Ceramic","Electrolytic"],
        "Inductor": ["Air Core","Ferrite Core"],
        "Diode": ["Rectifier","Zener","LED"],
        "Transistor": ["BJT","MOSFET"],
        "IC": ["Logic IC","Microcontroller"]
    }

    def generate_code(*args):
        if category.get() and type_box.get():
            code = f"{prefix.get(category.get())}-{value.get()}-{type_short.get(type_box.get())}"
            code_var.set(code)

    def update_type(e):
        selected = category.get()
        type_box["values"] = types.get(selected, [])
        type_box.set("")

        watt_label.pack_forget()
        watt.pack_forget()
        volt_label.pack_forget()
        volt.pack_forget()

        if selected == "Resistor":
            watt_label.pack(after=value)
            watt.pack(after=watt_label, pady=5)

        if selected in ["Capacitor","Diode","Transistor","IC"]:
            volt_label.pack(after=value)
            volt.pack(after=volt_label, pady=5)

    tk.Label(card, text="ประเภท", bg=PRIMARY, fg=TEXT).pack()
    category = ttk.Combobox(card, state="readonly", values=list(types.keys()))
    category.pack(pady=5)

    tk.Label(card, text="ชนิด", bg=PRIMARY, fg=TEXT).pack()
    type_box = ttk.Combobox(card, state="readonly")
    type_box.pack(pady=5)

    tk.Label(card, text="รหัสสินค้า", bg=PRIMARY, fg=TEXT).pack()
    code_var = tk.StringVar()
    tk.Entry(card, textvariable=code_var, state="readonly").pack(pady=5)

    tk.Label(card, text="ค่า", bg=PRIMARY, fg=TEXT).pack()
    value = tk.Entry(card)
    value.pack(pady=5)

    watt_label = tk.Label(card, text="กำลังไฟ (W)", bg=PRIMARY, fg=TEXT)
    watt = tk.Entry(card)

    volt_label = tk.Label(card, text="แรงดัน (V)", bg=PRIMARY, fg=TEXT)
    volt = tk.Entry(card)

    tk.Label(card, text="จำนวน", bg=PRIMARY, fg=TEXT).pack()
    qty = tk.Entry(card)
    qty.pack(pady=5)

    category.bind("<<ComboboxSelected>>", update_type)
    type_box.bind("<<ComboboxSelected>>", generate_code)
    value.bind("<KeyRelease>", generate_code)

    def save():
        try:
            amount = int(qty.get())
        except:
            tk.Label(card, text="จำนวนต้องเป็นตัวเลข", fg="red").pack()
            return

        if not code_var.get():
            tk.Label(card, text="กรอกข้อมูลให้ครบ", fg="red").pack()
            return

        stock_data.append({
            "code": code_var.get(),
            "category": category.get(),
            "type": type_box.get(),
            "value": value.get(),
            "watt": watt.get(),
            "volt": volt.get(),
            "qty": amount
        })
        form.destroy()

    tk.Button(card, text="บันทึก", bg=ACCENT, fg="white",
              command=save).pack(pady=10)

# =========================
# ADD STOCK
# =========================
def open_add():
    win = tk.Toplevel(root)
    win.title("เพิ่มสินค้า")

    tk.Label(win, text="รหัสสินค้า").pack()
    code = tk.Entry(win)
    code.pack()

    tk.Label(win, text="จำนวนเพิ่ม").pack()
    qty = tk.Entry(win)
    qty.pack()

    def add():
        try:
            amount = int(qty.get())
        except:
            tk.Label(win, text="กรอกตัวเลขเท่านั้น", fg="red").pack()
            return

        for item in stock_data:
            if item["code"] == code.get():
                item["qty"] += amount
                win.destroy()
                return
        tk.Label(win, text="ไม่พบสินค้า", fg="red").pack()

    tk.Button(win, text="เพิ่ม", bg=SUCCESS, command=add).pack(pady=10)

# =========================
# REMOVE STOCK
# =========================
def open_remove():
    win = tk.Toplevel(root)
    win.title("เบิกสินค้า")

    tk.Label(win, text="รหัสสินค้า").pack()
    code = tk.Entry(win)
    code.pack()

    tk.Label(win, text="จำนวน").pack()
    qty = tk.Entry(win)
    qty.pack()

    def remove():
        try:
            amount = int(qty.get())
        except:
            tk.Label(win, text="กรอกตัวเลขเท่านั้น", fg="red").pack()
            return

        for item in stock_data:
            if item["code"] == code.get():
                if item["qty"] >= amount:
                    item["qty"] -= amount
                    win.destroy()
                else:
                    tk.Label(win, text="ของไม่พอ", fg="red").pack()
                return
        tk.Label(win, text="ไม่พบสินค้า", fg="red").pack()

    tk.Button(win, text="เบิก", bg=DANGER, command=remove).pack(pady=10)

# =========================
# TABLE
# =========================
def open_table():
    win = tk.Toplevel(root)
    tree = ttk.Treeview(win, columns=("code","qty"), show="headings")
    tree.heading("code", text="Code")
    tree.heading("qty", text="Qty")
    tree.pack(fill="both", expand=True)

    for i in stock_data:
        tree.insert("", "end", values=(i["code"], i["qty"]))

# =========================
# MENU UI
# =========================
card = tk.Frame(canvas, bg=PRIMARY)
card.place(relx=0.5, rely=0.5, anchor="center")

def btn(text, color, cmd):
    b = tk.Button(card, text=text, bg=color, fg="white", width=25, height=2, command=cmd)
    add_hover_effect(b, color, "#5dade2")
    return b

btn("ลงทะเบียนสินค้า", ACCENT, open_register).pack(pady=5)
btn("เพิ่มสินค้า", SUCCESS, open_add).pack(pady=5)
btn("เบิกสินค้า", DANGER, open_remove).pack(pady=5)
btn("ดู Stock", "#9b59b6", open_table).pack(pady=5)

root.mainloop()

#ควย