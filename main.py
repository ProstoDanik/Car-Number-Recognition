#импорт библиотек
import matplotlib.pyplot as plt 
import cv2
import easyocr

#База номеров
REGIST_CARS = ['A222AA', 'MOO8MM', 'EOO8EE']


#Открытие фото
def open_img(img_path):
    carplate_img = cv2.imread(img_path)
    carplate_img = cv2.cvtColor(carplate_img, cv2.COLOR_BGR2RGB)
    plt.axis('off')
    plt.imshow(carplate_img)
    plt.show()

    return carplate_img


#Обнаружение и извлечение координат номера на фото
def carplate_extract(image, carplate_haar_cascade):
    carplate_rects = carplate_haar_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)

    for x, y, w, h in carplate_rects:
        carplate_img = image[y+15:y+h-10, x+15:x+w-20]

    return carplate_img


#Увеличивание фото для лучшего распознания номера после обработки
def enlarge_img(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    plt.axis('off')
    resized_image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

    return resized_image


#Главная функция, в которой вызываются и обрабатываются значения других функций
def main():
    carplate_img_rgb = open_img(img_path='cars/car1.jpg')
    carplate_haar_cascade = cv2.CascadeClassifier('haar_cascades/haarcascade_russian_plate_number.xml')

    carplate_extract_img = carplate_extract(carplate_img_rgb, carplate_haar_cascade)
    carplate_extract_img = enlarge_img(carplate_extract_img, 150)
    plt.imshow(carplate_extract_img)
    # plt.show()

    carplate_extract_img_gray = cv2.cvtColor(carplate_extract_img, cv2.COLOR_RGB2GRAY)
    plt.axis('off')
    plt.imshow(carplate_extract_img_gray, cmap='gray')
    plt.show()

    
    text = easyocr.Reader(['en'])
    text = text.readtext(carplate_extract_img_gray)
    res = text[0][-2]
    length = len(res)

    
    if length > 6:
        n = length - 6
        res = res[:-n]


    if res[0] or res[4] or res[5] == '0':
        new_res = res.replace('0', 'О')
    print(new_res)


   
    if res in REGIST_CARS:
        print('ДОСТУП ОТКРЫТ!')
    else:
        print('ДОСТУП ЗАКРЫТ!')

    

#Запуск программы
if __name__ == '__main__':
    main()




