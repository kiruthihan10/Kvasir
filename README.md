# Kvasir
Solution for kvasir dataset with transfer learning

As for the transfer learning I used Mobilenet v2 because it is comparetively light weight with low number of parameters.
As this is a simple 8 classes of classfication we can use this simple pretrained model.
The metrics used here is accuracy which is a catagorical cross Accuracy and the loss function is categorical cross entropy. Becuase This is a classification task.
# Model Details
Batch size is 128
Used Inception V2 pretrained model with it's weight.
Used adam optimizer with learning rate scheduler
Inital Learning rate is 0.05
Didn't used any image augmentations other than resizing and rescaling
Didn't used any GPU training strategies
# Model Requirment
Used Colab GPU and 25.51 GB RAM
# Obesrvations
average time per epoch is 88.92857142857143
After 14 epoch the system crashed with RAM usage exceeding
The Accuracy could be get high as 0.8747 for training accuracy and 0.6504 for validation accuracy
![Accuracy changing over the epochs](https://drive.google.com/open?id=1PWTRdjKy7KhkN0I-lSwAbH7-Z-MypP0o)


# Fine Tune
Tried to fine tune the model but ultimately failed to train it in 128 batch size
In lower batch size finetuning only mananged to spoil the system by bring the accuracy low as 0.35

https://colab.research.google.com/drive/19tKO2eeTUdnoJO5ybbnEumanaIz2jDXt
