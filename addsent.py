import v2enlib as v2l


def signalHandler(sig, handle):
    if v2l.libs.const.main_execute:
        print("\tStop program!")
        main_execute = False


def on_press(key):
    with v2l.libs.contextlib.suppress(AttributeError):
        if key.char == "z" and v2l.libs.const.main_execute:
            v2l.libs.os.kill(v2l.libs.os.getpid(), v2l.libs.signal.SIGINT)


class ExitButton:
    def __init__(self, func, **kwargs):
        if v2l.libs.const.allow_GUI:
            self.root = v2l.libs.tk.Tk()
            self.root.title("My App")
            self.button = v2l.tk.Button(
                self.root, text="Turn Off", command=self.turn_off
            )
            self.button.pack()
            self.thread = v2l.libs.Process(
                target=self.run_loop, kwargs={"func": func, "kwargs": kwargs}
            )
            self.thread.start()
            self.root.mainloop()
            self.thread.join()
        else:
            func(**kwargs)

    def run_loop(self, func, kwargs):
        func(**kwargs)

        if v2l.libs.const.allow_GUI and self.root.winfo_exists():
            self.root.destroy()

    def turn_off(self):
        self.root.destroy()
        if v2l.libs.const.main_execute:
            v2l.libs.os.kill(v2l.libs.os.getpid(), v2l.libs.signal.SIGINT)


def saveFiles(
    saveIN,
    saveOU,
    first_dump_sents,
    second_dump_sents,
    first_dictionary_path,
    second_dictionary_path,
    first_dictionary,
    second_dictionary,
):
    v2l.language.saveDictionary(first_dictionary_path, first_dictionary)
    v2l.language.saveDictionary(second_dictionary_path, second_dictionary)
    with open(v2l.libs.const.first_path, "w") as file:
        file.writelines(saveIN)
    with open(v2l.libs.const.second_path, "w") as file:
        file.writelines(saveOU)
    with open(f"./data/{v2l.libs.const.first_lang}.dump", "a") as f:
        for sent in first_dump_sents:
            f.write(f"{sent}\n")
    with open(f"./data/{v2l.libs.const.second_lang}.dump", "a") as f:
        for sent in second_dump_sents:
            f.write(f"{sent}\n")


def safeExecute(saveIN, saveOU, first_dictionary, second_dictionary, fargs):
    false_count, first_dump_sents, second_dump_sents, exe_count, cmds = 0, [], [], 0, []
    while v2l.libs.const.main_execute:
        # pre run section
        time_start = v2l.libs.time.time()
        if v2l.utils.emptyFile(v2l.libs.const.first_path) or v2l.utils.emptyFile(
            v2l.libs.const.second_path
        ):
            print("Done!")
            break
        first_dump_sent, second_dump_sent = [], []

        # run section
        for e in v2l.utils.functionPool(
            v2l.language.addSentExecutor,
            [
                [
                    v2l.language.InputSent(saveIN[idx], saveOU[idx]),
                    first_dictionary,
                    second_dictionary,
                ]
                for idx in range(
                    v2l.libs.const.num_sent
                    if min(len(saveIN), len(saveOU)) > v2l.libs.const.num_sent
                    else min(len(saveIN), len(saveOU))
                )
            ],
            v2l.libs.Pool,
            strictOrder=True,
            poolName="addSent",
        ):
            if e[0] != "" and e[1] != "":
                first_dump_sent.append(e[0])
                second_dump_sent.append(e[1])
            cmds.extend(i for i in e[2] if i)
            false_count += -false_count if e[3] else 1
            if (
                false_count > v2l.libs.const.false_allow
                and v2l.libs.const.main_execute
                and not v2l.libs.const.limit_false_translation
            ):
                v2l.utils.printError(
                    "mainModule", Exception("Too many fatal translation!"), True
                )
                v2l.libs.const.main_execute = False

        # post run section
        second_dump_sents += second_dump_sent
        first_dump_sents += first_dump_sent
        saveOU = saveOU[v2l.libs.const.num_sent :]
        saveIN = saveIN[v2l.libs.const.num_sent :]
        cmds = [list(x) for x in {tuple(x) for x in cmds}]

        print(
            f"\t\t(mainModule) time consume: {(v2l.libs.time.time()-time_start):0,.2f} ({len(cmds)})",
        )
        del first_dump_sent, second_dump_sent
        v2l.libs.gc.collect()
        exe_count += len(cmds)
        if exe_count >= fargs.amount_exe:
            break

    # save files
    if v2l.libs.const.main_execute:
        v2l.SQL.createOBJPool(cmds)
        saveFiles(
            saveIN,
            saveOU,
            first_dump_sents,
            second_dump_sents,
            v2l.libs.const.first_dictionary_path,
            v2l.libs.const.second_dictionary_path,
            first_dictionary,
            second_dictionary,
        )


def unsafeExecute(saveIN, saveOU, sql_connection, first_dictionary, second_dictionary):
    false_count, first_dump_sents, second_dump_sents = 0, [], []
    global main_execute


def main(fargs):
    # premain section
    if not fargs.ci_cd:
        v2l.utils.playNotes(*v2l.libs.const.sound_tracks["macos_startup"])
        listener = keyboard.Listener(on_press=on_press)
        listener.start()
    v2l.libs.signal.signal(v2l.libs.signal.SIGINT, signalHandler)

    # init dictionaries
    v2l.language.checkLangFile(v2l.libs.const.first_lang, v2l.libs.const.second_lang)
    first_dictionary = v2l.language.loadDictionary(v2l.libs.const.first_dictionary_path)
    second_dictionary = v2l.language.loadDictionary(v2l.libs.const.second_dictionary_path)
    # init inputs
    with open(v2l.libs.const.first_path, "r") as first_file:
        with open(v2l.libs.const.second_path, "r") as second_file:
            saveIN, saveOU = first_file.read().splitlines(
                True
            ), second_file.read().splitlines(True)

    # main section
    if v2l.libs.const.safe_execute:
        ExitButton(
            safeExecute,
            saveIN=saveIN,
            saveOU=saveOU,
            first_dictionary=first_dictionary,
            second_dictionary=second_dictionary,
            fargs=fargs,
        )

    # postmain section
    if not fargs.ci_cd:
        v2l.utils.playNotes(*v2l.libs.const.sound_tracks["windows7_shutdown"])


if __name__ == "__main__":
    # init program parse
    parser = v2l.libs.argparse.ArgumentParser()
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
        default="sentences",
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
        v2l.libs.const.thread_alow = False
    if not fargs.ci_cd:
        from pynput import keyboard
    else:
        v2l.libs.const.disableTQDM = True
    v2l.libs.const.worksheet_name = fargs.test
    # execute program
    main(fargs)
