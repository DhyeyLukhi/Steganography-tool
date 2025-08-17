from PIL import Image
import getpass


def pixel_to_binary():
    image = Image.open("/home/dhyey/Codes/.PROjects Level/Steganography/image.jpeg")
    image.load()
    newImage = Image.new(image.mode, image.size)
    newImage.load()
    print("Converting pixels into binary")
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

            # Always put a pixel, even if no bits are left to hide
            newImage.putpixel((x, y), (int(r_binary, 2), int(g_binary, 2), int(b_binary, 2)))


    newImage.save("new_image.png")



def encode():
    start_sequence = "(!%&#"
    end_sequence = "(*&()"
    secret_Message = str(getpass.getpass("Message: "))
    secret_Message = start_sequence + f"  {secret_Message}  " + end_sequence


    # Now the secret message will be converted into binary and stored into the file
    print("Converting message into binary")
    with open(".binaryMessage.txt", 'w') as file:
        file.write("")
    for length in secret_Message:
        ascii_value = ord(length)
        
        with open(".binaryMessage.txt", 'a') as file:
            file.write(format(ascii_value, '08b'))
    print("Message Converted successfully")
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
            """
            r & 1, g & 1, b & 1 will get the last bit of red, green, and blue channels by doing AND operation with the RGB value
            
            """

    # Join bits into a string
    binary_message = ''.join(bits)

    # Find the start and end sequence in the binary message
    start_idx = binary_message.find(startseq_bin)
    end_idx = binary_message.find(endseq_bin, start_idx + len(startseq_bin))

    if start_idx == -1 or end_idx == -1:
        print("No hidden message found.")
        return

    # Extract the message between start and end sequence
    secret_bin = binary_message[start_idx + len(startseq_bin):end_idx]
    decoded_message = ""
    for i in range(0, len(secret_bin), 8):
        byte = secret_bin[i:i+8]
        if len(byte) == 8:
            decoded_message += chr(int(byte, 2))
    print("Secret Message:", decoded_message)

if __name__ == "__main__":
    print("Steganography Tool:")
    print("1. Encode")
    print("2. Decode")
    choice = int(input("Answer: "))
    if choice == 1:
        encode()
    elif choice == 2:
        decode()
    else:
        print("Invalid choice")