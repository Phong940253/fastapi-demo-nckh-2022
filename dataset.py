from torch.utils.data import Dataset
import pandas as pd


class NewDataset(Dataset):
    def __init__(self, file_name):
        df = pd.read_csv(file_name)
        df.pop("Pre-Comment")

        x = df.iloc[:, 0:2].values
        y = df.iloc[:, 2].values

        self.x_train = x
        self.y_train = y

    def __len__(self):
        return len(self.y_train)

    def __getitem__(self, idx):
        return self.x_train[idx], self.y_train[idx]
