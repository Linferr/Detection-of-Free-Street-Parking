directory = './'

from ultralytics import YOLO

# Load a model
# use pretrained model 
model = YOLO("./yolov8n.pt")  

# train the model
# using 300 epochs, 6 workers
model.train(data=directory+"data-def.yaml", epochs=300, workers=6, device=0)  

metrics = model.val()

# save results in onnx format
model.export(format="onnx")