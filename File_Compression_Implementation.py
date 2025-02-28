import heapq
import os
import sys
import tkinter as tk
from tkinter import messagebox
from collections import defaultdict

class HuffmanCoding:
    def __init__(self):
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}
        self.root = None

    class HeapNode:
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None
        
        def __lt__(self, other):
            return self.freq < other.freq

    def frequency_dict(self, text):
        frequency = defaultdict(int)
        for char in text:
            frequency[char] += 1
        return frequency

    def build_heap(self, frequency):
        for key in frequency:
            node = self.HeapNode(key, frequency[key])
            heapq.heappush(self.heap, node)

    def build_tree(self):
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)
            merged = self.HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2
            heapq.heappush(self.heap, merged)
        self.root = self.heap[0] if self.heap else None

    def generate_codes(self, root, current_code=""):
        if root is None:
            return
        if root.char is not None:
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
        self.generate_codes(root.left, current_code + "0")
        self.generate_codes(root.right, current_code + "1")

    def encode_text(self, text):
        encoded_text = "".join(self.codes[char] for char in text)
        extra_padding = 8 - len(encoded_text) % 8
        encoded_text += "0" * extra_padding
        padded_info = "{0:08b}".format(extra_padding)
        return padded_info + encoded_text

    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""
        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                decoded_text += self.reverse_mapping[current_code]
                current_code = ""
        return decoded_text

    def compress(self):
        file_path = r"C:\\Users\\Leverage\\Documents\\saad.txt"
        output_folder = r"D:\\project 288\\outputcompressed"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found.")
            return None
        
        frequency = self.frequency_dict(text)
        self.build_heap(frequency)
        self.build_tree()
        if not self.root:
            messagebox.showerror("Error", "Cannot compress an empty file.")
            return None
        self.generate_codes(self.root)
        encoded_text = self.encode_text(text)
        
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        output_path = os.path.join(output_folder, "compressed.huff")
        
        with open(output_path, 'wb') as output:
            output.write(len(text).to_bytes(4, 'big'))
            output.write(bytes([int(encoded_text[i:i+8], 2) for i in range(0, len(encoded_text), 8)]))
        messagebox.showinfo("Success", f"File compressed successfully: {output_path}")
        return output_path

    def decompress(self):
        compressed_file = r"D:\\project 288\\outputcompressed\\compressed.huff"
        output_folder = r"D:\\project 288\\outputcompressed"
        
        try:
            with open(compressed_file, 'rb') as file:
                original_length = int.from_bytes(file.read(4), 'big')
                bit_string = "".join(f"{byte:08b}" for byte in file.read())
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found.")
            return None
        
        if len(bit_string) < 8:
            messagebox.showerror("Error", "Invalid compressed file.")
            return None
        
        padded_info = bit_string[:8]
        extra_padding = int(padded_info, 2)
        encoded_text = bit_string[8:]
        if extra_padding > len(encoded_text):
            messagebox.showerror("Error", "Corrupt compressed file.")
            return None
        encoded_text = encoded_text[:-extra_padding]
        
        decompressed_text = self.decode_text(encoded_text)[:original_length]
        output_path = os.path.join(output_folder, "decompressed.txt")
        
        with open(output_path, 'w', encoding='utf-8') as output:
            output.write(decompressed_text)
        messagebox.showinfo("Success", f"File decompressed successfully: {output_path}")
        return output_path

if __name__ == "__main__":
    huffman = HuffmanCoding()
    root = tk.Tk()
    root.title("File Compression Tool")
    root.geometry("500x400")
    root.resizable(False, False)
    root.configure(bg="#282c34")

    label = tk.Label(root, text="FILE COMPRESSION TOOL", font=("Arial", 16, "bold"), bg="#282c34", fg="white")
    label.pack(pady=20)

    compress_button = tk.Button(root, text="Compress File", font=("Arial", 14), bg="#61afef", fg="white", width=20, height=2, command=huffman.compress)
    compress_button.pack(pady=10)

    decompress_button = tk.Button(root, text="Decompress File", font=("Arial", 14), bg="#98c379", fg="white", width=20, height=2, command=huffman.decompress)
    decompress_button.pack(pady=10)

    exit_button = tk.Button(root, text="Exit", font=("Arial", 14), bg="#e06c75", fg="white", width=20, height=2, command=root.destroy)
    exit_button.pack(pady=10)

    root.mainloop()
