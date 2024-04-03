import pickle
import numpy as np

data = [14,2,11,0,105, 146, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 1, 0, 0, 255, 222, 0, 0, 0, 0, 0, 0, 0, 0]
print(data)
data = np.array(data)
print(f"type of the test data is {type(data)}")
try:
    # Load the pickle file
    with open('HIDS_model.pkl', 'rb') as model:
        loadedModel = pickle.load(model)
        predict = loadedModel.predict(data.reshape(1,-1))
        print(f"raw prediction is {predict}")
        resultDict = {'normal': 0, 'buffer_overflow': 1, 'loadmodule': 2, 'perl': 3, 'neptune': 4, 'smurf': 5, 'guess_passwd': 6,
                    'pod': 7, 'teardrop': 8, 'portsweep': 9, 'ipsweep': 10, 'land': 11, 'ftp_write': 12, 'back': 13, 'imap': 14,
                    'satan': 15, 'phf': 16, 'nmap': 17, 'multihop': 18, 'warezmaster': 19, 'warezclient': 20, 'spy': 21, 'rootkit': 22}
        prediction_label = list(resultDict.keys())[list(resultDict.values()).index(predict)]
        print(f"predicted attack type is {prediction_label}")
        
except Exception as e:
    raise e
