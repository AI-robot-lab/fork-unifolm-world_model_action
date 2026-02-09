import argparse
import os
import time
import cv2
import numpy as np
import torch
import tqdm

from typing import Any, Deque, MutableMapping, OrderedDict
from collections import deque
from pathlib import Path

from unitree_deploy.real_unitree_env import make_real_env
from unitree_deploy.utils.eval_utils import (
    ACTTemporalEnsembler,
    LongConnectionClient,
    populate_queues,
)

# -----------------------------------------------------------------------------
# Domyślne ustawienia sieci i środowiska
# -----------------------------------------------------------------------------
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""
HOST = "127.0.0.1"
PORT = 8000
BASE_URL = f"http://{HOST}:{PORT}"

# fmt: off
INIT_POSE = {
    'g1_dex1': np.array([0.10559805, 0.02726714, -0.01210221, -0.33341318, -0.22513399, -0.02627627, -0.15437093,  0.1273793 , -0.1674708 , -0.11544029, -0.40095493,  0.44332668,  0.11566751,  0.3936641, 5.4, 5.4], dtype=np.float32),
    'z1_dual_dex1_realsense': np.array([-1.0262332,  1.4281361, -1.2149128,  0.6473399, -0.12425245, 0.44945636,  0.89584476,  1.2593982, -1.0737865,  0.6672816, 0.39730102, -0.47400007, 0.9894176, 0.9817477 ], dtype=np.float32),
    'z1_realsense': np.array([-0.06940782, 1.4751548, -0.7554075, 1.0501366, 0.02931615, -0.02810347, -0.99238837], dtype=np.float32),
}
ZERO_ACTION = {
    'g1_dex1': torch.zeros(16, dtype=torch.float32),
    'z1_dual_dex1_realsense': torch.zeros(14, dtype=torch.float32),
    'z1_realsense': torch.zeros(7, dtype=torch.float32),
}
CAM_KEY = {
    'g1_dex1': 'cam_right_high',
    'z1_dual_dex1_realsense': 'cam_high',
    'z1_realsense': 'cam_high',
}
# fmt: on


def prepare_observation(args: argparse.Namespace, obs: Any) -> OrderedDict:
    """
    Konwertuje surową obserwację środowiska na słownik wejściowy wymagany przez model.
    """
    rgb_image = cv2.cvtColor(
        obs.observation["images"][CAM_KEY[args.robot_type]], cv2.COLOR_BGR2RGB)
    observation = {
        "observation.images.top":
        torch.from_numpy(rgb_image).permute(2, 0, 1),
        "observation.state":
        torch.from_numpy(obs.observation["qpos"]),
        "action": ZERO_ACTION[args.robot_type],
    }
    return OrderedDict(observation)


def run_policy(
    args: argparse.Namespace,
    env: Any,
    client: LongConnectionClient,
    temporal_ensembler: ACTTemporalEnsembler,
    cond_obs_queues: MutableMapping[str, Deque[torch.Tensor]],
    output_dir: Path,
) -> None:
    """
    Pojedyncza pętla rollout:
        1) ustawia robota w pozycji startowej,
        2) strumieniuje obserwacje,
        3) pobiera akcje z serwera polityki,
        4) wykonuje je z uśrednianiem czasowym dla płynniejszego sterowania.
    """

    _ = env.step(INIT_POSE[args.robot_type])
    time.sleep(2.0)
    t = 0

    while True:
        # Pobierz aktualną obserwację robota i środowiska.
        obs = env.get_observation(t)
        # Sformatuj obserwację do postaci wejściowej dla modelu.
        obs = prepare_observation(args, obs)
        cond_obs_queues = populate_queues(cond_obs_queues, obs)
        # Wyślij obserwacje na serwer i pobierz przewidywane akcje.
        pred_actions = client.predict_action(args.language_instruction,
                                             cond_obs_queues).unsqueeze(0)
        # Zachowaj horyzont akcji i zastosuj wygładzanie czasowe.
        actions = temporal_ensembler.update(
            pred_actions[:, :args.action_horizon])[0]

        # Wykonuj akcje w pętli sterowania w czasie rzeczywistym.
        for n in range(args.exe_steps):
            action = actions[n].cpu().numpy()
            print(f">>> Exec => step {n} action: {action}", flush=True)
            print("---------------------------------------------")

            # Zachowaj częstotliwość sterowania `control_freq` Hz.
            t1 = time.time()
            obs = env.step(action)
            time.sleep(max(0, 1 / args.control_freq - time.time() + t1))
            t += 1

            # Uzupełnij kolejkę obserwacji dla kolejnego kroku (oprócz ostatniego).
            if n < args.exe_steps - 1:
                obs = prepare_observation(args, obs)
                cond_obs_queues = populate_queues(cond_obs_queues, obs)


def run_eval(args: argparse.Namespace) -> None:
    client = LongConnectionClient(BASE_URL)

    # Zainicjalizuj czasowe uśrednianie ACT, aby ograniczyć drgania ruchu.
    temporal_ensembler = ACTTemporalEnsembler(temporal_ensemble_coeff=0.01,
                                              chunk_size=args.action_horizon,
                                              exe_steps=args.exe_steps)
    temporal_ensembler.reset()

    # Utwórz kolejki obserwacji oraz akcji dla zadanego horyzontu czasowego.
    cond_obs_queues = {
        "observation.images.top": deque(maxlen=args.observation_horizon),
        "observation.state": deque(maxlen=args.observation_horizon),
        "action": deque(
            maxlen=16),  # UWAGA: model przewiduje z wyprzedzeniem 16 kroków
    }

    env = make_real_env(
        robot_type=args.robot_type,
        dt=1 / args.control_freq,
    )
    env.connect()

    try:
        for episode_idx in tqdm.tqdm(range(0, args.num_rollouts_planned)):
            output_dir = Path(args.output_dir) / f"episode_{episode_idx:03d}"
            output_dir.mkdir(parents=True, exist_ok=True)
            run_policy(args, env, client, temporal_ensembler, cond_obs_queues,
                       output_dir)
    finally:
        env.close()
    env.close()


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--robot_type",
                        type=str,
                        default="g1_dex1",
                        help="Typ platformy robota.")
    parser.add_argument(
        "--action_horizon",
        type=int,
        default=16,
        help="Liczba przyszłych akcji przewidzianych przez politykę.",
    )
    parser.add_argument(
        "--exe_steps",
        type=int,
        default=16,
        help=
        "Liczba przyszłych akcji do wykonania (mniejsza niż action_horizon).",
    )
    parser.add_argument(
        "--observation_horizon",
        type=int,
        default=2,
        help="Liczba ostatnich klatek/stadiów używana w obserwacji.",
    )
    parser.add_argument(
        "--language_instruction",
        type=str,
        default="Pack black camera into box",
        help="Instrukcja językowa przekazywana do serwera polityki.",
    )
    parser.add_argument("--num_rollouts_planned",
                        type=int,
                        default=10,
                        help="Liczba planowanych rolloutów.")
    parser.add_argument("--output_dir",
                        type=str,
                        default="./results",
                        help="Katalog zapisu wyników.")
    parser.add_argument("--control_freq",
                        type=float,
                        default=30,
                        help="Częstotliwość sterowania niskiego poziomu w Hz.")
    return parser


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    run_eval(args)
