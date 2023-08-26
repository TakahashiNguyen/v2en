from argparse import ArgumentParser
from contextlib import suppress
from multiprocessing import Process
from multiprocessing.pool import Pool as mpPool
import os, signal, time, gc

import v2enlib as v2l


def signalHandler(sig, handle):
    if v2l.config.main_execute:
        print("\tStop program!")
        v2l.config.main_execute = False


def on_press(key):
    with suppress(AttributeError):
        if key.char == "z" and v2l.config.main_execute:
            os.kill(os.getpid(), signal.SIGINT)


class ExitButton:
    def __init__(self, func, **kwargs):
        if v2l.config.v2en.allow.GUI:
            import tkinter as tk

            self.root = tk.Tk()
            self.root.title("My App")
            self.button = tk.Button(self.root, text="Turn Off", command=self.turn_off)
            self.button.pack()
            self.thread = Process(
                target=self.run_loop, kwargs={"func": func, "kwargs": kwargs}
            )
            self.thread.start()
            self.root.mainloop()
            self.thread.join()
        else:
            func(**kwargs)

    def run_loop(self, func, kwargs):
        func(**kwargs)

        if v2l.config.v2en.allow.GUI and self.root.winfo_exists():
            self.root.destroy()

    def turn_off(self):
        self.root.destroy()
        if v2l.config.main_execute:
            os.kill(os.getpid(), signal.SIGINT)


def saveFiles(
    saveIN,
    saveOU,
    first_dump_sents,
    second_dump_sents,
    flang,
    slang,
    fdictionary,
    sdictionary,
):
    v2l.Language.saveDictionary(flang, fdictionary)
    v2l.Language.saveDictionary(slang, sdictionary)

    with open(v2l.config.v2en.first_path, "w") as file:
        file.writelines(saveIN)
    with open(v2l.config.v2en.second_path, "w") as file:
        file.writelines(saveOU)

    fsh = v2l.GSQLClass(v2l.config.v2en.sheet, f"dump_{flang}")
    ssh = v2l.GSQLClass(v2l.config.v2en.sheet, f"dump_{slang}")
    fsh.writeLRow([[e] for e in first_dump_sents])
    ssh.writeLRow([[e] for e in second_dump_sents])
    fsh.autoFit(), ssh.autoFit()


def safeExecute(saveIN, saveOU, fdictionary, sdictionary, fargs):
    false_count, first_dump_sents, second_dump_sents, exe_count, cmds = 0, [], [], 0, []
    while v2l.config.main_execute:
        # pre run section
        time_start, pre_cmd = time.time(), len(cmds)
        if v2l.utils.emptyFile(v2l.config.v2en.first_path) or v2l.utils.emptyFile(
            v2l.config.v2en.second_path
        ):
            print("Done!")
            break
        first_dump_sent, second_dump_sent = [], []

        # run section
        for e in v2l.Pool.function(
            func=v2l.Executor.addSent,
            iterable=[
                [
                    v2l.InputSent(saveIN[idx], saveOU[idx]),
                    fdictionary,
                    sdictionary,
                ]
                for idx in range(
                    v2l.config.v2en.num_sent
                    if min(len(saveIN), len(saveOU)) > v2l.config.v2en.num_sent
                    else min(len(saveIN), len(saveOU))
                )
            ],
        ):
            if e[0] != "" and e[1] != "":
                first_dump_sent.append(e[0])
                second_dump_sent.append(e[1])
            cmds.extend(i for i in e[2] if i)
            false_count += -false_count if e[3] else 1
            fdictionary += e[4]
            sdictionary += e[5]
            if (
                false_count > v2l.config.v2en.false_allow
                and v2l.config.main_execute
                and not v2l.config.v2en.allow.FalseTranslation
            ):
                v2l.utils.printError(
                    "mainModule", Exception("Too many fatal translation!"), True
                )
                v2l.config.main_execute = False

        # post run section
        second_dump_sents += second_dump_sent
        first_dump_sents += first_dump_sent
        saveOU = saveOU[v2l.config.v2en.num_sent :]
        saveIN = saveIN[v2l.config.v2en.num_sent :]
        cmds = [list(x) for x in {tuple(x) for x in cmds}]

        print(
            f"\t\t(mainModule) time consume: {(time.time()-time_start):0,.2f} ({len(cmds)})",
        )
        del first_dump_sent, second_dump_sent
        gc.collect()
        exe_count += len(cmds) - pre_cmd
        if exe_count >= fargs.amount_exe:
            break

    # save files
    if v2l.config.main_execute:
        sh = v2l.GSQLClass(v2l.config.v2en.sheet, v2l.config.v2en.worksheet)
        sh.writeLRow(cmds), sh.autoFit()
        saveFiles(
            saveIN,
            saveOU,
            first_dump_sents,
            second_dump_sents,
            v2l.config.v2en.flang,
            v2l.config.v2en.slang,
            fdictionary,
            sdictionary,
        )


def unsafeExecute(saveIN, saveOU, sql_connection, fdictionary, sdictionary):
    false_count, first_dump_sents, second_dump_sents = 0, [], []


def main(fargs):
    # premain section
    if not fargs.ci_cd:
        v2l.utils.playNotes(*v2l.config.v2en.sound_tracks["macos_startup"])
        listener = keyboard.Listener(on_press=on_press)
        listener.start()
    signal.signal(signal.SIGINT, signalHandler)

    # init dictionaries
    fdictionary = v2l.Language.loadDictionary(v2l.config.v2en.flang)
    sdictionary = v2l.Language.loadDictionary(v2l.config.v2en.slang)
    # init inputs
    with open(v2l.config.v2en.first_path, "r") as first_file:
        with open(v2l.config.v2en.second_path, "r") as second_file:
            saveIN, saveOU = first_file.read().splitlines(
                True
            ), second_file.read().splitlines(True)

    # main section
    if v2l.config.v2en.safe_execute:
        ExitButton(
            safeExecute,
            saveIN=saveIN,
            saveOU=saveOU,
            fdictionary=fdictionary,
            sdictionary=sdictionary,
            fargs=fargs,
        )

    # postmain section
    if not fargs.ci_cd:
        v2l.Sound.playNotes(*v2l.config.v2en.sound_tracks["windows7_shutdown"])


if __name__ == "__main__":
    # init program parse
    parser = ArgumentParser()
    parser.add_argument(
        "--amount-exe",
        type=int,
        help="enter amount of execute to translate a number of sentence and add to .db",
        nargs="?",
        default=0,
    )
    parser.add_argument(
        "--ci_cd",
        type=bool,
        help="run addsent.py on ci/cd environment",
        nargs="?",
        default=False,
        const=True,
    )
    parser.add_argument(
        "--test",
        help="worksheet name to save output",
        nargs="?",
        const="test",
        default=v2l.config.v2en.worksheet,
    )
    parser.add_argument(
        "--disable-thread",
        type=bool,
        help="disable thread feature for addsent.py",
        nargs="?",
        default=False,
        const=True,
    )
    fargs = parser.parse_args()
    # reconfig program value
    if fargs.disable_thread:
        v2l.config.v2en.thread_alow = False
    if not fargs.ci_cd:
        from pynput import keyboard
    else:
        v2l.config.v2en.allow.tqdm = False
    v2l.config.v2en.worksheet = fargs.test
    # execute program
    main(fargs)
