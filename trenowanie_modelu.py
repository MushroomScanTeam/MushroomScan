import os
import timm
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from tqdm import tqdm
from sklearn.metrics import classification_report
from torch.cuda.amp import autocast, GradScaler
from torchvision import datasets
from torchvision import transforms

torch.cuda.empty_cache()

script_directory = os.getcwd()

directory_path_train = os.path.join(script_directory, "scripts","downloaded_images","train")
directory_path_val = os.path.join(script_directory, "scripts","downloaded_images", "val")

train_transforms = transforms.Compose([
    transforms.Resize((384, 384)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ToTensor(),
    # Normalize means subtract mean, divide by std for each color channel
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

val_transforms = transforms.Compose([
    transforms.Resize((384, 384)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Konfiguracja urządzenia
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Ścieżka do checkpointu
directory_path_pre_trained = os.path.join(script_directory, "scripts", "DF20-ViT_base_patch16_384_best_accuracy.pth")
checkpoint_path = directory_path_pre_trained

train_dataset = datasets.ImageFolder(directory_path_train, transform=train_transforms)
val_dataset   = datasets.ImageFolder(directory_path_val,   transform=val_transforms)

train_loader = torch.utils.data.DataLoader(
    train_dataset, batch_size=16, shuffle=True, num_workers=0
)
val_loader = torch.utils.data.DataLoader(
    val_dataset, batch_size=16, shuffle=False, num_workers=0
)

class_to_idx = train_dataset.class_to_idx
idx_to_class = {v: k for k, v in class_to_idx.items()}
print("Mapowanie indeksów klas na nazwy folderów:")
for idx, class_name in idx_to_class.items():
    print(f"Indeks {idx}: Klasa '{class_name}'")

# Liczba klas
num_classes = 16

# Model ViT
model_name = "vit_base_patch16_384"
model = timm.create_model(model_name, pretrained=False, num_classes=1604)

# Wczytanie checkpointu
checkpoint = torch.load(checkpoint_path, map_location=device)
model.load_state_dict(checkpoint, strict=False)

# Dostosowanie warstwy wyjściowej
model.head = nn.Linear(model.head.in_features, num_classes)

# Przeniesienie modelu na GPU/CPU
model.to(device)

train_labels = []
for _, labels in train_loader:
    train_labels.extend(labels.numpy())

train_labels = torch.tensor(train_labels)


# Definicja strat, optymalizatora i scheduler
class_counts = [len([label for label in train_labels if label == c]) for c in range(num_classes)]
class_weights = 1.0 / torch.tensor(class_counts, dtype=torch.float).to(device)

# Użycie ważonej funkcji strat
criterion = nn.CrossEntropyLoss(weight=class_weights)
#criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-4)
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)

# Mixed precision
scaler = GradScaler()

# Trening
num_epochs = 3
for epoch in range(num_epochs):
    print(f"Epoch {epoch+1}/{num_epochs}")
    model.train()
    running_loss = 0.0

    for images, labels in tqdm(train_loader, desc="Training", leave=False):
        images, labels = images.to(device), labels.to(device)

        # Mixed precision forward
        with autocast():
            outputs = model(images)
            loss = criterion(outputs, labels)

        # Backward pass with gradient scaling
        optimizer.zero_grad()
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()

        running_loss += loss.item()

    avg_loss = running_loss / len(train_loader)

    # Walidacja
    all_labels = []
    all_preds = []
    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in tqdm(val_loader, desc="Validating", leave=False):
            images, labels = images.to(device), labels.to(device)
            with autocast():
                outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            all_labels.extend(labels.cpu().numpy())
            all_preds.extend(predicted.cpu().numpy())
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    val_accuracy = 100 * correct / total
    print(f"Loss: {avg_loss:.4f}, Val Accuracy: {val_accuracy:.2f}%")

    if epoch == num_epochs - 1:
        print(classification_report(all_labels, all_preds, target_names=train_dataset.classes))

    scheduler.step()
    torch.cuda.empty_cache()

print("Trening zakończony!")

# Ścieżka do zapisania modelu
export_path = os.path.join(script_directory, "scripts", "exported_model_state_dict.pth")

# Zapis modelu
torch.save(model.state_dict(), export_path)

print(f"Model zapisany w formacie state_dict w: {export_path}")