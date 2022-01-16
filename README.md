# Photomath
Basic implementation of handwritten digit recognizer with equation solver. It consists of three main parts.
First are the open CV image processing tools which is located in imageproc.py. Pass the image of the equation to the imageproc.cropped_dataset to get the array of cropped symbols. 
You can fine tune the function with dilate_multiplier parameter if the symbols are too partitioned and minimum_area parameter if background noise is being recognized as a symbol.

The second part is the trained convolutional network model. The training was done by using two publicly available datasets. 
https://github.com/wblachowski/bhmsds
https://www.kaggle.com/clarencezhao/handwritten-math-symbol-dataset
Network consists of ![network_architecture](https://user-images.githubusercontent.com/53495210/149681422-ab9810e2-5bdf-4f35-890b-e434910bb69f.png)
