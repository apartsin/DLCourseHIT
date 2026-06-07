# -*- coding: utf-8 -*-
"""Per-week lecture content (LESSONS) and instructor practice demonstrations (PRACTICE)
for the lesson plans. Concept blocks carry detailed talking points for the long lecture segments."""

LESSONS = {1: {'motivation': 'Why deep learning now: representation learning, scale, and one framework that spans '
                   'vision, language, and more.',
     'conceptA': {'title': 'What a neural network is',
                  'points': ['A neural network is a parametric function: it maps an input tensor to an output '
                             'tensor through learned weights.',
                             'It is built from layers (linear transforms) interleaved with nonlinear '
                             'activations; without the nonlinearity it collapses to a single linear map.',
                             'Learning means adjusting the weights to reduce a loss that scores how wrong the '
                             'outputs are.',
                             'Board work: a single neuron computing w.x + b, then stacking neurons into a '
                             'layer.']},
     'conceptB': {'title': 'Framing an ML task as a network',
                  'points': ['Decide the input representation and its tensor shape (a vector, an image, a '
                             'sequence).',
                             'Choose the output layer: one value for regression, or one logit per class for '
                             'classification.',
                             'Match the loss to the output: MSE for regression, cross-entropy for '
                             'classification.',
                             'Assemble the loop: forward pass, compute loss, backward pass, optimizer step, '
                             'repeat over the data.']},
     'demo': 'Build a minimal training loop on a toy dataset, watch the loss fall, then change the learning '
             'rate to show divergence.',
     'takeaways': ['Every task reduces to data, a model, a loss, and optimization.',
                   'The output layer and the loss are chosen together.',
                   'PyTorch computes gradients, so effort goes into framing.']},
 2: {'motivation': 'Everything in PyTorch is a tensor; fluency here prevents most beginner bugs.',
     'conceptA': {'title': 'Tensors and shapes',
                  'points': ['A tensor has a shape, a dtype, and a device; most beginner bugs are a shape or '
                             'dtype mismatch.',
                             'Reshape, view, permute, and flatten rearrange dimensions; reductions (sum, mean) '
                             'collapse them.',
                             'Indexing and slicing select sub-tensors, with the same start-inclusive, '
                             'stop-exclusive rule as Python.',
                             'Contiguity: a view shares memory, a reshape may copy; call .contiguous() when an '
                             'op needs it.']},
     'conceptB': {'title': 'Broadcasting and data representation',
                  'points': ['Broadcasting compares shapes from the trailing dimension; sizes must match or be '
                             '1 (which then expands).',
                             'Images are (N, C, H, W); text is integer token ids; tabular data is (N, '
                             'features).',
                             'dtypes matter: float32 for inputs, long for class indices.',
                             'Move tensors and models to the GPU with .to(device) and keep them on the same '
                             'device.']},
     'demo': 'Shape gymnastics, a broadcasting puzzle, and a deliberate shape-mismatch error with its fix; '
             'then encode an image and a table.',
     'takeaways': ['Shape errors are the most common beginner bug.',
                   'Broadcasting aligns dimensions from the trailing axis.',
                   'Know when an operation copies versus views memory.']},
 3: {'motivation': 'From a single linear layer to a universal function approximator, and how learning actually '
                   'happens.',
     'conceptA': {'title': 'The multilayer perceptron',
                  'points': ['An MLP stacks linear layers with nonlinear activations (ReLU, sigmoid, tanh).',
                             'The nonlinearity is essential: stacked linear layers are still just a linear '
                             'map.',
                             'nn.Module holds the parameters and defines the forward pass; calling the module '
                             'runs forward.',
                             'Width and depth set capacity; more is not always better.']},
     'conceptB': {'title': 'Backpropagation and autograd',
                  'points': ['The forward pass builds a computational graph of the operations applied.',
                             'Backpropagation applies the chain rule backward through that graph to get each '
                             "parameter's gradient.",
                             'Autograd records the graph automatically; .backward() fills .grad; '
                             'optimizer.step() updates the weights.',
                             'Gradients accumulate, so call zero_grad() each iteration; verify a gradient '
                             'against a finite-difference estimate.']},
     'demo': 'Build an MLP, inspect .grad before and after zero_grad, and check a hand-derived gradient '
             'against autograd.',
     'takeaways': ['Nonlinearity is what makes depth worthwhile.',
                   'Backpropagation is the chain rule on a graph.',
                   'Autograd automates gradients, but they must be zeroed each step.']},
 4: {'motivation': 'Models are only as good as the data pipeline; leakage silently inflates results.',
     'conceptA': {'title': 'Dataset and DataLoader',
                  'points': ['A Dataset implements __len__ and __getitem__ to return one (input, label) at a '
                             'time.',
                             'A DataLoader batches, shuffles, and can parallelize loading with worker '
                             'processes.',
                             'Transforms preprocess each sample (to tensor, normalize, augment) as it is read.',
                             'Iterating the DataLoader yields batches shaped (batch, ...).']},
     'conceptB': {'title': 'Splits and leakage',
                  'points': ['Split into train, validation, and test; tune on validation, report once on test.',
                             'Fit normalization statistics on the training split only.',
                             'Leakage is any test or future information reaching training; it silently '
                             'inflates results.',
                             'Batch size trades gradient noise against speed and memory.']},
     'demo': 'Write a custom Dataset and DataLoader, iterate batches, then show a normalization leak inflating '
             'accuracy and fix it.',
     'takeaways': ['Fit preprocessing on the training split only.',
                   'Shuffle training data, not validation or test.',
                   'Batch size trades gradient noise against speed.']},
 5: {'motivation': 'The loss defines what the model optimizes; the metric defines what matters in practice, '
                   'and they are not the same.',
     'conceptA': {'title': 'Loss functions',
                  'points': ['Cross-entropy for classification takes raw logits and integer class indices.',
                             'BCE for binary or multi-label tasks; MSE (or MAE) for regression.',
                             'Pass logits, not softmax probabilities, to CrossEntropyLoss for numerical '
                             'stability.',
                             'The loss must be differentiable; the reported metric need not be.']},
     'conceptB': {'title': 'Metrics and evaluation',
                  'points': ['Accuracy is intuitive but misleading under class imbalance.',
                             'Precision, recall, and F1 expose minority-class behavior; the confusion matrix '
                             'shows the full picture.',
                             'model.eval() and torch.no_grad() switch off dropout and gradient tracking for '
                             'evaluation.',
                             'Track training and validation metrics together to catch overfitting early.']},
     'demo': 'A training loop with metric logging, MSE-on-classification failing, and accuracy versus F1 on an '
             'imbalanced set.',
     'takeaways': ['Optimize the right loss and report the right metric.',
                   'Accuracy hides minority-class failure.',
                   'Use logits with CrossEntropyLoss.']},
 6: {'motivation': 'Same model, different optimizer or learning rate, wildly different results.',
     'conceptA': {'title': 'Gradient descent and its variants',
                  'points': ['Batch gradient descent uses all data per step; SGD uses one minibatch, adding '
                             'useful noise.',
                             'Momentum accumulates a velocity over past gradients to smooth and accelerate '
                             'descent.',
                             'Adam adapts a per-parameter learning rate from gradient moment estimates.',
                             'Each optimizer has its own sensible default learning rate.']},
     'conceptB': {'title': 'Learning rate and dynamics',
                  'points': ['The learning rate is the single most important hyperparameter.',
                             'Too large diverges or oscillates; too small crawls.',
                             'Schedules (step, cosine, warmup) lower the rate over training for a cleaner '
                             'finish.',
                             'Reading the loss curve diagnoses the cause: spikes mean too large, a flat line '
                             'means too small.']},
     'demo': 'SGD versus momentum versus Adam on one model, a three-rate sweep, and a step-decay schedule.',
     'takeaways': ['The learning rate is the most important hyperparameter.',
                   'Momentum and Adam smooth and adapt the updates.',
                   'Read the loss curve to diagnose what went wrong.']},
 7: {'motivation': 'Fitting the training set is easy; generalizing is the actual job.',
     'conceptA': {'title': 'Overfitting and capacity',
                  'points': ['Training error always improves; the test error is what matters.',
                             'Overfitting shows as a widening gap between low training loss and higher '
                             'validation loss.',
                             'Capacity (width, depth) and dataset size set how easily a model overfits.',
                             'The bias-variance trade-off: too simple underfits, too complex overfits.']},
     'conceptB': {'title': 'Regularizers',
                  'points': ['Weight decay (L2) penalizes large weights, reducing variance.',
                             'Dropout randomly zeros activations during training (off at eval), forcing '
                             'redundancy.',
                             'Early stopping halts when the validation metric stops improving.',
                             'Data augmentation enlarges the effective training set; apply it to the training '
                             'split only.']},
     'demo': 'Force a model to overfit, then close the train/validation gap with dropout, weight decay, and '
             'augmentation.',
     'takeaways': ['Watch the train-minus-validation gap, not validation alone.',
                   'Augmentation applies to the training split only.',
                   'Dropout goes after activations, not on the output.']},
 8: {'motivation': 'Why fully-connected nets waste parameters on images, and how convolution exploits '
                   'structure.',
     'conceptA': {'title': 'Convolution and pooling',
                  'points': ['A convolution slides a small learned filter over the input, sharing weights '
                             'across positions.',
                             'Local connectivity plus weight sharing makes convolutions far cheaper than dense '
                             'layers on images.',
                             'Stride and padding set the output size: out = floor((in + 2p - k) / s) + 1.',
                             'Pooling downsamples and adds a little translation invariance.']},
     'conceptB': {'title': 'Building a CNN classifier',
                  'points': ['Stack conv, activation, and pooling blocks, growing channels while shrinking '
                             'spatial size.',
                             'Flatten the feature maps and add a linear classifier head.',
                             'Track the shape through each layer and verify the parameter count by hand.',
                             'Early layers learn edges; later layers learn parts and whole objects.']},
     'demo': 'Build a small CNN, print the per-layer shapes, train on FashionMNIST, and visualize a few '
             'feature maps.',
     'takeaways': ['Convolution means local connectivity with shared weights.',
                   'Output size = floor((in + 2p - k) / s) + 1.',
                   'Feature maps detect patterns at increasing abstraction.']},
 9: {'motivation': 'Why naively deeper networks train worse, and the two ideas that fixed it.',
     'conceptA': {'title': 'Normalization',
                  'points': ['Batch normalization standardizes each channel over the minibatch, stabilizing '
                             'and speeding training.',
                             'It allows higher learning rates and reduces sensitivity to initialization.',
                             'It behaves differently at train and eval (batch statistics versus running '
                             'statistics).',
                             'Layer normalization is the batch-independent alternative used in sequence and '
                             'transformer models.']},
     'conceptB': {'title': 'Residual connections',
                  'points': ['Very deep plain networks train worse, not better (the degradation problem).',
                             'A residual block adds the input back to the output: out = F(x) + x.',
                             'The skip path gives gradients a direct route, so very deep networks train.',
                             'Match shapes on the skip path with a 1x1 convolution when the channel count '
                             'changes.']},
     'demo': 'Add batch norm and residual blocks, ablate each, and show a deep network training only with '
             'residuals.',
     'takeaways': ['Normalization stabilizes and accelerates training.',
                   'Residual connections let gradients flow through deep nets.',
                   'Compare training curves, not just final accuracy.']},
 10: {'motivation': 'Sequences need memory; how recurrence shares parameters across time, and why it '
                    'struggles.',
      'conceptA': {'title': 'Recurrence and BPTT',
                   'points': ['An RNN processes a sequence step by step, carrying a hidden state forward.',
                              'The same weights are reused at every time step (weight sharing across time).',
                              'Unrolling over time turns the recurrence into a deep feedforward graph.',
                              'Backpropagation through time applies the chain rule across that unrolled '
                              'graph.']},
      'conceptB': {'title': 'Vanishing and exploding gradients',
                   'points': ['Repeated multiplication by the recurrent weights shrinks or grows gradients '
                              'exponentially.',
                              'Vanishing gradients make long-range dependencies nearly unlearnable.',
                              'Exploding gradients are tamed with gradient clipping.',
                              'These problems motivate the gated units in the next lecture.']},
      'demo': 'Train a plain RNN, plot the gradient reaching the first step versus sequence length, and apply '
              'clipping.',
      'takeaways': ['RNNs share weights across time steps.',
                    'Long-range gradients vanish or explode.',
                    'Clip gradients to stabilize training.']},
 11: {'motivation': 'Gates: a learned mechanism to keep or forget information across long sequences.',
      'conceptA': {'title': 'LSTM and GRU',
                   'points': ['An LSTM adds a cell state plus input, forget, and output gates that control '
                              'information flow.',
                              'The cell state provides a near-linear path that preserves gradients over long '
                              'sequences.',
                              'A GRU merges gates and states into a lighter unit with similar performance.',
                              'The gates are learned, so the network decides what to keep and what to '
                              'forget.']},
      'conceptB': {'title': 'Sequence tasks',
                   'points': ['Sequence classification produces one label for a whole sequence.',
                              'Sequence-to-sequence uses an encoder and a decoder for variable-length outputs.',
                              'Teacher forcing feeds the true previous token to the decoder during training.',
                              'Match the architecture (many-to-one, many-to-many) to the task.']},
      'demo': 'Swap an RNN for an LSTM, inspect the gates and cell state, and compare long- versus '
              'short-sequence gradients.',
      'takeaways': ['Gates preserve the gradient signal across long sequences.',
                    'A GRU is lighter than an LSTM.',
                    'Match the architecture to the sequence task.']},
 12: {'motivation': 'Good representations make downstream tasks easy; learn them with or without labels.',
      'conceptA': {'title': 'Autoencoders',
                   'points': ['An autoencoder compresses the input through a bottleneck (encoder) and '
                              'reconstructs it (decoder).',
                              'An undercomplete bottleneck forces it to learn salient structure rather than '
                              'copy the input.',
                              'The latent code is a learned, lower-dimensional representation.',
                              'Denoising variants reconstruct a clean input from a corrupted one.']},
      'conceptB': {'title': 'Contrastive and self-supervised learning',
                   'points': ['Self-supervised learning creates its own labels from unlabeled data.',
                              'Contrastive methods pull augmented views of the same example together and push '
                              'different examples apart.',
                              'The augmentation policy defines what counts as similar.',
                              'A linear probe on the frozen features measures representation quality.']},
      'demo': 'Train an autoencoder, visualize reconstructions and a latent interpolation, and sketch a '
              'contrastive setup.',
      'takeaways': ['A bottleneck forces useful compression.',
                    'Augmentation choices define similarity.',
                    'Learned representations transfer to new tasks.']},
 13: {'motivation': 'Training from scratch is rare; standing on pretrained models is the bridge to the '
                    'advanced courses.',
      'conceptA': {'title': 'Transfer learning',
                   'points': ['A model pretrained on a large dataset already knows general-purpose features.',
                              'Feature extraction freezes the backbone and trains only a new head (good for '
                              'small, similar data).',
                              'Fine-tuning updates the whole network, usually with a smaller learning rate on '
                              'the pretrained layers.',
                              'Match the input preprocessing to what the pretrained model expects.']},
      'conceptB': {'title': 'The end-to-end workflow',
                   'points': ['Data, model, train, evaluate, infer: the full pipeline assembled in one place.',
                              'Split and load the data, choose a loss and metric, train with validation, and '
                              'touch the test set once.',
                              'Inference uses model.eval() and no_grad(); save and load checkpoints.',
                              'This foundation carries directly into the advanced language and vision '
                              'courses.']},
      'demo': 'Fine-tune a pretrained ResNet, compare from-scratch versus frozen versus fine-tuned, and run '
              'inference.',
      'takeaways': ['Transfer learning beats training from scratch on small data.',
                    'Freeze first, then unfreeze gradually.',
                    "Match the pretrained model's input preprocessing."]}}

PRACTICE = {1: ['Set up PyTorch live and confirm the device (GPU or CPU).',
     'Walk through a minimal training loop on a toy dataset, run it, and read the loss curve.',
     'Vary the learning rate live to show divergence versus convergence.',
     'Frame a classification and a regression example as tensors-in, loss-out, in code.'],
 2: ['Demonstrate tensor creation, reshape, permute, and indexing in a notebook.',
     'Show broadcasting on several shape examples; trigger a shape-mismatch error and fix it.',
     'Encode an image and a small table into tensors and move them to the device.'],
 3: ['Build an MLP with nn.Module live and train it on a small task.',
     'Inspect .grad after a backward pass and show the effect of zero_grad.',
     'Compare a hand-computed gradient with autograd on a tiny example.'],
 4: ['Write a custom Dataset and DataLoader live and iterate over batches.',
     'Show how batch size and shuffling change each epoch.',
     'Introduce a data leak (normalizing on the full dataset), show the inflated metric, then fix it.'],
 5: ['Run a training loop with loss and metric logging.',
     'Show MSE on a classification task failing, then cross-entropy working.',
     'Compute accuracy versus F1 on an imbalanced example.'],
 6: ['Train the same model with SGD, momentum, and Adam, and compare the curves.',
     'Sweep three learning rates live and read the resulting curves.',
     'Add a learning-rate schedule and show its effect.'],
 7: ['Force a model to overfit and show the train-minus-validation gap.',
     'Add dropout and weight decay live and watch the gap close.',
     'Demonstrate data augmentation on a few images.'],
 8: ['Build a CNN and print the layer-by-layer output shapes.',
     'Compute output sizes and parameter counts by hand and verify against a summary.',
     'Train on FashionMNIST and visualize a few feature maps.'],
 9: ['Add batch normalization and residual blocks to the CNN.',
     'Ablate normalization and residuals live and compare the training curves.',
     'Show a deeper network failing without residuals and training with them.'],
 10: ['Build a plain RNN on a short sequence task and run it.',
      'Plot gradient norms across time steps to expose vanishing gradients.',
      'Demonstrate gradient clipping.'],
 11: ['Swap the RNN for an LSTM or GRU on the same task and compare.',
      'Walk through the gates and the cell state on the board and in code.',
      'Show behavior on long versus short sequences.'],
 12: ['Train an autoencoder and visualize reconstructions and the latent space.',
      'Interpolate between two points in latent space live.',
      'Sketch a contrastive setup and show the augmentation views.'],
 13: ['Load a pretrained model and fine-tune it live on a new task.',
      'Compare from-scratch, frozen-features, and fine-tuning side by side.',
      'Run inference on new inputs end to end.']}
