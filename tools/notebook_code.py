# -*- coding: utf-8 -*-
"""Deep, sectioned content for the instructor PRACTICE notebooks (one per week).
NB[week] is an ordered list of cells, each ("md", text) or ("code", text), authored to
fill a full 2-hour instructor-led practice lesson: worked demonstrations with explanations,
fuller code with output and plots, "try it live" variations, and a closing mini-exercise
with a worked solution. The setup cell (torch, nn, F, plt, device, seed) runs first, so
snippets assume it. Consumed by build_notebooks.py."""

# convenience for short markdown section headers
def _s(title, note=""):
    return ("md", f"## {title}" + (f"\n{note}" if note else ""))

def _ex(prompt):
    return ("md", f"### Mini-exercise\n{prompt}\n\n*Try it before revealing the solution below.*")

def _sol():
    return ("md", "**Solution.**")

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
print("output:", tuple(layer(batch).shape), "(one value per sample)")
# the layer just does this by hand:
by_hand = batch @ layer.weight.t() + layer.bias
print("matches manual w.x + b:", torch.allclose(layer(batch), by_hand))"""),

 _s("3. Gradient descent BY HAND", "Before autograd: fit y = 2x + 1 by computing the gradient of MSE yourself."),
 ("code",
"""torch.manual_seed(0)
X = torch.randn(200, 1)
y = 2 * X + 1 + 0.1 * torch.randn(200, 1)

w, b = torch.zeros(1), torch.zeros(1)      # start at 0
lr = 0.1
for step in range(60):
    pred = w * X + b
    err = pred - y
    grad_w = (2 * err * X).mean()          # d MSE / d w
    grad_b = (2 * err).mean()              # d MSE / d b
    w -= lr * grad_w; b -= lr * grad_b
print(f"by-hand GD: w={w.item():.3f} (target 2.0), b={b.item():.3f} (target 1.0)")"""),

 _s("4. The same loop with autograd", "Now let PyTorch compute the gradients. Watch the four steps: forward, loss, backward, step."),
 ("code",
"""model = nn.Linear(1, 1)
opt = torch.optim.SGD(model.parameters(), lr=0.1)
loss_fn = nn.MSELoss()

losses = []
for epoch in range(60):
    opt.zero_grad()           # 1. clear old gradients
    pred = model(X)           # 2. forward
    loss = loss_fn(pred, y)   # 3. measure error
    loss.backward()           # 4. gradients (autograd)
    opt.step()                # 5. update weights
    losses.append(loss.item())

print(f"autograd: weight {model.weight.item():.3f} (target 2.0), bias {model.bias.item():.3f} (target 1.0)")
plt.plot(losses); plt.xlabel("epoch"); plt.ylabel("MSE loss"); plt.title("Training loss"); plt.show()"""),

 _s("5. See the fitted line", "Plot the data and the line the model learned."),
 ("code",
"""xs = torch.linspace(X.min(), X.max(), 50).unsqueeze(1)
with torch.no_grad():
    ys = model(xs)
plt.scatter(X, y, s=8, alpha=0.4, label="data")
plt.plot(xs, ys, "r", label="fit"); plt.legend(); plt.title("Learned y = 2x + 1"); plt.show()"""),

 ("md", "**Try it live:** change `lr` to 0.01 and to 1.5 and re-run. The next cell sweeps all three at once."),
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

 _s("6. Framing: classification vs regression", "Same machinery, different output layer and loss."),
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

 _s("7. End to end: a tiny classifier", "Train a 2-class model on a separable toy set and read accuracy."),
 ("code",
"""torch.manual_seed(0)
Xc = torch.randn(300, 2); yc = (Xc[:, 0] + Xc[:, 1] > 0).long()
clf = nn.Sequential(nn.Linear(2, 16), nn.ReLU(), nn.Linear(16, 2))
opt = torch.optim.Adam(clf.parameters(), lr=0.05); loss_fn = nn.CrossEntropyLoss()
for epoch in range(80):
    opt.zero_grad(); loss = loss_fn(clf(Xc), yc); loss.backward(); opt.step()
acc = (clf(Xc).argmax(1) == yc).float().mean()
print(f"final loss {loss.item():.3f} | accuracy {acc.item():.3f}")"""),

 _ex("Generate `y = -3x + 2 + noise` and recover the slope and intercept with an `nn.Linear(1, 1)` "
     "trained by SGD. What learning rate and how many steps do you need?"),
 _sol(),
 ("code",
"""torch.manual_seed(1)
Xe = torch.randn(200, 1); ye = -3 * Xe + 2 + 0.1 * torch.randn(200, 1)
m = nn.Linear(1, 1); o = torch.optim.SGD(m.parameters(), lr=0.1); f = nn.MSELoss()
for _ in range(80):
    o.zero_grad(); f(m(Xe), ye).backward(); o.step()
print(f"recovered slope {m.weight.item():.3f} (target -3.0), intercept {m.bias.item():.3f} (target 2.0)")"""),

 ("md", "**Recap:** every task is data + model + loss + optimization. The output layer and loss are chosen "
        "together (regression: 1 unit + MSE; k-class: k logits + cross-entropy). Autograd computes the gradients "
        "the hand-written loop computed manually."),
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

 _s("2. Reductions and the dim argument", "sum / mean / max collapse a chosen axis; keepdim keeps it as size 1."),
 ("code",
"""m = torch.arange(12.0).reshape(3, 4)
print("full mean:", m.mean().item())
print("mean over rows (dim=0):", m.mean(dim=0).tolist())
print("mean over cols (dim=1):", m.mean(dim=1).tolist())
print("max over cols:", m.max(dim=1).values.tolist(), "at idx", m.max(dim=1).indices.tolist())
print("keepdim shape:", tuple(m.sum(dim=1, keepdim=True).shape), "(useful for broadcasting back)")"""),

 _s("3. Views vs copies", "A view shares memory; changing it changes the original."),
 ("code",
"""a = torch.arange(6)
b = a.view(2, 3)        # shares memory
b[0, 0] = 99
print("a after editing its view:", a.tolist())   # a is changed too
c = a.reshape(3, 2).clone()  # clone breaks the link
c[0, 0] = -1
print("a after editing a clone:", a.tolist())"""),

 _s("4. Matrix multiply and batched matmul", "@ is matrix multiply; for stacks of matrices use it with a batch dimension."),
 ("code",
"""A = torch.randn(2, 3); B = torch.randn(3, 4)
print("(2,3) @ (3,4) ->", tuple((A @ B).shape))
# a batch of 5 matrix multiplies at once:
batchA = torch.randn(5, 2, 3); batchB = torch.randn(5, 3, 4)
print("batched (5,2,3) @ (5,3,4) ->", tuple((batchA @ batchB).shape))
# einsum spells the indices out explicitly:
print("einsum matches @:", torch.allclose(torch.einsum('ij,jk->ik', A, B), A @ B))"""),

 _s("5. Broadcasting", "Shapes are compared from the trailing dimension; a size of 1 expands."),
 ("code",
"""a = torch.ones(3, 1); b = torch.ones(1, 4)
print("(3,1) + (1,4) ->", tuple((a + b).shape))          # 3x4
row = torch.arange(4.0)
mat = torch.zeros(3, 4)
print("matrix + row ->", (mat + row).tolist())           # row added to each row"""),

 ("md", "**Predict before running:** what is the result shape of `torch.ones(5,1,4) + torch.ones(3,1)`? Then run it."),
 ("code", "print(tuple((torch.ones(5, 1, 4) + torch.ones(3, 1)).shape))   # broadcasting puzzle"),

 _s("6. Normalize with broadcasting", "Subtract a per-column mean and divide by a per-column std, no loops."),
 ("code",
"""data = torch.randn(100, 3) * torch.tensor([5.0, 1.0, 20.0]) + torch.tensor([10.0, -3.0, 0.0])
normed = (data - data.mean(0)) / data.std(0)
print("per-column mean before:", data.mean(0).round(decimals=2).tolist())
print("per-column mean after :", normed.mean(0).round(decimals=2).tolist(), "(~0)")
print("per-column std after  :", normed.std(0).round(decimals=2).tolist(), "(~1)")"""),

 _s("7. Boolean masks and fancy indexing", "Select elements by condition or by an index tensor."),
 ("code",
"""v = torch.arange(10)
print("v > 5 ->", (v > 5).tolist())
print("v[v > 5] ->", v[v > 5].tolist())
idx = torch.tensor([0, 0, 9, 5])
print("v[[0,0,9,5]] ->", v[idx].tolist(), "(gather by index)")"""),

 _s("8. A shape-mismatch error, then the fix", "Read the error: it names the incompatible dimensions."),
 ("code",
"""x = torch.ones(3, 4); w = torch.ones(5)   # wrong trailing size
try:
    x + w
except RuntimeError as e:
    print("ERROR:", str(e).splitlines()[0])
w = torch.ones(4)                          # fix: matches trailing dim 4
print("fixed (3,4)+(4,) ->", tuple((x + w).shape))"""),

 _s("9. Encoding real data as tensors", "An image becomes (C, H, W); a table becomes (rows, features)."),
 ("code",
"""import numpy as np
img = np.random.randint(0, 256, size=(8, 8, 3), dtype=np.uint8)   # H, W, C
img_t = torch.from_numpy(img).permute(2, 0, 1).float() / 255.0     # -> C, H, W in [0,1]
print("image tensor:", tuple(img_t.shape), img_t.dtype, "range", img_t.min().item(), img_t.max().item())

table = torch.tensor([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
print("table tensor:", tuple(table.shape))
img_t, table = img_t.to(device), table.to(device)
print("moved to", img_t.device)"""),

 _ex("Given class labels `y = torch.tensor([2, 0, 1, 2])` and 3 classes, build the one-hot matrix of "
     "shape (4, 3) without a loop. Hint: `scatter_` or index a 3x3 identity."),
 _sol(),
 ("code",
"""y = torch.tensor([2, 0, 1, 2])
onehot = torch.eye(3)[y]                       # index the identity matrix
print(onehot.tolist())
# equivalent with scatter:
oh2 = torch.zeros(4, 3); oh2.scatter_(1, y.unsqueeze(1), 1.0)
print("scatter matches:", torch.equal(onehot, oh2))"""),

 ("md", "**Recap:** shape, dtype, device are the first things to check. Broadcasting aligns from the trailing "
        "axis. Know when an op views versus copies memory. Matrix multiply and reductions are the workhorses."),
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

 _s("2. Activation functions", "The nonlinearity between layers; here is what the common ones look like."),
 ("code",
"""z = torch.linspace(-5, 5, 100)
for name, fn in [("ReLU", F.relu), ("sigmoid", torch.sigmoid), ("tanh", torch.tanh)]:
    plt.plot(z, fn(z), label=name)
plt.legend(); plt.title("Activation functions"); plt.axhline(0, color="k", lw=0.5); plt.show()"""),

 _s("3. Why the nonlinearity matters", "Without ReLU, two linear layers collapse to one linear map."),
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

 _s("4. Forward and backward BY HAND", "A 2-layer net on one batch: do the chain rule yourself, then check against autograd."),
 ("code",
"""torch.manual_seed(0)
xb = torch.randn(5, 3)
W1 = torch.randn(3, 4, requires_grad=True); W2 = torch.randn(4, 1, requires_grad=True)

h = torch.relu(xb @ W1)        # forward
out = h @ W2
loss = (out ** 2).mean()
loss.backward()                # autograd gradients

# by hand: d loss / d W2 = h^T @ (2*out/N)
g = 2 * out / out.numel()
manual_W2 = h.t() @ g
print("autograd vs manual dW2 match:", torch.allclose(W2.grad, manual_W2, atol=1e-5))"""),

 _s("5. Inspect gradients and zero_grad", "backward() fills .grad. Gradients ACCUMULATE, so zero them each step."),
 ("code",
"""w = torch.tensor([2.0], requires_grad=True)
(w ** 2).sum().backward(); print("after 1st backward (d/dw of w^2 = 2w = 4):", w.grad.item())
(w ** 2).sum().backward(); print("WITHOUT zero_grad (accumulated to 8):", w.grad.item())
w.grad.zero_()
(w ** 2).sum().backward(); print("AFTER zero_grad (back to 4):", w.grad.item())"""),

 _s("6. Hand-derived gradient vs autograd", "Sanity-check autograd on something you can differentiate by hand."),
 ("code",
"""xs = torch.tensor(3.0, requires_grad=True)
ys = xs ** 3 + 2 * xs          # dy/dx = 3x^2 + 2 -> 29 at x = 3
ys.backward()
print("autograd:", xs.grad.item(), "| by hand 3*x^2+2:", 3 * 3 ** 2 + 2)"""),

 ("md", "**Try it live:** add `gradcheck`. `torch.autograd.gradcheck` compares autograd to a numerical estimate."),
 ("code",
"""from torch.autograd import gradcheck
gfn = lambda a: (a ** 3 + 2 * a).sum()
ok = gradcheck(gfn, (torch.randn(4, dtype=torch.double, requires_grad=True),))
print("gradcheck passed:", ok)"""),

 _s("7. Train the MLP and read the loss", "Put it together: the four-step loop from week 1, now with a real network."),
 ("code",
"""model = MLP(); o = torch.optim.Adam(model.parameters(), 0.03); f = nn.CrossEntropyLoss()
hist = []
for _ in range(300):
    o.zero_grad(); l = f(model(X), y); l.backward(); o.step(); hist.append(l.item())
print("final accuracy:", round((model(X).argmax(1) == y).float().mean().item(), 3))
plt.plot(hist); plt.xlabel("step"); plt.ylabel("loss"); plt.title("MLP training"); plt.show()"""),

 _s("8. Visualize the decision boundary", "Evaluate the trained MLP on a grid to see the nonlinear regions it learned."),
 ("code",
"""g = torch.linspace(-3, 3, 120)
gx, gy = torch.meshgrid(g, g, indexing="xy")
grid = torch.stack([gx.reshape(-1), gy.reshape(-1)], dim=1)
with torch.no_grad():
    zone = model(grid).argmax(1).reshape(gx.shape)
plt.contourf(gx, gy, zone, alpha=0.3, cmap="coolwarm")
plt.scatter(X[:, 0], X[:, 1], c=y, s=8, cmap="coolwarm"); plt.title("MLP decision boundary"); plt.show()"""),

 _ex("Does width help? Train the MLP with d_hidden in [2, 8, 64] and report the accuracy on the XOR-like task."),
 _sol(),
 ("code",
"""for h_units in [2, 8, 64]:
    torch.manual_seed(0)
    acc = fit(MLP(d_hidden=h_units))
    print(f"hidden={h_units:3d} -> accuracy {acc:.3f}")"""),

 ("md", "**Recap:** nonlinearity is what makes depth worthwhile. Backprop is the chain rule on the graph that "
        "the forward pass built; autograd automates it, but gradients must be zeroed each step."),
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

 _s("2. TensorDataset is the quick version", "When the data already fits in tensors, skip the class."),
 ("code",
"""from torch.utils.data import TensorDataset
X = torch.randn(120, 3); y = (X.sum(1) > 0).long()
quick = TensorDataset(X, y)
print("same interface:", len(quick), quick[0][0].shape, quick[0][1].item())"""),

 _s("3. A DataLoader batches and shuffles", "Iterating yields batches shaped (batch, ...)."),
 ("code",
"""dl = DataLoader(ds, batch_size=16, shuffle=True)
xb, yb = next(iter(dl))
print("batch:", tuple(xb.shape), tuple(yb.shape))
for i, (xb, yb) in enumerate(dl):
    print("batch", i, "->", xb.shape[0], "samples")
    if i == 3:
        break"""),

 _s("4. Batch size and shuffling", "Batch size sets the steps per epoch; shuffling reorders every epoch."),
 ("code",
"""for bs in [8, 16, 64]:
    print(f"batch_size={bs}: {len(DataLoader(ds, batch_size=bs))} batches per epoch")
dl = DataLoader(ds, batch_size=4, shuffle=True)
print("epoch 1 first labels:", next(iter(dl))[1].tolist())
print("epoch 2 first labels:", next(iter(dl))[1].tolist())"""),

 _s("5. Transforms preprocess each sample", "A transform pipeline runs as each item is read."),
 ("code",
"""from torchvision import transforms
pipe = transforms.Compose([
    transforms.ToTensor(),                                  # PIL/np -> CxHxW float in [0,1]
    transforms.Normalize(mean=[0.5], std=[0.5]),            # -> roughly [-1, 1]
])
import numpy as np
fake = (np.random.rand(8, 8) * 255).astype("uint8")
out = pipe(fake)
print("after ToTensor + Normalize:", tuple(out.shape), "range", round(out.min().item(), 2), round(out.max().item(), 2))"""),

 _s("6. A train / validation / test split", "Tune on validation, touch test once. random_split is the easy way."),
 ("code",
"""from torch.utils.data import random_split
gen = torch.Generator().manual_seed(0)
tr, va, te = random_split(ds, [80, 20, 20], generator=gen)
print("sizes:", len(tr), len(va), len(te))
train_dl = DataLoader(tr, batch_size=16, shuffle=True)
val_dl   = DataLoader(va, batch_size=16)            # no shuffle for val/test"""),

 _s("7. Imbalanced data: a weighted sampler", "Oversample the rare class so each batch is roughly balanced."),
 ("code",
"""from torch.utils.data import WeightedRandomSampler
labels = torch.cat([torch.zeros(90), torch.ones(10)]).long()       # 90 vs 10
class_count = torch.bincount(labels).float()
weight_per_sample = (1.0 / class_count)[labels]                    # rare class -> higher weight
sampler = WeightedRandomSampler(weight_per_sample, num_samples=100, replacement=True)
drawn = labels[list(sampler)]
print("class counts in a sampled epoch:", torch.bincount(drawn).tolist(), "(was 90 / 10)")"""),

 _s("8. Data leakage, demonstrated", "Normalizing with whole-dataset statistics leaks test information."),
 ("code",
"""data = torch.randn(100, 1) * 5 + 10
train, test = data[:80], data[80:]

mu, sd = data.mean(), data.std()                 # LEAK: uses test data
print("leaky   test mean ~ 0:", round(((test - mu) / sd).mean().item(), 3))

mu, sd = train.mean(), train.std()               # correct: train only
print("correct test mean (not 0):", round(((test - mu) / sd).mean().item(), 3))"""),

 _ex("Build a DataLoader over `ToyData` with batch_size 10, then compute the mean of every batch's labels. "
     "Are the batches roughly balanced when shuffle=True?"),
 _sol(),
 ("code",
"""dl = DataLoader(ToyData(100), batch_size=10, shuffle=True)
means = [yb.float().mean().item() for _, yb in dl]
print("per-batch label means:", [round(m, 2) for m in means])
print("they hover near the dataset base rate, not 0 or 1")"""),

 ("md", "**Recap:** fit preprocessing on the training split only; shuffle training, not val/test; batch size "
        "trades gradient noise against speed; leakage silently inflates results."),
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

 _s("3. logits, softmax, log_softmax", "CrossEntropyLoss takes raw logits; pre-softmaxing is a classic bug."),
 ("code",
"""logits = torch.tensor([[2.0, 0.5, -1.0]])
probs = logits.softmax(1)
print("softmax probs:", probs.round(decimals=3).tolist(), "sum", probs.sum().item())
# CrossEntropyLoss == NLLLoss(log_softmax(logits)):
t = torch.tensor([0])
a = nn.CrossEntropyLoss()(logits, t)
b = nn.NLLLoss()(F.log_softmax(logits, 1), t)
print("CE == NLL(log_softmax):", torch.allclose(a, b))"""),

 _s("4. Binary tasks: BCEWithLogitsLoss", "For one-output binary or multi-label problems, keep logits and use BCEWithLogits."),
 ("code",
"""scores = torch.tensor([2.5, -1.0, 0.3])           # one logit per example
target = torch.tensor([1.0, 0.0, 1.0])
bce = nn.BCEWithLogitsLoss()(scores, target)
print("BCEWithLogits:", round(bce.item(), 3), "| predicted probs:", scores.sigmoid().round(decimals=2).tolist())"""),

 _s("5. Accuracy can lie", "On imbalanced data a trivial predictor scores high; precision/recall/F1 expose it."),
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

 _s("6. The confusion matrix", "Two lines, no library: it shows exactly where errors go."),
 ("code",
"""def confusion(pred, true, k=2):
    m = torch.zeros(k, k, dtype=torch.long)
    for p, t in zip(pred, true):
        m[t, p] += 1
    return m
print("rows = true, cols = predicted\\n", confusion(y_pred, y_true))"""),

 _s("7. The threshold is a knob", "Sweeping the decision threshold trades precision against recall (a mini ROC)."),
 ("code",
"""torch.manual_seed(0)
score = torch.cat([torch.randn(80) - 1, torch.randn(20) + 1])   # negatives lower, positives higher
truth = torch.cat([torch.zeros(80), torch.ones(20)])
for thr in [-1.0, 0.0, 1.0]:
    pred = (score > thr).long()
    tp = ((pred == 1) & (truth == 1)).sum().item(); fp = ((pred == 1) & (truth == 0)).sum().item()
    fn = ((pred == 0) & (truth == 1)).sum().item()
    rec = tp / (tp + fn + 1e-9); prec = tp / (tp + fp + 1e-9)
    print(f"threshold {thr:+.1f}: recall {rec:.2f}  precision {prec:.2f}")"""),

 _ex("Make `y_pred` catch 3 of the 5 minority cases (and nothing else wrong) and recompute precision, recall, F1."),
 _sol(),
 ("code",
"""y_pred = y_true.clone(); y_pred[:] = 0
pos = (y_true == 1).nonzero().squeeze()
y_pred[pos[:3]] = 1                                # 3 true positives, 0 false positives
tp = ((y_pred == 1) & (y_true == 1)).sum().item()
fp = ((y_pred == 1) & (y_true == 0)).sum().item()
fn = ((y_pred == 0) & (y_true == 1)).sum().item()
prec = tp / (tp + fp + 1e-9); rec = tp / (tp + fn + 1e-9)
print(f"precision {prec:.2f}  recall {rec:.2f}  F1 {2*prec*rec/(prec+rec+1e-9):.2f}")"""),

 ("md", "**Recap:** optimize a differentiable loss, report the metric you care about. Pass logits to "
        "CrossEntropy / BCEWithLogits. Under imbalance, look at precision, recall, F1, and the confusion matrix."),
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

 _s("2. What momentum does, on a 2D surface", "Watch SGD vs momentum descend an elongated (ill-conditioned) bowl."),
 ("code",
"""# loss = 0.5*(a*x^2 + y^2): steep in x, shallow in y -> SGD zig-zags
def path(momentum, steps=40, lr=0.1):
    p = torch.tensor([4.0, 4.0], requires_grad=True)
    o = torch.optim.SGD([p], lr=lr, momentum=momentum); pts = []
    for _ in range(steps):
        o.zero_grad(); loss = 0.5 * (10 * p[0] ** 2 + p[1] ** 2); loss.backward(); o.step()
        pts.append(p.detach().clone())
    return torch.stack(pts)
for mtm in [0.0, 0.9]:
    pts = path(mtm); plt.plot(pts[:, 0], pts[:, 1], "-o", ms=3, label=f"momentum={mtm}")
plt.scatter([0], [0], c="k", marker="*", s=120); plt.legend(); plt.title("Momentum smooths the path"); plt.show()"""),

 _s("3. The learning rate is everything", "A three-rate sweep: too small, good, too large."),
 ("code",
"""for lr in [0.001, 0.05, 0.5]:
    torch.manual_seed(0); m = nn.Linear(5, 1); o = torch.optim.SGD(m.parameters(), lr=lr); f = nn.MSELoss()
    h = []
    for _ in range(80):
        o.zero_grad(); l = f(m(X), y); l.backward(); o.step(); h.append(l.item())
    plt.plot(h, label=f"lr={lr}")
plt.yscale("log"); plt.legend(); plt.xlabel("step"); plt.ylabel("loss (log)"); plt.show()"""),

 _s("4. Read the curve to diagnose", "Spikes = too large; flat = too small; smooth decline = good."),
 ("code",
"""torch.manual_seed(0); m = nn.Linear(5, 1); o = torch.optim.SGD(m.parameters(), lr=1.2); f = nn.MSELoss()
h = []
for _ in range(40):
    o.zero_grad(); l = f(m(X), y); l.backward(); o.step(); h.append(l.item())
print("loss exploded to:", h[-1])
plt.plot(h); plt.title("lr too large: divergence"); plt.xlabel("step"); plt.ylabel("loss"); plt.show()"""),

 _s("5. Batch size changes the gradient noise", "Smaller batches add useful noise to the descent path."),
 ("code",
"""from torch.utils.data import TensorDataset, DataLoader
ds = TensorDataset(X, y)
for bs in [8, 200]:
    torch.manual_seed(0); m = nn.Linear(5, 1); o = torch.optim.SGD(m.parameters(), 0.05); f = nn.MSELoss(); h = []
    dl = DataLoader(ds, batch_size=bs, shuffle=True)
    for _ in range(15):
        for xb, yb in dl:
            o.zero_grad(); l = f(m(xb), yb); l.backward(); o.step(); h.append(l.item())
    plt.plot(h, label=f"batch={bs}")
plt.legend(); plt.xlabel("update"); plt.ylabel("loss"); plt.title("Small batch = noisier updates"); plt.show()"""),

 _s("6. A learning-rate schedule", "Step decay: lower the rate as training settles."),
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
 ("code",
"""m = nn.Linear(5, 1); o = torch.optim.SGD(m.parameters(), lr=0.2); f = nn.MSELoss()
sched = torch.optim.lr_scheduler.CosineAnnealingLR(o, T_max=80)
lrs = []
for _ in range(80):
    o.zero_grad(); f(m(X), y).backward(); o.step(); sched.step(); lrs.append(o.param_groups[0]["lr"])
plt.plot(lrs); plt.title("Cosine annealing schedule"); plt.xlabel("step"); plt.ylabel("lr"); plt.show()"""),

 _ex("Find a single SGD learning rate (no momentum, no schedule) that reaches loss < 0.02 within 60 steps "
     "on this problem. What is the largest rate that still converges?"),
 _sol(),
 ("code",
"""for lr in [0.05, 0.1, 0.2, 0.3]:
    torch.manual_seed(0); m = nn.Linear(5, 1); o = torch.optim.SGD(m.parameters(), lr); f = nn.MSELoss()
    for _ in range(60):
        o.zero_grad(); l = f(m(X), y); l.backward(); o.step()
    print(f"lr={lr}: final loss {l.item():.4f}")"""),

 ("md", "**Recap:** the learning rate is the most important hyperparameter; momentum and Adam smooth and adapt "
        "the updates; the loss curve diagnoses what went wrong."),
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

 _s("3. Early stopping", "Stop when validation stops improving; keep the best checkpoint."),
 ("code",
"""import copy
model = big(); o = torch.optim.Adam(model.parameters(), 0.01); f = nn.CrossEntropyLoss()
best_acc, best_state, patience, bad = 0.0, None, 30, 0
for epoch in range(250):
    model.train(); o.zero_grad(); f(model(Xtr), ytr).backward(); o.step()
    model.eval()
    with torch.no_grad():
        va = (model(Xte).argmax(1) == yte).float().mean().item()
    if va > best_acc:
        best_acc, best_state, bad = va, copy.deepcopy(model.state_dict()), 0
    else:
        bad += 1
        if bad >= patience:
            print(f"stopped at epoch {epoch}; best val acc {best_acc:.2f}"); break"""),

 _s("4. Weight decay actually shrinks the weights", "Compare the weight norm with and without decay."),
 ("code",
"""def final_norm(wd):
    torch.manual_seed(0); m = nn.Linear(20, 2); o = torch.optim.Adam(m.parameters(), 0.01, weight_decay=wd); f = nn.CrossEntropyLoss()
    for _ in range(250):
        o.zero_grad(); f(m(Xtr), ytr).backward(); o.step()
    return m.weight.norm().item()
print("weight norm  no decay:", round(final_norm(0.0), 2))
print("weight norm  wd=1e-1 :", round(final_norm(0.1), 2))"""),

 _s("5. Dropout behaves differently at train vs eval", "On in training (random zeros), off at eval (deterministic)."),
 ("code",
"""drop = nn.Dropout(0.5)
x = torch.ones(1, 10)
drop.train(); print("train (random zeros):", drop(x))
drop.eval();  print("eval  (identity)    :", drop(x))"""),

 _s("6. Capacity vs the gap", "Wider models fit the small training set harder; watch the train/test gap grow."),
 ("code",
"""for width in [4, 16, 128]:
    torch.manual_seed(0)
    m = nn.Sequential(nn.Linear(20, width), nn.ReLU(), nn.Linear(width, 2))
    tr, te = fit(m)
    print(f"width {width:3d}: train {tr[-1]:.2f}  test {te[-1]:.2f}  gap {tr[-1]-te[-1]:+.2f}")"""),

 _s("7. Augmentation enlarges the training set", "On real images, each epoch sees slightly different inputs (train only)."),
 ("code",
"""from torchvision import transforms
img = torch.rand(3, 32, 32)
aug = transforms.Compose([transforms.RandomHorizontalFlip(p=1.0), transforms.RandomCrop(32, padding=4)])
print("original", tuple(img.shape), "-> augmented", tuple(aug(img).shape))
print("two augmentations differ:", not torch.equal(aug(img), aug(img)))"""),

 _ex("Add label smoothing (`CrossEntropyLoss(label_smoothing=0.1)`) to the overfitting model and report the "
     "train/test gap. Does it help here?"),
 _sol(),
 ("code",
"""torch.manual_seed(0)
m = big(); o = torch.optim.Adam(m.parameters(), 0.01); f = nn.CrossEntropyLoss(label_smoothing=0.1)
for _ in range(250):
    m.train(); o.zero_grad(); f(m(Xtr), ytr).backward(); o.step()
m.eval()
with torch.no_grad():
    tr_a = (m(Xtr).argmax(1) == ytr).float().mean().item()
    te_a = (m(Xte).argmax(1) == yte).float().mean().item()
print(f"label smoothing: train {tr_a:.2f} test {te_a:.2f} (labels are random, so test stays near 0.5)")"""),

 ("md", "**Recap:** watch the train-minus-validation gap, not validation alone; regularize with weight decay, "
        "dropout, early stopping, and augmentation; turn dropout and augmentation OFF at eval."),
],

# ============================== WEEK 8 ==============================
8: [
 _s("1. What a convolution does", "A small learned filter slides over the input, sharing weights across positions."),
 ("code",
"""conv = nn.Conv2d(in_channels=1, out_channels=4, kernel_size=3, padding=1)
x = torch.randn(1, 1, 8, 8)
print("input ", tuple(x.shape), "-> output", tuple(conv(x).shape))   # 4 feature maps, same H,W (padding=1)
print("filter weights:", tuple(conv.weight.shape), "(out, in, kh, kw)")"""),

 _s("2. A hand-set edge filter", "Convolution is intuitive: set a vertical-edge (Sobel) kernel and see it fire on edges."),
 ("code",
"""edge = torch.zeros(1, 1, 8, 8); edge[..., :, 4:] = 1.0      # left half 0, right half 1 (a vertical edge)
sobel = torch.tensor([[-1., 0., 1.], [-2., 0., 2.], [-1., 0., 1.]]).view(1, 1, 3, 3)
resp = F.conv2d(edge, sobel, padding=1)
fig, ax = plt.subplots(1, 2, figsize=(6, 3))
ax[0].imshow(edge[0, 0], cmap="gray"); ax[0].set_title("input (edge)")
ax[1].imshow(resp[0, 0]); ax[1].set_title("Sobel response (fires at the edge)")
for a in ax: a.axis("off")
plt.show()"""),

 _s("3. Output size and parameter count", "out = floor((in + 2p - k)/s) + 1 ; conv params = (k*k*Cin + 1)*Cout."),
 ("code",
"""c = nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1)
print("output:", tuple(c(torch.randn(1, 3, 32, 32)).shape), " formula (32+2-3)/1+1 = 32")
print("params:", sum(p.numel() for p in c.parameters()), "= (3*3*3 + 1) * 16 =", (3 * 3 * 3 + 1) * 16)"""),

 _s("4. Stride, padding, pooling change the size", "A small table of input -> output shapes."),
 ("code",
"""x = torch.randn(1, 1, 32, 32)
configs = [("conv k3 s1 p1", nn.Conv2d(1, 1, 3, stride=1, padding=1)),
           ("conv k3 s2 p1", nn.Conv2d(1, 1, 3, stride=2, padding=1)),
           ("conv k5 s1 p0", nn.Conv2d(1, 1, 5, stride=1, padding=0)),
           ("maxpool 2",     nn.MaxPool2d(2)),
           ("avgpool 2",     nn.AvgPool2d(2))]
for name, layer in configs:
    print(f"{name:14s}: 32x32 -> {tuple(layer(x).shape)[2:]}")"""),

 _s("5. CNN vs MLP parameter count on an image", "Weight sharing is why CNNs are far cheaper on images."),
 ("code",
"""mlp_params = 28 * 28 * 128 + 128        # one dense layer 784 -> 128
cnn_params = (3 * 3 * 1 + 1) * 32        # one conv layer, 32 filters of 3x3
print(f"dense 784->128 : {mlp_params:,} params")
print(f"conv 1->32 (3x3): {cnn_params:,} params  (reused at every position)")"""),

 _s("6. Build a CNN and trace shapes", "Stack conv/pool blocks; channels grow while spatial size shrinks."),
 ("code",
"""cnn = nn.Sequential(
    nn.Conv2d(1, 8, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),     # 28 -> 14
    nn.Conv2d(8, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),    # 14 -> 7
    nn.Flatten(), nn.Linear(16 * 7 * 7, 10))
x = torch.randn(4, 1, 28, 28)
for layer in cnn:
    x = layer(x); print(f"{layer.__class__.__name__:9s}", tuple(x.shape))"""),

 _s("7. Train on FashionMNIST", "A couple of hundred steps is enough to see it learn (downloads ~30 MB)."),
 ("code",
"""from torchvision import datasets, transforms
from torch.utils.data import DataLoader
train = datasets.FashionMNIST("./data", train=True, download=True, transform=transforms.ToTensor())
test  = datasets.FashionMNIST("./data", train=False, download=True, transform=transforms.ToTensor())
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

 _s("8. Measure test accuracy", "Evaluate on the held-out test split in eval mode."),
 ("code",
"""test_dl = DataLoader(test, batch_size=512)
model.eval(); correct = total = 0
with torch.no_grad():
    for xb, yb in test_dl:
        xb, yb = xb.to(device), yb.to(device)
        correct += (model(xb).argmax(1) == yb).sum().item(); total += yb.numel()
print(f"test accuracy after 200 steps: {correct/total:.3f}")"""),

 _s("9. Visualize the first-layer feature maps", "Each map is one filter's response across the image."),
 ("code",
"""fmap = model[0](xb[:1]).detach().cpu()
fig, ax = plt.subplots(1, 8, figsize=(12, 2))
for i in range(8):
    ax[i].imshow(fmap[0, i]); ax[i].axis("off")
plt.suptitle("First-conv feature maps"); plt.show()"""),

 ("md", "**Mini-exercise:** add a second conv block (8 -> 16 channels with a pool) before the linear head and "
        "retrain. Does test accuracy improve for the same number of steps? **Recap:** convolution is local "
        "connectivity with shared weights; out = floor((in + 2p - k)/s) + 1; deeper feature maps are more abstract."),
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

 _s("2. What batch norm does to activations", "It re-centers and re-scales each feature; look at the histogram."),
 ("code",
"""x = torch.randn(1000, 1) * 4 + 7          # mean 7, std 4
bn = nn.BatchNorm1d(1); bn.train(); out = bn(x).detach()
fig, ax = plt.subplots(1, 2, figsize=(8, 3))
ax[0].hist(x.squeeze().tolist(), bins=30); ax[0].set_title("before BN (mean 7)")
ax[1].hist(out.squeeze().tolist(), bins=30); ax[1].set_title("after BN (mean ~0, std ~1)")
plt.show()"""),

 _s("3. Batch norm helps a deep net train", "Ablation: with vs without batch normalization."),
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

 _s("4. Residual connections at depth", "Plain 12-layer net vs the same with skips."),
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

 _s("5. Skips let gradients reach the first layer", "Measure the gradient norm at the first block: plain vs residual."),
 ("code",
"""def first_grad(res):
    m = Deep(res); f = nn.CrossEntropyLoss()
    f(m(X), y).backward()
    return m.blocks[0].weight.grad.norm().item()
print(f"first-layer grad norm  plain: {first_grad(False):.2e}")
print(f"first-layer grad norm  resid: {first_grad(True):.2e}  (larger = signal reaches the start)")"""),

 _s("6. LayerNorm vs BatchNorm", "LayerNorm normalizes per sample (batch-independent), used in sequence models."),
 ("code",
"""x = torch.randn(4, 8)
ln = nn.LayerNorm(8)(x)
print("LayerNorm: each ROW has mean ~0:", ln.mean(dim=1).round(decimals=2).tolist())
bn = nn.BatchNorm1d(8)(x)
print("BatchNorm: each COLUMN has mean ~0:", bn.mean(dim=0).round(decimals=2).tolist())"""),

 _s("7. Batch norm: train vs eval statistics", "It uses batch stats in training, running stats at eval."),
 ("code",
"""bn = nn.BatchNorm1d(4)
x = torch.randn(8, 4) * 5 + 3
bn.train(); _ = bn(x)
print("running mean after a train batch:", bn.running_mean.round(decimals=2).tolist())
bn.eval(); print("eval uses those running stats, not the current batch.")"""),

 _ex("Build an 18-layer plain net and an 18-layer residual net (reuse `Deep`) and compare the final loss after "
     "100 SGD steps. Does the gap widen with depth?"),
 _sol(),
 ("code",
"""class DeepN(nn.Module):
    def __init__(self, res, n=18):
        super().__init__(); self.res = res
        self.blocks = nn.ModuleList([nn.Linear(16, 16) for _ in range(n)]); self.head = nn.Linear(16, 2)
    def forward(self, x):
        for b in self.blocks:
            h = F.relu(b(x)); x = h + x if self.res else h
        return self.head(x)
for res in [False, True]:
    m = DeepN(res); o = torch.optim.SGD(m.parameters(), 0.05); f = nn.CrossEntropyLoss()
    for _ in range(100):
        o.zero_grad(); l = f(m(X), y); l.backward(); o.step()
    print(("residual" if res else "plain   "), "final loss", round(l.item(), 3))"""),

 ("md", "**Recap:** normalization stabilizes and accelerates training; residual connections give gradients a "
        "direct path so very deep nets train; compare training curves, not just final accuracy."),
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

 _s("2. The recurrence BY HAND", "Implement one RNN step yourself and match PyTorch's output."),
 ("code",
"""torch.manual_seed(0)
cell = nn.RNNCell(1, 16)
seq = torch.randn(5, 1)                    # 5 time steps, 1 feature
h = torch.zeros(16)
states = []
for t in range(5):
    h = torch.tanh(cell.weight_ih @ seq[t] + cell.bias_ih + cell.weight_hh @ h + cell.bias_hh)
    states.append(h)
# compare with the built-in cell:
h2 = torch.zeros(1, 16)
for t in range(5):
    h2 = cell(seq[t:t+1], h2)
print("manual recurrence matches RNNCell:", torch.allclose(states[-1], h2.squeeze(), atol=1e-5))"""),

 _s("3. Vanishing gradients, measured", "Gradient of the LAST output w.r.t. each input step shrinks for early steps."),
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

 _s("4. Exploding gradients and clipping", "Large recurrent weights make the gradient blow up; clipping caps its norm."),
 ("code",
"""rnn = nn.RNN(1, 8, batch_first=True)
with torch.no_grad():
    rnn.weight_hh_l0 *= 3.0                 # force instability
x = torch.randn(1, 50, 1, requires_grad=True)
rnn(x)[0][:, -1].sum().backward()
raw = x.grad.norm().item()
o = torch.optim.SGD(rnn.parameters(), 0.1)
clipped = torch.nn.utils.clip_grad_norm_(rnn.parameters(), max_norm=1.0)
print(f"input-grad norm (huge): {raw:.1f} | param-grad norm before clip: {clipped:.1f} -> capped at 1.0")"""),

 _s("5. A tiny sequence task end to end", "Predict whether a short random walk ends positive."),
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

 _s("6. Hidden size is a capacity knob", "More hidden units = more memory, more parameters."),
 ("code",
"""for hs in [2, 8, 32]:
    torch.manual_seed(0)
    m = nn.RNN(1, hs, batch_first=True)
    print(f"hidden_size={hs:2d}: params {sum(p.numel() for p in m.parameters()):4d}")"""),

 _s("7. Many-to-many: an output at every step", "Use the full output sequence, not just the last hidden state."),
 ("code",
"""rnn = nn.RNN(1, 8, batch_first=True); head = nn.Linear(8, 1)
x = torch.randn(4, 10, 1)
out, _ = rnn(x)
per_step = head(out)                       # (batch, time, 1): a prediction per time step
print("per-step output shape:", tuple(per_step.shape))"""),

 ("md", "**Try it live:** raise the sequence length in section 5 to 60 and watch accuracy drop, the "
        "vanishing-gradient problem in action."),

 _ex("Train the section-5 classifier at sequence lengths 15 and 60 and report both accuracies. Why does the "
     "longer sequence hurt a plain RNN?"),
 _sol(),
 ("code",
"""def run(T):
    torch.manual_seed(0)
    s = torch.randn(400, T, 1); lab = (s.sum(dim=1).squeeze() > 0).long()
    m = SeqClf(); o = torch.optim.Adam(m.parameters(), 0.01); f = nn.CrossEntropyLoss()
    for _ in range(120):
        o.zero_grad(); f(m(s), lab).backward(); o.step()
    return (m(s).argmax(1) == lab).float().mean().item()
print("T=15 accuracy:", round(run(15), 3))
print("T=60 accuracy:", round(run(60), 3), "(gradients from early steps vanish)")"""),

 ("md", "**Recap:** RNNs share weights across time; unrolling makes them deep; long-range gradients vanish or "
        "explode; clip to tame explosion, and use gating (next week) to fight vanishing."),
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

 _s("3. Watch the gates open and close", "Use LSTMCell to read the forget/input/output gate activations over time."),
 ("code",
"""torch.manual_seed(0)
cell = nn.LSTMCell(1, 1)
seq = torch.randn(12, 1)
h = torch.zeros(1, 1); c = torch.zeros(1, 1); gates = []
for t in range(12):
    gi = (seq[t:t+1] @ cell.weight_ih.t() + cell.bias_ih + h @ cell.weight_hh.t() + cell.bias_hh).squeeze()
    i, f_, g_, o_ = gi.chunk(4)
    gates.append([torch.sigmoid(f_).item(), torch.sigmoid(i).item(), torch.sigmoid(o_).item()])
    h, c = cell(seq[t:t+1], (h, c))
import numpy as np
gates = np.array(gates)
for k, lab in enumerate(["forget", "input", "output"]):
    plt.plot(gates[:, k], "-o", ms=3, label=lab)
plt.legend(); plt.xlabel("time step"); plt.ylabel("gate value (0-1)"); plt.title("LSTM gate activations"); plt.show()"""),

 _s("4. Gates preserve gradients over long sequences", "Compare the gradient reaching the first step: RNN vs LSTM."),
 ("code",
"""def first_step_grad(layer, T):
    x = torch.randn(1, T, 1, requires_grad=True)
    out = layer(x)[0]; out[:, -1].sum().backward()
    return x.grad.abs()[:, 0].mean().item()
for T in [10, 50, 100]:
    r = first_step_grad(nn.RNN(1, 8, batch_first=True), T)
    l = first_step_grad(nn.LSTM(1, 8, batch_first=True), T)
    print(f"T={T:3d}:  RNN {r:.2e}   LSTM {l:.2e}")"""),

 _s("5. Same long-range task, RNN vs LSTM", "The label depends on the FIRST step, 40 steps back."),
 ("code",
"""torch.manual_seed(0)
seqs = torch.randn(500, 40, 1); labels = (seqs[:, 0, 0] > 0).long()   # answer is at step 0
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

 _s("6. A bidirectional RNN", "Read the sequence both ways; the output width doubles."),
 ("code",
"""bi = nn.LSTM(1, 8, batch_first=True, bidirectional=True)
out, _ = bi(torch.randn(4, 10, 1))
print("bidirectional output width:", tuple(out.shape), "(= 2 x hidden)")"""),

 _s("7. seq2seq, in shapes", "An encoder compresses the input; a decoder produces a variable-length output."),
 ("code",
"""enc = nn.LSTM(1, 16, batch_first=True); dec = nn.LSTM(1, 16, batch_first=True); out_head = nn.Linear(16, 1)
src = torch.randn(2, 7, 1)                  # source length 7
_, (h, c) = enc(src)                        # encode to a state
tgt_in = torch.randn(2, 5, 1)               # target length 5 (teacher forcing input)
dec_out, _ = dec(tgt_in, (h, c))            # decode conditioned on the encoder state
print("encoder state:", tuple(h.shape), "| decoder output:", tuple(out_head(dec_out).shape))"""),

 _ex("Make the section-5 task depend on the LAST step instead of the first (`labels = (seqs[:, -1, 0] > 0)`). "
     "Do the RNN and LSTM both solve it now? Why?"),
 _sol(),
 ("code",
"""torch.manual_seed(0)
seqs2 = torch.randn(500, 40, 1); labels2 = (seqs2[:, -1, 0] > 0).long()    # answer is at the LAST step
for name, cell in [("RNN", nn.RNN), ("LSTM", nn.LSTM)]:
    m = make(cell); o = torch.optim.Adam(m.parameters(), 0.01); f = nn.CrossEntropyLoss()
    for _ in range(150):
        o.zero_grad(); f(m(seqs2), labels2).backward(); o.step()
    print(name, "accuracy:", round((m(seqs2).argmax(1) == labels2).float().mean().item(), 3),
          "(recent info is easy for both)")"""),

 ("md", "**Recap:** gates preserve the gradient signal across long sequences; a GRU is lighter than an LSTM; "
        "match the architecture (many-to-one, many-to-many, seq2seq) to the task."),
],

# ============================== WEEK 12 ==============================
12: [
 _s("1. Train an autoencoder on MNIST", "Compress to a small bottleneck, then reconstruct (downloads ~10 MB)."),
 ("code",
"""from torchvision import datasets, transforms
from torch.utils.data import DataLoader
train = datasets.MNIST("./data", train=True, download=True, transform=transforms.ToTensor())
dl = DataLoader(train, batch_size=256, shuffle=True)

class AE(nn.Module):
    def __init__(self, latent=16):
        super().__init__()
        self.enc = nn.Sequential(nn.Flatten(), nn.Linear(784, 64), nn.ReLU(), nn.Linear(64, latent))
        self.dec = nn.Sequential(nn.Linear(latent, 64), nn.ReLU(), nn.Linear(64, 784), nn.Sigmoid())
    def forward(self, x):
        z = self.enc(x); return self.dec(z).view_as(x), z

ae = AE().to(device); opt = torch.optim.Adam(ae.parameters(), 1e-3); f = nn.MSELoss()
for epoch in range(2):
    for xb, _ in dl:
        xb = xb.to(device); opt.zero_grad(); rec, _ = ae(xb); f(rec, xb).backward(); opt.step()
    print(f"epoch {epoch}: reconstruction MSE {f(ae(xb)[0], xb).item():.4f}")"""),

 _s("2. Reconstructions", "Top row: originals; bottom row: reconstruction through a 16-d bottleneck."),
 ("code",
"""xb, yb = next(iter(dl)); xb = xb.to(device)
rec, _ = ae(xb); rec = rec.detach().cpu()
fig, ax = plt.subplots(2, 8, figsize=(12, 3))
for i in range(8):
    ax[0, i].imshow(xb[i, 0].cpu(), cmap="gray"); ax[0, i].axis("off")
    ax[1, i].imshow(rec[i, 0], cmap="gray"); ax[1, i].axis("off")
plt.show()"""),

 _s("3. The bottleneck width matters", "Wider latent = lower reconstruction error; the bottleneck forces compression."),
 ("code",
"""for latent in [2, 8, 32]:
    m = AE(latent).to(device); o = torch.optim.Adam(m.parameters(), 1e-3); f = nn.MSELoss()
    for xb, _ in dl:
        xb = xb.to(device); o.zero_grad(); rec, _ = m(xb); f(rec, xb).backward(); o.step()
    print(f"latent={latent:2d}: reconstruction MSE {f(m(xb)[0], xb).item():.4f}")"""),

 _s("4. The latent space carries class structure", "Encode the batch, project the 16-d code to 2-D with PCA, color by digit."),
 ("code",
"""with torch.no_grad():
    _, z = ae(xb)
z = z.cpu() - z.cpu().mean(0)
U, S, V = torch.pca_lowrank(z, q=2)
proj = z @ V[:, :2]
plt.scatter(proj[:, 0], proj[:, 1], c=yb[:len(proj)], cmap="tab10", s=10)
plt.title("Autoencoder latent space (PCA to 2-D)"); plt.colorbar(); plt.show()"""),

 _s("5. A linear probe measures representation quality", "Freeze the encoder, train a linear classifier on the latent code."),
 ("code",
"""with torch.no_grad():
    feats = ae.enc(xb).cpu()                  # frozen features
probe = nn.Linear(feats.shape[1], 10); o = torch.optim.Adam(probe.parameters(), 0.05); f = nn.CrossEntropyLoss()
for _ in range(200):
    o.zero_grad(); f(probe(feats), yb[:len(feats)]).backward(); o.step()
acc = (probe(feats).argmax(1) == yb[:len(feats)]).float().mean().item()
print(f"linear probe accuracy on frozen 16-d features: {acc:.3f}")"""),

 _s("6. A denoising autoencoder", "Corrupt the input, reconstruct the clean image: the model learns robust structure."),
 ("code",
"""noisy = (xb + 0.5 * torch.randn_like(xb)).clamp(0, 1)
dae = AE().to(device); o = torch.optim.Adam(dae.parameters(), 1e-3); f = nn.MSELoss()
for _ in range(200):
    o.zero_grad(); rec, _ = dae(noisy); f(rec, xb).backward(); o.step()   # input noisy, target clean
rec = dae(noisy)[0].detach().cpu()
fig, ax = plt.subplots(2, 6, figsize=(9, 3))
for i in range(6):
    ax[0, i].imshow(noisy[i, 0].cpu(), cmap="gray"); ax[0, i].set_title("noisy"); ax[0, i].axis("off")
    ax[1, i].imshow(rec[i, 0], cmap="gray"); ax[1, i].set_title("denoised"); ax[1, i].axis("off")
plt.show()"""),

 _s("7. The contrastive idea", "Two augmented views of one image form a positive pair; everything else is negative."),
 ("code",
"""from torchvision import transforms
aug = transforms.Compose([transforms.RandomResizedCrop(28, scale=(0.6, 1.0)), transforms.RandomHorizontalFlip()])
img = xb[0].cpu()
fig, ax = plt.subplots(1, 3, figsize=(6, 2))
for a_, t, title in zip(ax, [img, aug(img), aug(img)], ["original", "view 1", "view 2"]):
    a_.imshow(t[0], cmap="gray"); a_.set_title(title); a_.axis("off")
plt.show()"""),

 ("md", "**Mini-exercise:** compare the linear-probe accuracy from a 2-d vs a 32-d bottleneck. Wider codes carry "
        "more class structure. **Recap:** a bottleneck forces useful compression; the latent code is the point, "
        "not perfect reconstruction; augmentation choices define what 'similar' means; learned features transfer."),
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

 _s("2. The preprocessing must match the pretrained model", "ResNet expects 3x224x224, normalized with ImageNet statistics."),
 ("code",
"""from torchvision import transforms
prep = transforms.Compose([
    transforms.Resize(224),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # ImageNet stats
])
print("preprocessing pipeline:\\n", prep)"""),

 _s("3. Three regimes, by trainable-parameter count", "From-scratch trains everything; frozen trains only the head; fine-tune trains all from pretrained."),
 ("code",
"""def trainable(m): return sum(p.numel() for p in m.parameters() if p.requires_grad)

frozen = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
for p in frozen.parameters(): p.requires_grad = False
frozen.fc = nn.Linear(frozen.fc.in_features, 5)
print("frozen-features trainable:", f"{trainable(frozen):,}")

ft = models.resnet18(weights=models.ResNet18_Weights.DEFAULT); ft.fc = nn.Linear(ft.fc.in_features, 5)
print("fine-tune trainable:     ", f"{trainable(ft):,}")

scratch = models.resnet18(weights=None); scratch.fc = nn.Linear(scratch.fc.in_features, 5)
print("from-scratch trainable:  ", f"{trainable(scratch):,}")"""),

 _s("4. Feature extraction: the backbone as an encoder", "Run images through the frozen backbone to get embeddings, then classify them."),
 ("code",
"""backbone = nn.Sequential(*list(frozen.children())[:-1])   # everything except the final fc
backbone.eval()
batch = torch.randn(4, 3, 224, 224)                       # 4 preprocessed images
with torch.no_grad():
    emb = backbone(batch).flatten(1)
print("embeddings:", tuple(emb.shape), "(512-d per image) -> feed a linear classifier")"""),

 _s("5. A linear probe on the embeddings", "Train only a small head on the frozen 512-d features."),
 ("code",
"""torch.manual_seed(0)
feat = torch.randn(60, 512); lab = torch.randint(0, 5, (60,))   # stand-in for real embeddings + labels
head = nn.Linear(512, 5); o = torch.optim.Adam(head.parameters(), 0.01); f = nn.CrossEntropyLoss()
for _ in range(200):
    o.zero_grad(); f(head(feat), lab).backward(); o.step()
print("linear-probe train accuracy:", round((head(feat).argmax(1) == lab).float().mean().item(), 3))"""),

 _s("6. Layer-wise learning rates", "Fine-tuning usually uses a smaller rate on the pretrained backbone than on the new head."),
 ("code",
"""opt = torch.optim.Adam([
    {"params": ft.fc.parameters(), "lr": 1e-3},                 # new head: faster
    {"params": [p for n, p in ft.named_parameters() if not n.startswith("fc")], "lr": 1e-5},  # backbone: slower
])
print("param groups and their learning rates:", [g["lr"] for g in opt.param_groups])"""),

 _s("7. Inference end to end", "Eval mode, no gradients, softmax to probabilities."),
 ("code",
"""net.eval()
with torch.no_grad():
    logits = net(torch.randn(1, 3, 224, 224))         # one preprocessed image
    probs = logits.softmax(1)
print("predicted class:", probs.argmax(1).item(), "| confidence:", round(probs.max().item(), 3))"""),

 _s("8. Save and load a checkpoint", "Persist the weights, then restore them, the end of the workflow."),
 ("code",
"""torch.save(net.state_dict(), "model.pt")
fresh = models.resnet18(weights=None); fresh.fc = nn.Linear(fresh.fc.in_features, 5)
fresh.load_state_dict(torch.load("model.pt"))
print("checkpoint saved and reloaded; ready for inference or further fine-tuning.")"""),

 ("md", "**Mini-exercise:** time a forward pass through the full network vs the frozen backbone only. Feature "
        "extraction is cheaper because no gradients flow through the backbone. **Wrap-up:** this end-to-end "
        "workflow, data, model, train, evaluate, infer, is exactly what the advanced vision and language courses "
        "build on."),
],
}
