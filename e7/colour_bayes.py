# Exercise 7
# Author: Md Rownak Abtahee Diganta 
# Student ID: 301539632

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage.color import lab2rgb
import sys
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from skimage.color import (separate_stains, combine_stains, hdx_from_rgb, rgb_from_hdx)
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer
from skimage.color import rgb2lab
# representative RGB colours for each label, for nice display
COLOUR_RGB = {
    'red': (255, 0, 0),
    'orange': (255, 112, 0),
    'yellow': (255, 255, 0),
    'green': (0, 231, 0),
    'blue': (0, 0, 255),
    'purple': (185, 0, 185),
    'brown': (117, 60, 0),
    'pink': (255, 184, 184),
    'black': (0, 0, 0),
    'grey': (150, 150, 150),
    'white': (255, 255, 255),
}
name_to_rgb = np.vectorize(COLOUR_RGB.get, otypes=[np.uint8, np.uint8, np.uint8])


def plot_predictions(model, lum=67, resolution=300):
    """
    Create a slice of LAB colour space with given luminance; predict with the model; plot the results.
    """
    wid = resolution
    hei = resolution
    n_ticks = 5

    # create a hei*wid grid of LAB colour values, with L=lum
    ag = np.linspace(-100, 100, wid)
    bg = np.linspace(-100, 100, hei)
    aa, bb = np.meshgrid(ag, bg)
    ll = lum * np.ones((hei, wid))
    lab_grid = np.stack([ll, aa, bb], axis=2)

    # convert to RGB for consistency with original input
    X_grid = lab2rgb(lab_grid)

    # predict and convert predictions to colours so we can see what's happening
    y_grid = model.predict(X_grid.reshape((-1, 3)))
    pixels = np.stack(name_to_rgb(y_grid), axis=1) / 255
    pixels = pixels.reshape((hei, wid, 3))

    # plot input and predictions
    plt.figure(figsize=(10, 5))
    plt.suptitle('Predictions at L=%g' % (lum,))
    plt.subplot(1, 2, 1)
    plt.title('Inputs')
    plt.xticks(np.linspace(0, wid, n_ticks), np.linspace(-100, 100, n_ticks))
    plt.yticks(np.linspace(0, hei, n_ticks), np.linspace(-100, 100, n_ticks))
    plt.xlabel('A')
    plt.ylabel('B')
    plt.imshow(X_grid.reshape((hei, wid, -1)))

    plt.subplot(1, 2, 2)
    plt.title('Predicted Labels')
    plt.xticks(np.linspace(0, wid, n_ticks), np.linspace(-100, 100, n_ticks))
    plt.yticks(np.linspace(0, hei, n_ticks), np.linspace(-100, 100, n_ticks))
    plt.xlabel('A')
    plt.imshow(pixels)


def main(infile):
    data = pd.read_csv(infile)
    # ref: https://stackoverflow.com/questions/73121011/userwarning-x-has-feature-names-but-gaussiannb-was-fitted-without-feature-name
    # was having a warning X features as names... fixed it by looking at above reference 
    # changes X as fixing the warning 
    X = data[['R','G','B']].values # array with shape (n, 3). Divide by 255 so components are all 0-1.
    X = X/255
    y = data['Label'] # array with shape (n,) of colour words.

    # Partition your data into training and validation sets using train_test_split.
    X_train, X_test, y_train, y_test = train_test_split(X,y) # From the given hint 
    # TODO: build model_rgb to predict y from X.
    model_rgb = GaussianNB()         # From the given hint 
    model_rgb.fit(X_train,y_train)
    
    # TODO: print model_rgb's accuracy score
    model_accuracy_score = model_rgb.score(X_test,y_test)
    print("The model_rgb's accuracy score: ", model_accuracy_score)

    # TODO: build model_lab to predict y from X by converting to LAB colour first.
    model_lab = make_pipeline(FunctionTransformer(rgb2lab),GaussianNB())
    model_lab.fit(X_train,y_train)
    # TODO: print model_lab's accuracy score
    model_lab_accuracy_score = model_lab.score(X_test,y_test)
    print("The model_lab's accuracy score:", model_lab_accuracy_score)

    plot_predictions(model_rgb)
    #plt.show()
    plt.savefig('predictions_rgb.png')
    plot_predictions(model_lab)
    #plt.show()
    plt.savefig('predictions_lab.png')


if __name__ == '__main__':
    main(sys.argv[1])