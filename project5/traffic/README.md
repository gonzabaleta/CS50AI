Started with the example of the class: 1 conv layer with 32 3 by 3 filters, one max pooling of 2 by 2, one hidden layer with 128 nodes, and 0.5 dropout. The result was that the algorithm was somewhat fast but reached 0.05 accuracy after 10 epochs.

Next tried by augmenting the conv filter to 256 6 by 6 filters, and the accuracy was much better: 0.84 after 10 epochs.

Now added a new conv layer with 256 6 by 6 filters, and another max pooling layer. The result went down again to 0.05 accuracy.

Now augmented the amount of nodes of the hiddenl ayer from 128 to 400 and the accuracy went up again to 0.85. It seems to me that the amount of hidden layers should be proportional to the amount of filters.

Now raised the amount of filters in the first conv layer from 256 to 512, and the amount of nodes in the hidden layer from 400 to 512. Accuracy went back down to 0.5.

Now tried reducing the amount of filters in the first conv layer to 256, and reduced the kernel size to 4 by 4. The improvement was substantial: 0.90 accuracy.

Added new hidden layer with 256 nodes: accuracy went up to 0.96.

Added another hidden layer with 256 nodes, and accuracy stayed the same. Added a conv layer with 128 filters and the accuracy stayed the same.

Turned dropout to 0.1, and accuracy went down to 0.95.
Eliminated dropout, and accuracy went up to 0.975, which seems to me like the model is overfitting. Decided to leave dropout at 0.4
