import yaml
import multiprocessing.pool
import time
import deep_translator
import string
import translators
import signal
from v2enlib import *

with open("config.yml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)
target = cfg["v2en"]["target"]
table_name = cfg["sqlite"]["table_name"]
first_lang = target[:2]
second_lang = target[-2:]
accept_percentage = 0.65
is_auto = True
debug = False
first_dictionary_path = f"./cache/{first_lang}.dic"
second_dictionary_path = f"./cache/{second_lang}.dic"
main_execute = True
num_sent = 30
false_allow = 50
thread_alow = True
"""
    translate service:
    - google
    - bing
    - alibaba
    - sogou
"""
translators_target = ["google", "bing", "sogou", "alibaba"]


# translate def
def deepTransGoogle(x: str, source: str, target: str) -> str:
    try:
        return deep_translator.GoogleTranslator(source=source, target=target).translate(x)
    except Exception as e:
        printError(deepTransGoogle.__name__, e, False)
        return ""


def translatorsTrans(x: str, source: str, target: str, host: str) -> str:
    try:
        ou = translators.translate_text(
            x, from_language=source, to_language=target, translator=host
        )
        if type(ou) != str:
            printError(translatorsTrans.__name__, Exception("Type error"), False, True)
            return deepTransGoogle(x, source, target)
        return ou
    except Exception as e:
        printError(translatorsTrans.__name__, e, False)
        return deepTransGoogle(x, source, target)


def translatorsTransExecute(cmd):
    return translatorsTrans(*cmd)


def translatorsTransPool(cmds) -> list:
    if thread_alow:
        return multiprocessing.pool.ThreadPool(processes=len(cmds) + 2).map(
            translatorsTransExecute, cmds
        )
    return [translatorsTrans(*cmd) for cmd in cmds]


def transIntoList(sent, source_lang, target_lang, target_dictionary):
    return checkSpellingPool(
        [
            [convert(trans), target_dictionary, target_lang]
            for trans in translatorsTransPool(
                [(sent, source_lang, target_lang, host) for host in translators_target]
            )
        ]
    )


def transIntoListExecute(cmd):
    return transIntoList(*cmd)


def transIntoListPool(cmds):
    if thread_alow:
        return multiprocessing.pool.ThreadPool(processes=len(cmds) + 2).map(
            transIntoListExecute, cmds
        )
    return [transIntoList(*cmd) for cmd in cmds]


# language utils
def checkSpelling(text: str, dictionary: list, lang: str) -> str:
    printInfo(checkSpelling.__name__, multiprocessing.current_process().pid, debug)
    word = ""
    try:
        words = text.split()
        outstr = ""
        for idx, word in enumerate(words):
            if (
                word in dictionary
                or word.isnumeric()
                or word in string.punctuation
                or isExistOnWiki(word, lang, debug)
                or isExistOnWiki(f"{words[idx-1]} {word}", lang, debug)
                or (idx + 1 < len(words) and isExistOnWiki(f"{word} {words[idx+1]}", lang, debug))
            ):
                outstr += f"{word} "
            else:
                raise ValueError(f"{word} not existed")
            if word.isalpha() and word not in dictionary:
                dictionary.insert(0, word)
        return outstr
    except ValueError:
        printError(
            f"add word for {lang}", Exception(f"{word} isn't existed on Wikitionary!"), False
        )
    except Exception as e:
        printError(checkSpelling.__name__, e, debug)
    return ""


def checkSpellingExecute(cmd):
    return checkSpelling(*cmd)


def checkSpellingPool(cmds):
    if thread_alow:
        return multiprocessing.pool.ThreadPool(processes=len(cmds) + 2).map(
            checkSpellingExecute, cmds
        )
    return [checkSpelling(*cmd) for cmd in cmds]


def addSent(first_sent: str, second_sent: str):
    time_start = time.time()
    is_error, is_agree, first_dump_sent, second_dump_sent, cmds = True, False, "", "", []
    first_sent, second_sent = checkSpellingPool(
        [
            [convert(first_sent.replace("\n", "")), first_dictionary, first_lang],
            [convert(second_sent.replace("\n", "")), second_dictionary, second_lang],
        ]
    )
    if first_sent and second_sent:
        try:
            first_trans, second_trans = transIntoListPool(
                [
                    [first_sent, first_lang, second_lang, second_dictionary],
                    [second_sent, second_lang, first_lang, first_dictionary],
                ]
            )
        except Exception as e:
            printError("translate section", e, False)
        else:
            first_ratio = [diffratio(first_sent, trans_sent) for trans_sent in second_trans]
            second_ratio = [diffratio(second_sent, trans_sent) for trans_sent in first_trans]

            if any(ratio > accept_percentage for ratio in first_ratio) or any(
                ratio > accept_percentage for ratio in second_ratio
            ):
                is_agree = True
                is_error = False
            if is_agree and not is_error:
                table_command = """
                    INSERT INTO {}(Source, Target, Verify)
                    VALUES(?,?,?)
                """
                cmds += [
                    [
                        sql_connection,
                        table_command.format(table_name),
                        (first_sent, second_sent, 1),
                        debug,
                    ]
                ]
                for first_tran, second_tran, first_rate, second_rate in zip(
                    first_trans, second_trans, first_ratio, second_ratio
                ):
                    if first_rate > accept_percentage or second_rate > accept_percentage:
                        cmds += [
                            [
                                sql_connection,
                                table_command.format(table_name),
                                (first_sent, first_tran, 1),
                                debug,
                            ],
                            [
                                sql_connection,
                                table_command.format(table_name),
                                (second_tran, second_sent, 1),
                                debug,
                            ],
                        ]
    if first_sent != "" and second_sent != "" and is_error:
        first_dump_sent, second_dump_sent = first_sent, second_sent

    print(f"\t({(time.time()-time_start):0,.2f}) ({is_agree}) >> {first_sent} | {second_sent}")
    return first_dump_sent, second_dump_sent, cmds, is_agree


def addSentExecute(cmd):
    return addSent(*cmd)


def addSentPool(cmds: list):
    if thread_alow:
        return multiprocessing.pool.ThreadPool(processes=len(cmds) + 2).map(addSentExecute, cmds)
    return [addSent(*cmd) for cmd in cmds]


checkLangFile(first_lang, second_lang)
first_dictionary = loadDictionary(first_dictionary_path, debug)
second_dictionary = loadDictionary(second_dictionary_path, debug)
signal.signal(signal.SIGINT, signalHandler)

if __name__ == "__main__":
    sql_connection = getSQLCursor(cfg["sqlite"]["path"])
    createSQLtable(sql_connection, table_name, debug)
    false_count = 0

    first_path, second_path = f"./data/{first_lang}.txt", f"./data/{second_lang}.txt"
    while main_execute:
        time_start = time.time()
        if isEmpty(first_path) or isEmpty(second_path):
            print("Done!")
            exit()

        first_dump_sent, second_dump_sent, cmds = [], [], []
        with open(first_path, "r") as first_file:
            with open(second_path, "r") as second_file:
                saveIN, saveOU = first_file.read().splitlines(True), second_file.read().splitlines(
                    True
                )
                for e in addSentPool(
                    [
                        [saveIN[idx], saveOU[idx]]
                        for idx in range(num_sent if len(saveIN) > num_sent else len(saveIN))
                    ]
                ):
                    if e[0] != "" and e[1] != "":
                        first_dump_sent.append(e[0]), second_dump_sent.append(e[1])
                    cmds.extend(i for i in e[2] if len(i) == 4)
                    false_count += -false_count if e[3] else 1
                    if false_count > false_allow and main_execute:
                        printError(
                            "mainModule", Exception("Too many fatal translation!"), False, True
                        )
                        main_execute = False
        createOBJPool(cmds, sql_connection)

        with open(f"./data/{first_lang}.dump", "a") as f:
            for sent in first_dump_sent:
                f.write(f"{sent}\n")
        with open(f"./data/{second_lang}.dump", "a") as f:
            for sent in second_dump_sent:
                f.write(f"{sent}\n")

        if main_execute:
            with open(first_path, "w") as file:
                file.writelines(saveIN[num_sent:])
            with open(second_path, "w") as file:
                file.writelines(saveOU[num_sent:])

        saveDictionary(first_dictionary_path, first_dictionary, debug)
        saveDictionary(second_dictionary_path, second_dictionary, debug)
        print(f"\t\t(mainModule) time consume: {(time.time()-time_start):0,.2f}")
