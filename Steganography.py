from PIL import Image
import getpass
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from threading import Thread
import time
import os

selected_image_path = None

def pixel_to_binary():
    image = Image.open(selected_image_path)
    image.load()
    newImage = Image.new(image.mode, image.size)
    newImage.load()
    width, height = image.size

    with open(".binaryMessage.txt", 'r') as file:
        data = str(file.read().strip())
    count = 0
    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            r_binary = str(format(r, '08b'))
            g_binary = str(format(g, '08b'))
            b_binary = str(format(b, '08b'))
            if count < len(data):
                r_binary = r_binary[:7] + data[count]
                count += 1
            if count < len(data):
                g_binary = g_binary[:7] + data[count]
                count += 1
            if count < len(data):
                b_binary = b_binary[:7] + data[count]
                count += 1
            newImage.putpixel((x, y), (int(r_binary, 2), int(g_binary, 2), int(b_binary, 2)))
    newImage.save("new_image.png")

def encode():
    start_sequence = "(!%&#"
    end_sequence = "(*&()"
    # Use GUI input if available
    if gui_mode:
        secret_Message = simpledialog.askstring("Input", "Enter your secret message:")
        if not secret_Message:
            return
    else:
        secret_Message = str(getpass.getpass("Message: "))
    secret_Message = start_sequence + f"  {secret_Message}  " + end_sequence
    with open(".binaryMessage.txt", 'w') as file:
        file.write("")
    for length in secret_Message:
        ascii_value = ord(length)
        with open(".binaryMessage.txt", 'a') as file:
            file.write(format(ascii_value, '08b'))
    pixel_to_binary()

def decode():
    start_sequence = "(!%&#"
    end_sequence = "(*&()"
    startseq_bin = ''.join(format(ord(c), '08b') for c in start_sequence)
    endseq_bin = ''.join(format(ord(c), '08b') for c in end_sequence)
    image = Image.open("new_image.png")
    width, height = image.size
    bits = []
    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            bits.append(str((r & 1)))
            bits.append(str((g & 1)))
            bits.append(str((b & 1)))
    binary_message = ''.join(bits)
    start_idx = binary_message.find(startseq_bin)
    end_idx = binary_message.find(endseq_bin, start_idx + len(startseq_bin))
    if start_idx == -1 or end_idx == -1:
        if gui_mode:
            messagebox.showinfo("Result", "No hidden message found.")
        else:
            print("No hidden message found.")
        return
    secret_bin = binary_message[start_idx + len(startseq_bin):end_idx]
    decoded_message = ""
    for i in range(0, len(secret_bin), 8):
        byte = secret_bin[i:i+8]
        if len(byte) == 8:
            decoded_message += chr(int(byte, 2))
    if gui_mode:
        messagebox.showinfo("Secret Message", decoded_message)
    else:
        print("Secret Message:", decoded_message)

# --- GUI Section ---
def pick_image():
    global selected_image_path
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if path:
        selected_image_path = path
        image_label.config(text=os.path.basename(path))

def run_encode():
    if not selected_image_path:
        messagebox.showwarning("Warning", "Please select an image first.")
        return
    loading_screen("Encoding...")
    Thread(target=encode_and_notify).start()

def encode_and_notify():
    encode()
    loading_done()
    messagebox.showinfo("Done", "Message encoded and saved as new_image.png.")

def run_decode():
    if not os.path.exists("new_image.png"):
        messagebox.showwarning("Warning", "No encoded image found (new_image.png).")
        return
    loading_screen("Decoding...")
    Thread(target=decode_and_notify).start()

def decode_and_notify():
    decode()
    loading_done()

def loading_screen(text):
    loading_label.config(text=text)
    loading_label.place(relx=0.5, rely=0.7, anchor="center")
    animate_loading()

def loading_done():
    loading_label.place_forget()

def animate_loading():
    def animate():
        for i in range(10):
            loading_label.config(text=loading_label.cget("text") + ".")
            time.sleep(0.2)
        loading_label.config(text=loading_label.cget("text").split(".")[0])
    Thread(target=animate).start()

def start_gui():
    root.title("Steganography Tool")
    root.geometry("400x300")
    pick_btn.pack(pady=10)
    image_label.pack()
    encode_btn.pack(pady=10)
    decode_btn.pack(pady=10)
    loading_label.pack_forget()
    root.mainloop()

# --- Main ---
gui_mode = False
try:
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        gui_mode = True
except:
    pass

if gui_mode:
    root = tk.Tk()
    pick_btn = tk.Button(root, text="Pick Image", command=pick_image)
    image_label = tk.Label(root, text="No image selected")
    encode_btn = tk.Button(root, text="Encode Message", command=run_encode)
    decode_btn = tk.Button(root, text="Decode Message", command=run_decode)
    loading_label = tk.Label(root, text="", font=("Arial", 12))
    start_gui()
else:
    print("Steganography Tool:")
    print("1. Encode")
    print("2. Decode")
    choice = int(input("Answer: "))
    if choice == 1:
        selected_image_path = "/home/dhyey/Codes/.PROjects Level/Steganography/image.jpeg"
        encode()
    elif choice == 2:
        decode()
    else:
        print("Invalid choice")