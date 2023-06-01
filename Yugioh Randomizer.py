import sqlite3
import random
import os
from tkinter import Tk, Label, PhotoImage, Frame, Button
from shutil import copyfile
from tkinter.ttk import * # Import all the widgets from tkinter.ttk

import os
import random
import sqlite3
from shutil import copyfile
from tkinter import *

# Get the current directory of the Python script
current_directory = os.path.dirname(os.path.abspath(__file__))

def generate_random_cards():
    global card_name_labels, card_number_labels, image_labels

    # Generate 10 random numbers from 1 to 1138 and sort them in ascending order
    random_numbers = sorted([random.randint(1, 1138) for _ in range(10)])

    # Connect to the SQLite database
    db_path = os.path.join(current_directory, "Yugioh Card List.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Search for the card names and numbers for each random number in the "Number" field
    card_data = []
    for number in random_numbers:
        cursor.execute("SELECT Number, card FROM 'Yugioh Card List' WHERE Number = {}".format(number))
        result = cursor.fetchone()
        if result:
            card_number, card_name = result
            # Remove spaces, disregard anything after the "-", and strip apostrophes, " symbol, period, and "#"
            card_name = card_name.replace(" ", "").split("-")[0].replace("'", "").replace('"', "").replace(".", "").replace("#", "").replace(",", "").replace("&", "")
            card_data.append((card_number, card_name))

    # Close the database connection
    conn.close()

    # Destroy the previous UI labels (if any)
    if card_name_labels:
        for label in card_name_labels:
            label.destroy()
        card_name_labels = []
    if card_number_labels:
        for label in card_number_labels:
            label.destroy()
        card_number_labels = []
    if image_labels:
        for label in image_labels:
            label.destroy()
        image_labels = []

    # Search for matching image files in the folder
    image_folder = os.path.join(current_directory, "YugiohCards")
    matching_images = []
    trunk_folder = os.path.join(current_directory, "Trunk")

    for card_number, card_name in card_data:
        image_filenames = [filename for filename in os.listdir(image_folder) if card_name in filename]
        if image_filenames:
            matching_images.append(os.path.join(image_folder, image_filenames[0]))
            # Save the image to the "Trunk" folder
            if not os.path.exists(trunk_folder):
                os.makedirs(trunk_folder)
            copyfile(os.path.join(image_folder, image_filenames[0]), os.path.join(trunk_folder, image_filenames[0]))
        else:
            matching_images.append(None)  # Use None when image is not found

    # Display the card names, numbers, and images in a 2x5 grid
    for i, (card_number, card_name) in enumerate(card_data):
        # Display the card name
        card_name_label = Label(frame, text=card_name)
        card_name_label.grid(row=i // 5 * 3, column=i % 5 * 2)
        card_name_labels.append(card_name_label)

        # Display the card number
        card_number_label = Label(frame, text=card_number)
        card_number_label.grid(row=i // 5 * 3 + 1, column=i % 5 * 2)
        card_number_labels.append(card_number_label)
        

        # Display the card image if available
        image_path = matching_images[i]
        if image_path is not None:
            card_image = PhotoImage(file=image_path)
            image_label = Label(frame, image=card_image)
            image_label.image = card_image  # Keep a reference to prevent garbage collection
            image_label.grid(row=i // 5 * 3 + 2, column=i % 5 * 2)
            image_labels.append(image_label)


def update_window_size_label():
    window_size_label.config(text="Window size: {}x{}".format(root.winfo_width(), root.winfo_height()))
    window_size_label.after(100, update_window_size_label)

# Create the root window

root = Tk()
root.title("Yugioh Randomizer")
root.geometry("1250x550")
root.configure(background='black')
background_image = PhotoImage(file="background.png")
background_label = Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)






# # Create a label to display the current window size
window_size_label = Label(root, text="Window size: {}x{}".format(root.winfo_width(), root.winfo_height()))
window_size_label.pack(pady=10)

# Create a button to generate random cards
next_pack_button = Button(root, text="Next Pack", command=generate_random_cards, font=("Helvetica", 16))
next_pack_button.pack(pady=10)

# Create a frame to hold the card labels and images
frame = Frame(root)
frame.configure(background='grey')
frame.pack(pady=10)

# Lists to store references to the card labels and image labels
card_name_labels = []
card_number_labels = []
image_labels = []

# Start updating the window size label
update_window_size_label()

root.mainloop()
