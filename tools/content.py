# -*- coding: utf-8 -*-
"""Course content for DLCourseHIT: per-week metadata + lab handouts.
Consumed by build_site.py to generate the lab and reference HTML pages.
References live in refs.json (scouted, verified URLs)."""

COURSE = {
    "code": "DL 201",
    "title": "Introduction to Deep Learning",
    "subtitle": "Foundations of Neural Networks with PyTorch",
    "org": "HIT",
    "weeks": 13,
}

PARTS = {
    "I":   "Foundations",
    "II":  "Training Infrastructure",
    "III": "Architectures & Representation Learning",
    "IV":  "Integration",
}

# Each week: num, part, title, sub (one-line topic), goals, build, predict,
# explain, deliverables, hints. build/predict/explain mirror the syllabus's
# AI-aware exercise model (Build with an AI assistant / Predict & probe / Explain & defend).
WEEKS = [
    {
        "num": 1, "part": "I",
        "title": "Deep Learning Overview & ML-to-Network Framing",
        "sub": "What deep learning is; framing a task as tensor inputs, model outputs, and a loss function.",
        "goals": [
            "Set up the PyTorch toolchain and confirm it runs.",
            "Frame any ML task as tensors in, a model, and a loss out.",
            "Run a first end-to-end training loop and read the loss curve.",
        ],
        "build": [
            "Set up Python, PyTorch, and Jupyter or Colab; confirm whether a GPU is visible and fall back to CPU if not.",
            "With an AI assistant's help, scaffold a minimal training loop on a tiny dataset (a 2-class toy set or a small MNIST subset): model, loss, optimizer, and one train step.",
            "Train for a few epochs and plot the loss going down.",
        ],
        "predict": [
            "For three tasks (binary spam detection, house-price regression, 10-class digit recognition), write the input tensor shape, output-layer size, and loss, before any coding.",
            "Predict whether the loss should reach near zero on the toy task and roughly how fast.",
        ],
        "explain": [
            "Explain in a few sentences what the model, loss, and optimizer each do.",
            "Justify why the shape-and-loss framing is correct for each of the three tasks.",
            "Name one thing the AI assistant produced that needed correction or was not initially understood.",
        ],
        "deliverables": [
            "A notebook with the running loop and a loss curve.",
            "The three-task framing table (input shape, output size, loss).",
            "A short reflection (5 to 8 sentences).",
        ],
        "hints": [
            "Start on CPU with a tiny dataset; correctness first, speed later.",
            "If the loss is flat, check the learning rate and that the label format matches the loss.",
        ],
    },
    {
        "num": 2, "part": "I",
        "title": "Tensors & Data Representation",
        "sub": "Tensor operations, shapes, broadcasting, devices; representing images, text, and tabular data as tensors.",
        "goals": [
            "Manipulate tensors fluently (reshape, permute, reduce, index).",
            "Reason about shapes, broadcasting, and device placement.",
            "Encode real data into correctly shaped tensors.",
        ],
        "build": [
            "Implement a set of tensor manipulations (reshape, permute, broadcasting, reductions, indexing) with an AI assistant's help.",
            "Encode a small dataset (a few images and a small table) into tensors with the right dtype and device.",
        ],
        "predict": [
            "Predict the output shape of the eight provided broadcasting and reshape expressions before running them.",
            "Predict which operations return a view versus copy memory.",
        ],
        "explain": [
            "Explain the three expressions whose result shape is surprising, and why broadcasting produced it.",
            "Fix a seeded shape-mismatch bug and explain its root cause.",
        ],
        "deliverables": [
            "A notebook with the operations and a predicted-versus-actual shape table.",
            "The fixed bug with a one-paragraph explanation.",
        ],
        "hints": [
            "Print .shape and .dtype often; broadcasting aligns dimensions from the trailing axis.",
            ".view needs contiguous memory; .reshape may copy.",
        ],
    },
    {
        "num": 3, "part": "I",
        "title": "MLPs & Backpropagation",
        "sub": "Multilayer perceptrons; the forward pass; backpropagation mechanics via PyTorch autograd.",
        "goals": [
            "Build and train a multilayer perceptron.",
            "Understand the forward pass and backpropagation.",
            "Use autograd correctly and verify a gradient by hand.",
        ],
        "build": [
            "Implement an MLP (nn.Module) and train it on a small classification task with autograd.",
            "Implement the backward pass for one linear layer by hand (manual tensor ops).",
        ],
        "predict": [
            "Predict the sign and rough magnitude of one weight's gradient after a single step on a toy example.",
            "Predict how training changes if the nonlinearity is removed.",
        ],
        "explain": [
            "Verify the hand-computed gradient matches autograd within tolerance and explain any difference.",
            "Explain in words what each gradient tells its weight to do.",
        ],
        "deliverables": [
            "An MLP notebook with training results.",
            "The hand-derived gradient plus the autograd check.",
        ],
        "hints": [
            "Zero the gradients each step; compare against torch.autograd.gradcheck.",
            "Without a nonlinearity an MLP collapses to a linear model.",
        ],
    },
    {
        "num": 4, "part": "II",
        "title": "Data Pipelines",
        "sub": "The Dataset and DataLoader abstractions; batching, shuffling, transforms, and splits.",
        "goals": [
            "Build a custom Dataset and DataLoader.",
            "Reason about batching, shuffling, and clean splits.",
            "Recognize and avoid data leakage.",
        ],
        "build": [
            "Implement a custom Dataset and wrap it in a DataLoader with transforms, batching, and shuffling.",
            "Create a clean train, validation, and test split with a fixed seed.",
        ],
        "predict": [
            "Predict the effect of batch size on loss-curve smoothness and steps per epoch.",
            "Predict what happens to validation accuracy if normalization stats are computed on the full dataset.",
        ],
        "explain": [
            "Introduce a deliberate data leak, observe the inflated metric, and explain the mechanism and the fix.",
        ],
        "deliverables": [
            "A pipeline notebook with a working DataLoader.",
            "A short batch-size experiment and the leak demonstration with explanation.",
        ],
        "hints": [
            "Fit normalization on the training split only.",
            "shuffle=True for training, False for validation and test.",
        ],
    },
    {
        "num": 5, "part": "II",
        "title": "Loss Functions & Metrics",
        "sub": "Task-appropriate losses (cross-entropy, MSE, BCE); metrics; the train and eval loop.",
        "goals": [
            "Choose a task-appropriate loss.",
            "Track metrics that reveal real performance.",
            "Write a clean train and evaluation loop.",
        ],
        "build": [
            "Implement a training loop with loss and metric tracking (accuracy and F1 for classification, or MAE and R2 for regression).",
        ],
        "predict": [
            "Predict what happens if MSE is used for a classification task, before trying it.",
        ],
        "explain": [
            "Critique an AI-written accuracy metric that is wrong under class imbalance; explain the bug, fix it, and report a better metric.",
        ],
        "deliverables": [
            "A train and eval loop with metric logging.",
            "The wrong-loss experiment and the metric critique with fix.",
        ],
        "hints": [
            "CrossEntropyLoss expects logits and class indices, not softmax plus MSE.",
            "Accuracy hides minority-class failure; check per-class metrics or F1.",
        ],
    },
    {
        "num": 6, "part": "II",
        "title": "Optimization",
        "sub": "Gradient descent; SGD, momentum, and Adam; learning rates and optimization dynamics.",
        "goals": [
            "Understand SGD, momentum, and Adam.",
            "Reason about learning rates and convergence.",
            "Tune an optimizer to a target.",
        ],
        "build": [
            "Build an optimizer-comparison harness that trains the same model with SGD, SGD with momentum, and Adam.",
        ],
        "predict": [
            "For three learning rates (too small, good, too large), predict the loss-curve shape before running.",
        ],
        "explain": [
            "Explain divergence versus slow convergence in terms of step size, then tune to hit a target validation accuracy.",
        ],
        "deliverables": [
            "Comparison plots across optimizers.",
            "The learning-rate prediction table and a tuned run hitting the target.",
        ],
        "hints": [
            "Log loss every step; a diverging loss usually means the learning rate is too high.",
            "Adam is forgiving but still needs its learning rate tuned.",
        ],
    },
    {
        "num": 7, "part": "II",
        "title": "Regularization & Generalization",
        "sub": "Overfitting; dropout, weight decay, early stopping; basic data augmentation.",
        "goals": [
            "Diagnose overfitting from the train and validation gap.",
            "Apply dropout, weight decay, early stopping, and augmentation.",
            "Attribute a generalization gain to a specific cause.",
        ],
        "build": [
            "First make a model clearly overfit (small data, large model), then add regularization to close the gap.",
        ],
        "predict": [
            "Predict which regularizer will help most and how the train-minus-validation gap changes.",
        ],
        "explain": [
            "Run an ablation (dropout, weight decay, augmentation) and explain which helped and why; critique a claim about where to place dropout.",
        ],
        "deliverables": [
            "An overfit baseline plus a regularized run.",
            "An ablation table and an explanation.",
        ],
        "hints": [
            "Watch the train-minus-validation gap, not just validation alone.",
            "Augmentation applies to the training split only.",
        ],
    },
    {
        "num": 8, "part": "III",
        "title": "Convolutional Networks I",
        "sub": "Convolution, pooling, and feature maps; building a CNN image classifier.",
        "goals": [
            "Build and train a CNN image classifier.",
            "Understand convolution, pooling, and feature maps.",
            "Compute how shapes and parameters change layer by layer.",
        ],
        "build": [
            "Build and train a CNN image classifier (for example on MNIST, FashionMNIST, or a CIFAR-10 subset).",
        ],
        "predict": [
            "Compute by hand the output spatial size and parameter count of each conv and pool layer, and predict them before checking.",
        ],
        "explain": [
            "Verify against the model summary, explain any mismatch, and explain what a feature map represents.",
        ],
        "deliverables": [
            "A CNN notebook with accuracy.",
            "The hand-computed shape-and-parameter table versus the model summary.",
        ],
        "hints": [
            "Output size = floor((in + 2p - k) / s) + 1.",
            "Conv parameters = (k * k * Cin + 1) * Cout; verify with a summary tool.",
        ],
    },
    {
        "num": 9, "part": "III",
        "title": "Convolutional Networks II",
        "sub": "Batch and layer normalization; residual connections; modern CNN design.",
        "goals": [
            "Add normalization and residual connections.",
            "Understand why these help deeper networks train.",
            "Measure the effect of each with an ablation.",
        ],
        "build": [
            "Add batch normalization and residual blocks to the Week 8 CNN.",
        ],
        "predict": [
            "Predict the effect of removing normalization and residual connections on trainability and depth.",
        ],
        "explain": [
            "Ablate each, measure, and explain why residual connections help gradient flow in deep networks.",
        ],
        "deliverables": [
            "An improved CNN and an ablation table (with and without normalization, with and without residuals).",
            "An explanation. The mid-term mini-project starts this week.",
        ],
        "hints": [
            "Residual paths need matching shapes; use a 1x1 conv to match channels.",
            "Compare training curves, not just final accuracy.",
        ],
    },
    {
        "num": 10, "part": "III",
        "title": "Recurrent Networks (RNNs)",
        "sub": "Sequence data and recurrence; the RNN cell; backpropagation through time; vanishing and exploding gradients.",
        "goals": [
            "Build a plain RNN for sequence data.",
            "Understand recurrence and backpropagation through time.",
            "Observe the vanishing-gradient problem directly.",
        ],
        "build": [
            "Build a plain RNN on a character-level or short time-series task.",
        ],
        "predict": [
            "Predict how the gradient magnitude changes across time steps for long sequences.",
        ],
        "explain": [
            "Measure gradient norms across time steps, demonstrate vanishing gradients on long sequences, and explain why long-range dependencies are hard for a plain RNN.",
        ],
        "deliverables": [
            "An RNN notebook.",
            "A gradient-norm-versus-time-step plot with an explanation.",
        ],
        "hints": [
            "Clip gradients to avoid explosion; start with short sequences.",
            "Log the gradient norm at the earliest time steps to see vanishing.",
        ],
    },
    {
        "num": 11, "part": "III",
        "title": "LSTMs, GRUs & Sequence Tasks",
        "sub": "Gated recurrent units; how gates restore gradient flow; LSTM versus GRU; sequence classification and sequence-to-sequence tasks.",
        "goals": [
            "Build an LSTM or GRU and compare it to the plain RNN.",
            "Understand how gates restore gradient flow.",
            "Apply gated networks to a sequence task.",
        ],
        "build": [
            "Build an LSTM or GRU on the same task as Week 10 and compare it to the plain RNN.",
        ],
        "predict": [
            "Predict behavior on long versus short sequences and which gates matter most.",
        ],
        "explain": [
            "Ablate the gates, explain how gating preserves the gradient signal where the RNN failed, and compare LSTM with GRU.",
        ],
        "deliverables": [
            "An LSTM or GRU notebook with an RNN-versus-gated comparison.",
            "A gate ablation with an explanation.",
        ],
        "hints": [
            "Keep the task identical to Week 10 for a fair comparison.",
            "A GRU is lighter than an LSTM; watch long-sequence accuracy.",
        ],
    },
    {
        "num": 12, "part": "III",
        "title": "Representation Learning",
        "sub": "Autoencoders and latent representations; contrastive and self-supervised methods.",
        "goals": [
            "Train an autoencoder and a contrastive embedding.",
            "Probe and interpret a learned latent space.",
            "Reason about what makes a representation useful.",
        ],
        "build": [
            "Train an autoencoder and build a simple contrastive embedding.",
        ],
        "predict": [
            "Predict the expected latent-space structure (clusters by class, smooth interpolation).",
        ],
        "explain": [
            "Probe the latent space (interpolate, cluster, nearest neighbors), interpret what it captures, and critique an AI-suggested but flawed contrastive loss.",
        ],
        "deliverables": [
            "An autoencoder and embedding notebook with latent-space visualizations.",
            "An interpretation and the loss critique.",
        ],
        "hints": [
            "A too-large bottleneck just copies the input.",
            "For contrastive learning, the augmentation choice defines what counts as similar.",
        ],
    },
    {
        "num": 13, "part": "IV",
        "title": "Integration & Transfer Learning",
        "sub": "Transfer learning and fine-tuning; model inference; the end-to-end workflow into the advanced courses.",
        "goals": [
            "Fine-tune a pretrained model end-to-end.",
            "Run inference and assemble a full workflow.",
            "Reason about when transfer learning helps.",
        ],
        "build": [
            "Fine-tune a pretrained model end-to-end on a new task and run inference.",
        ],
        "predict": [
            "Predict the ranking of from-scratch, fine-tuning, and frozen-features under a fixed budget.",
        ],
        "explain": [
            "Compare the three regimes, explain when transfer learning helps and why, and reflect on the full workflow.",
        ],
        "deliverables": [
            "A fine-tuning notebook with a three-regime comparison.",
            "A reflection that doubles as final-project preparation. The final project is due this week.",
        ],
        "hints": [
            "Use a smaller learning rate for pretrained layers; unfreeze gradually.",
            "Match input preprocessing to the pretrained model.",
        ],
    },
]
