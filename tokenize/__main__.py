from pathlib import Path
from typing import Iterable, List

# https://github.com/c2nes/javalang/issues/58
# Voilà pourquoi l'auteur de SequenceR utilise sa propre version de javalang.
import javalang
import pandas as pd


class NoClassDefException(Exception):
    pass


def tokenize_java_codes(parsed_csv: pd.DataFrame) -> None:
    src_file = (Path(__file__).parent / "src-dataset.txt").open("wb")
    tgt_file = (Path(__file__).parent / "tgt-dataset.txt").open("wb")

    for _, row in parsed_csv.iterrows():
        error = row.error.replace("\r\n", "\n")
        correction = row.correction.replace("\r\n", "\n")
        error_with_bug_tokens = insert_bug_tokens(
            error, row.bug_start, row.bug_end, row.rule
        )
        try:
            src_file.write(tokenize_java_file(error_with_bug_tokens))
        except NoClassDefException:
            print("Encountered java file without class definition, skipping...")
            continue

        src_file.write(b"\n")

        tgt_file.write(tokenize_java_file(correction))
        tgt_file.write(b"\n")

    src_file.close()
    tgt_file.close()


def insert_bug_tokens(
    src: str, bug_start_idx: int, bug_end_idx: int, bug_type: str
) -> str:
    before_bug = src[:bug_start_idx]
    start_bug = f'"<START_BUG> <BUG_TYPE:{bug_type}>"\n'
    mid_bug = src[bug_start_idx : bug_end_idx + 1]
    end_bug = '"<END_BUG>"\n'
    after_bug = src[bug_end_idx + 1 :]

    return before_bug + start_bug + mid_bug + end_bug + after_bug


def tokenize_java_file(src: str) -> bytes:
    tokens = list(javalang.tokenizer.tokenize(src))
    tokens = remove_imports_section(tokens)

    res = ""
    for token in tokens:
        if is_special_bug_token(token):
            res += token.value[1:-1] + " "
        else:
            res += token.value + " "

    return res.encode("unicode_escape")


def remove_imports_section(
    tokens: List[javalang.tokenizer.JavaToken],
) -> List[javalang.tokenizer.JavaToken]:
    for i, token in enumerate(tokens):
        if isinstance(token, javalang.tokenizer.Keyword) and token.value == "class":
            return tokens[i:]
    raise NoClassDefException("Could not find class declaration in tokens")


def is_special_bug_token(token: javalang.tokenizer.JavaToken) -> bool:
    return isinstance(token, javalang.tokenizer.String) and (
        token.value.startswith(('"<START_BUG>', '"<END_BUG>'))
    )


if __name__ == "__main__":
    DATA_PATH = Path(__file__).parent / "test-data.csv"
    df = pd.read_csv(DATA_PATH, sep=",")
    tokenize_java_codes(df)
