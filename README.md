# Instalación del entorno para reconocimiento facial con Python

Este proyecto requiere una configuración específica del entorno para poder trabajar correctamente con reconocimiento facial utilizando `dlib`, `OpenCV`, y `face-recognition`.

---

## Requisitos

- **Python 3.11.4**  
  Durante la instalación:
  - Marcar la opción ✅ **"Add Python to PATH"**
  - Seleccionar ⚙️ **"Custom installation"**

---

## Instalación de dependencias

### 1. Instalar CMake

```bash
pip install cmake
```

---

### 2. Instalar `dlib`

- Seguí el tutorial en video:  
  ▶️ [https://www.youtube.com/watch?v=m6VHlvh4dTE](https://www.youtube.com/watch?v=m6VHlvh4dTE)

- Descargar el archivo `.whl` desde:  
  📥 [https://github.com/z-mahmud22/Dlib_Windows_Python3.x](https://github.com/z-mahmud22/Dlib_Windows_Python3.x)

- Abrir una terminal (`cmd`) en la carpeta donde descargaste el archivo `.whl`:
  - En el explorador de archivos, hacé clic en la barra de direcciones
  - Escribí `cmd` y presioná Enter
  - En la terminal, ejecutá:

```bash
pip install dlib-19.24.99-cp312-cp312-win_amd64.whl
```

📌 Asegurate de que el nombre del archivo coincida con el que descargaste.

---

### 3. Instalar otras librerías necesarias

```bash
pip install opencv-python
pip install pyserial
pip install face-recognition
```

---

## ⚠️ Nota importante sobre NumPy

`opencv-python` puede instalar una versión incompatible de `numpy`. Para corregirlo, hacé un downgrade:

```bash
pip uninstall -y numpy
pip install numpy==1.23.5
```

---

## ✅ Entorno listo

Tu entorno está preparado para comenzar a trabajar con reconocimiento facial en Python. 🚀
