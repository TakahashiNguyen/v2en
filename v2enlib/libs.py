import yaml, tensorflow_model_optimization as tfmot, tensorflow as tf
from oauth2client.service_account import ServiceAccountCredentials
from tqdm import tqdm
from difflib import SequenceMatcher
from multiprocess.pool import ThreadPool
from multiprocess.context import TimeoutError as TLE
import gspread, scipy
from translators import server as TransServer
from tabulate import tabulate
from functools import lru_cache
import string, httpx, gc, contextlib, os
import deep_translator.exceptions, langcodes, requests
import signal, time, argparse
from multiprocessing import Process
from multiprocessing.pool import Pool
import logging, resource, librosa, numpy as np
import hashlib, soundfile as sf, platform, subprocess


class CFG:
    def __init__(self) -> None:
        try:
            with open("config.yml", "r") as ymlfile:
                cfg = yaml.safe_load(ymlfile)
            self.target = cfg["v2en"]["target"]
            self.first_lang = self.target[:2]
            self.second_lang = self.target[-2:]
            self.accept_percentage = cfg["v2en"]["accept_percentage"]
            self.time_allow = cfg["v2en"]["allow"]["time"]
            self.resource_allow = cfg["v2en"]["allow"]["resource"]
            self.thread_alow = cfg["v2en"]["thread"]["allow"]
            self.thread_limit = cfg["v2en"]["thread"]["limit"]
            self.trans_timeout = cfg["v2en"]["trans_timeout"]
            self.initial_sparsity = cfg["training"]["initial_sparsity"]
            self.final_sparsity = cfg["training"]["final_sparsity"]
            self.begin_step = cfg["training"]["begin_step"]
            self.end_step = cfg["training"]["end_step"]
            self.learning_rate = cfg["training"]["learning_rate"]
            self.allow_pruning = cfg["training"]["allow_pruning"]
            self.disableTQDM = not cfg["v2en"]["allow"]["tqdm"]
            self.worksheet_name = "test"
            self.pruning_params = {
                "pruning_schedule": tfmot.sparsity.keras.PolynomialDecay(
                    initial_sparsity=self.initial_sparsity,
                    final_sparsity=self.final_sparsity,
                    begin_step=self.begin_step,
                    end_step=self.end_step,
                ),
            }
            self.trans_dict = TransServer.TranslatorsServer().translators_dict
            self.sound_tracks = {
                "macos_startup": [
                    ["F#2", "C#3", "F#3", "C#4", "F#4", "A#4"],
                    [5 / 3] * 6,
                    [0] * 6,
                ],
                "windows7_shutdown": [
                    ["G#4", "E4", "B4", "C5"],
                    [0.25, 0.25, 0.25, 0.25],
                    [0.0, 0.3, 0.6, 0.9],
                ],
            }
            self.num_sent = cfg["v2en"]["num_sent"]
            self.allow_GUI = cfg["v2en"]["allow"]["GUI"]
            self.first_lang = self.target[:2]
            self.second_lang = self.target[-2:]
            self.safe_execute = cfg["v2en"]["safe_execute"]
            self.limit_false_translation = cfg["v2en"]["allow"]["FalseTranslation"]
            if self.allow_GUI:
                import tkinter as tk
            self.first_dictionary_path, self.second_dictionary_path = (
                f"./cache/{self.first_lang}.dic",
                f"./cache/{self.second_lang}.dic",
            )
            self.first_path, self.second_path = (
                f"./data/{self.first_lang}.txt",
                f"./data/{self.second_lang}.txt",
            )
            self.main_execute = True
            self.false_allow = self.num_sent / 2 * 3
        except Exception as e:
            print("error while importing config\n", e)
            exit()


const = CFG()
