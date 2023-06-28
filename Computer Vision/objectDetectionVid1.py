import jetson.inference
import jetson.utils
import time

#net = jetson.inference.detectNet("ssd-mobilenet", threshold=0.5)

net = jetson.inference.detectNet(model="/home/sa/jetson-inference/python/training/detection/ssd/models/RobotModel2/ssd-mobilenet.onnx", labels="/home/sa/jetson-inference/python/training/detection/ssd/models/RobotModel2/labels.txt", input_blob="input_0", output_cvg="scores", output_bbox="boxes", threshold=0.5)

camera = jetson.utils.gstCamera(1280, 720, "/dev/video1")
display = jetson.utils.glDisplay()


while display.IsOpen():
	img, width, height = camera.CaptureRGBA()
	detections = net.Detect(img, width, height)
	display.RenderOnce(img, width, height)
	display.SetTitle("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

