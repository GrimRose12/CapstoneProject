from keras.models import load_model
from keras.applications.mobilenet_v2 import preprocess_input
from imageio import imread
from skimage.transform import resize
import numpy as np

def classify(directory):
    def decode_predictions_custom(predictions, labels):
        decoded_predictions = []
        for prediction in predictions:
            class_index = prediction.argmax()
            class_label = labels[class_index]
            confidence = prediction[class_index]
            decoded_predictions.append((class_label, confidence))
        return decoded_predictions
    
    model = load_model('mobilev2.h5')
    im = imread(directory)
    im = preprocess_input(im)
    im = resize(im, output_shape=(224, 224))
    im = np.expand_dims(im, axis=0)
    prediction = model.predict(im)
    #index = prediction.index(max(prediction)) + 1
    # labels = ['Monitoring', 'Alert', 'Warning']
    # decoded_predictions = decode_predictions_custom(prediction, labels)

    # for class_label, confidence in decoded_predictions:
    #     print(f"{class_label}: {confidence:.4f}")
    index = np.argmax(prediction) + 1
    return index # returns 1,2, or 3