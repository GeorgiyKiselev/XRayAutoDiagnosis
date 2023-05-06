# XRayAutoDiagnosis
Neural Network for diagnosis of 12 chest conditions (pneumonia, hernia, etc.) along with co-occurences, based on frontal chest X-ray images.

Project for GDSC at Davis. The Network will most likely involve the use of several architectures with frozen weights. Will experiment with ensemble.


The gdsc_mobilenet.py file is a brutish attempt at the initial architecture where a critical issue was discovered - many of the images are mis-labelled. 
To follow is an auto-labeller experiment I have been working on, and a PyTorch CNN model that somehow performs well on misclassified data. 
