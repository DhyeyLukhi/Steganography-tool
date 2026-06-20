<p align="center">
  <img src="assets/logo.png">
</p>


# 🔐 Steganography Tool

Hide messages in plain sight.

This Python-based steganography application allows you to embed secret text messages inside images using **Least Significant Bit (LSB) encoding**, making the hidden data virtually invisible to the human eye.

Whether you're exploring cybersecurity concepts, learning information hiding techniques, or experimenting with digital forensics, this project provides both a simple GUI and a command-line interface for encoding and decoding hidden messages.

## ✨ Features

* 🔐 Hide secret messages inside images
* 🕵️ Extract hidden messages from encoded images
* 🖥️ User-friendly Tkinter GUI
* ⌨️ Command Line Interface (CLI)
* 🖼️ Supports PNG and JPEG images
* ⚡ Threaded operations for a smoother user experience
* 📚 Educational implementation of LSB steganography

## 🛠 Technologies

* Python
* Pillow (PIL)
* Tkinter
* Threading

## 🚀 Usage

### GUI Mode

```bash
python Steganography.py --gui
```

### CLI Mode

```bash
python Steganography.py
```

## 🧠 How It Works

The application converts the secret message into binary data and stores it inside the least significant bits of RGB pixel values. Since only the final bit of each color channel is modified, the visual appearance of the image remains almost unchanged while carrying hidden information.
