# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 02:37:09 2025

@author: filip
"""

import os
script_directory = os.path.dirname(os.path.abspath(__file__))
directory_path = os.path.join(script_directory, "images")

def rename_files_in_folder(folder_path):
    # Przechodzenie przez wszystkie pliki w folderze
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        # Sprawdzanie, czy to jest plik (a nie folder)
        if os.path.isfile(file_path):
            # Dodanie literki 'a' na początku nazwy pliku
            new_file_name = f"a{file_name}"
            new_file_path = os.path.join(folder_path, new_file_name)
            
            # Zmiana nazwy pliku
            os.rename(file_path, new_file_path)
            print(f"Renamed: {file_name} -> {new_file_name}")

# Ścieżka do folderu z plikami

# Uruchomienie funkcji
rename_files_in_folder(directory_path)
