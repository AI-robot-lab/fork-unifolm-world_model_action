# UnifoLM-WMA-0: Framework World-Model-Action (WMA) w rodzinie UnifoLM
<p style="font-size: 1.2em;">
    <a href="https://unigen-x.github.io/unifolm-world-model-action.github.io"><strong>Project Page</strong></a> | 
    <a href="https://huggingface.co/collections/unitreerobotics/unifolm-wma-0-68ca23027310c0ca0f34959c"><strong>Models</strong></a> |
    <a href="https://huggingface.co/unitreerobotics/datasets"><strong>Dataset</strong></a> 
  </p>
<div align="center">
  <p align="right">
    <span> 🌎English </span> | <a href="README_cn.md"> 🇨🇳中文 </a>
  </p>
</div>
<div align="justify">
    <b>UnifoLM-WMA-0</b> to otwartoźródłowa architektura world-model–action firmy Unitree, działająca na wielu typach platform robotycznych i przeznaczona do ogólnego uczenia robotów. Jej rdzeniem jest world model rozumiejący fizyczne interakcje pomiędzy robotem a środowiskiem. Model ten zapewnia dwie kluczowe funkcje: (a) <b>Simulation Engine</b> – działa jako interaktywny symulator i generuje dane syntetyczne do uczenia robota; (b) <b>Policy Enhancement</b> – łączy się z action head i, przewidując przyszły przebieg interakcji w world model, usprawnia podejmowanie decyzji.
</div>

## 🎯 Cel dydaktyczny i kontekst Unitree G1 EDU-U6
Repozytorium stanowi kompletne środowisko dydaktyczne do zrozumienia, jak world model i policy head współpracują przy sterowaniu robotem humanoidalnym. W projekcie laboratorium szczególny nacisk kładziemy na pracę z platformą Unitree G1 EDU-U6, dlatego:
- pokazujemy, jak budować dane wejściowe dla world modelu (kamera + stan robota),
- uczymy uruchamiania serwera decyzyjnego oraz klienta robota,
- wyjaśniamy, gdzie modyfikować konfiguracje, aby dopasować model do konkretnej wersji sprzętowej.

## 🦾 Demonstracje na prawdziwym robocie
| <img src="assets/gifs/real_z1_stackbox.gif" style="border:none;box-shadow:none;margin:0;padding:0;" /> | <img src="assets/gifs/real_dual_stackbox.gif" style="border:none;box-shadow:none;margin:0;padding:0;" /> |
|:---:|:---:|
| <img src="assets/gifs/real_cleanup_pencils.gif" style="border:none;box-shadow:none;margin:0;padding:0;" /> | <img src="assets/gifs/real_g1_pack_camera.gif" style="border:none;box-shadow:none;margin:0;padding:0;" /> |

**Uwaga: w prawym górnym oknie widać predykcję world modelu dotyczącą przyszłych sekwencji wideo akcji.**

## 🔥 Aktualności

* 22 września 2025: 🚀 Udostępniliśmy kod wdrożeniowy do eksperymentów z robotami [Unitree](https://www.unitree.com/).
* 15 września 2025: 🚀 Udostępniliśmy kod treningu i inferencji wraz z wagami modelu [**UnifoLM-WMA-0**](https://huggingface.co/collections/unitreerobotics/unifolm-wma-0-68ca23027310c0ca0f34959c).

## 📑 Plan otwarcia kodu
- [x] Trening 
- [x] Inferencja
- [x] Checkpointy
- [x] Wdrożenie

## ⚙️  Instalacja
Poniższe kroki tworzą izolowane środowisko dla UnifoLM-WMA-0 i instalują zależności potrzebne do treningu oraz inferencji. Dzięki temu studenci unikają konfliktów wersji bibliotek i mogą powtarzalnie uruchamiać pipeline.
```
conda create -n unifolm-wma python==3.10.18
conda activate unifolm-wma

conda install pinocchio=3.2.0 -c conda-forge -y
conda install ffmpeg=7.1.1 -c conda-forge

git clone --recurse-submodules https://github.com/unitreerobotics/unifolm-world-model-action.git

# If you already downloaded the repo:
cd unifolm-world-model-action
git submodule update --init --recursive

pip install -e .

cd external/dlimp
pip install -e .
```
## 🧰 Checkpointy modeli
| Model | Opis | Link|
|---------|-------|------|
|$\text{UnifoLM-WMA-0}_{Base}$| Fine-tuning na zbiorze [Open-X](https://robotics-transformer-x.github.io/). | [HuggingFace](https://huggingface.co/unitreerobotics/UnifoLM-WMA-0-Base)|
|$\text{UnifoLM-WMA-0}_{Dual}$| Fine-tuning na pięciu [zbiorach Unitree opensource](https://huggingface.co/collections/unitreerobotics/g1-dex1-datasets-68bae98bf0a26d617f9983ab) w trybach decision-making i simulation. | [HuggingFace](https://huggingface.co/unitreerobotics/UnifoLM-WMA-0-Dual)|

## 🛢️ Dataset
W naszych eksperymentach wykorzystujemy następujące zbiory opensource:
| Zbiór danych | Robot | Link |
|---------|-------|------|
|Z1_StackBox| [Unitree Z1](https://www.unitree.com/z1)|[Huggingface](https://huggingface.co/datasets/unitreerobotics/Z1_StackBox_Dataset/tree/v2.1)|
|Z1_DualArm_StackBox|[Unitree Z1](https://www.unitree.com/z1)|[Huggingface](https://huggingface.co/datasets/unitreerobotics/Z1_Dual_Dex1_StackBox_Dataset/tree/v2.1)|
|Z1_DualArm_StackBox_V2|[Unitree Z1](https://www.unitree.com/z1)|[Huggingface](https://huggingface.co/datasets/unitreerobotics/Z1_Dual_Dex1_StackBox_Dataset_V2/tree/v2.1)|
|Z1_DualArm_Cleanup_Pencils|[Unitree Z1](https://www.unitree.com/z1)|[Huggingface](https://huggingface.co/datasets/unitreerobotics/Z1_Dual_Dex1_CleanupPencils_Dataset/tree/v2.1)|
|G1_Pack_Camera|[Unitree G1](https://www.unitree.com/g1)|[Huggingface](https://huggingface.co/datasets/unitreerobotics/G1_Dex1_MountCameraRedGripper_Dataset/tree/v2.1)|

Aby trenować na własnym zbiorze danych, najpierw przygotuj dane w formacie [Huggingface LeRobot V2.1](https://github.com/huggingface/lerobot). Załóżmy, że struktura katalogów źródłowych wygląda tak:
```
source_dir/
    ├── dataset1_name
    ├── dataset2_name
    ├── dataset3_name
    └── ...
```
Następnie skonwertuj dane do wymaganego formatu:
```python
cd prepare_data
python prepare_training_data.py \
    --source_dir /path/to/your/source_dir \
    --target_dir /path/to/save/the/converted/data \
    --dataset_name "dataset1_name" \
    --robot_name "a tag of the robot in the dataset" # e.g, Unitree Z1 Robot Arm or Unitree G1 Robot with Gripper.
```
Struktura wynikowa danych (Uwaga: trening wspiera tylko główną kamerę. Jeśli dataset ma wiele widoków, usuń odpowiednie wartości z kolumny ```data_dir``` w pliku CSV).
```
target_dir/
    ├── videos
    │     ├──dataset1_name
    │     │   ├──camera_view_dir
    │     │       ├── 0.mp4
    │     │       ├── 1.mp4
    │     │       └── ...
    │     └── ...
    ├── transitions
    │    ├── dataset1_name
    │        ├── meta_data
    │        ├── 0.h5
    │        ├── 1.h5
    │        └── ...
    └──  dataset1_name.csv
```
## 🚴‍♂️ Trening
A. Strategia treningu wygląda następująco:
- **Step 1**: Fine-tuning modelu generacji wideo jako world model na zbiorze [Open-X](https://robotics-transformer-x.github.io/); *Cel:* nauczenie modelu fizyki i dynamiki scen.
- **Step 2**: Post-trening $\text{UnifoLM-WMA}$ w trybie decision-making na docelowym zbiorze zadań; *Cel:* dopasowanie polityki do konkretnego zadania robota.
  <div align="left">
      <img src="assets/pngs/dm_mode.png" width="600">
  </div>
- **Step 3**: Post-trening $\text{UnifoLM-WMA}$ w trybie simulation na docelowym zbiorze zadań. *Cel:* poprawa jakości symulacji i przewidywania przyszłych interakcji.
  <div align="left">
      <img src="assets/pngs/sim_mode.png" width="600">
  </div>
**Uwaga**: Jeśli potrzebujesz $\text{UnifoLM-WMA}$ tylko w jednym trybie, możesz pominąć odpowiedni krok.

B. Aby przeprowadzić trening na jednym lub wielu zbiorach danych, wykonaj:
- **Step 1**: Maksymalne DoF ustawiono na 16; jeśli masz więcej DoF, zaktualizuj ```agent_state_dim``` i ```agent_action_dim``` w [configs/train/config.yaml](https://github.com/unitreerobotics/unifolm-wma/blob/working/configs/train/config.yaml). *Cel:* zgodność wymiarów stanu/akcji z realnym robotem.
- **Step 2**: Ustaw kształty wejść dla każdej modalności w [configs/train/meta.json](https://github.com/unitreerobotics/unitree-world-model/blob/main/configs/train/meta.json). *Cel:* poprawne mapowanie obrazów i stanu do modelu.
- **Step 3**: Skonfiguruj parametry treningu w [configs/train/config.yaml](https://github.com/unitreerobotics/unitree-world-model/blob/main/configs/train/config.yaml). Dla ```pretrained_checkpoint``` zalecamy " $\text{UnifoLM-WMA-0}_{Base}$ " wytrenowany na [Open-X](https://robotics-transformer-x.github.io/). *Cel:* start z sprawdzonych wag.
  ```yaml
  model:
      pretrained_checkpoint: /path/to/pretrained/checkpoint;
      ...
      decision_making_only: True # Train the world model only in decision-making mode. If False, jointly train it in both decision-making and simulation modes.
      ...
  data:
      ...
      train:
          ...
          data_dir: /path/to/training/dataset/directory
      dataset_and_weights: # list the name of each dataset below and make sure the summation of weights is 1.0
          dataset1_name: 0.2
          dataset2_name: 0.2
          dataset3_name: 0.2
      dataset4_name: 0.2
      dataset5_name: 0.2
  ```
- **Step 4**: Ustaw ```experiment_name``` oraz ```save_root``` w [scripts/train.sh](https://github.com/unitreerobotics/unitree-world-model/blob/main/scripts/train.sh). *Cel:* uporządkowany zapis wyników.
- **Step 5**: Uruchom trening:
```
bash scripts/train.sh
```
## 🌏 Inferencja w trybie Interactive Simulation
Aby uruchomić world model w trybie interaktywnej symulacji, wykonaj:
- **Step 1**: (Pomiń, jeśli używasz dostarczonych przykładów) Przygotuj własny prompt zgodnie z formatem z [examples/world_model_interaction_prompts](https://github.com/unitreerobotics/unitree-world-model/tree/main/examples/world_model_interaction_prompts). *Cel:* zapewnienie spójnego wejścia obraz + instrukcja.
  ```
  world_model_interaction_prompts/
    ├── images
    │    ├── dataset1_name
    │    │       ├── 0.png     # Image prompt
    │    │       └── ...
    │    └── ...
    ├── transitions
    │    ├── dataset1_name
    │    │       ├── meta_data # Used for normalization
    │    │       ├── 0.h       # Robot state and action data; in interaction mode,
    │    │       │             # only used to retrieve the robot state corresponding 
    │    │       │             # to the image prompt
    │    │       └── ...
    │    └── ...
    ├──  dataset1_name.csv     # File for loading image prompts, text instruction and corresponding robot states
    └── ...
  ```
- **Step 2**: Wskaż poprawne ścieżki dla ```pretrained_checkpoint``` (np. $\text{UnifoLM-WMA-0}_{Dual}$) i ```data_dir``` w [configs/inference/world_model_interaction.yaml](https://github.com/unitreerobotics/unitree-world-model/blob/main/configs/inference/world_model_interaction.yaml). *Cel:* model musi wiedzieć, skąd pobrać wagi i dane.
- **Step 3**: Ustaw ```checkpoint```, ```res_dir``` i ```prompt_dir``` w [scripts/run_world_model_interaction.sh](https://github.com/unitreerobotics/unitree-world-model/blob/main/scripts/run_world_model_interaction.sh) oraz wpisz nazwy datasetów w ```datasets=(...)```. Następnie uruchom:
    ```
    bash scripts/run_world_model_interaction.sh
    ```

## 🧠 Inferencja i wdrożenie w trybie Decision-Making

W tym wariancie inferencja działa na serwerze, a klient robota zbiera obserwacje z robota rzeczywistego i wysyła je do serwera po akcje. Ten podział ułatwia uruchomienie ciężkich obliczeń na GPU oraz utrzymuje szybki loop sterowania na robocie.

### Konfiguracja serwera:
- **Step-1**: Ustaw ```ckpt```, ```res_dir```, ```datasets``` w [scripts/run_real_eval_server.sh](https://github.com/unitreerobotics/unifolm-world-model-action/blob/main/scripts/run_real_eval_server.sh). *Cel:* wskazanie wag modelu i katalogu wyników.
- **Step-2**: Skonfiguruj ```data_dir``` oraz ```dataset_and_weights``` w [config/inference/world_model_decision_making.yaml](https://github.com/unitreerobotics/unifolm-world-model-action/blob/f12b4782652ca00452941d851b17446e4ee7124a/configs/inference/world_model_decision_making.yaml#L225). *Cel:* poprawne wczytanie danych wejściowych.
- **Step-3**: Uruchom serwer:
```
conda activate unifolm-wma
cd unifolm-world-model-action
bash scripts/run_real_eval_server.sh
```

### Konfiguracja klienta
- **Step-1**: Wykonaj instrukcje z [unitree_deploy/README.md](https://github.com/unitreerobotics/unifolm-world-model-action/blob/main/unitree_deploy/README.md), aby utworzyć środowisko ```unitree_deploy```, zainstalować pakiety i uruchomić kontrolery na robocie.
- **Step-2**: Otwórz nowy terminal i zestaw tunel SSH z klienta do serwera:
```
ssh user_name@remote_server_IP -CNg -L 8000:127.0.0.1:8000
```
- **Step-3**: Uruchom ```unitree_deploy/robot_client.py```, aby rozpocząć inferencję:
```
cd unitree_deploy
python scripts/robot_client.py --robot_type "g1_dex1" --action_horizon 16 --exe_steps 16 --observation_horizon 2 --language_instruction "pack black camera into box" --output_dir ./results --control_freq 15
```

## 🎓 Zastosowanie w projekcie Unitree G1 EDU-U6
Poniższa sekcja podsumowuje, jak studenci mogą wykorzystać repozytorium w projekcie z robotem humanoidalnym Unitree G1 EDU-U6:
- **Cel projektu**: nauczyć się, jak world model wspiera sterowanie robotem, przewidywanie przyszłych stanów oraz planowanie ruchu.
- **Zakres prac**: przygotowanie danych z kamery i stanu robota, uruchomienie serwera decision-making, wywołanie klienta na robocie oraz analiza wygenerowanych akcji.
- **Praktyczny scenariusz**:
  1) Zbierz krótkie demonstracje z G1 EDU-U6 (kamera + qpos) i przekonwertuj je do formatu LeRobot.
  2) Skonfiguruj training na bazie $\text{UnifoLM-WMA-0}_{Base}$, aby dostroić model do zadania (np. pakowanie obiektu).
  3) Uruchom serwer inferencji na stacji z GPU i klienta na robocie, przekazując instrukcję językową oraz parametry horyzontu akcji.
  4) Przeanalizuj zapisane wideo i logi, aby ocenić stabilność i jakość działania.

## 📝 Architektura kodu
Poniżej znajduje się uproszczony przegląd struktury i głównych komponentów projektu:
```
unitree-world-model/
    ├── assets                      # Media (GIF, obrazy, wideo demonstracyjne)
    ├── configs                     # Konfiguracje treningu i inferencji
    │    ├── inference
    │    └──  train
    ├── examples                    # Przykładowe wejścia i prompty do inferencji
    ├── external                    # Pakiety zewnętrzne
    ├── prepare_data                # Skrypty preprocessingu i konwersji datasetów
    ├── scripts                     # Skrypty treningu, ewaluacji i wdrożenia
    ├── src
    │    ├──unitree_worldmodel      # Główny pakiet Pythona dla Unitree world model
    │    │      ├── data            # Ładowanie datasetów, transformacje, dataloadery
    │    │      ├── models          # Architektury modeli i backbone
    │    │      ├── modules         # Moduły i komponenty modelu
    │    │      └──  utils          # Narzędzia pomocnicze
    └── unitree_deploy              # Kod wdrożeniowy
```

## 🙏 Podziękowania
Duża część kodu pochodzi z [DynamiCrafter](https://github.com/Doubiiu/DynamiCrafter), [Diffusion Policy](https://github.com/real-stanford/diffusion_policy), [ACT](https://github.com/MarkFzp/act-plus-plus) oraz [HPT](https://github.com/liruiw/HPT).

## 📝 Cytowanie
```
@misc{unifolm-wma-0,
  author       = {Unitree},
  title        = {UnifoLM-WMA-0: A World-Model-Action (WMA) Framework under UnifoLM Family},
  year         = {2025},
}
```
