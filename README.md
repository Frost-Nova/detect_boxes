# detect_boxes

This program is for box detection in a .jpg format document.

I created a find_box class, which is instantiated with a filename and 3 other adjustable parameters.
The first parameter is binary_threshold, which is used when determine the threshold of converting a grayscale image to a binary image.
The second parameter is strcuture_size, which is used to generate kernels for erosion and dilation. This parameter can adjust the smallest line stucture to be found.
The last parameter is min_area, which is used to filter out small boxes like a '0' or checkbox.

 The program will read from a folder and output jpg and json files to a designated folder.
