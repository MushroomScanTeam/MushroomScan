# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 22:29:28 2025

@author: filip
"""

import os
import random
import shutil

def create_val_folders(base_dir):
    # Ścieżki do folderów train i val
    train_dir = os.path.join(base_dir, "train")
    val_dir = os.path.join(base_dir, "val")

    # Sprawdź, czy folder train istnieje
    if not os.path.exists(train_dir):
        print(f"Folder train nie istnieje w lokalizacji: {train_dir}")
        return

    # Upewnij się, że folder val istnieje
    if not os.path.exists(val_dir):
        os.makedirs(val_dir)

    # Iteracja przez foldery na pierwszym poziomie w train i tworzenie ich odpowiedników w val
    for folder_name in os.listdir(train_dir):
        folder_path = os.path.join(train_dir, folder_name)
        if os.path.isdir(folder_path):  # Sprawdzenie, czy to folder (tylko pierwszy poziom)
            val_folder_path = os.path.join(val_dir, folder_name)
            if not os.path.exists(val_folder_path):
                os.makedirs(val_folder_path)
                print(f"Utworzono folder: {val_folder_path}")
            else:
                print(f"Folder już istnieje: {val_folder_path}")

def move_random_images(base_dir):
    # Ścieżki do folderów train i val
    train_dir = os.path.join(base_dir, "train")
    val_dir = os.path.join(base_dir, "val")

    # Iteracja przez foldery na pierwszym poziomie w train
    for folder_name in os.listdir(train_dir):
        folder_path = os.path.join(train_dir, folder_name)
        if os.path.isdir(folder_path):  # Sprawdzenie, czy to folder
            val_folder_path = os.path.join(val_dir, folder_name)

            # Pobranie listy zdjęć w folderze
            images = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

            # Wyliczenie 10% zdjęć do przeniesienia
            num_to_move = max(1, len(images) // 10)  # Przynajmniej jedno zdjęcie
            images_to_move = random.sample(images, num_to_move)

            # Przenoszenie zdjęć
            for image in images_to_move:
                src_path = os.path.join(folder_path, image)
                dest_path = os.path.join(val_folder_path, image)
                shutil.move(src_path, dest_path)
                print(f"Przeniesiono {src_path} do {dest_path}")

if __name__ == "__main__":
    base_dir = "C:\\Users\\filip\\Documents\\GitHub\\MuschroomScan\\scripts\\downloaded_images"
    #create_val_folders(base_dir)
    move_random_images(base_dir)