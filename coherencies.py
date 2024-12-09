import pandas as pd


class Coherencies:
    def __init__(self, data):
        self.data = data

    @classmethod
    def read_coherences(cls, path, columns):
        print("Reading participants from file: ", path)
        df = pd.read_csv(path, sep=';', encoding='latin1', usecols=columns)
        print("Participants read successfully")

        return df


if __name__ == "__main__":
    ...
