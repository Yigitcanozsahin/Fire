import cv2
import os

def take_photos(num_photos, save_path):
    # Kamera yakalama cihazını başlat
    camera = cv2.VideoCapture(0)

    # Kamera yakalama cihazını kontrol et
    if not camera.isOpened():
        print("Kamera bulunamadı veya açılamadı.")
        return

    # Kayıt klasörünün var olduğundan emin olun
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # 165 fotoğraf çek
    for i in range(num_photos):
        ret, frame = camera.read()
        
        # Görüntüyü dosyaya kaydet
        if ret:
            file_name = os.path.join(save_path, f"photo_{i+1}.jpg")
            cv2.imwrite(file_name, frame)
            print(f"Yüz fotoğrafı kaydedildi: {file_name}")
        else:
            print(f"Görüntü alınamadı: {i+1}")

    # Kamera yakalama cihazını serbest bırak
    camera.release()

if __name__ == "__main__":
    save_path = "/Users/yigitcanozsahin/Desktop/Fire/faces/usr7"
    take_photos(80, save_path)
