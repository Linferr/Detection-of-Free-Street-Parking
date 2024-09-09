from sklearn.model_selection import train_test_split
import os
import shutil

# CONFIGURE THESE AS REQUIRED
# PATH TO DATASET
data_path = './MLModel/data'
# PATH TO IMAGES
image_rel_path = '/images/'
# PATH TO YOLO FORMAT LABELS FROM ANNOTATION SOFTWARE 
label_rel_path = '/labels/'

img_list = os.listdir(data_path + image_rel_path)
label_list = os.listdir(data_path + label_rel_path)

train_parking_ct = 0
test_parking_ct = 0

img_train, img_test, label_train, label_test = train_test_split(img_list, label_list, test_size=0.15, random_state=88)

# ULTRALYTICS YOLO EXPECTS TRAIN DATA TO BE IN /TRAIN
# AND TEST DATA TO BE IN /TEST
end_path = './data'
train_rel_path = '/train'
test_rel_path = '/test'

# COPY DATA INTO RESPECTIVE FOLDERS 
for img in img_train:
    shutil.copy2(data_path+image_rel_path+img, end_path+train_rel_path+image_rel_path)

for img in img_test:
    shutil.copy2(data_path+image_rel_path+img, end_path+test_rel_path+image_rel_path)

for lbl in label_train:
    shutil.copy2(data_path+label_rel_path+lbl, end_path+train_rel_path+label_rel_path)
    if open(data_path+label_rel_path+lbl).read():
        train_parking_ct+=1

for lbl in label_test:
    shutil.copy2(data_path+label_rel_path+lbl, end_path+test_rel_path+label_rel_path)
    if open(data_path+label_rel_path+lbl).read():
        test_parking_ct+=1

print("train parking count " + str(train_parking_ct))
print("test parking count " + str(test_parking_ct))



