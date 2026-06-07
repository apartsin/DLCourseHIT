# -*- coding: utf-8 -*-
"""Prerequisite review content. Rendered by build_site.py into prereq/ pages so students
can self-assess and refresh the math, Python, and ML background the course assumes."""

PREREQ = {
    "math": {
        "title": "Mathematics",
        "icon": "&#8721;",
        "intro": "Deep learning is applied linear algebra and calculus with a probabilistic flavor. "
                 "A mathematician's depth is not required, but these ideas should feel familiar so the "
                 "course can move quickly from notation to networks.",
        "sections": [
            {"h": "Linear algebra", "points": [
                "Vectors and matrices; addition, scaling, transpose.",
                "Matrix multiplication and the dot product (and what shapes are compatible).",
                "Norms (L1, L2), and the geometric meaning of a dot product.",
                "The idea of rank, and a light acquaintance with eigenvalues and SVD.",
            ]},
            {"h": "Probability and statistics", "points": [
                "Random variables, discrete and continuous distributions.",
                "Expectation, mean, variance, and standard deviation.",
                "Conditional probability, independence, and Bayes' rule.",
                "Why cross-entropy and likelihood show up in loss functions.",
            ]},
            {"h": "Multivariable functions", "points": [
                "Functions of several variables and their surfaces.",
                "Partial derivatives and the gradient as the vector of partials.",
                "The chain rule (the engine behind backpropagation).",
                "A light feel for the Jacobian and Hessian.",
            ]},
            {"h": "Gradients and optimization", "points": [
                "The gradient points in the direction of steepest ascent.",
                "Gradient descent: step opposite the gradient to minimize.",
                "Learning rate intuition: too large diverges, too small crawls.",
                "Local versus global minima; what convexity provides.",
            ]},
        ],
        "checklist": [
            "Multiply two matrices by hand and state the result shape.",
            "Compute a gradient of a simple multivariable function.",
            "Explain what expectation and variance measure.",
            "Describe how gradient descent uses the gradient.",
        ],
        "selfcheck": [
            ("If A is 3x4 and B is 4x2, what is the shape of AB?", "3x2 (inner dimensions 4 must match; outer dimensions give the result)."),
            ("What does the gradient of a scalar function indicate?", "The direction of steepest increase; its negative is the descent direction."),
            ("Why is the chain rule central to deep learning?", "Backpropagation applies it to compose per-layer derivatives into parameter gradients."),
            ("What is the difference between mean and variance?", "Mean is the average value; variance measures the spread around the mean."),
        ],
        "resources": [
            {"title": "3Blue1Brown: Essence of Linear Algebra", "url": "https://www.3blue1brown.com/topics/linear-algebra"},
            {"title": "3Blue1Brown: Essence of Calculus", "url": "https://www.3blue1brown.com/topics/calculus"},
            {"title": "Khan Academy: Multivariable Calculus", "url": "https://www.khanacademy.org/math/multivariable-calculus"},
            {"title": "Mathematics for Machine Learning (free book)", "url": "https://mml-book.github.io/"},
        ],
    },
    "python": {
        "title": "Python Foundations & Advanced Features",
        "icon": "&#128013;",
        "intro": "PyTorch is a Python library, and idiomatic Python makes deep-learning code short and "
                 "readable. Beyond the basics, a handful of features appear constantly in PyTorch and "
                 "data code; know them and the framework stops feeling mysterious.",
        "sections": [
            {"h": "Core Python", "points": [
                "Data types, control flow, functions, and modules.",
                "Classes and objects (PyTorch models are classes).",
                "Slicing and negative indexing.",
            ]},
            {"h": "Idiomatic and advanced features", "points": [
                "List, dict, and set comprehensions.",
                "Generators and iterators (yield) for streaming data.",
                "lambda, and *args / **kwargs.",
                "enumerate and zip; f-strings; context managers (with).",
                "Decorators at a reading level (e.g. @torch.no_grad()).",
            ]},
            {"h": "Useful dunder (magic) methods", "points": [
                "__init__ for construction.",
                "__len__ and __getitem__: exactly what a PyTorch Dataset implements.",
                "__call__: why model(x) runs the forward pass (nn.Module defines __call__).",
                "__repr__ for readable objects.",
            ]},
            {"h": "NumPy versus Python lists", "points": [
                "ndarray is typed and contiguous; lists are generic and slow.",
                "Vectorized operations replace explicit Python loops.",
                "Broadcasting and dtypes carry over directly to PyTorch tensors.",
                "tensor.numpy() and torch.from_numpy() bridge the two.",
            ]},
            {"h": "What recurs in PyTorch and DL code", "points": [
                "Fancy indexing and boolean masks.",
                "Broadcasting to avoid loops over batches.",
                "In-place operations (the trailing underscore, e.g. add_).",
                "Moving data with .to(device).",
            ]},
        ],
        "checklist": [
            "Rewrite a for-loop that builds a list as a comprehension.",
            "Write a generator that yields batches from a list.",
            "Implement a tiny class with __len__ and __getitem__.",
            "Explain why a NumPy vectorized op beats a Python loop.",
        ],
        "selfcheck": [
            ("What does a generator provide over a list?", "Lazy, memory-efficient iteration; values are produced on demand with yield."),
            ("Which dunder methods does a PyTorch Dataset implement?", "__len__ and __getitem__."),
            ("Why does calling model(x) work instead of model.forward(x)?", "nn.Module defines __call__, which invokes forward (plus hooks)."),
            ("Why prefer a NumPy array over a Python list for numeric work?", "Typed contiguous memory plus vectorized C-level operations, far faster than Python loops."),
        ],
        "resources": [
            {"title": "The Python Tutorial (official)", "url": "https://docs.python.org/3/tutorial/"},
            {"title": "Real Python: List Comprehensions", "url": "https://realpython.com/list-comprehension-python/"},
            {"title": "Real Python: Generators", "url": "https://realpython.com/introduction-to-python-generators/"},
            {"title": "NumPy: the absolute basics for beginners", "url": "https://numpy.org/doc/stable/user/absolute_beginners.html"},
        ],
    },
    "ml": {
        "title": "Basic Machine Learning Concepts",
        "icon": "&#129518;",
        "intro": "This course assumes an introductory machine-learning course. Deep learning reuses its "
                 "vocabulary, models, losses, splits, and the overfitting story, so the network material "
                 "lands on familiar ground.",
        "sections": [
            {"h": "Supervised learning", "points": [
                "Regression (predict a number) versus classification (predict a class).",
                "Features, labels, and the train/test setup.",
                "Linear and logistic regression as the simplest models.",
            ]},
            {"h": "Error, cost, and loss", "points": [
                "Loss is the error on one example; cost or objective aggregates it over the data.",
                "MSE for regression; cross-entropy for classification.",
                "The loss is what training minimizes; the metric is what is reported.",
            ]},
            {"h": "Overfitting and generalization", "points": [
                "Training error versus test (generalization) error.",
                "Train/validation/test splits and cross-validation.",
                "Learning curves and the train-minus-validation gap.",
            ]},
            {"h": "Regularization", "points": [
                "L2 (weight decay) and L1 penalties.",
                "Early stopping and (in DL) dropout and data augmentation.",
                "Regularization trades a little fit for better generalization.",
            ]},
            {"h": "The bias-variance dilemma", "points": [
                "High bias (underfitting) versus high variance (overfitting).",
                "Model capacity and data size shift the balance along the trade-off.",
                "The goal is the sweet spot that minimizes test error.",
            ]},
            {"h": "Other essentials", "points": [
                "Gradient descent and the learning rate.",
                "Feature scaling and normalization.",
                "Evaluation: accuracy, precision, recall, F1, ROC/AUC, the confusion matrix.",
                "Parameters versus hyperparameters; baselines; data leakage; class imbalance.",
            ]},
        ],
        "checklist": [
            "State whether a task is regression or classification and pick a loss.",
            "Explain overfitting using the train/validation gap.",
            "Describe how L2 regularization changes the objective.",
            "Read a confusion matrix and compute precision and recall.",
        ],
        "selfcheck": [
            ("What is the difference between a loss and a metric?", "The loss is optimized during training; the metric is the human-facing measure reported (they can differ)."),
            ("How is overfitting detected?", "A low training error with a much higher validation/test error (a large gap)."),
            ("What does the bias-variance trade-off describe?", "Balancing underfitting (high bias) against overfitting (high variance) to minimize test error."),
            ("Why can accuracy mislead under class imbalance?", "A trivial majority predictor scores high; use precision/recall, F1, or balanced accuracy instead."),
        ],
        "resources": [
            {"title": "Google Machine Learning Crash Course", "url": "https://developers.google.com/machine-learning/crash-course"},
            {"title": "An Introduction to Statistical Learning (free book)", "url": "https://www.statlearning.com/"},
            {"title": "StatQuest: Machine Learning playlist", "url": "https://www.youtube.com/playlist?list=PLblh5JKOoLUICTaGLRoHQDuF_7q2GfuJF"},
            {"title": "scikit-learn: Metrics and scoring", "url": "https://scikit-learn.org/stable/modules/model_evaluation.html"},
        ],
    },
}

ORDER = ["math", "python", "ml"]
