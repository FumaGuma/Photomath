# Photomath

### App

https://photomathproject.herokuapp.com/

## Instructions
Basic implementation of handwritten digit recognizer with equation solver. When passing an image to the system the multiplication should be written as `x` and division as `/`  It consists of three main parts.
First are the open CV image processing tools which are located in <code>imageprocessing.py</code>. Pass the image of the equation to the <code>imageprocessing.cropped_dataset</code> to get the array of cropped symbols.
You can fine tune the function with <code>dilate_multiplier</code> parameter if the symbols are too partitioned and <code>minimum_area</code> parameter if the background noise is being recognized as a symbol.

Basic Handwritten Math Symbols Dataset<br/>
https://github.com/wblachowski/bhmsds

Handwritten math symbols dataset<br/>
https://www.kaggle.com/xainano/handwrittenmathsymbols

<p float="left">
  <img src="https://user-images.githubusercontent.com/53495210/149681422-ab9810e2-5bdf-4f35-890b-e434910bb69f.png"/ width="400">
  <img src="https://user-images.githubusercontent.com/53495210/149789537-5c83d79f-3cac-4a80-9988-238d3cb2f60c.png"/ width="400">
</p>

The second part is the trained convolutional network model. The training was done using two publicly available datasets. 
The bigger dataset, which is extracted from CHROME dataset, has symbols which are very thin, almost never thicker than `1px`. That's why we also preprocess all the input images so
they are `1px` thin so that the input data is as similar as possible to the training dataset. Afterwards, the cropped images are centered.
The first convolutional layer has a `(5x5)` kernel which is more suited towards the extraction of data in low information environment of binarized single channel images while second and third have `(3x3)` kernel. The data is
also regularized with `2` MaxPool layers, a Batch Normalization layer and a Dropout layer to ensure that our model is not overfitted.
It took `30` epochs to sucessfully train our model, reaching a `99%` train and validation accuracy. You can run the cropped data through the network with the <code>imageprocessing.data_to_model</code> to obtain the model's prediction. Alternatively you can simply pass the original image to <code>imageprocessing.process_image</code> function to get the equation from the image.

Equation solver is very straightforward. It checks the equation for invalid inputs and if the equation is valid, it splits it into a list of tokens. Solver then goes through the equation while respecting the order of operations. It solves the content of brackets first, applying multiplication and division, then addition and subtraction. You can run the solver using the <code>solver.solve</code> function.

## Discussion

There are a lot of edge cases and changing one parameter in processing can significantly alter the predictions of the model, so if you optimize the preprocessing parameters for one series of images your model will give a worse performance on the other. Centering the images by their moments helped for majority of examples that I investigated but would be a deterrent in some nieche cases where the image weight is distributed in a corner. There are also many small tweaks that can help the model correctly identify the equation, for example, the bounding boxes can be expanded on the `x-axis` around the brackets symbols because it helps maintain they shape when they are being reshaped to the dimensions of training data.

Our Deep learning model is also limited by the quality of the available data. A better dataset for training this kind of problem would have either a collection of handwritten digits without much processing, with background information and preserved details of the strokes. Alternatively, a dataset of labeled equations could also work since inference of value of particular symbols is highly dependent on the context (opened brackets must be closed, two operators cannot be adjacent), so the model which has the information about the entire system, not only of individual symbols could utilize the context dependent information.

<p float="left">
  <img src="https://user-images.githubusercontent.com/53495210/149847896-6d0f80ab-4686-4beb-a5d1-6ac92cd415db.jpg"/ width="400">
  <img src="https://user-images.githubusercontent.com/53495210/149847509-7a855326-80cc-4b0d-90f2-1e2ec1d8f4a3.jpg"/ width="400">
</p>

