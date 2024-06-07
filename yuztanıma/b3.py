import cv2
import os
import numpy as np

# Yüz tanıma için ön eğitilmiş modeli yükle
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Yüz görüntülerinin bulunduğu dizin
dataset_path = "dataset"

# Yüz görüntülerini ve etiketlerini saklamak için listeler
faces = []
labels = []

# Veri setindeki her bir alt dizini (her bir kullanıcıyı) döngüye al
for user_folder in os.listdir(dataset_path):
    # Kullanıcının adını ve id'sini al
    user_name = user_folder
    user_id = int(user_name.split("_")[1])

    # Kullanıcının yüz görüntülerinin bulunduğu dizini oluştur
    user_folder_path = os.path.join(dataset_path, user_folder)

    # Her bir kullanıcının yüz görüntülerini döngüye al
    for image_name in os.listdir(user_folder_path):
        # Yüz görüntüsünü yükle
        image_path = os.path.join(user_folder_path, image_name)
        image = cv2.imread(image_path)

        # Yüzleri algıla
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_rects = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Yüz görüntüsünde yüz algılandıysa
        if len(face_rects) == 1:
            x, y, w, h = face_rects[0]
            face_roi = gray[y:y+h, x:x+w]

            # Yüzü yeniden boyutlandır ve ortalama bir boyuta getir
            face_roi = cv2.resize(face_roi, (100, 100))

            # Yüz görüntüsünü listeye ekle
            faces.append(face_roi)

            # Etiketi listeye ekle
            labels.append(user_id)

# Eğitim için NumPy dizilerine dönüştür
faces = np.array(faces, dtype='uint8')
labels = np.array(labels)

# Yüz tanıma modelini eğitmek için LBPH (Local Binary Patterns Histograms) algoritmasını kullan
model = cv2.face.LBPHFaceRecognizer_create()
model.train(faces, labels)

# Modeli kaydet
model.save("face_recognition_model.yml")
