import pandas as pd
import scipy
from sklearn.model_selection import train_test_split
import torch
import os
import sys

from rdkit import Chem
from torch_geometric.data import Data
from torch_geometric.loader import DataLoader
from torch_geometric.nn import GCNConv, global_mean_pool
import torch.nn.functional as F
import torch.nn as nn

# =====================================================
# MODEL DEFINITION
# =====================================================
class GNN(nn.Module):
    def __init__(self, hidden_channels):
        super(GNN, self).__init__()
        torch.manual_seed(12345)
        self.conv1 = GCNConv(1, hidden_channels) # 1 node feature (atomic number)
        self.conv2 = GCNConv(hidden_channels, hidden_channels)
        self.conv3 = GCNConv(hidden_channels, hidden_channels)
        self.lin = nn.Linear(hidden_channels, 1)

    def forward(self, x, edge_index, batch):
        x = self.conv1(x, edge_index)
        x = x.relu()
        x = self.conv2(x, edge_index)
        x = x.relu()
        x = self.conv3(x, edge_index)

        x = global_mean_pool(x, batch)

        x = F.dropout(x, p=0.5, training=self.training)
        x = self.lin(x)
        return x

def smiles_to_graph(smiles):
    """Utility to convert a SMILES string into a PyTorch Geometric Data object."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    
    atoms = []
    for atom in mol.GetAtoms():
        atoms.append([atom.GetAtomicNum()])
    if len(atoms) == 0:
        return None
        
    x = torch.tensor(atoms, dtype=torch.float)
    
    edges = []
    for bond in mol.GetBonds():
        a = bond.GetBeginAtomIdx()
        b = bond.GetEndAtomIdx()
        edges.append([a, b])
        edges.append([b, a])
        
    if len(edges) == 0:
        return None
        
    edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()
    return Data(x=x, edge_index=edge_index)

if __name__ == "__main__":
    print("PyTorch version:", torch.__version__)
    
    FILE = "chemical_compounds.csv"
    if not os.path.exists(FILE):
        print("❌ Dataset file not found:", FILE)
        sys.exit()

    try:
        df = pd.read_csv(FILE)
        print("✅ Dataset loaded")
    except Exception as e:
        print("❌ Failed to load dataset:", e)
        sys.exit()

    required_cols = ["SMILES", "% ToxCast Active"]
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        print("❌ Missing columns:", missing)
        sys.exit()

    df = df.dropna(subset=required_cols)
    df["% ToxCast Active"] = pd.to_numeric(df["% ToxCast Active"])

    graphs = []
    for i, row in df.iterrows():
        try:
            smiles = str(row["SMILES"]).split(' |')[0].split()[0].strip()
        except:
            continue
        if not smiles: continue
        
        graph = smiles_to_graph(smiles)
        if graph is not None:
            try:
                graph.y = torch.tensor([float(row["% ToxCast Active"])], dtype=torch.float)
                graphs.append(graph)
            except:
                pass
            
    if len(graphs) < 20:
        print("❌ Dataset too small for training")
        sys.exit()

    train_data, test_data = train_test_split(graphs, test_size=0.2, random_state=42)
    train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
    test_loader = DataLoader(test_data, batch_size=64, shuffle=False)

    model = GNN(hidden_channels=64)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.005)
    criterion = nn.MSELoss()

    def train():
        model.train()
        total_loss = 0
        for data in train_loader:
            out = model(data.x, data.edge_index, data.batch)
            loss = criterion(out, data.y.view(-1, 1))
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            total_loss += loss.item() * data.num_graphs
        return total_loss / len(train_loader.dataset)

    def test(loader):
        model.eval()
        total_loss = 0
        with torch.no_grad():
            for data in loader:
                out = model(data.x, data.edge_index, data.batch)
                loss = criterion(out, data.y.view(-1, 1))
                total_loss += loss.item() * data.num_graphs
        return total_loss / len(loader.dataset)

    print("Starting training...")
    for epoch in range(1, 21):
        _ = train()
        train_loss = test(train_loader)
        test_loss = test(test_loader)
        print(f'Epoch: {epoch:03d}, Train Loss: {train_loss:.4f}, Test Loss: {test_loss:.4f}')

    torch.save(model.state_dict(), "gnn_model.pth")
    print("✅ Training complete. Model saved to gnn_model.pth")
