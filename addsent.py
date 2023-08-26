from argparse import ArgumentParser
from config import ExtraConfig, config as cconfig
from v2enlib import utils, Language, Executor, InputSent, GSQLClass, Pool
from multiprocessing import Manager, Process, current_process

import signal, os, time, gc


def initArgs(config: ExtraConfig):
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
        default=config.v2en.worksheet,
    )

    parser.add_argument(
        "--disable-thread",
        type=bool,
        help="disable thread feature for addsent.py",
        nargs="?",
        default=False,
        const=True,
    )

    return parser.parse_args()


class Execute:
    def __init__(self, func, config: ExtraConfig) -> None:
        self.config = config
        with Manager() as manager:
            if config.v2en.allow.GUI:
                import tkinter as tk

                self.root = tk.Tk()
                self.root.title("[v2en] AddSent.py")
                self.button = tk.Button(self.root, text="Exit", command=self.exit)
                self.button.pack()
                self.thread = Process(target=self.loop, args=(func, manager))
                self.thread.start()
                self.root.mainloop()
                self.thread.join()
            else:
                func(manager)

    def loop(self, func, manger: Manager):
        func(manger)

        if self.config.v2en.allow.GUI and self.root.winfo_exists():
            self.root.destroy()

    def exit(self):
        self.root.destroy()
        if self.config.main_execute:
            os.kill(os.getpid(), signal.SIGINT)


class Main:
    def __init__(self, args, config: ExtraConfig) -> None:
        if args.disable_thread:
            config.v2en.thread.allow = False
        if args.ci_cd:
            config.v2en.allow.tqdm = False
        config.v2en.worksheet = args.test

        self.args = args
        self.config = config
        self.cmds = []
        self.main()

    def signalHandler(self):
        if self.config.main_execute:
            print("Stop programme!")
            self.config.main_execute = False

    def handelEnvironment(self):
        if not self.args.ci_cd:
            utils.Sound.playNotes(*self.config.v2en.sound_tracks["macos_startup"])
        signal.signal(signal.SIGINT, self.signalHandler)

    def initValues(self):
        self.fdictionary = Language.loadDictionary(
            self.config.v2en.flang, self.config.v2en.sheet
        )
        self.sdictionary = Language.loadDictionary(
            self.config.v2en.slang, self.config.v2en.sheet
        )

        with open(self.config.v2en.fpath, "r") as ffile:
            self.fsent = ffile.read().splitlines(True)
        with open(self.config.v2en.spath, "r") as sfile:
            self.ssent = sfile.read().splitlines(True)
        self.config.main_execute = self.fsent and self.ssent

    def inputList(self, num_exe: int):
        return [
            [
                InputSent(self.fsent[idx], self.ssent[idx]),
                self.fdictionary,
                self.sdictionary,
                self.cmds,
                self.config,
            ]
            for idx in range(num_exe)
        ]

    def mainExecute(self, manager: Manager):
        self.fdictionary = manager.list(self.fdictionary)
        self.sdictionary = manager.list(self.sdictionary)
        self.cmds = manager.list(self.cmds)
        false_count, fdump_sents, sdump_sents = 0, [], []
        while self.config.main_execute and self.fsent and self.ssent:
            time_start, pre_cmds = time.time(), len(self.cmds)

            num_exe = min(len(self.fsent), len(self.ssent), self.config.v2en.num_sent)
            for e in Pool.function(
                func=Executor.addSent,
                iterable=self.inputList(num_exe=num_exe),
                force_pro=num_exe,
            ):
                if e[0] and e[1]:
                    fdump_sents.append(e[0])
                    sdump_sents.append(e[1])
                false_count += -false_count if e[2] else 1
                if (
                    false_count > self.config.v2en.false_allow
                    and self.config.main_execute
                    and not self.config.v2en.allow.FalseTranslation
                ):
                    utils.debuger.printError(
                        self.mainExecute.__name__,
                        Exception("Too many fatal traslation!"),
                        True,
                    )
                    self.config.main_execute = False
            self.fsent = self.fsent[self.config.v2en.num_sent :]
            self.ssent = self.ssent[self.config.v2en.num_sent :]

            gc.collect()
            self.cmds = manager.list(
                [elem for i, elem in enumerate(self.cmds) if elem not in self.cmds[:i]]
            )
            print(
                f"\t\t({self.mainExecute.__name__}@{current_process().name}) time consume:\
                {(time.time()-time_start):0,.2f} ({len(self.cmds)}) ({len(self.cmds)-pre_cmds})"
            )
            if len(self.cmds) >= self.args.amount_exe:
                break
        self.save(fdump=fdump_sents, sdump=sdump_sents)

    def execute(self):
        Execute(func=self.mainExecute, config=self.config)

    def save(self, fdump: list, sdump: list):
        if self.config.main_execute:
            sh = GSQLClass(self.config.v2en.sheet, self.config.v2en.worksheet)
            sh.writeLRow(self.cmds), sh.autoFit()

            Language.saveDictionary(self.config.v2en.flang, self.fdictionary)
            Language.saveDictionary(self.config.v2en.slang, self.sdictionary)

            with open(self.config.v2en.fpath, "w") as f:
                f.writelines(self.fsent)
            with open(self.config.v2en.spath, "w") as f:
                f.writelines(self.ssent)

            for e in [[self.config.v2en.flang, fdump], [self.config.v2en.slang, sdump]]:
                sheet = GSQLClass(self.config.v2en.sheet, f"dump_{e[0]}")
                sheet.writeLRow([[e] for e in e[1]])
                sheet.autoFit()

    def exit(self):
        if not self.args.ci_cd:
            utils.Sound.playNotes(*self.config.v2en.sound_tracks["windows7_shutdown"])

    def main(self) -> None:
        self.handelEnvironment()
        self.initValues()
        self.execute()
        self.exit()


if __name__ == "__main__":
    args = initArgs(config=cconfig)
    main = Main(args=args, config=cconfig)
