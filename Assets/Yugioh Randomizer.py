import sqlite3
import random
import os
from tkinter import Tk, Label, PhotoImage, Frame, Button
import shutil
from shutil import copyfile
from tkinter.ttk import * # Import all the widgets from tkinter.ttk
import re
from tkinter import *

# Get the current directory of the Python script
current_directory = os.path.dirname(os.path.abspath(__file__))



outputFile = open("Trunk\Trunk.txt", "a")
trunk_folder = "Trunk\\"

def generate_random_cards():
    #TODO make the frame that holds the cards scale with the window size

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

    # Fill the trunk folder with the images of the cards that were selected
    ###########################################################################
    for card_number, card_name in card_data:
        image_filenames = [filename for filename in os.listdir(image_folder) if card_name in filename]
        if image_filenames:
            matching_images.append(os.path.join(image_folder, image_filenames[0]))
            # Save the image to the "Trunk" folder
            if not os.path.exists(trunk_folder):
                os.makedirs(trunk_folder)
            source = os.path.join(image_folder, image_filenames[0])
            #destination = os.path.join(trunk_folder, image_filenames[0])
            #copy the image to the trunk folder but append the card number to the front of the file name
            destination = ("Trunk\\" + str(card_number) + " " + image_filenames[0])
            copyfile(source, destination)
        else:
            matching_images.append(None)  # Use None when image is not found

    # Display the cards to the Tkinter window
    ###########################################################################
    for i, (card_number, card_name) in enumerate(card_data):
        # Display the card name
        

        # Use regex to see if detect every Capital letter other than the first one and add a space before it
        card_name = re.sub(r"(?!^)([A-Z])", r" \1", card_name)

        # Add a space in front of the words "of", "the", and "and"
        card_name = re.sub(r"(\w)(of|the|and)", r"\1 \2", card_name)

        #write the card name to the output file
        outputFile.write(str(card_number) + " " + card_name + "\n")


        card_name_label = Label(frame, text=card_name, font=("Helvetica", 12))
        card_name_label.configure(background='grey')
        card_name_label.grid(row=i // 5 * 3, column=i % 5 * 2)
        card_name_labels.append(card_name_label)

        # Display the card number
        card_number_label = Label(frame, text=card_number)
        card_number_label.configure(background='grey')
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


def clear_trunk():
    #Clear the trunk folder
    for filename in os.listdir(trunk_folder):
        file_path = os.path.join(trunk_folder, filename)
        if file_path != os.path.join(trunk_folder, "Trunk.txt"):
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print("Failed to delete %s. Reason: %s" % (file_path, e))

    #Now clear the output file
    with open("Trunk\Trunk.txt", "w") as outputFile:
        outputFile.write("")
    

root = Tk()
root.title("Yugioh Randomizer")
root.geometry("1300x650")
root.configure(background='black')
background_image = PhotoImage(file=r"Assets\background.png")
background_label = Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)






 # Create a label to display the current window size
window_size_label = Label(root, text="Window size: {}x{}".format(root.winfo_width(), root.winfo_height()), font=("Helvetica", 10),background='black', foreground='white')
#place in bottom right corner
window_size_label.place(relx=1.0, rely=1.0, anchor=SE)

#Add a welcome message
welcome_message = Label(root, text="Welcome to the Yugioh Randomizer!", font=("Helvetica", 16))
welcome_message.pack(pady=10)


# Create a button to generate random cards
next_pack_button = Button(root, text="Next Pack", command=generate_random_cards, font=("Helvetica", 16))
next_pack_button.pack(pady=10)

# Create a button to clear the trunk folder
clear_trunk_button = Button(root, text="Clear Trunk", command=clear_trunk, font=("Helvetica", 16))
clear_trunk_button.pack(pady=10)


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
