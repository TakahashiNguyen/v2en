from multiprocess.pool import ThreadPool
from multiprocess.context import TimeoutError
from contextlib import suppress
from os import makedirs, get_terminal_size, system as ossys, path, stat
from logging import Formatter, FileHandler, INFO, basicConfig, DEBUG, warn, fatal, info
from v2enlib.config import config
from time import monotonic, sleep
from resource import getrusage, RUSAGE_SELF
from platform import system
from librosa import note_to_hz
from numpy import pi, arange, linspace, max, abs
from hashlib import sha256
from soundfile import write as sfwrite
from subprocess import Popen
from difflib import SequenceMatcher
from tqdm import tqdm


class Debugging:
    def __init__(self) -> None:
        formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s\n%(message)s")
        makedirs("logs", exist_ok=True)
        makedirs(".wav", exist_ok=True)

        file_handler = FileHandler(f"./logs/{config.v2en.target}.log")
        file_handler.setLevel(INFO)
        file_handler.setFormatter(formatter)

        basicConfig(level=DEBUG, handlers=[file_handler])

    def functionTimeoutWrapper(self, s):
        def outer(fn):
            def inner(*args, **kwargs):
                with ThreadPool(processes=1) as pool:
                    result = pool.apply_async(fn, args=args, kwds=kwargs)
                    output = kwargs.get("default_value", None)
                    with suppress(TimeoutError):
                        output = result.get(timeout=s) if s else result.get()
                    return output

            return inner

        return outer

    def functionTimeout(self, timeout, func, **kwargs):
        @self.functionTimeoutWrapper(timeout)
        def execute(func, **kwargs):
            args, kwargs = kwargs.get("args", None), kwargs.get("kwargs", None)
            return (
                func(*args, **kwargs)
                if args and kwargs
                else func(**kwargs)
                if kwargs
                else func(*args)
            )

        return execute(func, **kwargs)

    def measureFunction(self, func):
        def wrapper(*args, **kwargs):
            start_time = monotonic()
            result = func(*args, **kwargs)
            end_time = monotonic()
            execution_time = end_time - start_time
            before = getrusage(RUSAGE_SELF).ru_maxrss
            resource_consumption = before / 1024 / 1024  # Memory usage in MB
            if (
                execution_time < config.v2en.allow.time
                and resource_consumption < config.v2en.allow.resource
            ):
                return result

            warn(
                f"{func.__name__}'s result:\n\tExecution time: {execution_time} seconds\n\tMemory consumption: {resource_consumption} MB"
            )
            return result

        return wrapper

    def printError(self, text, error, important):
        text = f"{'_'*50}\n\tExpectation while {text}\n\tError type: {type(error)}\n\t{error}\n{chr(8254)*50}"
        fatal(text)
        if important:
            print(text)

    def printInfo(self, text):
        info(text)


class Terminal:
    @staticmethod
    def terminalWidth():
        try:
            return get_terminal_size().columns
        except Exception:
            return 0

    @staticmethod
    def cleanScreen() -> None:
        ossys("cls" if system() == "Windows" else "clear")


class Sound:
    @staticmethod
    def playNotes(notes, durations, note_start_times):
        """
        Plays multiple notes simultaneously with varying durations and decreasing volume using a thread pool.
        """
        pool = ThreadPool(len(notes))
        for i in range(len(notes)):
            pool.apply_async(
                Sound.playNote,
                (
                    notes[i],
                    durations[i],
                    1 - (i / len(notes)),
                    durations[i],
                    note_start_times[i],
                ),
            )
        pool.close()
        pool.join()

    @staticmethod
    def playNote(note, duration, volume, note_duration, start_time):
        """
        Plays a single note with the given duration and volume using the soundfile library.
        """
        sr = 44100  # sample rate
        freq = note_to_hz(note)
        samples = scipy.signal.sawtooth(  # type: ignore
            2 * pi * arange(sr * note_duration) * freq / sr, 0.5
        )
        decay = linspace(volume, 0, int(sr * note_duration))
        scaled = samples * decay
        scaled /= max(abs(scaled))

        # Compute hash of audio data
        hashname = sha256(scaled).hexdigest()

        # Create subdirectory for stored audio files
        makedirs(".wav", exist_ok=True)

        # Check if file with the same hash already exists
        filename = path.join(".wav", f"{hashname[:10]}.wav")
        if not path.exists(filename):
            # Write scaled audio data to file
            sfwrite(filename, scaled, sr)

        sleep(start_time)

        # Play audio file using appropriate command depending on platform
        if system() == "Windows":
            Popen(
                [
                    "powershell",
                    'New-Object Media.SoundPlayer "{filename}"'.format(
                        filename=filename
                    ),
                ]
            )
        elif system() == "Darwin":
            Popen(["afplay", filename])
        else:
            Popen(["play", "-q", filename])


# other utils
def differentRatio(x, y):
    return SequenceMatcher(None, x, y).ratio()


def emptyFile(path):
    return stat(path).st_size == 0


def getKeyByValue(d, value):
    return [k for k, v in d.items() if v == value]


class Pool:
    @staticmethod
    def function(
        func,
        cmds,
        executor,
        isAllowThread=True,
        strictOrder=False,
        alwaysThread: bool = False,
        poolName: str = "",
    ) -> list:
        if (len(cmds)) == 0:
            return []
        with executor(
            processes=min(
                len(cmds),
                config.v2en.thread.limit if config.v2en.thread.limit > 0 else len(cmds),
            ),
        ) as ex:
            if (not config.v2en.thread.allow or not isAllowThread) and not alwaysThread:
                return [
                    func(cmd)
                    for cmd in tqdm(
                        cmds,
                        leave=False,
                        desc=poolName,
                        disable=not config.v2en.allow.tqdm,
                    )
                ]
            with tqdm(
                total=len(cmds),
                leave=False,
                desc=poolName,
                disable=not config.v2en.allow.tqdm,
            ) as pbar:
                results = []
                for res in (
                    ex.imap(func, cmds)
                    if strictOrder
                    else ex.imap_unordered(func, cmds)
                ):
                    pbar.update(1)
                    results.append(res)
                return results

    @staticmethod
    def args(
        funcs: list,
        executor,
        subexecutor,
        isAllowThread: bool = True,
        strictOrder: bool = False,
        alwaysThread: bool = False,
        poolName: str = "",
        **kwargs,
    ) -> list:
        with executor(
            processes=min(
                len(funcs),
                config.v2en.thread.limit
                if config.v2en.thread.limit > 0
                else len(funcs),
            ),
        ) as ex:
            if (not config.v2en.thread.allow or not isAllowThread) and not alwaysThread:
                return [
                    subexecutor([func, kwargs])
                    for func in tqdm(
                        funcs,
                        leave=False,
                        desc=poolName,
                        disable=not config.v2en.allow.tqdm,
                    )
                ]
            with tqdm(
                total=len(funcs),
                leave=False,
                desc=poolName,
                disable=not config.v2en.allow.tqdm,
            ) as pbar:
                results = []
                kwargsc = [dict(kwargs) for _ in range(len(funcs))]
                for res in (
                    ex.imap(
                        subexecutor,
                        [[func, kwargsc[i]] for i, func in enumerate(funcs)],
                    )
                    if strictOrder
                    else ex.imap_unordered(
                        subexecutor,
                        [[func, kwargsc[i]] for i, func in enumerate(funcs)],
                    )
                ):
                    pbar.update(1)
                    results.append(res)
                return results


debuger = Debugging()
