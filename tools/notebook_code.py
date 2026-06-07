# -*- coding: utf-8 -*-
"""Deep, sectioned content for the instructor PRACTICE notebooks (one per week).
NB[week] is an ordered list of cells, each ("md", text) or ("code", text), authored to
fill a 2-hour instructor-led practice lesson: worked demonstrations with explanations,
fuller code with output and plots, and "try it live" variations. The setup cell
(torch, nn, F, plt, device) runs first, so snippets assume it. Consumed by build_notebooks.py."""

# convenience for short markdown section headers
def _s(title, note=""):
    return ("md", f"## {title}" + (f"\n{note}" if note else ""))

NB = {

# ============================== WEEK 1 ==============================
1: [
 _s("1. Tensors live on a device", "Everything is a tensor; a tensor lives on the CPU or the GPU."),
 ("code",
"""x = torch.randn(2, 3)
print("on cpu:", x.device, "| shape:", tuple(x.shape), "| dtype:", x.dtype)
x = x.to(device)
print("moved to:", x.device)
print("a few ops:", x.sum().item(), x.mean().item())"""),

 _s("2. A neuron, then a layer", "A linear layer is just w.x + b applied to every row of the input."),
 ("code",
"""layer = nn.Linear(in_features=3, out_features=1)
print("weight:", tuple(layer.weight.shape), "bias:", tuple(layer.bias.shape))
batch = torch.randn(4, 3)              # 4 samples, 3 features
print("output:", tuple(layer(batch).shape), "(one value per sample)")"""),

 _s("3. A minimal training loop", "Toy task: learn y = 2x + 1 from noisy data. Watch the four steps: forward, loss, backward, step."),
 ("code",
"""torch.manual_seed(0)
X = torch.randn(200, 1)
y = 2 * X + 1 + 0.1 * torch.randn(200, 1)

model = nn.Linear(1, 1)
opt = torch.optim.SGD(model.parameters(), lr=0.1)
loss_fn = nn.MSELoss()

losses = []
for epoch in range(60):
    opt.zero_grad()           # 1. clear old gradients
    pred = model(X)           # 2. forward
    loss = loss_fn(pred, y)   # 3. measure error
    loss.backward()           # 4. gradients
    opt.step()                # 5. update weights
    losses.append(loss.item())

print(f"learned weight {model.weight.item():.3f} (target 2.0), bias {model.bias.item():.3f} (target 1.0)")
plt.plot(losses); plt.xlabel("epoch"); plt.ylabel("MSE loss"); plt.title("Training loss"); plt.show()"""),

 ("md", "**Try it live:** change `lr` to 0.01 and to 1.5 and re-run. The next cell does all three at once."),
 ("code",
"""def train(lr, steps=60):
    torch.manual_seed(0)
    m = nn.Linear(1, 1); o = torch.optim.SGD(m.parameters(), lr=lr); f = nn.MSELoss()
    h = []
    for _ in range(steps):
        o.zero_grad(); l = f(m(X), y); l.backward(); o.step(); h.append(l.item())
    return h

for lr in [0.01, 0.1, 1.5]:
    plt.plot(train(lr), label=f"lr={lr}")
plt.yscale("log"); plt.xlabel("step"); plt.ylabel("loss (log)"); plt.legend()
plt.title("Too small crawls, good converges, too large diverges"); plt.show()"""),

 _s("4. Framing: classification vs regression", "Same machinery, different output layer and loss."),
 ("code",
"""xb = torch.randn(8, 4)                          # 8 samples, 4 features

# Classification: one logit per class + cross-entropy
clf = nn.Linear(4, 3)
ce = nn.CrossEntropyLoss()(clf(xb), torch.randint(0, 3, (8,)))
print("classification -> logits", tuple(clf(xb).shape), "| CE loss", round(ce.item(), 3))

# Regression: one value + MSE
reg = nn.Linear(4, 1)
mse = nn.MSELoss()(reg(xb), torch.randn(8, 1))
print("regression     -> output", tuple(reg(xb).shape), "| MSE loss", round(mse.item(), 3))"""),

 _s("5. End to end: a tiny classifier", "Train a 2-class model on a separable toy set and read accuracy."),
 ("code",
"""torch.manual_seed(0)
Xc = torch.randn(300, 2); yc = (Xc[:, 0] + Xc[:, 1] > 0).long()
clf = nn.Sequential(nn.Linear(2, 16), nn.ReLU(), nn.Linear(16, 2))
opt = torch.optim.Adam(clf.parameters(), lr=0.05); loss_fn = nn.CrossEntropyLoss()
for epoch in range(80):
    opt.zero_grad(); loss = loss_fn(clf(Xc), yc); loss.backward(); opt.step()
acc = (clf(Xc).argmax(1) == yc).float().mean()
print(f"final loss {loss.item():.3f} | accuracy {acc.item():.3f}")"""),

 ("md", "**Discuss:** what would change to make this a 3-class problem? A regression problem? (Output size and loss.)"),
],

# ============================== WEEK 2 ==============================
2: [
 _s("1. Shape, dtype, device", "Three properties to check whenever something breaks."),
 ("code",
"""t = torch.arange(24)
print("shape", tuple(t.shape), "| dtype", t.dtype, "| device", t.device)
t = t.reshape(2, 3, 4)
print("reshaped", tuple(t.shape))
print("permute(2,0,1)", tuple(t.permute(2, 0, 1).shape))
print("t[0,1] ->", t[0, 1].tolist())
print("t[:,:,0] ->", tuple(t[:, :, 0].shape))
print("sum over last dim ->", tuple(t.sum(dim=-1).shape))"""),

 _s("2. Views vs copies", "A view shares memory; changing it changes the original."),
 ("code",
"""a = torch.arange(6)
b = a.view(2, 3)        # shares memory
b[0, 0] = 99
print("a after editing its view:", a.tolist())   # a is changed too
c = a.reshape(3, 2).clone()  # clone breaks the link
c[0, 0] = -1
print("a after editing a clone:", a.tolist())"""),

 _s("3. Broadcasting", "Shapes are compared from the trailing dimension; a size of 1 expands."),
 ("code",
"""a = torch.ones(3, 1); b = torch.ones(1, 4)
print("(3,1) + (1,4) ->", tuple((a + b).shape))          # 3x4
row = torch.arange(4.0)
mat = torch.zeros(3, 4)
print("matrix + row ->", (mat + row).tolist())           # row added to each row"""),

 ("md", "**Predict before running:** what is the result shape of `torch.ones(5,1,4) + torch.ones(3,1)`? Then run it."),
 ("code", "print(tuple((torch.ones(5, 1, 4) + torch.ones(3, 1)).shape))   # broadcasting puzzle"),

 _s("4. A shape-mismatch error, then the fix", "Read the error: it names the incompatible dimensions."),
 ("code",
"""x = torch.ones(3, 4); w = torch.ones(5)   # wrong trailing size
try:
    x + w
except RuntimeError as e:
    print("ERROR:", str(e).splitlines()[0])
w = torch.ones(4)                          # fix: matches trailing dim 4
print("fixed (3,4)+(4,) ->", tuple((x + w).shape))"""),

 _s("5. Encoding real data as tensors", "An image becomes (C, H, W); a table becomes (rows, features)."),
 ("code",
"""import numpy as np
img = np.random.randint(0, 256, size=(8, 8, 3), dtype=np.uint8)   # H, W, C
img_t = torch.from_numpy(img).permute(2, 0, 1).float() / 255.0     # -> C, H, W in [0,1]
print("image tensor:", tuple(img_t.shape), img_t.dtype, "range", img_t.min().item(), img_t.max().item())

table = torch.tensor([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
print("table tensor:", tuple(table.shape))
img_t, table = img_t.to(device), table.to(device)
print("moved to", img_t.device)"""),

 ("md", "**Try it live:** normalize the table to zero mean and unit variance per column with broadcasting (`(table - table.mean(0)) / table.std(0)`)."),
],

# ============================== WEEK 3 ==============================
3: [
 _s("1. Build an MLP", "Linear layers plus a nonlinearity. nn.Module bundles parameters and the forward pass."),
 ("code",
"""class MLP(nn.Module):
    def __init__(self, d_in=2, d_hidden=16, d_out=2):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d_in, d_hidden), nn.ReLU(), nn.Linear(d_hidden, d_out))
    def forward(self, x):
        return self.net(x)

model = MLP()
print(model)
print("parameter tensors:", sum(p.numel() for p in model.parameters()))"""),

 _s("2. Why the nonlinearity matters", "Without ReLU, two linear layers collapse to one linear map."),
 ("code",
"""torch.manual_seed(0)
X = torch.randn(400, 2); y = (X[:, 0] * X[:, 1] > 0).long()   # XOR-like, not linearly separable

def fit(model, steps=300):
    o = torch.optim.Adam(model.parameters(), 0.03); f = nn.CrossEntropyLoss()
    for _ in range(steps):
        o.zero_grad(); f(model(X), y).backward(); o.step()
    return (model(X).argmax(1) == y).float().mean().item()

linear = nn.Sequential(nn.Linear(2, 16), nn.Linear(16, 2))      # no activation
print("no nonlinearity  accuracy:", round(fit(linear), 3))
print("with ReLU (MLP)  accuracy:", round(fit(MLP()), 3))"""),

 _s("3. Inspect gradients", "backward() fills .grad. Gradients ACCUMULATE, so zero them each step."),
 ("code",
"""w = torch.tensor([2.0], requires_grad=True)
(w ** 2).sum().backward(); print("after 1st backward (d/dw of w^2 = 2w = 4):", w.grad.item())
(w ** 2).sum().backward(); print("WITHOUT zero_grad (accumulated to 8):", w.grad.item())
w.grad.zero_()
(w ** 2).sum().backward(); print("AFTER zero_grad (back to 4):", w.grad.item())"""),

 _s("4. Hand-derived gradient vs autograd", "Sanity-check autograd on something you can differentiate by hand."),
 ("code",
"""xs = torch.tensor(3.0, requires_grad=True)
ys = xs ** 3 + 2 * xs          # dy/dx = 3x^2 + 2 -> 29 at x = 3
ys.backward()
print("autograd:", xs.grad.item(), "| by hand 3*x^2+2:", 3 * 3 ** 2 + 2)"""),

 ("md", "**Try it live:** add `gradcheck`. `torch.autograd.gradcheck` compares autograd to a numerical estimate."),
 ("code",
"""from torch.autograd import gradcheck
f = lambda a: (a ** 3 + 2 * a).sum()
ok = gradcheck(f, (torch.randn(4, dtype=torch.double, requires_grad=True),))
print("gradcheck passed:", ok)"""),

 _s("5. Train the MLP and read the loss", "Put it together: the same four-step loop from week 1, now with a real network."),
 ("code",
"""model = MLP(); o = torch.optim.Adam(model.parameters(), 0.03); f = nn.CrossEntropyLoss()
hist = []
for _ in range(300):
    o.zero_grad(); l = f(model(X), y); l.backward(); o.step(); hist.append(l.item())
print("final accuracy:", round((model(X).argmax(1) == y).float().mean().item(), 3))
plt.plot(hist); plt.xlabel("step"); plt.ylabel("loss"); plt.show()"""),
],

# ============================== WEEK 4 ==============================
4: [
 _s("1. A custom Dataset", "Implement __len__ and __getitem__ to return one (input, label)."),
 ("code",
"""from torch.utils.data import Dataset, DataLoader

class ToyData(Dataset):
    def __init__(self, n=120):
        self.x = torch.randn(n, 3)
        self.y = (self.x.sum(1) > 0).long()
    def __len__(self):
        return len(self.x)
    def __getitem__(self, i):
        return self.x[i], self.y[i]

ds = ToyData()
print("len:", len(ds), "| one item:", ds[0][0].shape, ds[0][1].item())"""),

 _s("2. A DataLoader batches and shuffles", "Iterating yields batches shaped (batch, ...)."),
 ("code",
"""dl = DataLoader(ds, batch_size=16, shuffle=True)
xb, yb = next(iter(dl))
print("batch:", tuple(xb.shape), tuple(yb.shape))
for i, (xb, yb) in enumerate(dl):
    print("batch", i, "->", xb.shape[0], "samples")
    if i == 3:
        break"""),

 _s("3. Batch size and shuffling", "Batch size sets the steps per epoch; shuffling reorders every epoch."),
 ("code",
"""for bs in [8, 16, 64]:
    print(f"batch_size={bs}: {len(DataLoader(ds, batch_size=bs))} batches per epoch")
dl = DataLoader(ds, batch_size=4, shuffle=True)
print("epoch 1 first labels:", next(iter(dl))[1].tolist())
print("epoch 2 first labels:", next(iter(dl))[1].tolist())"""),

 _s("4. A train / validation / test split", "Tune on validation, touch test once. random_split is the easy way."),
 ("code",
"""from torch.utils.data import random_split
g = torch.Generator().manual_seed(0)
tr, va, te = random_split(ds, [80, 20, 20], generator=g)
print("sizes:", len(tr), len(va), len(te))
train_dl = DataLoader(tr, batch_size=16, shuffle=True)
val_dl   = DataLoader(va, batch_size=16)            # no shuffle for val/test"""),

 _s("5. Data leakage, demonstrated", "Normalizing with whole-dataset statistics leaks test information."),
 ("code",
"""data = torch.randn(100, 1) * 5 + 10
train, test = data[:80], data[80:]

mu, sd = data.mean(), data.std()                 # LEAK: uses test data
print("leaky   test mean ~ 0:", round(((test - mu) / sd).mean().item(), 3))

mu, sd = train.mean(), train.std()               # correct: train only
print("correct test mean (not 0):", round(((test - mu) / sd).mean().item(), 3))"""),

 ("md", "**Discuss:** name three other ways leakage sneaks in (feature selection on all data, time order ignored, duplicate rows across splits)."),
],

# ============================== WEEK 5 ==============================
5: [
 _s("1. A reusable train/eval loop", "Track both loss and a metric; switch to eval mode for evaluation."),
 ("code",
"""torch.manual_seed(0)
X = torch.randn(400, 4); y = (X.sum(1) > 0).long()
Xtr, ytr, Xte, yte = X[:300], y[:300], X[300:], y[300:]
model = nn.Linear(4, 2); opt = torch.optim.Adam(model.parameters(), 0.05); loss_fn = nn.CrossEntropyLoss()

def accuracy(logits, target):
    return (logits.argmax(1) == target).float().mean().item()

for epoch in range(60):
    model.train(); opt.zero_grad()
    loss = loss_fn(model(Xtr), ytr); loss.backward(); opt.step()
    if epoch % 15 == 0:
        model.eval()
        with torch.no_grad():
            print(f"epoch {epoch:2d}: train acc {accuracy(model(Xtr), ytr):.3f} | test acc {accuracy(model(Xte), yte):.3f}")"""),

 _s("2. The right loss matters", "Cross-entropy expects logits and class indices; squaring label numbers is meaningless."),
 ("code",
"""logits = model(Xte)
ce = nn.CrossEntropyLoss()(logits, yte)
mse_on_labels = nn.MSELoss()(logits.argmax(1).float(), yte.float())   # treats classes as numbers
print("cross-entropy (correct):", round(ce.item(), 3))
print("MSE on label numbers (meaningless):", round(mse_on_labels.item(), 3))"""),

 _s("3. Accuracy can lie", "On imbalanced data a trivial predictor scores high; precision/recall/F1 expose it."),
 ("code",
"""y_true = torch.cat([torch.zeros(95), torch.ones(5)]).long()
y_pred = torch.zeros(100).long()                 # always predict the majority class
tp = ((y_pred == 1) & (y_true == 1)).sum().item()
fp = ((y_pred == 1) & (y_true == 0)).sum().item()
fn = ((y_pred == 0) & (y_true == 1)).sum().item()
prec = tp / (tp + fp + 1e-9); rec = tp / (tp + fn + 1e-9)
f1 = 2 * prec * rec / (prec + rec + 1e-9)
acc = (y_pred == y_true).float().mean().item()
print(f"accuracy {acc:.2f}  but  precision {prec:.2f}  recall {rec:.2f}  F1 {f1:.2f}")"""),

 _s("4. The confusion matrix", "Two lines, no library: it shows exactly where errors go."),
 ("code",
"""def confusion(pred, true, k=2):
    m = torch.zeros(k, k, dtype=torch.long)
    for p, t in zip(pred, true):
        m[t, p] += 1
    return m
print("rows = true, cols = predicted\\n", confusion(y_pred, y_true))"""),

 ("md", "**Try it live:** make `y_pred` predict the minority class 3 times correctly and recompute precision, recall, and F1."),
],

# ============================== WEEK 6 ==============================
6: [
 _s("1. One model, three optimizers", "SGD, SGD+momentum, and Adam on the same problem."),
 ("code",
"""torch.manual_seed(0)
X = torch.randn(200, 5); y = X @ torch.randn(5, 1) + 0.1 * torch.randn(200, 1)

def run(name, steps=80):
    torch.manual_seed(0); m = nn.Linear(5, 1); f = nn.MSELoss()
    o = {"SGD": torch.optim.SGD(m.parameters(), lr=0.05),
         "Momentum": torch.optim.SGD(m.parameters(), lr=0.05, momentum=0.9),
         "Adam": torch.optim.Adam(m.parameters(), lr=0.05)}[name]
    h = []
    for _ in range(steps):
        o.zero_grad(); l = f(m(X), y); l.backward(); o.step(); h.append(l.item())
    return h

for name in ["SGD", "Momentum", "Adam"]:
    plt.plot(run(name), label=name)
plt.legend(); plt.xlabel("step"); plt.ylabel("loss"); plt.title("Optimizer comparison"); plt.show()"""),

 _s("2. The learning rate is everything", "A three-rate sweep: too small, good, too large."),
 ("code",
"""for lr in [0.001, 0.05, 0.5]:
    torch.manual_seed(0); m = nn.Linear(5, 1); o = torch.optim.SGD(m.parameters(), lr=lr); f = nn.MSELoss()
    h = []
    for _ in range(80):
        o.zero_grad(); l = f(m(X), y); l.backward(); o.step(); h.append(l.item())
    plt.plot(h, label=f"lr={lr}")
plt.yscale("log"); plt.legend(); plt.xlabel("step"); plt.ylabel("loss (log)"); plt.show()"""),

 _s("3. Read the curve to diagnose", "Spikes = too large; flat = too small; smooth decline = good."),
 ("code",
"""# deliberately too large -> watch it blow up
torch.manual_seed(0); m = nn.Linear(5, 1); o = torch.optim.SGD(m.parameters(), lr=1.2); f = nn.MSELoss()
h = []
for _ in range(40):
    o.zero_grad(); l = f(m(X), y); l.backward(); o.step(); h.append(l.item())
print("loss exploded to:", h[-1])
plt.plot(h); plt.title("lr too large: divergence"); plt.xlabel("step"); plt.ylabel("loss"); plt.show()"""),

 _s("4. A learning-rate schedule", "Step decay: lower the rate as training settles."),
 ("code",
"""m = nn.Linear(5, 1); o = torch.optim.SGD(m.parameters(), lr=0.2); f = nn.MSELoss()
sched = torch.optim.lr_scheduler.StepLR(o, step_size=25, gamma=0.3)
lrs, h = [], []
for _ in range(80):
    o.zero_grad(); l = f(m(X), y); l.backward(); o.step(); sched.step()
    lrs.append(o.param_groups[0]["lr"]); h.append(l.item())
fig, ax = plt.subplots(1, 2, figsize=(9, 3))
ax[0].plot(lrs); ax[0].set_title("learning rate"); ax[1].plot(h); ax[1].set_title("loss")
plt.show()"""),

 ("md", "**Try it live:** swap `StepLR` for `CosineAnnealingLR(o, T_max=80)` and compare the curves."),
],

# ============================== WEEK 7 ==============================
7: [
 _s("1. Make a model overfit", "Tiny training set, large model: train accuracy goes high, test stays at chance."),
 ("code",
"""torch.manual_seed(0)
Xtr = torch.randn(30, 20); ytr = torch.randint(0, 2, (30,))   # 30 samples, random labels
Xte = torch.randn(300, 20); yte = torch.randint(0, 2, (300,))

def fit(model, epochs=250, wd=0.0):
    o = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=wd); f = nn.CrossEntropyLoss()
    tr, te = [], []
    for _ in range(epochs):
        model.train(); o.zero_grad(); f(model(Xtr), ytr).backward(); o.step()
        model.eval()
        with torch.no_grad():
            tr.append((model(Xtr).argmax(1) == ytr).float().mean().item())
            te.append((model(Xte).argmax(1) == yte).float().mean().item())
    return tr, te

big = lambda: nn.Sequential(nn.Linear(20, 128), nn.ReLU(), nn.Linear(128, 128), nn.ReLU(), nn.Linear(128, 2))
tr, te = fit(big())
print(f"overfit: train {tr[-1]:.2f} vs test {te[-1]:.2f}")
plt.plot(tr, label="train"); plt.plot(te, label="test"); plt.legend(); plt.title("Overfitting"); plt.show()"""),

 _s("2. Weight decay and dropout close the gap", "Same model, add regularization, watch the gap shrink."),
 ("code",
"""reg = nn.Sequential(nn.Linear(20, 128), nn.ReLU(), nn.Dropout(0.5),
                    nn.Linear(128, 128), nn.ReLU(), nn.Dropout(0.5), nn.Linear(128, 2))
tr, te = fit(reg, wd=1e-2)
print(f"regularized: train {tr[-1]:.2f} vs test {te[-1]:.2f}")
plt.plot(tr, label="train"); plt.plot(te, label="test"); plt.legend(); plt.title("With dropout + weight decay"); plt.show()"""),

 _s("3. Dropout behaves differently at train vs eval", "On in training (random zeros), off at eval (deterministic)."),
 ("code",
"""drop = nn.Dropout(0.5)
x = torch.ones(1, 10)
drop.train(); print("train (random zeros):", drop(x))
drop.eval();  print("eval  (identity)    :", drop(x))"""),

 _s("4. Data augmentation (train only)", "Augmentation enlarges the effective training set."),
 ("code",
"""from torchvision import transforms
img = torch.rand(3, 32, 32)
aug = transforms.Compose([transforms.RandomHorizontalFlip(p=1.0), transforms.RandomCrop(32, padding=4)])
print("original", tuple(img.shape), "-> augmented", tuple(aug(img).shape))
print("two augmentations differ:", not torch.equal(aug(img), aug(img)))"""),

 ("md", "**Discuss:** why must augmentation and dropout be OFF at test time? (We evaluate the real model on real inputs.)"),
],

# ============================== WEEK 8 ==============================
8: [
 _s("1. What a convolution does", "A small learned filter slides over the input, sharing weights across positions."),
 ("code",
"""conv = nn.Conv2d(in_channels=1, out_channels=4, kernel_size=3, padding=1)
x = torch.randn(1, 1, 8, 8)
print("input ", tuple(x.shape), "-> output", tuple(conv(x).shape))   # 4 feature maps, same H,W (padding=1)
print("filter weights:", tuple(conv.weight.shape), "(out, in, kh, kw)")"""),

 _s("2. Output size and parameter count", "out = floor((in + 2p - k)/s) + 1 ; conv params = (k*k*Cin + 1)*Cout."),
 ("code",
"""c = nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1)
print("output:", tuple(c(torch.randn(1, 3, 32, 32)).shape), " formula (32+2-3)/1+1 = 32")
print("params:", sum(p.numel() for p in c.parameters()), "= (3*3*3 + 1) * 16 =", (3 * 3 * 3 + 1) * 16)"""),

 _s("3. Build a CNN and trace shapes", "Stack conv/pool blocks; channels grow while spatial size shrinks."),
 ("code",
"""cnn = nn.Sequential(
    nn.Conv2d(1, 8, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),     # 28 -> 14
    nn.Conv2d(8, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),    # 14 -> 7
    nn.Flatten(), nn.Linear(16 * 7 * 7, 10))
x = torch.randn(4, 1, 28, 28)
for layer in cnn:
    x = layer(x); print(f"{layer.__class__.__name__:9s}", tuple(x.shape))"""),

 _s("4. Train on FashionMNIST", "A couple of hundred steps is enough to see it learn (downloads ~30 MB)."),
 ("code",
"""from torchvision import datasets, transforms
from torch.utils.data import DataLoader
train = datasets.FashionMNIST("./data", train=True, download=True, transform=transforms.ToTensor())
dl = DataLoader(train, batch_size=128, shuffle=True)
model = nn.Sequential(nn.Conv2d(1, 8, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
                      nn.Flatten(), nn.Linear(8 * 14 * 14, 10)).to(device)
opt = torch.optim.Adam(model.parameters(), 1e-3); f = nn.CrossEntropyLoss()
for step, (xb, yb) in enumerate(dl):
    xb, yb = xb.to(device), yb.to(device)
    opt.zero_grad(); loss = f(model(xb), yb); loss.backward(); opt.step()
    if step % 50 == 0:
        print(f"step {step}: loss {loss.item():.3f}")
    if step == 200:
        break"""),

 _s("5. Visualize the first-layer feature maps", "Each map is one filter's response across the image."),
 ("code",
"""fmap = model[0](xb[:1]).detach().cpu()
fig, ax = plt.subplots(1, 8, figsize=(12, 2))
for i in range(8):
    ax[i].imshow(fmap[0, i]); ax[i].axis("off")
plt.suptitle("First-conv feature maps"); plt.show()"""),
],

# ============================== WEEK 9 ==============================
9: [
 _s("1. A residual block", "out = F(x) + x keeps the input shape and adds a skip path."),
 ("code",
"""class ResBlock(nn.Module):
    def __init__(self, c):
        super().__init__()
        self.c1 = nn.Conv2d(c, c, 3, padding=1); self.bn1 = nn.BatchNorm2d(c)
        self.c2 = nn.Conv2d(c, c, 3, padding=1); self.bn2 = nn.BatchNorm2d(c)
    def forward(self, x):
        h = F.relu(self.bn1(self.c1(x)))
        h = self.bn2(self.c2(h))
        return F.relu(h + x)              # the skip connection
print("ResBlock keeps shape:", tuple(ResBlock(16)(torch.randn(2, 16, 8, 8)).shape))"""),

 _s("2. Batch norm helps a deep net train", "Ablation: with vs without batch normalization."),
 ("code",
"""torch.manual_seed(0)
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
    for _ in range(80):
        o.zero_grad(); l = f(m(X), y); l.backward(); o.step(); h.append(l.item())
    plt.plot(h, label="with BN" if bn else "no BN")
plt.legend(); plt.xlabel("step"); plt.ylabel("loss"); plt.title("Normalization ablation"); plt.show()"""),

 _s("3. Residual connections at depth", "Plain 12-layer net vs the same with skips."),
 ("code",
"""class Deep(nn.Module):
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
    for _ in range(100):
        o.zero_grad(); l = f(m(X), y); l.backward(); o.step(); h.append(l.item())
    plt.plot(h, label="residual" if res else "plain")
plt.legend(); plt.xlabel("step"); plt.ylabel("loss"); plt.title("Residual vs plain (12 layers)"); plt.show()"""),

 _s("4. Batch norm: train vs eval statistics", "It uses batch stats in training, running stats at eval."),
 ("code",
"""bn = nn.BatchNorm1d(4)
x = torch.randn(8, 4) * 5 + 3
bn.train(); _ = bn(x)
print("running mean after a train batch:", bn.running_mean.round(decimals=2).tolist())
bn.eval(); print("eval uses those running stats, not the current batch.")"""),

 ("md", "**Discuss:** why do very deep PLAIN networks train worse, not just slower? (Gradients struggle to reach early layers; residuals give them a direct path.)"),
],

# ============================== WEEK 10 ==============================
10: [
 _s("1. An RNN over a sequence", "It carries a hidden state forward, reusing the same weights at every step."),
 ("code",
"""torch.manual_seed(0)
rnn = nn.RNN(input_size=1, hidden_size=16, batch_first=True)
x = torch.randn(8, 20, 1)                 # (batch, time, features)
out, h = rnn(x)
print("output sequence:", tuple(out.shape), "| final hidden:", tuple(h.shape))
print("the same weight is used at all 20 steps:", tuple(rnn.weight_hh_l0.shape))"""),

 _s("2. Vanishing gradients, measured", "Gradient of the LAST output w.r.t. each input step shrinks for early steps."),
 ("code",
"""T = 40
rnn = nn.RNN(1, 8, batch_first=True)
x = torch.randn(1, T, 1, requires_grad=True)
out, _ = rnn(x)
out[:, -1].sum().backward()
g = x.grad.abs().squeeze().tolist()
plt.plot(range(T), g); plt.xlabel("time step"); plt.ylabel("|grad of last output|")
plt.title("Early steps receive tiny gradients"); plt.show()
print("grad at step 0:", f"{g[0]:.2e}", "| grad at last step:", f"{g[-1]:.2e}")"""),

 _s("3. Gradient clipping", "Cap the global gradient norm so a spike cannot blow up training."),
 ("code",
"""rnn = nn.RNN(1, 8, batch_first=True); o = torch.optim.SGD(rnn.parameters(), 0.1)
x = torch.randn(4, 30, 1); y = torch.randn(4, 30, 8)
o.zero_grad(); out, _ = rnn(x); ((out - y) ** 2).mean().backward()
norm = torch.nn.utils.clip_grad_norm_(rnn.parameters(), max_norm=1.0)
print("global grad norm before clip:", round(norm.item(), 3), "-> clipped to <= 1.0")"""),

 _s("4. A tiny sequence task end to end", "Predict whether a short random walk ends positive."),
 ("code",
"""torch.manual_seed(0)
seqs = torch.randn(400, 15, 1)
labels = (seqs.sum(dim=1).squeeze() > 0).long()
class SeqClf(nn.Module):
    def __init__(self):
        super().__init__(); self.rnn = nn.RNN(1, 16, batch_first=True); self.head = nn.Linear(16, 2)
    def forward(self, x):
        out, _ = self.rnn(x); return self.head(out[:, -1])     # last hidden -> 2 classes
m = SeqClf(); o = torch.optim.Adam(m.parameters(), 0.01); f = nn.CrossEntropyLoss()
for _ in range(120):
    o.zero_grad(); f(m(seqs), labels).backward(); o.step()
print("accuracy:", round((m(seqs).argmax(1) == labels).float().mean().item(), 3))"""),

 ("md", "**Try it live:** raise the sequence length to 60 and see the accuracy drop, the vanishing-gradient problem in action."),
],

# ============================== WEEK 11 ==============================
11: [
 _s("1. RNN vs LSTM vs GRU", "Same input; note the parameter counts (gates cost more weights)."),
 ("code",
"""x = torch.randn(8, 20, 1)
for name, layer in [("RNN", nn.RNN(1, 16, batch_first=True)),
                    ("LSTM", nn.LSTM(1, 16, batch_first=True)),
                    ("GRU", nn.GRU(1, 16, batch_first=True))]:
    out = layer(x)[0]
    print(f"{name:4s}: output {tuple(out.shape)}, params {sum(p.numel() for p in layer.parameters())}")"""),

 _s("2. The cell state and gates", "An LSTM returns a hidden state h and a cell state c; weights are 4x hidden (four gates)."),
 ("code",
"""lstm = nn.LSTM(1, 4, batch_first=True)
out, (h, c) = lstm(torch.randn(1, 5, 1))
print("hidden h:", tuple(h.shape), "| cell c:", tuple(c.shape))
print("weight_ih_l0:", tuple(lstm.weight_ih_l0.shape), "= (4*hidden, input): input/forget/cell/output gates")"""),

 _s("3. Gates preserve gradients over long sequences", "Compare the gradient reaching the first step: RNN vs LSTM."),
 ("code",
"""def first_step_grad(layer, T):
    x = torch.randn(1, T, 1, requires_grad=True)
    out = layer(x)[0]; out[:, -1].sum().backward()
    return x.grad.abs()[:, 0].mean().item()
for T in [10, 50, 100]:
    r = first_step_grad(nn.RNN(1, 8, batch_first=True), T)
    l = first_step_grad(nn.LSTM(1, 8, batch_first=True), T)
    print(f"T={T:3d}:  RNN {r:.2e}   LSTM {l:.2e}")"""),

 _s("4. Same task, RNN vs LSTM", "On a longer-range task the gated unit usually wins."),
 ("code",
"""torch.manual_seed(0)
seqs = torch.randn(500, 40, 1); labels = (seqs[:, 0, 0] > 0).long()   # answer depends on the FIRST step
def make(cell):
    class M(nn.Module):
        def __init__(self):
            super().__init__(); self.r = cell(1, 16, batch_first=True); self.head = nn.Linear(16, 2)
        def forward(self, x):
            out, *_ = self.r(x); return self.head(out[:, -1])
    return M()
for name, cell in [("RNN", nn.RNN), ("LSTM", nn.LSTM)]:
    m = make(cell); o = torch.optim.Adam(m.parameters(), 0.01); f = nn.CrossEntropyLoss()
    for _ in range(150):
        o.zero_grad(); f(m(seqs), labels).backward(); o.step()
    print(name, "accuracy:", round((m(seqs).argmax(1) == labels).float().mean().item(), 3))"""),

 ("md", "**Discuss:** the label depends on the very first time step, 40 steps back. Why does the LSTM handle this better than the plain RNN?"),
],

# ============================== WEEK 12 ==============================
12: [
 _s("1. Train an autoencoder on MNIST", "Compress to a small bottleneck, then reconstruct (downloads ~10 MB)."),
 ("code",
"""from torchvision import datasets, transforms
from torch.utils.data import DataLoader
dl = DataLoader(datasets.MNIST("./data", train=True, download=True, transform=transforms.ToTensor()),
                batch_size=256, shuffle=True)
ae = nn.Sequential(nn.Flatten(), nn.Linear(784, 64), nn.ReLU(), nn.Linear(64, 16), nn.ReLU(),   # encoder
                   nn.Linear(16, 64), nn.ReLU(), nn.Linear(64, 784), nn.Sigmoid()).to(device)   # decoder
opt = torch.optim.Adam(ae.parameters(), 1e-3); f = nn.MSELoss()
for epoch in range(2):
    for xb, _ in dl:
        xb = xb.to(device); opt.zero_grad(); f(ae(xb).view_as(xb), xb).backward(); opt.step()
    print(f"epoch {epoch}: reconstruction MSE {f(ae(xb).view_as(xb), xb).item():.4f}")"""),

 _s("2. Reconstructions", "Top row: originals; bottom row: the autoencoder's reconstruction through a 16-d bottleneck."),
 ("code",
"""xb, _ = next(iter(dl)); xb = xb.to(device); rec = ae(xb).view_as(xb).detach().cpu()
fig, ax = plt.subplots(2, 8, figsize=(12, 3))
for i in range(8):
    ax[0, i].imshow(xb[i, 0].cpu(), cmap="gray"); ax[0, i].axis("off")
    ax[1, i].imshow(rec[i, 0], cmap="gray"); ax[1, i].axis("off")
plt.show()"""),

 _s("3. Latent interpolation", "Walk in pixel space between two digits, the idea behind interpolating in a learned latent space."),
 ("code",
"""a, b = xb[0].cpu(), xb[1].cpu()
fig, ax = plt.subplots(1, 6, figsize=(9, 2))
for i, alpha in enumerate(torch.linspace(0, 1, 6)):
    ax[i].imshow(((1 - alpha) * a + alpha * b)[0], cmap="gray"); ax[i].axis("off")
plt.show()"""),

 _s("4. The contrastive idea", "Two augmented views of one image form a positive pair; everything else is negative."),
 ("code",
"""from torchvision import transforms
aug = transforms.Compose([transforms.RandomResizedCrop(28, scale=(0.6, 1.0)), transforms.RandomHorizontalFlip()])
img = xb[0].cpu()
fig, ax = plt.subplots(1, 3, figsize=(6, 2))
for a_, t, title in zip(ax, [img, aug(img), aug(img)], ["original", "view 1", "view 2"]):
    a_.imshow(t[0], cmap="gray"); a_.set_title(title); a_.axis("off")
plt.show()"""),

 ("md", "**Discuss:** the augmentation policy defines what 'similar' means. What would the model learn if the only augmentation were a color shift?"),
],

# ============================== WEEK 13 ==============================
13: [
 _s("1. A pretrained model with a new head", "Load ResNet-18 trained on ImageNet, replace the final layer for 5 classes (downloads ~45 MB)."),
 ("code",
"""from torchvision import models
net = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
print("original final layer:", net.fc)
net.fc = nn.Linear(net.fc.in_features, 5)        # new 5-class head
print("new final layer:", net.fc)
print("total params:", sum(p.numel() for p in net.parameters()))"""),

 _s("2. Three regimes, by trainable-parameter count", "From-scratch trains everything from random; frozen trains only the head; fine-tune trains all from pretrained."),
 ("code",
"""from torchvision import models
def trainable(m): return sum(p.numel() for p in m.parameters() if p.requires_grad)

frozen = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
for p in frozen.parameters(): p.requires_grad = False
frozen.fc = nn.Linear(frozen.fc.in_features, 5)
print("frozen-features trainable:", f"{trainable(frozen):,}")

ft = models.resnet18(weights=models.ResNet18_Weights.DEFAULT); ft.fc = nn.Linear(ft.fc.in_features, 5)
print("fine-tune trainable:     ", f"{trainable(ft):,}")

scratch = models.resnet18(weights=None); scratch.fc = nn.Linear(scratch.fc.in_features, 5)
print("from-scratch trainable:  ", f"{trainable(scratch):,}")"""),

 _s("3. Layer-wise learning rates", "Fine-tuning usually uses a smaller rate on the pretrained backbone than on the new head."),
 ("code",
"""opt = torch.optim.Adam([
    {"params": ft.fc.parameters(), "lr": 1e-3},                 # new head: faster
    {"params": [p for n, p in ft.named_parameters() if not n.startswith("fc")], "lr": 1e-5},  # backbone: slower
])
print("param groups and their learning rates:", [g["lr"] for g in opt.param_groups])"""),

 _s("4. Inference end to end", "Eval mode, no gradients, softmax to probabilities."),
 ("code",
"""net.eval()
with torch.no_grad():
    logits = net(torch.randn(1, 3, 224, 224))         # one preprocessed image
    probs = logits.softmax(1)
print("predicted class:", probs.argmax(1).item(), "| confidence:", round(probs.max().item(), 3))"""),

 _s("5. Save and load a checkpoint", "Persist the weights, then restore them, the end of the workflow."),
 ("code",
"""torch.save(net.state_dict(), "model.pt")
fresh = models.resnet18(weights=None); fresh.fc = nn.Linear(fresh.fc.in_features, 5)
fresh.load_state_dict(torch.load("model.pt"))
print("checkpoint saved and reloaded; ready for inference or further fine-tuning.")"""),

 ("md", "**Wrap-up:** this end-to-end workflow, data, model, train, evaluate, infer, is exactly what the advanced vision and language courses build on."),
],
}
