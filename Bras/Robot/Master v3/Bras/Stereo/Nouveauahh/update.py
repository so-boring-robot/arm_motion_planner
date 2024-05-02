import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, Label, Button, Scale, Checkbutton, IntVar

# Function to update the disparity map when parameters change
def update_disparity_map():
    # Check if the blur filter is enabled
    if blur_enabled.get() == 1:
        # Get the blur level from the scale
        blur_level = blur_scale.get()
        # Apply Gaussian blur with the chosen kernel size
        blur_kernel_size = (blur_level, blur_level)
        left_image_blurred = cv2.GaussianBlur(left_image, blur_kernel_size, 0)
        right_image_blurred = cv2.GaussianBlur(right_image, blur_kernel_size, 0)
    else:
        left_image_blurred = left_image
        right_image_blurred = right_image

    num_disparities = num_disparities_scale.get()
    block_size = block_size_scale.get()

    # Ensure num_disparities is positive and divisible by 16
    num_disparities = max(16, num_disparities)
    num_disparities = num_disparities + (16 - (num_disparities % 16)) if num_disparities % 16 != 0 else num_disparities

    stereo = cv2.StereoBM_create(numDisparities=num_disparities, blockSize=block_size)
    disparity_map = stereo.compute(left_image_blurred, right_image_blurred)

    min_disparity = disparity_map.min()
    max_disparity = disparity_map.max()
    normalized_disparity = (disparity_map - min_disparity) / (max_disparity - min_disparity)
    normalized_disparity = (normalized_disparity * 255).astype(np.uint8)

    cv2.imshow('Disparity Map', normalized_disparity)

# Function to load stereo images and resize them to 500x500
def load_images():
    global left_image, right_image
    left_image_path = filedialog.askopenfilename(title='Select Left Image', filetypes=[('Image files', '*.png *.jpg *.jpeg *.bmp')])
    right_image_path = filedialog.askopenfilename(title='Select Right Image', filetypes=[('Image files', '*.png *.jpg *.jpeg *.bmp')])

    if left_image_path and right_image_path:
        left_image = cv2.imread(left_image_path, cv2.IMREAD_GRAYSCALE)
        right_image = cv2.imread(right_image_path, cv2.IMREAD_GRAYSCALE)

        # Resize images to 500x500
        left_image = cv2.resize(left_image, (500, 500))
        right_image = cv2.resize(right_image, (500, 500))

        update_disparity_map()

# Create the main application window
app = tk.Tk()
app.title('StereoBM Parameter Tuning')

# Load images button
load_button = Button(app, text='Load Stereo Images', command=load_images)
load_button.pack()

# Parameter sliders
num_disparities_label = Label(app, text='Num Disparities')
num_disparities_label.pack()
# Ensure num_disparities_scale starts with a value that is positive and divisible by 16
num_disparities_scale = Scale(app, from_=16, to=256, orient='horizontal', length=300)
num_disparities_scale.set(64)  # Set an appropriate positive value divisible by 16
num_disparities_scale.pack()

block_size_label = Label(app, text='Block Size (Odd)')
block_size_label.pack()

# Create a custom list of allowed block sizes (odd values only)
allowed_block_sizes = [i for i in range(5, 26) if i % 2 != 0]

block_size_scale = Scale(app, from_=allowed_block_sizes[0], to=allowed_block_sizes[-1], orient='horizontal', length=300, tickinterval=2)
block_size_scale.set(15)  # Set an initial odd value
block_size_scale.pack()

# Add a Checkbutton for enabling/disabling blur
blur_enabled = IntVar()
blur_checkbutton = Checkbutton(app, text='Enable Blur', variable=blur_enabled)
blur_checkbutton.pack()

# Add a Scale for choosing the blur level
blur_scale_label = Label(app, text='Blur Level')
blur_scale_label.pack()
blur_scale = Scale(app, from_=1, to=15, orient='horizontal', length=300, label='Blur Amount')
blur_scale.set(5)  # Set an initial blur level
blur_scale.pack()

# Update disparity map button
update_button = Button(app, text='Update Disparity Map', command=update_disparity_map)
update_button.pack()

# Run the Tkinter main loop
app.mainloop()
