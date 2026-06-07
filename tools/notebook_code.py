# -*- coding: utf-8 -*-
"""Runnable code for each practice-lesson demonstration, aligned 1:1 with
lessons.PRACTICE[week]. Used by build_notebooks.py to fill the demo code cells.
The setup cell (torch, nn, F, plt, device) runs first, so these snippets assume it."""

CODE = {
    1: [
"""# Confirm the device with a small tensor
x = torch.randn(3, device=device)
print("device:", x.device, "| tensor:", x)""",
"""# Minimal training loop on a toy linear dataset y = 2x + 1 + noise
torch.manual_seed(0)
X = torch.randn(200, 1)
y = 2 * X + 1 + 0.1 * torch.randn(200, 1)

model = nn.Linear(1, 1)
opt = torch.optim.SGD(model.parameters(), lr=0.1)
loss_fn = nn.MSELoss()

losses = []
for epoch in range(50):
    opt.zero_grad()
    loss = loss_fn(model(X), y)
    loss.backward()
    opt.step()
    losses.append(loss.item())

print("learned weight, bias:", model.weight.item(), model.bias.item())
plt.plot(losses); plt.xlabel("epoch"); plt.ylabel("MSE"); plt.title("Training loss"); plt.show()""",
"""# Same problem, three learning rates: convergence vs divergence
def train(lr, steps=50):
    torch.manual_seed(0)
    m = nn.Linear(1, 1); o = torch.optim.SGD(m.parameters(), lr=lr); f = nn.MSELoss()
    hist = []
    for _ in range(steps):
        o.zero_grad(); l = f(m(X), y); l.backward(); o.step(); hist.append(l.item())
    return hist

for lr in [0.01, 0.1, 1.5]:
    plt.plot(train(lr), label=f"lr={lr}")
plt.yscale("log"); plt.xlabel("step"); plt.ylabel("loss (log)"); plt.legend(); plt.show()""",
"""# Framing: classification (logits + cross-entropy) vs regression (value + MSE)
xb = torch.randn(8, 4)                       # 8 samples, 4 features

clf = nn.Linear(4, 3)                        # -> 3 class logits
ce = nn.CrossEntropyLoss()(clf(xb), torch.randint(0, 3, (8,)))
print("classification: logits", tuple(clf(xb).shape), "| CE loss", round(ce.item(), 3))

reg = nn.Linear(4, 1)                        # -> 1 continuous value
mse = nn.MSELoss()(reg(xb), torch.randn(8, 1))
print("regression: output", tuple(reg(xb).shape), "| MSE loss", round(mse.item(), 3))""",
    ],
    2: [
"""# Creation, reshape, permute, indexing
t = torch.arange(24)
print("1D:", tuple(t.shape))
t = t.reshape(2, 3, 4); print("reshaped:", tuple(t.shape))
print("permute(2,0,1):", tuple(t.permute(2, 0, 1).shape))
print("t[0, 1]:", t[0, 1].tolist())
print("t[:, :, 0]:", tuple(t[:, :, 0].shape))
print("sum over last dim:", tuple(t.sum(dim=-1).shape))""",
"""# Broadcasting, then a shape-mismatch error and its fix
a = torch.ones(3, 1); b = torch.ones(1, 4)
print("(3,1)+(1,4) ->", tuple((a + b).shape))

x = torch.ones(3, 4); w = torch.ones(5)      # wrong trailing size
try:
    x + w
except RuntimeError as e:
    print("error:", str(e).split('\\n')[0])
w = torch.ones(4)                            # fix: matches trailing dim 4
print("fixed (3,4)+(4,) ->", tuple((x + w).shape))""",
"""# Encode an image (H,W,C -> C,H,W) and a small table, then move to the device
import numpy as np
img = np.random.randint(0, 256, size=(8, 8, 3), dtype=np.uint8)
img_t = torch.from_numpy(img).permute(2, 0, 1).float() / 255.0
print("image tensor:", tuple(img_t.shape), img_t.dtype)

table = torch.tensor([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
print("table tensor:", tuple(table.shape))
img_t, table = img_t.to(device), table.to(device)
print("moved to:", img_t.device)""",
    ],
    3: [
"""# Build and train a small MLP on a 2-class toy problem
torch.manual_seed(0)
X = torch.randn(200, 2); y = (X[:, 0] + X[:, 1] > 0).long()

class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(2, 16), nn.ReLU(), nn.Linear(16, 2))
    def forward(self, x):
        return self.net(x)

model = MLP(); opt = torch.optim.Adam(model.parameters(), lr=0.05); loss_fn = nn.CrossEntropyLoss()
for epoch in range(100):
    opt.zero_grad(); loss = loss_fn(model(X), y); loss.backward(); opt.step()
acc = (model(X).argmax(1) == y).float().mean()
print(f"final loss {loss.item():.3f} | accuracy {acc.item():.3f}")""",
"""# .grad accumulates; zero_grad clears it
w = torch.tensor([2.0], requires_grad=True)
(w ** 2).sum().backward(); print("after 1st backward (2w=4):", w.grad.item())
(w ** 2).sum().backward(); print("WITHOUT zero_grad (accumulated):", w.grad.item())
w.grad.zero_()
(w ** 2).sum().backward(); print("AFTER zero_grad:", w.grad.item())""",
"""# Hand-derived gradient vs autograd
x = torch.tensor(3.0, requires_grad=True)
y = x ** 3 + 2 * x            # dy/dx = 3x^2 + 2 -> 29 at x = 3
y.backward()
print("autograd:", x.grad.item(), "| hand 3*x^2+2:", 3 * 3 ** 2 + 2)""",
    ],
    4: [
"""# A custom Dataset + DataLoader, then iterate batches
from torch.utils.data import Dataset, DataLoader

class ToyData(Dataset):
    def __init__(self, n=100):
        self.x = torch.randn(n, 3); self.y = torch.randint(0, 2, (n,))
    def __len__(self):
        return len(self.x)
    def __getitem__(self, i):
        return self.x[i], self.y[i]

ds = ToyData()
dl = DataLoader(ds, batch_size=16, shuffle=True)
xb, yb = next(iter(dl))
print("dataset size:", len(ds), "| one batch:", tuple(xb.shape), tuple(yb.shape))""",
"""# Batch size sets steps per epoch; shuffling reorders each epoch
for bs in [8, 32]:
    print(f"batch_size={bs}: {len(DataLoader(ds, batch_size=bs))} batches per epoch")
dl = DataLoader(ds, batch_size=4, shuffle=True)
print("epoch 1 first labels:", next(iter(dl))[1].tolist())
print("epoch 2 first labels:", next(iter(dl))[1].tolist())""",
"""# Data leak: normalizing with whole-dataset stats vs train-only stats
data = torch.randn(100, 1) * 5 + 10
train, test = data[:80], data[80:]

mu, sd = data.mean(), data.std()                 # LEAK: uses test data
print("leaky test mean ~ 0:", round(((test - mu) / sd).mean().item(), 3))

mu, sd = train.mean(), train.std()               # correct: train only
print("correct test mean (not 0):", round(((test - mu) / sd).mean().item(), 3))""",
    ],
    5: [
"""# Training loop with loss and accuracy logging
torch.manual_seed(0)
X = torch.randn(300, 4); y = (X.sum(1) > 0).long()
model = nn.Linear(4, 2); opt = torch.optim.Adam(model.parameters(), lr=0.05); loss_fn = nn.CrossEntropyLoss()
for epoch in range(50):
    opt.zero_grad(); out = model(X); loss = loss_fn(out, y); loss.backward(); opt.step()
    if epoch % 10 == 0:
        acc = (out.argmax(1) == y).float().mean()
        print(f"epoch {epoch:2d}: loss {loss.item():.3f} acc {acc.item():.3f}")""",
"""# Cross-entropy is the right loss; squaring label numbers is meaningless
logits = model(X)
ce = nn.CrossEntropyLoss()(logits, y)
mse = nn.MSELoss()(logits.argmax(1).float(), y.float())   # treats classes as numbers
print("cross-entropy (correct):", round(ce.item(), 3),
      "| MSE-on-labels (meaningless):", round(mse.item(), 3))""",
"""# Accuracy hides minority-class failure; F1 does not
y_true = torch.cat([torch.zeros(95), torch.ones(5)]).long()
y_pred = torch.zeros(100).long()                 # trivial: always predict class 0
acc = (y_pred == y_true).float().mean().item()
tp = ((y_pred == 1) & (y_true == 1)).sum().item()
fp = ((y_pred == 1) & (y_true == 0)).sum().item()
fn = ((y_pred == 0) & (y_true == 1)).sum().item()
prec = tp / (tp + fp + 1e-9); rec = tp / (tp + fn + 1e-9)
f1 = 2 * prec * rec / (prec + rec + 1e-9)
print(f"accuracy {acc:.2f} but F1 {f1:.2f} (recall {rec:.2f})")""",
    ],
    6: [
"""# Same model and data, three optimizers
torch.manual_seed(0)
X = torch.randn(200, 5); y = X @ torch.randn(5, 1) + 0.1 * torch.randn(200, 1)
def run(name):
    torch.manual_seed(0); m = nn.Linear(5, 1); f = nn.MSELoss()
    o = {"SGD": torch.optim.SGD(m.parameters(), lr=0.05),
         "Momentum": torch.optim.SGD(m.parameters(), lr=0.05, momentum=0.9),
         "Adam": torch.optim.Adam(m.parameters(), lr=0.05)}[name]
    h = []
    for _ in range(60):
        o.zero_grad(); l = f(m(X), y); l.backward(); o.step(); h.append(l.item())
    return h
for name in ["SGD", "Momentum", "Adam"]:
    plt.plot(run(name), label=name)
plt.legend(); plt.xlabel("step"); plt.ylabel("loss"); plt.show()""",
"""# Learning-rate sweep
for lr in [0.001, 0.05, 0.5]:
    torch.manual_seed(0); m = nn.Linear(5, 1); o = torch.optim.SGD(m.parameters(), lr=lr); f = nn.MSELoss()
    h = []
    for _ in range(60):
        o.zero_grad(); l = f(m(X), y); l.backward(); o.step(); h.append(l.item())
    plt.plot(h, label=f"lr={lr}")
plt.yscale("log"); plt.legend(); plt.xlabel("step"); plt.ylabel("loss (log)"); plt.show()""",
"""# A learning-rate schedule (step decay)
m = nn.Linear(5, 1); o = torch.optim.SGD(m.parameters(), lr=0.1); f = nn.MSELoss()
sched = torch.optim.lr_scheduler.StepLR(o, step_size=20, gamma=0.3)
lrs = []
for _ in range(60):
    o.zero_grad(); f(m(X), y).backward(); o.step(); sched.step()
    lrs.append(o.param_groups[0]["lr"])
plt.plot(lrs); plt.xlabel("step"); plt.ylabel("learning rate"); plt.title("StepLR"); plt.show()""",
    ],
    7: [
"""# Force overfitting: tiny train set, large model
torch.manual_seed(0)
Xtr = torch.randn(30, 20); ytr = torch.randint(0, 2, (30,))
Xte = torch.randn(200, 20); yte = torch.randint(0, 2, (200,))
def fit(model, epochs=200, wd=0.0):
    o = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=wd); f = nn.CrossEntropyLoss()
    tr, te = [], []
    for _ in range(epochs):
        o.zero_grad(); f(model(Xtr), ytr).backward(); o.step()
        tr.append((model(Xtr).argmax(1) == ytr).float().mean().item())
        te.append((model(Xte).argmax(1) == yte).float().mean().item())
    return tr, te
big = lambda: nn.Sequential(nn.Linear(20, 128), nn.ReLU(), nn.Linear(128, 128), nn.ReLU(), nn.Linear(128, 2))
tr, te = fit(big())
print(f"overfit: train {tr[-1]:.2f} vs test {te[-1]:.2f}")
plt.plot(tr, label="train"); plt.plot(te, label="test"); plt.legend(); plt.show()""",
"""# Dropout + weight decay shrink the train/test gap
reg = nn.Sequential(nn.Linear(20, 128), nn.ReLU(), nn.Dropout(0.5), nn.Linear(128, 2))
tr, te = fit(reg, wd=1e-2)
print(f"regularized: train {tr[-1]:.2f} vs test {te[-1]:.2f}")
plt.plot(tr, label="train"); plt.plot(te, label="test"); plt.legend(); plt.show()""",
"""# Data augmentation (applied to TRAIN only)
from torchvision import transforms
img = torch.rand(3, 32, 32)
aug = transforms.Compose([transforms.RandomHorizontalFlip(p=1.0),
                          transforms.RandomCrop(32, padding=4)])
print("original", tuple(img.shape), "-> augmented", tuple(aug(img).shape))""",
    ],
    8: [
"""# A small CNN; print the shape after each layer
cnn = nn.Sequential(
    nn.Conv2d(1, 8, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),    # 28 -> 14
    nn.Conv2d(8, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),   # 14 -> 7
    nn.Flatten(), nn.Linear(16 * 7 * 7, 10))
x = torch.randn(4, 1, 28, 28)
for layer in cnn:
    x = layer(x); print(f"{layer.__class__.__name__:9s}", tuple(x.shape))""",
"""# Output size and parameter count, by formula and by code
conv = nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1)
print("output:", tuple(conv(torch.randn(1, 3, 32, 32)).shape), "  formula (32+2-3)/1+1 = 32")
params = sum(p.numel() for p in conv.parameters())
print("params:", params, "= (3*3*3 + 1) * 16 =", (3 * 3 * 3 + 1) * 16)""",
"""# Train one batch on FashionMNIST and visualize first-conv feature maps
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
dl = DataLoader(datasets.FashionMNIST("./data", train=True, download=True, transform=transforms.ToTensor()),
                batch_size=128, shuffle=True)
model = nn.Sequential(nn.Conv2d(1, 8, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
                      nn.Flatten(), nn.Linear(8 * 14 * 14, 10)).to(device)
opt = torch.optim.Adam(model.parameters(), 1e-3); f = nn.CrossEntropyLoss()
xb, yb = next(iter(dl)); xb, yb = xb.to(device), yb.to(device)
opt.zero_grad(); f(model(xb), yb).backward(); opt.step()
fmap = model[0](xb[:1]).detach().cpu()
fig, ax = plt.subplots(1, 4, figsize=(8, 2))
for i in range(4):
    ax[i].imshow(fmap[0, i]); ax[i].axis("off")
plt.show()""",
    ],
    9: [
"""# A residual block with batch normalization (keeps the input shape)
class ResBlock(nn.Module):
    def __init__(self, c):
        super().__init__()
        self.c1 = nn.Conv2d(c, c, 3, padding=1); self.bn1 = nn.BatchNorm2d(c)
        self.c2 = nn.Conv2d(c, c, 3, padding=1); self.bn2 = nn.BatchNorm2d(c)
    def forward(self, x):
        h = F.relu(self.bn1(self.c1(x)))
        h = self.bn2(self.c2(h))
        return F.relu(h + x)               # the skip (residual) connection
print("ResBlock keeps shape:", tuple(ResBlock(16)(torch.randn(2, 16, 8, 8)).shape))""",
"""# Batch norm helps a deep network train (ablation)
torch.manual_seed(0)
X = torch.randn(256, 16); y = torch.randint(0, 2, (256,))
def deepnet(bn):
    layers = []
    for _ in range(6):
        layers.append(nn.Linear(16, 16))
        if bn: layers.append(nn.BatchNorm1d(16))
        layers.append(nn.ReLU())
    return nn.Sequential(*layers, nn.Linear(16, 2))
for bn in [False, True]:
    m = deepnet(bn); o = torch.optim.SGD(m.parameters(), 0.1); f = nn.CrossEntropyLoss(); h = []
    for _ in range(60):
        o.zero_grad(); l = f(m(X), y); l.backward(); o.step(); h.append(l.item())
    plt.plot(h, label="with BN" if bn else "no BN")
plt.legend(); plt.xlabel("step"); plt.ylabel("loss"); plt.title("Normalization ablation"); plt.show()""",
"""# Residual connections let a deep network keep training
class Deep(nn.Module):
    def __init__(self, res):
        super().__init__(); self.res = res
        self.blocks = nn.ModuleList([nn.Linear(16, 16) for _ in range(12)])
        self.head = nn.Linear(16, 2)
    def forward(self, x):
        for b in self.blocks:
            h = F.relu(b(x)); x = h + x if self.res else h
        return self.head(x)
for res in [False, True]:
    m = Deep(res); o = torch.optim.SGD(m.parameters(), 0.05); f = nn.CrossEntropyLoss(); h = []
    for _ in range(80):
        o.zero_grad(); l = f(m(X), y); l.backward(); o.step(); h.append(l.item())
    plt.plot(h, label="residual" if res else "plain")
plt.legend(); plt.xlabel("step"); plt.ylabel("loss"); plt.title("Residual vs plain (12 layers)"); plt.show()""",
    ],
    10: [
"""# A plain RNN over a sequence
torch.manual_seed(0)
rnn = nn.RNN(input_size=1, hidden_size=16, batch_first=True)
x = torch.randn(8, 20, 1)                 # (batch, time, features)
out, h = rnn(x)
print("output sequence:", tuple(out.shape), "| final hidden:", tuple(h.shape))""",
"""# Gradient of the last output w.r.t. each input step: it vanishes for early steps
T = 40
rnn = nn.RNN(1, 8, batch_first=True)
x = torch.randn(1, T, 1, requires_grad=True)
out, _ = rnn(x)
out[:, -1].sum().backward()
g = x.grad.abs().squeeze().tolist()
plt.plot(range(T), g); plt.xlabel("time step"); plt.ylabel("|grad of last output|")
plt.title("Vanishing gradient"); plt.show()""",
"""# Gradient clipping caps the global gradient norm
rnn = nn.RNN(1, 8, batch_first=True); o = torch.optim.SGD(rnn.parameters(), 0.1)
x = torch.randn(4, 30, 1); y = torch.randn(4, 30, 8)
o.zero_grad(); out, _ = rnn(x); ((out - y) ** 2).mean().backward()
norm = torch.nn.utils.clip_grad_norm_(rnn.parameters(), max_norm=1.0)
print("grad norm before clip:", round(norm.item(), 3), "-> clipped to <= 1.0")""",
    ],
    11: [
"""# Same input through RNN, LSTM, and GRU (note the parameter counts)
x = torch.randn(8, 20, 1)
for name, layer in [("RNN", nn.RNN(1, 16, batch_first=True)),
                    ("LSTM", nn.LSTM(1, 16, batch_first=True)),
                    ("GRU", nn.GRU(1, 16, batch_first=True))]:
    out = layer(x)[0]
    print(f"{name:4s}: output {tuple(out.shape)}, params {sum(p.numel() for p in layer.parameters())}")""",
"""# The LSTM carries a hidden state h and a cell state c; gates are 4x hidden
lstm = nn.LSTM(1, 4, batch_first=True)
out, (h, c) = lstm(torch.randn(1, 5, 1))
print("hidden h:", tuple(h.shape), "| cell c:", tuple(c.shape))
print("weight_ih_l0:", tuple(lstm.weight_ih_l0.shape), "= (4*hidden, input): input/forget/cell/output gates")""",
"""# Gradient reaching the first step stays larger on long sequences than a plain RNN
lstm = nn.LSTM(1, 8, batch_first=True)
for T in [5, 100]:
    x = torch.randn(2, T, 1, requires_grad=True)
    out, _ = lstm(x); out[:, -1].sum().backward()
    print(f"seq len {T:3d}: gradient to first step ~ {x.grad.abs()[:, 0].mean().item():.2e}")""",
    ],
    12: [
"""# Train a small autoencoder on MNIST and show reconstructions
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
dl = DataLoader(datasets.MNIST("./data", train=True, download=True, transform=transforms.ToTensor()),
                batch_size=256, shuffle=True)
ae = nn.Sequential(nn.Flatten(), nn.Linear(784, 32), nn.ReLU(),
                   nn.Linear(32, 784), nn.Sigmoid()).to(device)
opt = torch.optim.Adam(ae.parameters(), 1e-3); f = nn.MSELoss()
for epoch in range(2):
    for xb, _ in dl:
        xb = xb.to(device); opt.zero_grad(); f(ae(xb).view_as(xb), xb).backward(); opt.step()
xb, _ = next(iter(dl)); xb = xb.to(device); rec = ae(xb).view_as(xb).detach().cpu()
fig, ax = plt.subplots(2, 5, figsize=(8, 3))
for i in range(5):
    ax[0, i].imshow(xb[i, 0].cpu(), cmap="gray"); ax[0, i].axis("off")
    ax[1, i].imshow(rec[i, 0], cmap="gray"); ax[1, i].axis("off")
plt.show()""",
"""# Interpolate between two examples (the idea behind latent interpolation)
a, b = xb[0].cpu(), xb[1].cpu()
fig, ax = plt.subplots(1, 6, figsize=(9, 2))
for i, alpha in enumerate(torch.linspace(0, 1, 6)):
    ax[i].imshow(((1 - alpha) * a + alpha * b)[0], cmap="gray"); ax[i].axis("off")
plt.show()""",
"""# Two augmented views of one image form a positive pair (contrastive setup)
from torchvision import transforms
aug = transforms.Compose([transforms.RandomResizedCrop(28, scale=(0.6, 1.0)),
                          transforms.RandomHorizontalFlip()])
img = xb[0].cpu()
fig, ax = plt.subplots(1, 3, figsize=(6, 2))
for a_, t, title in zip(ax, [img, aug(img), aug(img)], ["original", "view 1", "view 2"]):
    a_.imshow(t[0], cmap="gray"); a_.set_title(title); a_.axis("off")
plt.show()""",
    ],
    13: [
"""# Load a pretrained ResNet-18 and give it a fresh classification head
from torchvision import models
net = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
net.fc = nn.Linear(net.fc.in_features, 5)        # new 5-class head
print("pretrained ResNet-18, total params:", sum(p.numel() for p in net.parameters()))""",
"""# From-scratch vs frozen-features vs fine-tuning: trainable parameter counts
from torchvision import models
def trainable(m): return sum(p.numel() for p in m.parameters() if p.requires_grad)

frozen = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
for p in frozen.parameters(): p.requires_grad = False
frozen.fc = nn.Linear(frozen.fc.in_features, 5)
print("frozen-features trainable:", trainable(frozen))

ft = models.resnet18(weights=models.ResNet18_Weights.DEFAULT); ft.fc = nn.Linear(ft.fc.in_features, 5)
print("fine-tune trainable:     ", trainable(ft))

scratch = models.resnet18(weights=None); scratch.fc = nn.Linear(scratch.fc.in_features, 5)
print("from-scratch trainable:  ", trainable(scratch))""",
"""# End-to-end inference on one preprocessed input
net.eval()
with torch.no_grad():
    probs = net(torch.randn(1, 3, 224, 224)).softmax(1)
print("predicted class:", probs.argmax(1).item(), "| confidence:", round(probs.max().item(), 3))""",
    ],
}
