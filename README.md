# Optical Communications Capstone
YCP Optical Communications Capstone - Class of 2024 <br><br>
Summer 2023 and Spring 2024 Computer Vision Aided Optical Communications Repository <br><br>
Based on [implementation](https://github.com/rblack5/OpticalCommunications-2023) developed by YCP Optical Communications Capstone - Class of 2023

# Project Overview
The purpose of this project is to improve upon the optical wireless
communication (OWC) system design by developing a computer vision system to aid in the discovery and maintenance of connections. The system establishes dynamic OWC links and maintains them among mobile
robot devices. Communication between devices is completed optically using infrared light from transceivers which require a direct Line of Sight (LOS) with other devices. Optical communication can allow for data to be communicated at a much faster rate than other forms of communication such as radio frequency which are more commonly used. Additionally, signals sent over optical are directionally targeted, which limits the ability for attackers to sniff data or jam communications. To establish a communication between two mobile robot devices, a discovery method identifies a robot visually and attempts to make a communication socket. Once connected, a maintenance algorithm ensures reliable connection for the duration of the communication. These algorithms are capable of enhancing security of the discovery process and reliability of the
maintenance algorithm.<br>

The specific implementation employs TCP to establish reliable connections between robots. TCP ensures that all data is transmitted successfully without losing any packets. It also uses ICMP pings to assist in associating a visual robot with an IP address. The Python implementation does not limit the number of robots that can be connected at any given time. Additionally, multi-hop/message-passing is under development, which would allow robots to communicate with other robots in the network that they cannot physically see.

# Required Hardware
## Common Hardware
- 1x Turtlebot
- 8x IRdA 3 Click
- 8x USB to Serial Converters (Unique Serial Numbers)
- 1x NeoPixel
- 2-3x 4-Port USB Hub
- 1x 12V Battery Pack (or 1x 5V Battery Pack for NVIDIA Jetson Nano and Legacy)
- 1x PCB
- 1x 3D Printed Housing Set

## CV Enabled
- NVIDIA Jetson Orin Nano Dev Kit (Recommended) or NVIDIA Jetson Nano Dev
- 3x 120HFOV Cameras (Compatibility is Different on Each SBC)

## Legacy
- Raspberry Pi 4B - 4GB

# Setup Guide
- [Our Nano/Orin Setup Instructions](https://docs.google.com/document/d/15JkEmvYgIEC3yA9PwDp5FkcV1Wi_gssA3jcVqShUcK4/edit?usp=sharing)

## SBC Setup
### Jetson Orin Nano (Recommended)
- [NVIDIA Jetson Orin Nano SDK Manager Tutorial - Jetson Hacks](https://www.youtube.com/watch?v=Ucg5Zqm9ZMk)
- [NVIDIA Jetson Orin Nano Setup Instructions](https://developer.nvidia.com/embedded/learn/get-started-jetson-orin-nano-devkit)

### Jetson Nano
- [NVIDIA Jetson Nano Setup Instructions](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#setup)

## Dependencies
- [Pip Packages](https://docs.google.com/document/d/19U83-BOBsWA5D3D2DjtCTBzkktnS8ETZsRZ8RgFJoPo/edit?usp=sharing)
- The project is also dependent upon having trained an ONXX model on images of your robot. This model must be trained using the same configuration variables as the script in the Jetson-Inference library uses. See the model training section for more information.

## Config
The config file requires a variety of information:
- Robot Name: Nano, Orin, or Pi - Used to determine robot's IP
- Serial Numbers: A list of the serial numbers for each of the 8 USB to Serial Converters
- numCameras: The number of cameras to be configured
- camConfig: List which shows the type of camera configuration to be performed on each camera. Each element is num or str
- camera: Number indicating /dev/video# or the camera setup string

## Model Training
- [Model Training Guide](https://docs.google.com/document/d/1wqQ4I6UneBfly3QXc5Vk7nawu_xqPGS6TMjoguLXod0/edit?usp=sharing)

# Scripts

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

# Explanation of Algorithms
## Lucid Chart
The [chart](https://lucid.app/lucidchart/68bc1108-b73c-4437-a24c-5dfeb9024ba8/edit?viewport_loc=-1045%2C-367%2C3211%2C1505%2CP0rfHEjzH4FS&invitationId=inv_ac62b577-ed63-40af-b33c-7325d81c58c3) shows an overview of a generic form of the algorithms and classes used in the project.

## Transceiver Selection Algorithm
- Let the width of the frame be an arbitrary number represented by w.
- For each camera, the FOV is 120 degrees
- For each transceiver, the FOV is 45 degrees
- Sectioning the frame into x sections where x is the cieled integer value of 2.5 * # of cameras. This allowed the proper amount of trasnceviers to fit into the frame based on the number of cameras utilized.
- Implmenting each section into frame width w and further dividing each section into 2 divisions allows for higher accuracy. Since 2 divisions exist for each section, when dividing by 2, the integer result (if odd) exists in the previous section rather than current. Therefore it is necessary to add one to the divsion such that both divisions now exist in the same section.
- The value returned minus 1 is the best trasnceiver value.
- Update the current_transceiver variable for memory retention and return value to main function. 
