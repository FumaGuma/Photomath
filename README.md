# Photomath
Basic implementation of handwritten digit recognizer with equation solver. It consists of three main parts.
First part is the open CV image processing tool which are located in <code>imageprocessing.py</code>. Pass the image of the equation to the <code>imageprocessing.cropped_dataset</code> to get the array of cropped symbols.
You can fine tune the function with <code>dilate_multiplier</code> parameter if the symbols are too partitioned and <code>minimum_area</code> parameter if background noise is being recognized as a symbol.

Basic Handwritten Math Symbols Dataset<br/>
https://github.com/wblachowski/bhmsds

Handwritten math symbols dataset<br/>
https://www.kaggle.com/xainano/handwrittenmathsymbols

<p float="left">
  <img src="https://user-images.githubusercontent.com/53495210/149681422-ab9810e2-5bdf-4f35-890b-e434910bb69f.png"/>
  <img src="https://user-images.githubusercontent.com/53495210/149789537-5c83d79f-3cac-4a80-9988-238d3cb2f60c.png"/>
</p>

The second part is the trained convolutional network model. The training was done using two publicly available datasets. 
The bigger dataset, which is extracted from CHROME dataset, has symbols which are very thin, almost never thicker than *1px*. That's why we also preprocess all the input images so
they are 1px thin so that the input data is as similar as possible to the training dataset. Afterwards, they are centered.
The first convolutional layer has a (5x5) kernel which is more suited towards the extraction of data in low information environment of binarized single channel images. The data is
also regularized with 2 MaxPool layers, a Batch Normalization layer and a Dropout layer to ensure that our model is not overfitted.
It took 30 epochs to sucessfully train our model, reaching a 99% train and validation accuracy. You can run the cropped data through the network with the <code>imageprocessing.data_to_model</code> to obtain the model's prediction. Alternatively you can simply pass the original image to <code>imageprocessing.process_image</code> function to get the equation from the image.

Solver is based on the 
