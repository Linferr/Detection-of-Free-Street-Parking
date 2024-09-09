import cv2
from ultralytics import YOLO

def predict(location, ser, model_path, window_size, writing_lock, video_path=None, out_path=None):
    # load model
    model = YOLO(model_path)

    # Predicting an unprocessed video
    if video_path is not None:
        cap = cv2.VideoCapture(video_path)
    # Predicting the video stream from camera
    else:
        cap = cv2.VideoCapture(0)


    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    
    if video_path is not None and out_path is not None:
        out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'avc1'), 15, (frame_width, frame_height))


    cv2.namedWindow("YOLOv8 predictions", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("YOLOv8 predictions", window_size[0], window_size[1])

    ref_location_frequency = 0

    while cap.isOpened():
        
        success, frame = cap.read()
        
        # Send the reference location every 10 frames.
        if ref_location_frequency % 10 == 0:
            ser.write('[11,12,0]'.encode('utf-8'))
            ref_location_frequency = 0
        
        ref_location_frequency += 1
        
        if success:
            # Prediction
            results = model(frame)


            for result in results:
                box = result.boxes.data
                for values in box:
                    class_id = values[-1].item()
                
                    if int(class_id) == 0:
                        print("Parking Space")
                        
                        

                        if ser.isOpen():
                            print("socket is open")
                            
                            try:
                                data = location
                                
                                writing_lock.acquire()
                                ser.write(data.encode('utf-8'))
                                writing_lock.release()
                                
                            except KeyboardInterrupt:
                                print("Program terminate")
                                                                    
        
            # Visualize results
            annotated_frame = results[0].plot()

            if video_path is not None and out_path is not None:
                out.write(annotated_frame)


            # Show in camera
            cv2.imshow("YOLOv8 predictions", annotated_frame)


            # q: quit
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            break



    ser.close()
    cap.release()
    if video_path is not None and out_path is not None:
        out.release()
    cv2.destroyAllWindows()