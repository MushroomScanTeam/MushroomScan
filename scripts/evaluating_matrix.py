import os
import numpy as np
import onnxruntime as ort
from sklearn.metrics import classification_report, confusion_matrix
import torch
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
import seaborn as sns

# Set script directory and dataset paths
script_directory = os.getcwd()
directory_path_val = os.path.join(script_directory, "scripts", "downloaded_images", "val")

# Preprocessing transformations for validation data
val_transforms = transforms.Compose([
    transforms.Resize((384, 384)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Load validation dataset
val_dataset = datasets.ImageFolder(directory_path_val, transform=val_transforms)
val_loader = torch.utils.data.DataLoader(val_dataset, batch_size=16, shuffle=False, num_workers=4)

# Class-to-index mapping with Polish names
class_to_idx = val_dataset.class_to_idx
idx_to_class = {
    0: "Pieczarka polna (Agaricus campestris)",
    1: "Muchomor czerwony (Amanita muscaria)",
    2: "Opieńka miodowa (Armillaria mellea)",
    3: "Borowik szlachetny (Boletus edulis)",
    4: "Kurka (Pieprznik jadalny, Cantharellus cibarius)",
    5: "Podgrzybek brunatny (Imleria badia)",
    6: "Rydz (Lactarius deliciosus)",
    7: "Koźlarz czerwony (Leccinum aurantiacum)",
    8: "Koźlarz babka (Leccinum scabrum)",
    9: "Czubajka kania (Macrolepiota procera)",
    10: "Smardz jadalny (Morchella esculenta)",
    11: "Borowik ceglastopory (Neoboletus erythropus)",
    12: "Borowik szatański (Rubroboletus satanas)",
    13: "Maślak zwyczajny (Suillus luteus)",
    14: "Gąska zielonka (Tricholoma equestre)",
    15: "Gąska niekształtna (Tricholoma portentosum)"
}

print("Mapowanie indeksów klas na nazwy folderów:")
for idx, class_name in idx_to_class.items():
    print(f"Indeks {idx}: Klasa '{class_name}'")

# Load the ONNX model with GPU execution provider
onnx_model_path = os.path.join(script_directory, "scripts", "model.onnx")
session = ort.InferenceSession(onnx_model_path, providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

print("Execution providers:", session.get_providers())

# Perform inference and collect predictions
all_labels = []
all_preds = []

print("Running inference on validation set...")
for images, labels in val_loader:
    # Prepare input tensor for ONNX model
    input_tensor = images.numpy().astype(np.float32)
    outputs = session.run([output_name], {input_name: input_tensor})
    preds = np.argmax(outputs[0], axis=1)

    all_labels.extend(labels.numpy())
    all_preds.extend(preds)

# Calculate confusion matrix
cm = confusion_matrix(all_labels, all_preds)

# Polish class names for the confusion matrix
polish_class_names = [idx_to_class[i] for i in range(len(idx_to_class))]

# Print classification report
print("\nClassification Report:")
print(classification_report(all_labels, all_preds, target_names=polish_class_names))

# Visualize confusion matrix
plt.figure(figsize=(12, 10))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=polish_class_names, yticklabels=polish_class_names)
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix")
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()
