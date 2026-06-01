import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models
import json

# ===== PATHS =====
train_dir = "dataset/train"
val_dir = "dataset/val"

# ===== IMAGE PREPROCESSING =====
train_gen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    brightness_range=[0.8, 1.2],
    horizontal_flip=True
)

val_gen = ImageDataGenerator(rescale=1./255)

train_data = train_gen.flow_from_directory(
    train_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

val_data = val_gen.flow_from_directory(
    val_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

# ===== PRINT & SAVE CLASS MAPPING =====
print("Class indices:", train_data.class_indices)

with open("classes.json", "w") as f:
    json.dump(train_data.class_indices, f)

# ===== LOAD MODEL =====
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224,224,3))
base_model.trainable = False

# ===== ADD CUSTOM LAYERS =====
x = base_model.output
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dense(128, activation='relu')(x)
x = layers.Dropout(0.3)(x)   # helps reduce overfitting
output = layers.Dense(train_data.num_classes, activation='softmax')(x)

model = models.Model(inputs=base_model.input, outputs=output)

# ===== COMPILE =====
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# ===== TRAIN =====
history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=5
)

# ===== SAVE MODEL =====
model.save("activity_model.h5")

print("✅ Model trained and class mapping saved!")