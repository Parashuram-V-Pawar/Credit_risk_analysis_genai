from pathlib import Path


def load_documents(folder):

    docs = []

    for file in Path(folder).glob("*.txt"):

        with open(
            file,
            encoding="utf-8"
        ) as f:

            docs.append(
                f.read()
            )

    return docs