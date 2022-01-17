# Photomath
Basic implementation of handwritten digit recognizer with equation solver. It consists of three main parts.
First are the open CV image processing tools which is located in imageproc.py. Pass the image of the equation to the imageproc.cropped_dataset to get the array of cropped symbols. 
You can fine tune the function with dilate_multiplier parameter if the symbols are too partitioned and minimum_area parameter if background noise is being recognized as a symbol.

The second part is the trained convolutional network model. The training was done by using two publicly available datasets. 

https://github.com/wblachowski/bhmsds

https://www.kaggle.com/xainano/handwrittenmathsymbols

<p align="center">
  <img src="https://user-images.githubusercontent.com/53495210/149681422-ab9810e2-5bdf-4f35-890b-e434910bb69f.png"/>
</p>
The bigger dataset, which is extracted from CHROME dataset, has symbols which are very thin, almost never thicker than 1px. That's why we also preprocess all the input images so
they are 1px thin so that the input data is as similar as possible to the training dataset. Afterwards, they are centered.
The first convolutional layer has a (5x5) kernel which is more suited towards the extraction of data in low information environment of binarized single channel images. The data is
also regularized with 2 MaxPool layers, a Batch Normalization layer and a Dropout layer to ensure that our model is not overfitted.
The model is sucessfully trained through 20 epochs, reaching a 99,7 train and validation accuracy.
#
#
#

Solver is

<p align="center">
  <img src="https://user-images.githubusercontent.com/53495210/149789537-5c83d79f-3cac-4a80-9988-238d3cb2f60c.png"/>
</p>
