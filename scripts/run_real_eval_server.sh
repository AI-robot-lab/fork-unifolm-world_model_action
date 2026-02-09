# Nazwa eksperymentu widoczna w katalogu wyników.
model_name=testing
# Ścieżka do checkpointu z wagami modelu UnifoLM-WMA-0.
ckpt=/path/to/model/checkpoint
# Konfiguracja inferencji w trybie decision-making.
config=configs/inference/world_model_decision_making.yaml
# Ziarno losowe dla powtarzalności eksperymentów.
seed=123
# Katalog, w którym zapiszemy wygenerowane wyniki.
res_dir="path/to/results/directory"
# Lista datasetów, które mają zostać przetworzone przez serwer.
datasets=(
    "unitree_g1_pack_camera"
)


for dataset in "${datasets[@]}"; do
    # Uruchom serwer inferencji dla jednego zbioru danych i zapisz wideo wynikowe.
    CUDA_VISIBLE_DEVICES=0 python3 scripts/evaluation/real_eval_server.py \
    --seed ${seed} \
    --ckpt_path $ckpt \
    --config $config \
    --savedir "${res_dir}/${dataset}/${model_name}/videos" \
    --bs 1 --height 320 --width 512 \
    --unconditional_guidance_scale 1.0 \
    --ddim_steps 16 \
    --ddim_eta 1.0 \
    --video_length 16 \
    --frame_stride 2 \
    --timestep_spacing 'uniform_trailing' \
    --guidance_rescale 0.7 \
    --perframe_ae
done
