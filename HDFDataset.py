import h5py
import numpy as np
import torch
from torch.utils.data import Dataset

class DeformDataset(Dataset):

    def __init__(self, hdf5_path):
        self.hdf5_path = hdf5_path
        self.dataset_names = ['temperature', 'altitude', 'thickness', 'trajectory', 'deformation']
        self.file = None
        self.means = {}
        self.stds = {}

    def __len__(self):
        with h5py.File(self.hdf5_path, 'r') as hdf_file:
            return len(hdf_file[self.dataset_names[0]])

    def __getitem__(self, idx):
        if self.file is None:
            self.file = h5py.File(self.hdf5_path, 'r')
            self._compute_stats()

        sample = {name: self.file[name][idx] for name in self.dataset_names}
        # Convert numpy arrays to PyTorch tensors
        sample = {key: torch.tensor(value, dtype=torch.float32) for key, value in sample.items()}
        
        sample = self.normalize(sample)
        
        return sample

    def _compute_stats(self):
        for name in self.dataset_names:
            data = self.file[name][:]
            self.means[name] = torch.tensor(data.mean())
            self.stds[name] = torch.tensor(data.mean())

    def normalize(self, sample):
        normalized_sample = {}
        for key, value in sample.items():
            normalized_sample[key] = (value - self.means[key]) / self.stds[key]
        return normalized_sample

    def denormalize(self, sample):
        denormalized_sample = {}
        for key, value in sample.items():
            denormalized_sample[key] = value * self.stds[key] + self.means[key]
        return denormalized_sample

if __name__ == '__main__':
    dataset = DeformDataset('fake_deform_data.hdf5')
    data = dataset[0]
    import pdb; pdb.set_trace()