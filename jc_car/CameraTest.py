# import the necessary packages
from __future__ import division, print_function, absolute_import

import tflearn
from tflearn.data_utils import shuffle
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from tflearn.data_preprocessing import ImagePreprocessing
from tflearn.data_augmentation import ImageAugmentation
import scipy
import numpy as np
# import tensorflow as tf
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 15
camera.rotation = 180
camera.brightness = 60
camera.contrast = 60
camera.awb_mode = 'off'
camera.awb_gains = [1.2, 1.8]
#camera.start_preview()
#camera.capture('/home/pi/Documents/jumblecube_repo/jc_car/CameraImage/Image2.jpg')
#time.sleep(0.05)
#camera.stop_preview()
rawCapture = PiRGBArray(camera, size=(640, 480))
# allow the camera to warmup
time.sleep(0.1)


def load_model():
    img_prep = ImagePreprocessing()
    img_prep.add_featurewise_zero_center()
    img_prep.add_featurewise_stdnorm()
    img_aug = ImageAugmentation()
    img_aug.add_random_flip_leftright()
    img_aug.add_random_rotation(max_angle=25.)
    img_aug.add_random_blur(sigma_max=3.)

    input_layer = input_data(shape=[None, 32, 32, 3],
                             data_preprocessing=img_prep,
                             data_augmentation=img_aug, name='input')
    # Step 1: Convolution
    conv2d_l1 = conv_2d(input_layer, 120, 5,
                        activation='relu', name='conv2d_l1')
    # Step 2: Max pooling
    max_pool_l1 = max_pool_2d(conv2d_l1, 2, name='max_pool_l1')
    # Step 3: Convolution again
    conv2d_l2 = conv_2d(max_pool_l1, 150, 3,
                        activation='relu', name='conv2d_l2')
    # Step 4: Max pooling
    max_pool_l2 = max_pool_2d(conv2d_l2, 2, name='max_pool_l2')
    # Step 5: Convolution yet again
    conv2d_l3 = conv_2d(max_pool_l2, 250, 3,
                        activation='relu', name='conv2d_l3')
    # Step 6: Max pooling again
    max_pool_l3 = max_pool_2d(conv2d_l3, 2, name='max_pool_l3')
    # Step 7: Dropout - throw away some data randomly to prevent over-fitting
    dropout_1 = dropout(max_pool_l3, 0.5)
    # Step 8: Fully-connected 300 node neural network
    dense_1 = fully_connected(dropout_1, 300,
                              activation='tanh', name='dense_1')
    # Step 9: Dropout - throw away some data randomly to prevent over-fitting
    dropout_2 = dropout(dense_1, 0.5)
    # Step 8: Fully-connected neural network with two outputs
    dense_2 = fully_connected(dropout_2, 43,
                              activation='softmax', name='dense_2')
    # Tell tflearn how we want to train the network
    network = regression(dense_2, optimizer='adam',
                         loss='categorical_crossentropy',
                         learning_rate=0.001, name='target')
    # Wrap the network in a model object
    model = tflearn.DNN(network, tensorboard_verbose=0)
    model.load("sign-classifier.tfl")
    time.sleep(0.1)
    return model


def process_image(img, model):
    img = scipy.misc.imresize(img, (32, 32),
                              interp="bicubic").astype(np.float32,
                                                       casting='unsafe')
    prediction = model.predict([img])
    return np.argmax(prediction)+1


model = load_model()

i = 0
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture,
                                       format="rgb", use_video_port=True):
    start = time.time()
    image = frame.array
    predict_img = process_image(image, model)
    print('Image classified as ', predict_img, 'in ', i,
          ' time ', (time.time()-start))
    rawCapture.truncate(0)
    i = i + 1
    if i > 50:
        break
