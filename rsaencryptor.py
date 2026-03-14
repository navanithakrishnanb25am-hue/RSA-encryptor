import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
from math import gcd
import matplotlib.pyplot as plt
import pandas as pd

# ---------- GLOBAL VARIABLES ----------
e = None
d = None
n = None
encrypted_data = []

# ---------- PRIME GENERATOR ----------
def generate_prime():
    primes = [11,13,17,19,23,29,31,37,41,43,47,53,59]
    return random.choice(primes)

# ---------- GENERATE RSA KEYS ----------
def generate_keys():
    global e,d,n

    p = generate_prime()
    q = generate_prime()

    while p == q:
        q = generate_prime()

    n = p*q
    phi = (p-1)*(q-1)

    e = 3
    while gcd(e,phi) != 1:
        e += 2

    d = pow(e,-1,phi)

    key_label.config(
        text=f"Public Key (e,n): ({e},{n})\nPrivate Key (d,n): ({d},{n})"
    )

# ---------- ENCRYPT ----------
def encrypt_message():
    global encrypted_data

    if e is None:
        messagebox.showerror("Error","Generate keys first")
        return

    msg = entry_message.get()

    encrypted_data = [pow(ord(ch),e,n) for ch in msg]

    encrypted_box.delete("1.0",tk.END)
    encrypted_box.insert(tk.END,str(encrypted_data))

# ---------- DECRYPT ----------
def decrypt_message():

    if d is None:
        messagebox.showerror("Error","Generate keys first")
        return

    try:

        data = eval(encrypted_box.get("1.0",tk.END))
        decrypted = ''.join(chr(pow(num,d,n)) for num in data)

        decrypted_box.delete("1.0",tk.END)
        decrypted_box.insert(tk.END,decrypted)

    except:
        messagebox.showerror("Error","Invalid encrypted data")

# ---------- GRAPH ----------
def plot_graph():

    if not encrypted_data:
        messagebox.showerror("Error","Encrypt a message first")
        return

    x = list(range(1,len(encrypted_data)+1))

    plt.figure()
    plt.plot(x, encrypted_data, marker='o')
    plt.title("RSA Encryption Visualization")
    plt.xlabel("Character Position")
    plt.ylabel("Encrypted Value")
    plt.grid()
    plt.show()

# ---------- SAVE CSV ----------
def save_csv():

    if not encrypted_data:
        messagebox.showerror("Error","No data to save")
        return

    file = filedialog.asksaveasfilename(defaultextension=".csv")

    if file:

        df = pd.DataFrame({
            "Index": list(range(1,len(encrypted_data)+1)),
            "Encrypted Value": encrypted_data
        })

        df.to_csv(file,index=False)

# ---------- SAVE TXT ----------
def save_txt():

    if not encrypted_data:
        messagebox.showerror("Error","No data to save")
        return

    file = filedialog.asksaveasfilename(defaultextension=".txt")

    if file:
        with open(file,"w") as f:
            f.write(str(encrypted_data))

# ---------- RSA EXPLANATION ----------
def show_info():

    info = """
RSA Encryption Steps

1. Choose two prime numbers p and q

2. Compute
n = p × q

3. Compute Euler Totient
φ(n) = (p−1)(q−1)

4. Choose e such that
gcd(e,φ(n)) = 1

5. Compute private key d

6. Encryption
c = m^e mod n

7. Decryption
m = c^d mod n
"""

    messagebox.showinfo("RSA Algorithm",info)

# ---------- GUI ----------
root = tk.Tk()
root.title("RSA Cybersecurity Dashboard")
root.geometry("900x650")
root.configure(bg="#1e1e1e")

title = tk.Label(root,text="RSA Encryption Cybersecurity Tool",
                 font=("Arial",22,"bold"),
                 fg="cyan",
                 bg="#1e1e1e")

title.pack(pady=10)

# MESSAGE INPUT
tk.Label(root,text="Enter Message",
         fg="white",
         bg="#1e1e1e").pack()

entry_message = tk.Entry(root,width=60)
entry_message.pack(pady=5)

# BUTTONS
btn_frame = tk.Frame(root,bg="#1e1e1e")
btn_frame.pack(pady=10)

tk.Button(btn_frame,text="Generate Keys",
          command=generate_keys,
          bg="#00adb5").grid(row=0,column=0,padx=10)

tk.Button(btn_frame,text="Encrypt",
          command=encrypt_message,
          bg="#00adb5").grid(row=0,column=1,padx=10)

tk.Button(btn_frame,text="Decrypt",
          command=decrypt_message,
          bg="#00adb5").grid(row=0,column=2,padx=10)

tk.Button(btn_frame,text="Algorithm Info",
          command=show_info,
          bg="#00adb5").grid(row=0,column=3,padx=10)

# KEY DISPLAY
key_label = tk.Label(root,text="",
                     fg="yellow",
                     bg="#1e1e1e",
                     font=("Arial",10))

key_label.pack()

# ENCRYPTED BOX
tk.Label(root,text="Encrypted Message",
         fg="white",
         bg="#1e1e1e").pack()

encrypted_box = tk.Text(root,height=5,width=70)
encrypted_box.pack()

# DECRYPTED BOX
tk.Label(root,text="Decrypted Message",
         fg="white",
         bg="#1e1e1e").pack()

decrypted_box = tk.Text(root,height=5,width=70)
decrypted_box.pack()

# EXTRA FEATURES
extra_frame = tk.Frame(root,bg="#1e1e1e")
extra_frame.pack(pady=10)

tk.Button(extra_frame,text="Plot Encryption Graph",
          command=plot_graph,
          bg="#393e46",
          fg="white").grid(row=0,column=0,padx=10)

tk.Button(extra_frame,text="Save CSV",
          command=save_csv,
          bg="#393e46",
          fg="white").grid(row=0,column=1,padx=10)

tk.Button(extra_frame,text="Save TXT",
          command=save_txt,
          bg="#393e46",
          fg="white").grid(row=0,column=2,padx=10)

root.mainloop()