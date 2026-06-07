# -*- coding: utf-8 -*-
"""Per-week student self-check questions (with short answers).
Rendered as collapsible Q/A on each lab page so students can verify understanding."""

SELFCHECK = {
    1: [
        ("What four components does every ML task reduce to?", "Data, a model, a loss (objective), and optimization."),
        ("For 10-class digit classification, what output-layer size and loss would you use?", "Ten output logits with cross-entropy loss."),
        ("Why pass logits, not softmax probabilities, to CrossEntropyLoss?", "It applies log-softmax internally, which is more numerically stable."),
        ("What is the difference in role between the loss and the optimizer?", "The loss measures error; the optimizer updates parameters to reduce it."),
        ("Training loss stays flat. Name two things to check.", "The learning rate, and that the label format matches the chosen loss."),
    ],
    2: [
        ("State the broadcasting rule.", "Shapes align from the trailing dimension; each pair of sizes must be equal or one of them 1."),
        ("What is the difference between .view and .reshape?", ".view needs contiguous memory and shares storage; .reshape may copy."),
        ("What is the conventional shape of a batch of images in PyTorch?", "(N, C, H, W): batch, channels, height, width."),
        ("How do you move a tensor to the GPU?", "tensor.to(device), with device chosen from torch.cuda.is_available()."),
        ("Why does a tensor's dtype matter?", "Layers and losses expect specific types (e.g., float32 inputs, long class indices)."),
    ],
    3: [
        ("Why does an MLP need nonlinear activations?", "Without them, stacked linear layers collapse into a single linear map."),
        ("What does backpropagation compute?", "Gradients of the loss with respect to each parameter, via the chain rule."),
        ("Why call optimizer.zero_grad() each step?", "PyTorch accumulates gradients, so they must be cleared before each backward pass."),
        ("What does .backward() do?", "Computes and stores .grad for every tensor with requires_grad=True."),
        ("How can you check a computed gradient is correct?", "Compare it to a finite-difference (numerical) estimate, e.g. with gradcheck."),
    ],
    4: [
        ("Which two methods must a custom Dataset implement?", "__len__ and __getitem__."),
        ("Why fit normalization statistics on the training split only?", "Using validation/test statistics leaks information and inflates metrics."),
        ("Should you shuffle the validation set?", "No. Shuffle the training set only."),
        ("What does batch size trade off?", "Gradient noise/stability against compute, memory, and steps per epoch."),
        ("Give one concrete example of data leakage.", "Computing scaling or feature selection over the whole dataset before splitting."),
    ],
    5: [
        ("Which loss fits multi-class classification, binary classification, and regression?", "Cross-entropy; binary cross-entropy; MSE (or MAE)."),
        ("Why can accuracy be misleading?", "Under class imbalance a trivial majority predictor can score high."),
        ("Name a metric more robust to imbalance.", "F1 (or per-class precision/recall, balanced accuracy, AUC)."),
        ("What does model.eval() change?", "It disables dropout and uses running statistics in batch normalization."),
        ("What inputs does CrossEntropyLoss expect?", "Raw logits and integer class indices."),
    ],
    6: [
        ("What is the single most important optimization hyperparameter?", "The learning rate."),
        ("What does momentum do?", "Accumulates a velocity over past gradients to smooth and accelerate descent."),
        ("How does Adam differ from plain SGD?", "It adapts a per-parameter learning rate using gradient moment estimates."),
        ("A rising (diverging) loss usually means what?", "The learning rate is too high."),
        ("What is a learning-rate schedule?", "A rule that changes the learning rate over training (e.g. decay or warmup)."),
    ],
    7: [
        ("What signals overfitting?", "A growing gap between low training loss and higher validation loss."),
        ("What does weight decay do?", "Penalizes large weights (L2), reducing variance and overfitting."),
        ("Where should dropout be applied, and when is it disabled?", "After activations in hidden layers; disabled at evaluation time."),
        ("Should augmentation be applied to validation and test?", "No, only to the training set."),
        ("What is early stopping?", "Stopping training once the validation metric stops improving."),
    ],
    8: [
        ("Name two properties of convolution that save parameters.", "Local connectivity and weight sharing."),
        ("What is the output-size formula for a conv layer?", "floor((in + 2p - k) / s) + 1."),
        ("What does a pooling layer do?", "Downsamples spatially and adds a little translation invariance."),
        ("What is the parameter count of a conv layer?", "(k * k * Cin + 1) * Cout."),
        ("What does a feature map represent?", "One filter's activations across spatial positions, i.e. a detected pattern."),
    ],
    9: [
        ("What problem do residual connections address?", "Degradation and vanishing gradients in very deep networks."),
        ("How does a skip connection help gradients?", "It provides an identity path so gradients reach earlier layers directly."),
        ("What does batch normalization normalize?", "Layer activations per mini-batch, stabilizing and scaling them."),
        ("Why compare training curves, not just final accuracy, in the ablation?", "To see effects on trainability and convergence speed, not only the endpoint."),
        ("How do you match shapes for a residual add when channels change?", "Use a 1x1 convolution on the skip path."),
    ],
    10: [
        ("What does an RNN share across time steps?", "The same weights (parameters)."),
        ("What is backpropagation through time?", "Backpropagation on the network unrolled across time steps."),
        ("Why do long sequences cause vanishing gradients?", "Repeated multiplication shrinks (or explodes) gradients across many steps."),
        ("Name one remedy for exploding gradients.", "Gradient clipping."),
        ("What is the hidden state?", "The recurrent memory passed from one time step to the next."),
    ],
    11: [
        ("What do the gates in an LSTM control?", "How much information to forget, add, and output from the cell state."),
        ("How does a GRU differ from an LSTM?", "It merges gates and state into a simpler, lighter unit."),
        ("How does gating help with vanishing gradients?", "The cell state provides a near-linear path that preserves the gradient signal."),
        ("What is teacher forcing?", "Feeding the ground-truth previous token as the decoder input during training."),
        ("How does sequence classification differ from seq2seq?", "One label for the whole sequence versus an output sequence (encoder-decoder)."),
    ],
    12: [
        ("What are the three parts of an autoencoder?", "Encoder, bottleneck (latent), and decoder."),
        ("What happens if the bottleneck is too large?", "It can copy the input without learning useful structure."),
        ("In contrastive learning, what defines a similar pair?", "Two augmented views of the same example."),
        ("What is the goal of representation learning?", "To learn features that make downstream tasks easier and transferable."),
        ("Name a self-supervised method.", "SimCLR (or MoCo, BYOL, SwAV)."),
    ],
    13: [
        ("Name the two transfer-learning strategies.", "Fixed feature extraction (freezing) and fine-tuning."),
        ("When does freezing the backbone make most sense?", "When the target dataset is small and similar to the source."),
        ("Why use a smaller learning rate for pretrained layers?", "To avoid destroying useful pretrained features."),
        ("Why match the pretrained model's preprocessing?", "Inputs must match the normalization/distribution it was trained on."),
        ("What is the end-to-end workflow?", "Data, model, train, evaluate, infer/deploy."),
    ],
}
