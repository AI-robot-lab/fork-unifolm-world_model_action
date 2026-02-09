# Nazwa eksperymentu widoczna w katalogu wyników.
model_name=testing
# Ścieżka do checkpointu z wagami modelu.
ckpt=/path/to/model/checkpoint
# Konfiguracja inferencji w trybie interakcyjnej symulacji.
config=configs/inference/world_model_interaction.yaml
# Ziarno losowe dla powtarzalności wyników.
seed=123
# Katalog docelowy na materiały wideo.
res_dir="/path/to/result/directory"

# Lista datasetów do interaktywnej symulacji.
datasets=(
    "unitree_z1_stackbox"
    "unitree_z1_dual_arm_stackbox"
    "unitree_z1_dual_arm_stackbox_v2"
    "unitree_z1_dual_arm_cleanup_pencils"
    "unitree_g1_pack_camera"
)

# Liczba iteracji dla każdego datasetu (dopasowana do długości trajektorii).
n_iters=(12 7 11 8 11)
# Frame stride dla poszczególnych datasetów.
fses=(4 4 4 4 6)

for i in "${!datasets[@]}"; do
    dataset=${datasets[$i]}
    n_iter=${n_iters[$i]}
    fs=${fses[$i]}

    # Uruchom skrypt interakcji world modelu i zapisz wyniki do katalogu.
    CUDA_VISIBLE_DEVICES=0 python3 scripts/evaluation/world_model_interaction.py \
    --seed ${seed} \
    --ckpt_path $ckpt \
    --config $config \
    --savedir "${res_dir}/${model_name}/${dataset}" \
    --bs 1 --height 320 --width 512 \
    --unconditional_guidance_scale 1.0 \
    --ddim_steps 50 \
    --ddim_eta 1.0 \
    --prompt_dir "/path/to/unifolm-world-model-action/examples/world_model_interaction_prompts" \
    --dataset ${dataset} \
    --video_length 16 \
    --frame_stride ${fs} \
    --n_action_steps 16 \
    --exe_steps 16 \
    --n_iter ${n_iter} \
    --timestep_spacing 'uniform_trailing' \
    --guidance_rescale 0.7 \
    --perframe_ae
done
