# OpticalCapstoneComputerVision2023
Summer 2023 Optical Communications Capstone Computer Vision Repository

## Multicam Object Detection
Runs object detection model on USB cameras at video0 and video1. The model is a custom Robot model for detecting the TurtleBots with the green balls on top of them. 
Also outputs the locations of objects in the frame.
Close the object detection window to quit.

## Multicam Video
Shows live video concatenated horizontally in a new window from two USB cameras on video0 and video1.
Press q to quit.

## 360 Image
With 3 USB Cameras on video0...2, the script will capture a frame on each camera and then display the 360-degree image in a new window. 
Press q to quit.

## Random Selection
1. Fill the text file in the random selection script with newline-separated values of the file names for all images in the dataset.
2. Run the Random Selection script
3. Copy and paste the script outputs into their respective text files within the dataset.

## Transceiver Selection Algorithm
- Let the width of the frame be an arbitrary number represented by w.
- For each camera, the FOV is 120 degrees
- For each transceiver, the FOV is 45 degrees
- Sectioning the frame into x sections where x is the cieled integer value of 2.5 * # of cameras. This allowed the proper amount of trasnceviers to fit into the frame based on the number of cameras utilized.
- Implmenting each section into frame width w and further dividing each section into 2 divisions allows for higher accuracy. Since 2 divisions exist for each section, when dividing by 2, the integer result (if odd) exists in the previous section rather than current. Therefore it is necessary to add one to the divsion such that both divisions now exist in the same section.
- The value returned minus 1 is the best trasnceiver value.
- Update the current_transceiver variable for memory retention and return value to main function. 
