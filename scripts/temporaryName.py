# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 22:48:36 2025

@author: filip

Agaricus_bisporus 
Boletus_edulis 
Cantharellus_cibarius 
Macrolepiota_procera

Borowik szlachetny (Boletus edulis) – "prawdziwek" x
Podgrzybek brunatny (Imleria badia)
Koźlarz czerwony (Leccinum aurantiacum)
Koźlarz babka (Leccinum scabrum)
Maślak zwyczajny (Suillus luteus)
Kurka (Pieprznik jadalny) (Cantharellus cibarius) x
Rydz prawdziwy (Lactarius deliciosus)
Gąska zielonka (Tricholoma equestre)
Pieczarka łąkowa (Agaricus campestris)
Opieńka miodowa (Armillaria mellea)
Smardz jadalny (Morchella esculenta) – pod ochroną!
Czubajka kania (Macrolepiota procera) x
"""

#https://mushroomobserver.org/api2/images?size=small&name=Macrolepiota%20procera&detail=high&content_type=jpg

#https://mushroomobserver.org/api2/images?id=269&detail=high

#https://github.com/MushroomObserver/mushroom-observer/blob/main/README_API.md
    
#https://docs.google.com/spreadsheets/d/1aQSmLlthx99pCt_IS6aHyhZdn_hUiv3EBLbf4h3Zg7s/edit?gid=661544393#gid=661544393

#https://chatgpt.com/c/67786b05-374c-8006-9a97-573294573dab?model=gpt-4o

#https://mushroomobserver.org/api2/images?name=Imleria%20badia&detail=none&content_type=jpg&page=1&ok_for_export=true

import time
import requests
import os

script_directory = os.path.dirname(os.path.abspath(__file__))


def download_images(image_ids, resolution="320", save_directory="images", delay=6):
    """
    Pobiera zdjęcia z Mushroom Observer na podstawie listy ID.
    
    :param image_ids: Lista ID obrazów do pobrania.
    :param resolution: Rozdzielczość obrazów (np. "320", "640", "1280").
    :param save_directory: Katalog, w którym zapisywane będą obrazy.
    :param delay: Opóźnienie (w sekundach) między pobieraniem kolejnych obrazów.
    """
    # Tworzymy katalog na obrazy, jeśli nie istnieje
    os.makedirs(save_directory, exist_ok=True)

    for image_id in image_ids:
        # Budujemy URL obrazu
        image_url = f"https://images.mushroomobserver.org/{resolution}/{image_id}.jpg"
        save_path = os.path.join(save_directory, f"{image_id}.jpg")
        
        try:
            # Pobieramy obraz
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                with open(save_path, "wb") as image_file:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            image_file.write(chunk)
                print(f"Pobrano obraz {image_id} i zapisano w {save_path}")
            else:
                print(f"Nie udało się pobrać obrazu {image_id}: {response.status_code}")
        except Exception as e:
            print(f"Błąd przy pobieraniu obrazu {image_id}: {e}")
        
        # Czekamy przed kolejnym pobraniem
        time.sleep(delay)

# Przykład użycia
if __name__ == "__main__":
    # Lista ID obrazów do pobrania [16841, 16842, 16843, 148262, 148263, 148264, 152088, 152089, 152090, 152202, 245771, 245772, 249322, 255178, 255179, 255180, 255757, 255758, 260639, 260640, 260641, 273083, 273084, 275183, 275184, 275185, 289383, 289384, 289386, 289389, 297901, 297902, 297903, 297904, 345658, 345659, 358426, 358427, 358428, 428450, 428451, 428452, 428580, 428581, 436414, 436415, 436416, 436417, 436418, 436419, 438153, 439329, 439330, 443498, 443499, 443500, 443501, 445445, 445446, 445447, 445448, 445645, 446672, 446673, 491168, 491169, 494636, 494637, 494638, 494641, 494642, 494643, 494644, 505032, 505033, 512422,]
    image_ids_Imleria_badia = [529241, 529242, 531023, 531024, 531502, 531503, 533840, 533841, 533842, 534041, 534042, 535386, 535387, 537201, 537202, 539881, 539882, 540649, 546053, 546055, 546056, 567028, 567029, 567030, 567031, 567032, 568739, 568740, 568741, 568742, 581098, 581099, 581100, 582271, 600993, 600994, 600995, 618959, 618960, 618961, 618962, 618963, 618964, 623914, 627138, 627139, 627140, 627141, 627142, 637057, 637058, 638773, 654843, 654844, 654845, 655245, 655246, 660565, 660566, 660567, 660568, 660569, 662784, 662786, 662787, 663868, 663869, 663870, 663872, 663873, 663874, 667045, 667046, 667048, 667193, 667194, 667195, 667196, 667865, 667866, 667867, 687645, 687646, 687647, 699793, 699794, 699795, 699796, 756027, 756028, 756029, 756278, 756279, 756919, 757757, 757758, 757759, 757760, 760550, 760551, 761597, 761598, 766572, 766573, 766574, 766958, 766959, 766960, 768729, 768730, 768731, 768732, 768733, 771929, 771933, 772875, 785987, 785988, 785989, 785990, 792404, 792405, 792406, 792410, 792413, 793911, 793912, 812751, 812752, 812753, 812754, 818508, 900510, 900511, 900512, 900513, 900515, 900516, 902411, 902412, 902413, 902414, 920769, 920770, 921243, 922154, 922155, 922156, 922157, 929287, 929288, 934411, 934412, 934413, 934445, 934446, 934447, 936453, 936454, 936455, 936456, 936457, 938427, 938428, 938429, 944498, 944499, 948645, 948646, 952965, 952966, 952967, 966868, 966872, 966876, 966879, 1001372, 1001373, 1001374, 1001375, 1001376, 1001377, 1004109, 1051269, 1051270, 1051271, 1051272, 1053534, 1053535, 1053536, 1053537, 1067349, 1067350, 1072032, 1072033, 1084386, 1084387, 1084388, 1084389, 1086390, 1086391, 1086392, 1086393, 1086739, 1086740, 1086741, 1086742, 1089662, 1094734, 1095366, 1105567, 1105568, 1105569, 1116795, 1120165, 1120166, 1135828, 1151928, 1151929, 1194757, 1194758, 1194759, 1194760, 1194761, 1194762, 1200056, 1200057, 1200058, 1200059, 1200060, 1200061, 1200062, 1200063, 1200064, 1200065, 1206340, 1206341, 1206342, 1206343, 1206344, 1206924, 1206927, 1206929, 1206930, 1210910, 1210911, 1223464, 1223465, 1223466, 1223467, 1227706, 1227707, 1227708, 1227970, 1227972, 1227973, 1227974, 1237703, 1237704, 1237705, 1265816, 1265817, 1265818, 1265819, 1267610, 1267611, 1267612, 1267613, 1267614, 1267615, 1267616, 1267617, 1267618, 1267619, 1267620, 1267621, 1267622, 1298835, 1298836, 1320256, 1320257, 1320258, 1339343, 1339344, 1339345, 1354821, 1354822, 1354823, 1357156, 1357157, 1357158, 1381377, 1381378, 1381379, 1381380, 1388295, 1388296, 1388365, 1388366, 1388367, 1388368, 1388369, 1398978, 1398979, 1398980, 1439840, 1443403, 1443404, 1443405, 1467534, 1467535, 1467536, 1474953, 1474954, 1474955, 1474956, 1474957, 1474958, 1483566, 1483567, 1484769, 1484770, 1484771, 1484772, 1484773, 1484774, 1484775, 1484776, 1484777, 1484778, 1484779, 1484780, 1484781, 1491527, 1491528, 1491529, 1496773, 1496774, 1496775, 1498849, 1500478, 1500479, 1500480, 1500481, 1500482, 1500483, 1500484, 1508106, 1508107, 1508108, 1508109, 1508110, 1508111, 1518451, 1518453, 1518456, 1534934, 1557876, 1557877, 1557878, 1557879, 1579331, 1579332, 1579787, 1579788, 1579789, 1579790, 1579791, 1583154, 1583155, 1583156, 1583157, 1583158, 1583159, 1583160, 1583161, 1586211, 1586212, 1586213, 1586230, 1586231, 1586232, 1586233, 1586234, 1591538, 1591945, 1591946, 1591947, 1592747, 1592748, 1592749, 1592750, 1600700, 1600701, 1600702, 1600703, 1670472, 1670473, 1670474, 1670475, 1670476, 1675107, 1675108, 1675109, 1675110, 1679893, 1679909, 1679910, 1682236, 1682237, 1682238, 1682239, 1683631, 1683632, 1683633, 1699770, 1699771, 1706668, 1706669, 1707972, 1707973, 1707974, 1722175]
    resolution = "320"  # Zmień rozdzielczość, jeśli potrzeba (np. "320", "640", "1280")
    directory_path = os.path.join(script_directory, "downloaded_images")

    
    # Wywołanie funkcji
    download_images(image_ids_Imleria_badia, resolution=resolution, save_directory=directory_path, delay=6)
