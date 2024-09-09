# CG78: Precise Detection of Free Street Parking using AI and Video Processing
UBC Capstone Group CG-78 – CPEN 491




## <a name="_toc139170921"></a>Table of Contents  

[Context](#_toc856990244)

[Overview](#_toc508109995)

[Quick Start Manual](#_toc1854123075)

[Component Description](#_toc1259664631)

[Machine learning component](#_toc1854305356)

[Cloud component](#_toc659762245)

[Edge component](#_toc411784410)

[Backend component](#_toc1113651561)

[Front-end component](#_toc1113651562)




## <a name="_toc856990244"></a>Context
As urban environments worldwide grapple with escalating traffic congestion, the challenge of parking has emerged as a central concern. Traditional parking management systems, encompassing physical sensors or fixed surveillance cameras, have been demonstrated to have limitations in addressing the dynamic nature of street parking. These systems not only offer limited coverage but also come with high deployment costs and lack the flexibility to adapt to the ever-evolving urban landscape.  

Addressing this, the UBC Digital Multimedia Lab, under the leadership of Professor Panos Nasiopoulos, stands at the forefront of deep learning model research and development. The lab's commitment to technological advancement extends beyond mere research, actively applying it to real-world scenarios by developing an application that harnesses artificial intelligence to detect and pinpoint free street parking spots using videos from built-in vehicle cameras. Furthermore, they have ventured into diverse parking detection techniques ranging from aerial views to indoor parking environments. This latest project, focusing on the dynamic environment of street parking, not only sets a new benchmark for the lab but also collaborates with entities like TELUS and potential car manufacturers. The aim is to lay a solid foundation for future smart city projects, redefining urban transportation, and envisioning a cityscape equipped with intelligent infrastructure.


## <a name="_toc508109995"></a>Overview
This documentation provides an essential guide to the "Precise Detection of Free Street Parking using AI and Video Processing" system. It covers the machine learning, cloud, edge, and front-end components, along with their functionalities and interactions. The system is designed to identify 6-meter-long parking spaces using a YOLOv8 model, store and process data using MongoDB Atlas, communicate over long distances using LoRaWAN, and interface with users through a React Native application.



## <a name="_toc1854123075"></a>Quick Start Manual

**Prerequisites**

Software:

1. Python 3.8 or higher
1. Node.js 12.x or higher
1. MongoDB Atlas account
1. An environment to deploy and test YOLOv8 models (GPU recommended)

Hardware:
1. Jetson Nano with a monitor, a keyboard, and a mouse
2. LoRa SX1262 


**GitHub Repository**

Please visit the following GitHub repository to access the codebase and documentation:

<https://github.com/yf-ivanguo/CG78/tree/main>

## <a name="_toc1259664631"></a>Component Description
Follow the individual instructions for each component provided in the component descriptions to start each part of the system.

### <a name="_toc1854305356"></a>Machine learning component
This component uses the YOLOv8 model to detect free street parking spaces from video data captured via vehicle-mounted cameras. 

#### **Environment Setup:**

- Python 3.8 or higher  
- Libraries (to install with `pip` or other equivalent):  <br>
`ultralytics` 
`sklearn` (optional – for if you would like to retrain on different dataset) 
- GPU with CUDA for model training and inference will increase training/interference speed 

**Details:** 

Training the ML Model  <br> <br>
Our data split (into training and test dataset with images and labels) can be accessed via the Microsoft Sharepoint link provided by email. You can find the complete dataset used for training/testing in the `/data` directory. We used data_split.py (described below) to obtain this split of the data. 

1. Use data_split.py to split the data into train and test datasets. This script uses `sklearn` to split the data. We used an 85% train, 15% test split. To use this, you need to set: 
- `data_path` 
- `image_rel_path` 
- `label_rel_path` <br>
To the path to your directory for the dataset. The images and labels should be in the `data_path` directory as separate folders, and you can set the names of those to image and label relative path.  
The script will output the data to `data/train` and `data/test` directories, which is the expected format by YOLO (read more from Ultralytics documentation https://docs.ultralytics.com/datasets/detect/).

2. Assuming the data_split.py script was used, the `data-def.yaml` describes the directory structure of the data as an input to the YOLO model. It is currently configured assuming the data directory is in the same directory as the ML training script. If a different split was used, you can change the input of the `YOLO()` constructor function to the `yaml` file corresponding to the format that you used. `model.py` is the script used to train the model. We used 300 epochs and 6 workers, but you can change those as necessary. This script then exports the model in `onnx` format. 

<br>The model weights we obtained from training are in the `best.pt` file.<br><br>

Validating the ML model  <br>

1. We used `calculate_performance_metrics.ipynb` to evaluate model performance. Using Ultralytics’ `val()` method, we can obtain the mAP, precision, and recall scores using the test dataset. You can see the mAP, precision, and recall scores obtained as outputs in this notebook file, and it is also summarized in the table below under "Performance Metrics". We also test the model on some of the example images from the test dataset and visualize the results. You can change the directory to another .pt file, or by default, we use the .pt file we provided in the repository.  
2. We used `run_on_video.ipynb` to test the script on some videos that we filmed ourselves. You will need to change the directory to the path of the video you want to test. You can change the directory to another .pt file, or by default, we use the .pt file we provided in the repository.  


#### **Performance Metrics:**

Given camera data from passing vehicles, the machine learning (ML) model should be able to detect individual available parking spots with a performance score that achieves or exceeds the current implementation’s performance. The performance evaluated by using the following metrics:  

|Metric |Performance Target |Achieved Performance |
| :- | :- | :- |
|mAP@0.5|≥ 0.90|0.98|
|Precision|≥ 0.85|0.91|
|Recall|≥ 0.82|0.95|
|F1-Score|≥ 0.83|0.93|
##

### <a name="_toc659762245"></a>Cloud component
Handles data storage and processing in MongoDB Atlas and manages communication over frontend UI and edge devices.

#### **Environment Setup:**

- Python 3.8 and Node.js 12.x
- MongoDB Atlas account
- Node.js for server-side functions

#### **MongoDB Atlas API Setup:**

1. Create a MongoDB Atlas Account:
   1. If you don't already have a MongoDB Atlas account, visit MongoDB Atlas and sign up.
   1. Follow the prompts to set up a new organization and project and deploy your first cluster if you haven't already.
1. Access Settings (link: [Create an API Key - MongoDB Cloud Manager](https://www.mongodb.com/docs/cloud-manager/reference/api/api-keys/org/create-one-org-api-key/)):
   1. Once logged into MongoDB Atlas, click on the Project Settings.
   1. Select the Access Manager from the drop-down menu. Within the Access Manager, select the API Keys tab.
   1. Click the Create API Key button.
   1. Add IP Whitelist: Add IP addresses that will use this API key or configure it to allow access from anywhere (not recommended for production environments).
1. Setting Up the MongoDB Data API:
   1. Under the Data API section, click Enable Data API.
   1. Configure the Data API
   1. Generate Data API Key

After generating the Data API key, you can start using it to make requests to your MongoDB clusters. MongoDB provides an API endpoint URL for your project (link: [Data API Examples — Atlas App Services (mongodb.com)](https://www.mongodb.com/docs/atlas/app-services/data-api/examples/)), which you will use to send requests.

#### **Details:** 

Here is a brief description of each Python script in the cloud component of the system.

1. insertoneData.py:
   1. Description: This script sends a POST request to the MongoDB Atlas API to insert a single document into a specified collection. It is used for adding data about available parking spots, including location, device identifier, timestamp, and validity status.
   1. Dependencies: 
      1. Python 3.8+
      1. requests library
   1. Environment Setup: ```python -m pip install requests```
1. invalidoneData.py
   1. Description: This script uses the MongoDB Atlas API to potentially replace a document based on the 'edgedevice' identifier and the proximity of the location. If a document with the same 'edgedevice' identifier exists within a 2-meter radius of a new specified location, it is replaced; otherwise, the document is inserted.
   1. Dependencies: 
      1. Python 3.8+
      1. requests library
   1. Environment Setup: ```python -m pip install requests```
1. updateAllData.py
   1. Description: This script updates all documents in a MongoDB collection, setting the 'isValid' field to 0 for documents where this field is not already 1 or where the timestamp is more than one day old. It also includes functionality to delete all documents where 'isValid' is set to 0.
   1. Dependencies: 
      1. Python 3.8+
      1. requests library
   1. Environment Setup: ```python -m pip install requests```
1. runUpdate.py
   1. Description: This script periodically executes updateAllData.py every two minutes. It uses subprocesses to handle the execution and schedules these executions using a simple time delay loop.
   1. Dependencies: 
      1. Python 3.8+
      1. requests library
   1. Environment Setup: ```python -m pip install requests```

Each script interacts with MongoDB Atlas via REST API, requiring a valid API key and specific configuration settings such as the collection name, database name, and data source. These scripts handle different aspects of data management for parking availability, ensuring that the information is up-to-date and accurately reflects the current parking situation as captured and reported by edge devices.



#### **Performance Check:**

##### **Checking Communication**

Ensure your application can successfully communicate with MongoDB Atlas by making test API calls. Use tools like curl or Postman, or write simple scripts in Python or another programming language to verify that your API key and endpoints are functioning as expected. If the response is successful, it indicates that the communication link is healthy. Check for any error messages or codes to troubleshoot issues related to permissions, network settings, or API key validity.

Example code:
``` bash
curl -X POST -H "Content-Type: application/json" -H "api-key: your-api-key" -d '{"collection":"your-collection","database":"your-database","dataSource":"your-cluster"}' "https://data.mongodb-api.com/app/data-xxxxx/endpoint/data/beta/action/findOne"
```

##### **Using MongoDB Compass to Check Database**

MongoDB Compass (link: [MongoDB Compass | MongoDB](https://www.mongodb.com/products/tools/compass)) is a graphical client that allows you to manage and inspect your MongoDB databases more intuitively.


### <a name="_toc411784410"></a>Edge component 

#### **Decision algorithm**
   All the files are implemented in python 3.11.7. 
1. 1. insertoneData.py:
   1. Description: Define two cache classes. The first one is called timeCache. This cache is applied for filtering out redundant locations. The second cache will store valid locations. Specifically, when the server receives one location, it will store it in the first cache for m seconds. All the subsequent locations will be calculated the distance from the first location. If the distance is less than 6 meters, the new location will be filtered out. After m seconds, the first location will be send to the second cache. 
1. ServerPredefined.py 
   1. Description: Set up predefined functions and variables for server. The predefined functions include distance calculation between two locations and request creating functions. 
   1. Dependencies: 
      1. requests library
   1. Environment Setup: ```pip install requests```
1. SenderPredefined.py 
   1. Description: Mainly about predicting the videos using YOLOv8. This function will also display a window for the processed video stream. 
   1. Dependencies: 
      1. ultralytics library for using YOLO 
      1. OpenCV library 
   1. Environment Setup:
      1. ```pip install opencv-python```
      1. ```pip install ultralytics```
1. CompleteServer.py
   1. Description: Listening to a port to receive serial data and parses the location data from it. Specifically, it uses a string buffer to concatenate all incoming data. Simultaneously, the string buffer is split into individual locations. 
   1. Dependencies: 
      1. pyserial package
   1. Environment Setup: ```pip install pyserial```
1. CompleteSender.py
   1. Description: higher level of SenderPredefined.py. 
   1. Dependencies: 
      1. PyTorch library (optional) 
      1. pyserial library 
   1. Environment Setup:
      1. For CUDA 12.1, use: ```conda install pytorch==2.2.1 torchvision==0.17.1 torchaudio==2.2.1 pytorch-cuda=12.1 -c pytorch -c nvidia```
      1. pip install pyserial 

#### **LoRa**
LoRaReceiver.ino and LoRaSender.ino: Please refer to [HelTecAutomation/CubeCell-Arduino: Heltec CubeCell Series (based on ASR6501, ASR6502 chip) Arduino support. (github.com) ](https://github.com/HelTecAutomation/CubeCell-Arduino?tab=readme-ov-file)

Serial connection drive: Please refer to [Establish Serial Connection — main latest documentation (heltec.org) ](https://docs.heltec.org/general/establish_serial_connection.html)

1. TestSender.py
   1. Description: Testing LoRa range.
   1. Dependencies: 
      1. pyserial package
   1. Environment Setup: ```pip install pyserial```

1. TestReceiver.py
   1. Description: Testing LoRa range.
   1. Dependencies: 
      1. pyserial package
   1. Environment Setup: ```pip install pyserial```

#### **Reconstruction**
An uninitialized Jetson Nano requires a monitor, a keyboard, and a mouse for setup. After this, you can configure the device to automatically connect to WiFi. Consequently, you can use remote SSH, such as PuTTY, to control it. To run the decision algorithm, simply upload CompleteServer.py and ServerPredefined.py to the Jetson Nano. 

To develop the LoRa SX1262, please refer to the first link I provided in the LoRa section. Since the LoRa SX1262 is an embedded board, you can upload the code via the Arduino IDE. The boards we are using are HTCC-AB01. These boards can be connected with a data transfer USB to a Type-C cable. To set up the driver, please follow the second link. After downloading the driver files, you can set up the driver by searching in the computer's Device Manager. You don’t need to set up the driver on the Jetson Nano. 

Currently, the LoRa transmission distance is about 1 km. This can be improved by increasing the LORA_SPREADING_FACTOR. Please note that increasing this factor will reduce the transmission throughput. Also, the LORA_SPREADING_FACTOR can only be set from 7 to 12. To significantly increase the transmission distance, we still need better equipment, such as a stronger antenna. The transmission range can be tested using the files in the Test directory. One computer should run TestSender.py while another runs TestReceiver.py. Then, you can determine the distance at which the receiver no longer receives the data sent from the sender.

### <a name="_toc1113651561"></a>Backend component

The main backend component of the server is located at /backend/server.js 

To prepare the backend server, install node: [https://nodejs.org/en/download](https://nodejs.org/en/download) then install all dependencies: ```npm install```

To run the backend server, run: ```node server.js``` 

#### **Description** 

This server application loads in the necessary modules to start a server. It connects to the MongoDB database and has a single HTTP POST request defined. The request is located at the /parkingData endpoint. The request takes in 3 parameters: the user latitude, user longitude, and the range (metres). It then awaits the data to the database, which returns to the server application with a list of parking space coordinates that are within the range of the user. The server then formats the parking space coordinates accordingly and sends it back to the caller of the request. 

### <a name="_toc1113651562"></a>Front-end component 
   
The frontend components of the application are located at /frontend 

To prepare the frontend, install node: [https://nodejs.org/en/download](https://nodejs.org/en/download) then install all dependencies: ```npm install``` 

To run the frontend server, run: ```npx expo start```

#### **Description**

The frontend component begins in /frontend/App.js, which uses a NavigationContainer to notify state changes and move around to other screens. The Navigator that it uses is defined as MyStack, which currently moves the application to the title screen on startup.  

#### **Screens**

The screens that a user can view are located at /frontend/src/screens - currently there are only two screens: the title screen and the map screen, which is navigated to after the start button is pressed. The title screen shows the logo and navigate to the map screen. The map screen consists of several important components: 

1. addMarkers(coordinates) 
    1. This takes an array of coordinates and adds a parking marker to the map. This sets a ParkingMarker component.  
1. fetchData() 
    1. This function calls the API service to receive parking data, then calls addMarkers to add the coordinates as markers on the map. 
1. fetchLocation() 
    1. This function retrieves the current location of the user which is used to display the user marker on the map as well as used in retrieval of parking coordinates within a certain range of the user. 
1. Range buttons 
    1. There are several range buttons that are available to the user to press, respectively representing 500 m, 1 km, and 3 km. These values are then given to fetchData() to be processed by the API service and the database. 

#### **Components**

There are two components located at /frontend/src/components: MapComponent and ParkingMarker. 

1. MapComponent 
    1. This component is used by the map screen to set the initial map region that the user can see, which is centered on their location. This component also provides the infrastructure to    add markers to the map to represent parking spots and some of the styling utilized by the map. 
1. ParkingMarker 
    1. This is mostly a stylistic component that utilizes a png file to designate parking spots and sets the height and width of the marker.  

#### **Services**

There is one main service, located at /frontend/src/services, the ApiService. This service’s primary role is to communicate with the backend by sending a POST request to hostURL/parkingData. The ApiService sends the current location and the range and awaits an array of coordinates that it will give to the map screen. The host/base URL should be specified above in this file, or in another file for modularity.  




