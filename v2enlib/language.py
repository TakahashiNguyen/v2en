from v2enlib.utils import debuger, getKeyByValue, differentRatio, Pool, ThreadPool
from v2enlib.gSQL import GSQLClass
from v2enlib.config import config
from deep_translator import GoogleTranslator
from deep_translator.exceptions import *
from requests.exceptions import *
from langcodes import Language as lcLanguage
from translators.server import TranslatorError
from contextlib import suppress
from string import punctuation
from tabulate import tabulate
from functools import lru_cache
from gc import collect
import httpx


class InputSent:
    def __init__(
        self,
        first: str = "",
        second: str = "",
        isFrom: str = "",
        accurate: float = 0,
    ) -> None:
        self.isFrom = isFrom or "Data set"
        self.first = first or "N/A"
        self.second = second or "N/A"
        self.accurate = accurate

    def isValid(self) -> bool:
        return bool(self.first and self.second)

    def SQLFormat(self) -> tuple:
        return self.first, self.second


class Executor:
    @staticmethod
    def transIntoList(cmd):
        return Translator.intoList(*cmd)

    @staticmethod
    def addSent(cmd):
        return Language.addSent(*cmd)

    @staticmethod
    def checkSpelling(cmd):
        return Language.checkSpelling(*cmd)


class Translator:
    @staticmethod
    def deepGoogle(query_text: str, from_language: str, to_language: str) -> str:
        try:
            return GoogleTranslator(source=from_language, target=to_language).translate(
                query_text
            )
        except (
            LanguageNotSupportedException,
            InvalidSourceOrTargetLanguage,
        ):
            return Translator.deepGoogle(
                query_text,
                str(lcLanguage.get(from_language)),
                str(lcLanguage.get(to_language)),
            )
        except Exception as e:
            debuger.printError(Translator.deepGoogle.__name__, e, False)
            return ""

    @staticmethod
    def translatorsTransSub(cmd: list):
        function_timeout = cmd[1].get("function_timeout", None)
        config = cmd[1].get("config")
        trans_name = getKeyByValue(config.v2en.trans_dict, cmd[0])[0]

        def execute(cmd: list):
            ou = ""
            allow_error = (
                JSONDecodeError,
                TranslatorError,
                HTTPError,
                ConnectionError,
            )
            if function_timeout:
                del cmd[1]["function_timeout"]
                del cmd[1]["config"]
            if cmd[0]:
                try:
                    ou = debuger.functionTimeout(
                        function_timeout, cmd[0], kwargs=cmd[1]
                    )
                except TranslatorError as e:
                    with suppress(*allow_error):
                        if tcmd := Translator.handleCodes(cmd[1].values(), e):
                            ou = debuger.functionTimeout(
                                function_timeout / 2, cmd[0], args=tcmd
                            )
                        else:
                            ou = debuger.functionTimeout(
                                function_timeout,
                                Translator.deepGoogle,
                                **cmd[1],
                            )
                except allow_error:
                    ou = debuger.functionTimeout(
                        function_timeout / 2, Translator.deepGoogle, kwargs=cmd[1]
                    )
                except Exception as e:
                    debuger.printError("translatorsTransSub", e, False)
            if function_timeout:
                cmd[1]["function_timeout"] = function_timeout
            if config:
                cmd[1]["config"] = config
            return [ou, trans_name]

        return execute(cmd)

    @staticmethod
    def translatorsTrans(cmd: list, trans_timeout, config) -> list:
        return ThreadPool.args(
            funcs=config.v2en.trans_dict.values(),
            subexecutor=Translator.translatorsTransSub,
            poolName="translationPool",
            query_text=cmd[0],
            from_language=cmd[1],
            to_language=cmd[2],
            function_timeout=trans_timeout,
            config=config,
        )

    # TODO Rename this here and in `translatorsTrans`
    @staticmethod
    @debuger.measureFunction
    def handleCodes(cmd: list, e) -> list:
        try:
            if not len(e.args):
                return []
            tcmd, execute = list(cmd), False
            if (e.args[0]).find("vie") != -1:
                tcmd[2 if (e.args[0]).find("to_language") != -1 else 1] = "vie"
                execute = True

            if (e.args[0]).find("vi_VN") != -1:
                tcmd[2 if (e.args[0]).find("to_language") != -1 else 1] = "vi_VN"
                execute = True

            if (e.args[0]).find("vi-VN") != -1:
                tcmd[2 if (e.args[0]).find("to_language") != -1 else 1] = "vi-VN"
                execute = True
            if execute:
                return tcmd
        except Exception as e:
            debuger.printError("change format language", e, False)
        return []

    @staticmethod
    def intoList(sent, source_lang, target_lang, target_dictionary, timeout, config):
        return ThreadPool.function(
            func=Executor.checkSpelling,
            iterable=[
                [Language.convert(e[0]), target_dictionary, target_lang, e[1]]
                for e in Translator.translatorsTrans(
                    cmd=[sent, source_lang, target_lang],
                    trans_timeout=timeout,
                    config=config,
                )
            ],
        )


class Language:
    @staticmethod
    @debuger.measureFunction
    def checkSpelling(text: str, dictionary: list, lang: str, tname: str = ""):
        word = ""
        try:
            words = text.split()
            outstr = ""
            for idx, word in enumerate(words):
                if (
                    word in dictionary
                    or word.isnumeric()
                    or word in punctuation
                    or Language.existOnWiki(word, lang)
                    or Language.existOnWiki(f"{words[idx-1]} {word}", lang)
                    or (
                        idx + 1 < len(words)
                        and Language.existOnWiki(f"{word} {words[idx+1]}", lang)
                    )
                ):
                    outstr += f"{word} "
                else:
                    raise ValueError(f"{word} not existed")
                if word.isalpha() and word not in dictionary:
                    dictionary.append(word)
            return [outstr, tname] if tname else outstr
        except ValueError:
            debuger.printError(
                f"add word for {lang}",
                Exception(f"{word} isn't existed on Wikitionary!"),
                False,
            )
        except Exception as e:
            debuger.printError(Language.checkSpelling.__name__, e, False)
        return ["", ""] if tname else ""

    @staticmethod
    @debuger.measureFunction
    def addSent(input_sent: InputSent, fdictionary, sdictionary, cmds, config):
        is_agree, fdump = False, []
        print_data = ["Data set", input_sent.first, input_sent.second, "N/A"]
        fdump, sdump = "", ""
        input_sent.first, input_sent.second = ThreadPool.function(
            func=Executor.checkSpelling,
            iterable=[
                [Language.convert(e[0].replace("\n", "")), e[1], e[2]]
                for e in [
                    [input_sent.first, fdictionary, config.v2en.flang],
                    [input_sent.second, sdictionary, config.v2en.slang],
                ]
            ],
        )
        if not input_sent.isValid():
            return "", "", False
        is_error, trans_data = True, []
        for first_tran, second_tran in zip(
            *Pool.function(
                func=Executor.transIntoList,
                iterable=[
                    [
                        input_sent.first,
                        config.v2en.flang,
                        config.v2en.slang,
                        sdictionary,
                        config.v2en.trans_timeout,
                        config,
                    ],
                    [
                        input_sent.second,
                        config.v2en.slang,
                        config.v2en.flang,
                        fdictionary,
                        config.v2en.trans_timeout,
                        config,
                    ],
                ],
            )
        ):
            if first_tran[0]:
                trans_data.append(
                    InputSent(
                        input_sent.first,
                        first_tran[0],
                        first_tran[1],
                        differentRatio(input_sent.second, first_tran[0]),
                    )
                )
            if second_tran[0]:
                trans_data.append(
                    InputSent(
                        second_tran[0],
                        input_sent.second,
                        second_tran[1],
                        differentRatio(input_sent.first, second_tran[0]),
                    )
                )

        if any(e.accurate > config.v2en.accept_percentage for e in trans_data):
            is_agree = True
            is_error = False
        if is_agree and not is_error:
            cmds += [[input_sent.first, input_sent.second]] + [
                e.SQLFormat()
                for e in trans_data
                if e.accurate > config.v2en.accept_percentage
            ]
        if is_error:
            fdump, sdump = input_sent.first, input_sent.second

        print_data += [
            [e.isFrom, e.first, e.second, e.accurate]
            for e in trans_data
            if e.accurate > config.v2en.accept_percentage
        ]
        if len(print_data) < 10:
            debuger.printInfo(
                tabulate(
                    tabular_data=print_data,
                    headers=["From", "Source", "Target", "Accuracy?"],
                    tablefmt="fancy_grid",
                    showindex="always",
                    maxcolwidths=[None, None, 45, 45, 7],
                    floatfmt=(".2f" * 5),
                ),
            )
        del trans_data, print_data
        collect()
        return fdump, sdump, is_agree

    @staticmethod
    def convert(x: str) -> str:
        if not x:
            return ""
        # fix bad data
        if "apos" in x or "quot" in x or "amp" in x or "&#91;" in x or "--" in x:
            return ""

        x = x.replace("“", " “ ").replace("”", " ” ").replace("’", " ’ ")
        for punc in punctuation:
            x = x.replace(punc, f" {punc} ")
        try:
            return x.lower().replace("  ", " ").replace("  ", " ")
        except Exception as e:
            debuger.printError(Language.convert.__name__, e, False)
            return ""

    @staticmethod
    @lru_cache(maxsize=1024)
    def getWikitionaryHeaders(word: str) -> httpx.Response:
        return httpx.get(f"https://en.wiktionary.org/wiki/{word}")

    @staticmethod
    def existOnWiki(word: str, lang: str) -> bool:
        display_name = lcLanguage.make(language=lang).display_name()

        response = Language.getWikitionaryHeaders(word)
        return (
            f'href="#{display_name}"' in response.headers.get("link", "")
            or f'id="{display_name}"' in response.text
        )

    @staticmethod
    def loadDictionary(lang: str, sheet: str) -> list:
        try:
            return GSQLClass(sheet, f"dictionary_{lang}").getCol(1)
        except Exception as e:
            debuger.printError(Language.loadDictionary.__name__, e, False)
        return []

    @staticmethod
    def saveDictionary(lang, dictionary):
        try:
            sheet = GSQLClass(config.v2en.sheet, f"dictionary_{lang}")
            sheet.clear()
            sheet.writeLRow([[e] for e in list(dict.fromkeys(dictionary))])
            sheet.autoFit()
        except Exception as e:
            debuger.printError("saveDictionary", e, False)
