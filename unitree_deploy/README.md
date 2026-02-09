# Unitree Deploy 

<div align="center">
  <p align="right">
    <span> 🌎English </span> | <a href="./docs/README_cn.md"> 🇨🇳中文 </a>
  </p>
</div>



Ten dokument opisuje konfigurację środowiska wdrożeniowego dla platform Unitree G1 (z chwytakiem) oraz Z1, w tym instalację zależności, uruchomienie usług obrazu i sterowanie chwytakiem. Materiał jest szczególnie przydatny w laboratoriach z robotem Unitree G1 EDU-U6.

# 0. 📖 Wprowadzenie

Repozytorium służy do wdrażania modeli na robotach Unitree. W praktyce obejmuje uruchomienie usług na robocie, przygotowanie sterowników i testów, aby model mógł wykonywać realne zadania.

---

# 1. 🛠️ Konfiguracja środowiska 

```bash
conda create -n unitree_deploy python=3.10 && conda activate unitree_deploy

conda install pinocchio -c conda-forge
pip install -e .

# Opcjonalnie: zainstaluj zależności lerobot
pip install -e ".[lerobot]"

git clone https://github.com/unitreerobotics/unitree_sdk2_python.git
cd unitree_sdk2_python  && pip install -e . && cd ..
```

---
# 2. 🚀 Start 

**Wskazówka: utrzymuj wszystkie urządzenia w tej samej sieci LAN, aby zmniejszyć opóźnienia.**

## 2.1 🤖 Uruchom G1 z chwytakiem Dex_1 

### 2.1.1 📷 Konfiguracja usługi przechwytywania obrazu (płyta G1) 

[Aby uruchomić image_server, wykonaj te kroki](https://github.com/unitreerobotics/xr_teleoperate?tab=readme-ov-file#31-%EF%B8%8F-image-service)
1. Połącz się z płytą G1 (cel: zdalne uruchomienie usługi obrazu):
    ```bash
    ssh unitree@192.168.123.164  # Password: 123
    ```

2. Aktywuj środowisko i uruchom image server (cel: strumieniowanie obrazu do klienta):
    ```bash
    conda activate tv
    cd ~/image_server
    python image_server.py
    ```

---

### 2.1.2 🤏 Konfiguracja usługi chwytaka Dex_1 (Development PC2)

Szczegóły instalacji znajdziesz w [Dex_1 Gripper Installation Guide](https://github.com/unitreerobotics/dex1_1_service?tab=readme-ov-file#1--installation).

1. Przejdź do katalogu usługi (cel: uruchomienie serwera chwytaka):
    ```bash
    cd ~/dex1_1_service/build
    ```

2. Uruchom usługę chwytaka, **ifconfig sprawdza własny interfejs dds**:
    ```bash
    sudo ./dex1_1_gripper_server --network eth0 -l -r
    ```

3. Zweryfikuj komunikację z usługą chwytaka:
    ```bash
    ./test_dex1_1_gripper_server --network eth0 -l -r
    ```

---

### 2.1.2 ✅Testy 

Wykonaj testy, aby upewnić się, że wszystkie elementy działają poprawnie:

- **Test chwytaka Dex1**:
  ```bash
  python test/endeffector/test_dex1.py
  ```

- **Test ramienia G1**:
  ```bash
  python test/arm/g1/test_g1_arm.py
  ```

- **Test kamery (Image Client)**:
  ```bash
  python test/camera/test_image_client_camera.py
  ```

- **Odtwarzanie datasetów G1**:
  ```bash
  # --repo-id     Twój unikalny identyfikator repo na Hugging Face Hub 
  # --robot_type     Typ robota, np. z1_dual_dex1_realsense, z1_realsense, g1_dex1, 
  
  python test/test_replay.py --repo-id unitreerobotics/G1_CameraPackaging_NewDataset --robot_type g1_dex1
  ```
---

## 2.2 🦿 Uruchom Z1 

### 2.2.1 🦿 Konfiguracja Z1
Pobierz i zbuduj wymagane repozytoria:

1. Pobierz [z1_controller](https://github.com/unitreerobotics/z1_controller.git) oraz [z1_sdk](https://github.com/unitreerobotics/z1_sdk.git).

2. Zbuduj repozytoria:
    ```bash
    mkdir build && cd build
    cmake .. && make -j
    ```

3. Skopiuj bibliotekę `unitree_arm_interface`: [Zmodyfikuj ścieżkę]
    ```bash
    cp z1_sdk/lib/unitree_arm_interface.cpython-310-x86_64-linux-gnu.so ./unitree_deploy/robot_devices/arm
    ```

4. Uruchom kontroler Z1 [Zmodyfikuj ścieżkę]:
    ```bash
    cd z1_controller/build && ./z1_ctrl
    ```

---

### 2.2.2 Testy ✅

Uruchom następujące testy:

- **Test kamery Realsense**:
  ```bash
  python test/camera/test_realsense_camera.py # Modify the corresponding serial number according to your realsense
  ```

- **Test ramienia Z1**:
  ```bash
  python test/arm/z1/test_z1_arm.py
  ```

- **Test środowiska Z1**:
  ```bash
  python test/arm/z1/test_z1_env.py
  ```

- **Odtwarzanie datasetów Z1**:
  ```bash
  # --repo-id     Twój unikalny identyfikator repo na Hugging Face Hub 
  # --robot_type     Typ robota, np. z1_dual_dex1_realsense, z1_realsense, g1_dex1, 

  python test/test_replay.py --repo-id unitreerobotics/Z1_StackBox_Dataset --robot_type z1_realsense
  ```
---

## 2.3 🦿 Uruchom Z1_Dual

### 2.3.1 🦿 Konfiguracja Z1 oraz Dex1
Pobierz i zbuduj wymagane repozytoria:

1. Pobierz i skompiluj kod zgodnie z krokami dla Z1 oraz pobierz program chwytaka do uruchomienia lokalnego

2. [Dostosuj sterowanie wielomaszynowe zgodnie z dokumentacją](https://support.unitree.com/home/zh/Z1_developer/sdk_operation)

3. [Pobierz zmodyfikowane z1_sdk_1 i je skompiluj](https://github.com/unitreerobotics/z1_sdk/tree/z1_dual), skopiuj bibliotekę `unitree_arm_interface`: [Zmodyfikuj ścieżkę]
    ```bash
    cp z1_sdk/lib/unitree_arm_interface.cpython-310-x86_64-linux-gnu.so ./unitree_deploy/robot_devices/arm
    ```

4. Uruchom kontroler Z1 [Zmodyfikuj ścieżkę]:
    ```bash
    cd z1_controller/builb && ./z1_ctrl
    cd z1_controller_1/builb && ./z1_ctrl
    ```
5. Uruchom usługę chwytaka, **ifconfig sprawdza własny interfejs dds**:
    ```
    sudo ./dex1_1_gripper_server --network eth0 -l -r
    ```
---

### 2.3.2 Testy ✅

Uruchom następujące testy:

- **Test ramienia Z1_Dual**:
  ```bash
  python test/arm/z1/test_z1_arm_dual.py
  ```

- **Odtwarzanie datasetów Z1_Dual**:
  ```bash
  # --repo-id     Twój unikalny identyfikator repo na Hugging Face Hub 
  # --robot_type     Typ robota, np. z1_dual_dex1_realsense, z1_realsense, g1_dex1, 

  python test/test_replay.py --repo-id unitreerobotics/Z1_Dual_Dex1_StackBox_Dataset_V2 --robot_type z1_dual_dex1_realsense
  ```
---


# 3.🧠 Inference and Deploy
1. [Modify the corresponding parameters according to your configuration](./unitree_deploy/robot/robot_configs.py)
2. Go back the **step-2 of Client Setup** under the [Inference and Deployment under Decision-Making Mode](https://github.com/unitreerobotics/unifolm-world-model-action/blob/main/README.md).

# 4.🏗️ Code structure

[If you want to add your own robot equipment, you can build it according to this document](./docs/GettingStarted.md)


# 5. 🤔 Troubleshooting

For assistance, contact the project maintainer or refer to the respective GitHub repository documentation. 📖


# 6. 🙏 Acknowledgement

This code builds upon following open-source code-bases. Please visit the URLs to see the respective LICENSES (If you find these projects valuable, it would be greatly appreciated if you could give them a star rating.):

1. https://github.com/huggingface/lerobot
2. https://github.com/unitreerobotics/unitree_sdk2_python
