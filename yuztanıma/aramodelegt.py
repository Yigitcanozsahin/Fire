import os
import cv2

# Görüntülerin bulunduğu ve ön işlenmiş görüntülerin kaydedileceği klasörlerin yolları
input_folder = "/Users/yigitcanozsahin/Desktop/Fire/faces/usr2"
output_folder = "/Users/yigitcanozsahin/Desktop/Fire/faces2"

# Eğer çıktı klasörü yoksa oluştur
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Görüntü dosyalarını döngüye al
file_names = sorted(os.listdir(input_folder))  # Dosya adlarını sıralı şekilde al

for filename in file_names:
    # Dosyanın tam yolu
    file_path = os.path.join(input_folder, filename)

    # Dosya uzantısını kontrol et, sadece görüntü dosyalarını işle
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        # Görüntüyü yükle
        image = cv2.imread(file_path)

        if image is None:
            print(f"Failed to load image {file_path}")
            continue

        # Görüntü boyutlandırma (INTER_LINEAR veya INTER_CUBIC kullanarak daha iyi sonuçlar elde edilir)
        resized_image = cv2.resize(image, (100, 100), interpolation=cv2.INTER_LINEAR)

        # Gri tonlamaya dönüştürme
        gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

        # Kontrastı artırma (Histogram eşitleme)
        enhanced_image = cv2.equalizeHist(gray_image)

        # Çıktı klasörüne ön işlenmiş görüntüyü kaydet
        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, enhanced_image)

        print(f"Processed: {filename}")

print("Preprocessing completed.")
