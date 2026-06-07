# -*- coding: utf-8 -*-
"""Per-week lecture content for the instructor lesson plans.
The practice-class plan is derived in build_site.py from each week's lab
(Build / Predict & probe / Explain & defend). Here we author the lecture-specific
material: motivation, two concept blocks, a live demo, and takeaways."""

LESSONS = {
    1: {
        "motivation": "Why deep learning now: representation learning, scale, and one framework that spans vision, language, and more.",
        "conceptA": {"title": "What a neural network is", "points": [
            "A parametric function mapping input tensors to output tensors.",
            "Layers and nonlinearities; learning means adjusting parameters to reduce a loss.",
            "The mental model for the whole course: tensors in, a model, a loss out.",
        ]},
        "conceptB": {"title": "Framing an ML task as a network", "points": [
            "Choosing an input representation and its tensor shape.",
            "The output layer for classification versus regression.",
            "Matching the loss to the task (cross-entropy, MSE) and the train/eval loop.",
        ]},
        "demo": "Build a minimal PyTorch training loop on a toy dataset and watch the loss fall.",
        "takeaways": [
            "Every task reduces to data, a model, a loss, and optimization.",
            "The output layer and the loss are chosen together.",
            "PyTorch computes gradients, so effort goes into framing.",
        ],
    },
    2: {
        "motivation": "Everything in PyTorch is a tensor; fluency here prevents most beginner bugs.",
        "conceptA": {"title": "Tensors and shapes", "points": [
            "Rank, shape, dtype, and device.",
            "reshape, permute, view, reductions, and indexing.",
            "Contiguous memory: when an operation returns a view versus a copy.",
        ]},
        "conceptB": {"title": "Broadcasting and data representation", "points": [
            "Broadcasting rules (alignment from the trailing dimension).",
            "Representing images (N, C, H, W), text (token ids), and tabular data.",
            "Moving data and models to the GPU.",
        ]},
        "demo": "Shape gymnastics and a broadcasting puzzle, then encode a small dataset into tensors.",
        "takeaways": [
            "Shape errors are the most common beginner bug.",
            "Broadcasting aligns dimensions from the trailing axis.",
            "Know when an operation copies versus views memory.",
        ],
    },
    3: {
        "motivation": "From a single linear layer to a universal function approximator, and how learning actually happens.",
        "conceptA": {"title": "The multilayer perceptron", "points": [
            "Linear layers composed with nonlinear activations.",
            "Why the nonlinearity is what makes depth useful.",
            "The forward pass and nn.Module.",
        ]},
        "conceptB": {"title": "Backpropagation and autograd", "points": [
            "The chain rule on a computational graph.",
            "Each gradient tells its weight how to change.",
            "autograd, .backward(), zero_grad, and gradient checking.",
        ]},
        "demo": "Build an MLP, inspect .grad, and compare a hand-derived gradient to autograd.",
        "takeaways": [
            "Nonlinearity is what makes depth worthwhile.",
            "Backpropagation is the chain rule on a graph.",
            "Autograd automates gradients, but they must be zeroed each step.",
        ],
    },
    4: {
        "motivation": "Models are only as good as the data pipeline; leakage silently inflates results.",
        "conceptA": {"title": "Dataset and DataLoader", "points": [
            "The Dataset interface: __len__ and __getitem__.",
            "DataLoader batching, shuffling, and workers.",
            "Transforms and where they apply.",
        ]},
        "conceptB": {"title": "Splits and leakage", "points": [
            "Train/validation/test discipline.",
            "Fitting normalization statistics on the training split only.",
            "Common sources of leakage; the effect of batch size.",
        ]},
        "demo": "Build a custom Dataset and DataLoader, then show a leak inflating accuracy and fix it.",
        "takeaways": [
            "Fit preprocessing on the training split only.",
            "Shuffle training data, not validation or test.",
            "Batch size trades gradient noise against speed.",
        ],
    },
    5: {
        "motivation": "The loss defines what the model optimizes; the metric defines what matters in practice, and they are not the same.",
        "conceptA": {"title": "Loss functions", "points": [
            "Cross-entropy (logits and class indices), BCE, and MSE.",
            "When each loss applies.",
            "Numerical stability: pass logits, not softmax probabilities.",
        ]},
        "conceptB": {"title": "Metrics and evaluation", "points": [
            "Accuracy versus precision, recall, and F1.",
            "Why class imbalance breaks accuracy.",
            "The train/eval loop and model.eval().",
        ]},
        "demo": "Show a wrong-loss failure (MSE on classification) and a metric that lies under imbalance.",
        "takeaways": [
            "Optimize the right loss and report the right metric.",
            "Accuracy hides minority-class failure.",
            "Use logits with CrossEntropyLoss.",
        ],
    },
    6: {
        "motivation": "Same model, different optimizer or learning rate, wildly different results.",
        "conceptA": {"title": "Gradient descent and its variants", "points": [
            "Batch gradient descent versus SGD.",
            "Momentum and why it helps.",
            "Adam and adaptive learning rates.",
        ]},
        "conceptB": {"title": "Learning rate and dynamics", "points": [
            "Too small versus too large; learning-rate schedules.",
            "Divergence versus slow convergence.",
            "Reading a loss curve to diagnose training.",
        ]},
        "demo": "A learning-rate sweep showing divergence, slow, and good runs; SGD versus Adam on one model.",
        "takeaways": [
            "The learning rate is the most important hyperparameter.",
            "Momentum and Adam smooth and adapt the updates.",
            "Read the loss curve to diagnose what went wrong.",
        ],
    },
    7: {
        "motivation": "Fitting the training set is easy; generalizing is the actual job.",
        "conceptA": {"title": "Overfitting and capacity", "points": [
            "Bias and variance.",
            "The train-minus-validation gap as the signal.",
            "Capacity versus dataset size.",
        ]},
        "conceptB": {"title": "Regularizers", "points": [
            "Weight decay (L2) and how it constrains weights.",
            "Dropout and where to place it.",
            "Early stopping and data augmentation.",
        ]},
        "demo": "Force a model to overfit, then close the gap with dropout, weight decay, and augmentation.",
        "takeaways": [
            "Watch the train-minus-validation gap, not validation alone.",
            "Augmentation applies to the training split only.",
            "Dropout goes after activations, not on the output.",
        ],
    },
    8: {
        "motivation": "Why fully-connected nets waste parameters on images, and how convolution exploits structure.",
        "conceptA": {"title": "Convolution and pooling", "points": [
            "Filters, feature maps, stride, and padding.",
            "Parameter sharing and locality.",
            "Pooling and downsampling.",
        ]},
        "conceptB": {"title": "Building a CNN classifier", "points": [
            "Stacking convolution and pooling layers.",
            "Spatial-size and parameter arithmetic.",
            "From feature maps to a classifier head.",
        ]},
        "demo": "Build a small CNN, compute output shapes by hand, and train on FashionMNIST.",
        "takeaways": [
            "Convolution means local connectivity with shared weights.",
            "Output size = floor((in + 2p - k) / s) + 1.",
            "Feature maps detect patterns at increasing abstraction.",
        ],
    },
    9: {
        "motivation": "Why naively deeper networks train worse, and the two ideas that fixed it.",
        "conceptA": {"title": "Normalization", "points": [
            "The intuition for normalizing activations.",
            "Batch normalization and layer normalization.",
            "The effect on training stability and speed.",
        ]},
        "conceptB": {"title": "Residual connections", "points": [
            "The degradation problem in deep networks.",
            "Skip connections and how they help gradient flow.",
            "The ResNet residual block.",
        ]},
        "demo": "Add normalization and residual blocks, with an ablation showing deeper trains better.",
        "takeaways": [
            "Normalization stabilizes and accelerates training.",
            "Residual connections let gradients flow through deep nets.",
            "Compare training curves, not just final accuracy.",
        ],
    },
    10: {
        "motivation": "Sequences need memory; how recurrence shares parameters across time, and why it struggles.",
        "conceptA": {"title": "Recurrence and BPTT", "points": [
            "The RNN cell and the hidden state.",
            "Unrolling a network across time steps.",
            "Backpropagation through time.",
        ]},
        "conceptB": {"title": "Vanishing and exploding gradients", "points": [
            "Why long-range dependencies are hard.",
            "Gradient magnitude across time steps.",
            "Gradient clipping.",
        ]},
        "demo": "Train an RNN and plot the gradient norm versus time step to show vanishing.",
        "takeaways": [
            "RNNs share weights across time steps.",
            "Long-range gradients vanish or explode.",
            "Clip gradients to stabilize training.",
        ],
    },
    11: {
        "motivation": "Gates: a learned mechanism to keep or forget information across long sequences.",
        "conceptA": {"title": "LSTM and GRU", "points": [
            "The cell state and the forget, input, and output gates.",
            "The GRU as a lighter simplification.",
            "How gating restores gradient flow.",
        ]},
        "conceptB": {"title": "Sequence tasks", "points": [
            "Sequence classification versus sequence-to-sequence.",
            "The encoder-decoder structure.",
            "Teacher forcing.",
        ]},
        "demo": "Swap an RNN for an LSTM on the same task, ablate the gates, and compare long-sequence accuracy.",
        "takeaways": [
            "Gates preserve the gradient signal across long sequences.",
            "A GRU is lighter than an LSTM.",
            "Match the architecture to the sequence task.",
        ],
    },
    12: {
        "motivation": "Good representations make downstream tasks easy; learn them with or without labels.",
        "conceptA": {"title": "Autoencoders", "points": [
            "Encoder, bottleneck, and decoder.",
            "Undercomplete versus overcomplete.",
            "What the latent space captures.",
        ]},
        "conceptB": {"title": "Contrastive and self-supervised learning", "points": [
            "Augmentation defines what counts as similar.",
            "The contrastive loss.",
            "The SimCLR idea.",
        ]},
        "demo": "Train an autoencoder, interpolate the latent space, and sketch a contrastive setup.",
        "takeaways": [
            "A bottleneck forces useful compression.",
            "Augmentation choices define similarity.",
            "Learned representations transfer to new tasks.",
        ],
    },
    13: {
        "motivation": "Training from scratch is rare; standing on pretrained models is the bridge to the advanced courses.",
        "conceptA": {"title": "Transfer learning", "points": [
            "Fixed feature extraction versus fine-tuning.",
            "When each strategy works (data size and similarity).",
            "Layer-wise learning rates.",
        ]},
        "conceptB": {"title": "The end-to-end workflow", "points": [
            "Data, model, train, evaluate, infer.",
            "Matching preprocessing to the pretrained model.",
            "Inference and deployment basics.",
        ]},
        "demo": "Fine-tune a pretrained ResNet and compare from-scratch, frozen-features, and fine-tuning.",
        "takeaways": [
            "Transfer learning beats training from scratch on small data.",
            "Freeze first, then unfreeze gradually.",
            "Match the pretrained model's input preprocessing.",
        ],
    },
}


# Practice-lesson content: what the INSTRUCTOR demonstrates live in the 2-hour
# practice lesson (implementations, code runs, worked examples). Distinct from the
# weekly LAB, which is the student's homework (the Build / Predict / Explain exercise).
PRACTICE = {
    1: [
        "Set up PyTorch live and confirm the device (GPU or CPU).",
        "Walk through a minimal training loop on a toy dataset, run it, and read the loss curve.",
        "Vary the learning rate live to show divergence versus convergence.",
        "Frame a classification and a regression example as tensors-in, loss-out, in code.",
    ],
    2: [
        "Demonstrate tensor creation, reshape, permute, and indexing in a notebook.",
        "Show broadcasting on several shape examples; trigger a shape-mismatch error and fix it.",
        "Encode an image and a small table into tensors and move them to the device.",
    ],
    3: [
        "Build an MLP with nn.Module live and train it on a small task.",
        "Inspect .grad after a backward pass and show the effect of zero_grad.",
        "Compare a hand-computed gradient with autograd on a tiny example.",
    ],
    4: [
        "Write a custom Dataset and DataLoader live and iterate over batches.",
        "Show how batch size and shuffling change each epoch.",
        "Introduce a data leak (normalizing on the full dataset), show the inflated metric, then fix it.",
    ],
    5: [
        "Run a training loop with loss and metric logging.",
        "Show MSE on a classification task failing, then cross-entropy working.",
        "Compute accuracy versus F1 on an imbalanced example.",
    ],
    6: [
        "Train the same model with SGD, momentum, and Adam, and compare the curves.",
        "Sweep three learning rates live and read the resulting curves.",
        "Add a learning-rate schedule and show its effect.",
    ],
    7: [
        "Force a model to overfit and show the train-minus-validation gap.",
        "Add dropout and weight decay live and watch the gap close.",
        "Demonstrate data augmentation on a few images.",
    ],
    8: [
        "Build a CNN and print the layer-by-layer output shapes.",
        "Compute output sizes and parameter counts by hand and verify against a summary.",
        "Train on FashionMNIST and visualize a few feature maps.",
    ],
    9: [
        "Add batch normalization and residual blocks to the CNN.",
        "Ablate normalization and residuals live and compare the training curves.",
        "Show a deeper network failing without residuals and training with them.",
    ],
    10: [
        "Build a plain RNN on a short sequence task and run it.",
        "Plot gradient norms across time steps to expose vanishing gradients.",
        "Demonstrate gradient clipping.",
    ],
    11: [
        "Swap the RNN for an LSTM or GRU on the same task and compare.",
        "Walk through the gates and the cell state on the board and in code.",
        "Show behavior on long versus short sequences.",
    ],
    12: [
        "Train an autoencoder and visualize reconstructions and the latent space.",
        "Interpolate between two points in latent space live.",
        "Sketch a contrastive setup and show the augmentation views.",
    ],
    13: [
        "Load a pretrained model and fine-tune it live on a new task.",
        "Compare from-scratch, frozen-features, and fine-tuning side by side.",
        "Run inference on new inputs end to end.",
    ],
}
