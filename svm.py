import numpy as np
from csv import reader
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score, precision_score

# Load a CSV file
def load_csv(filename):
    dataset = list()
    with open(filename, 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            if not row:
                continue
            dataset.append(row)
    return dataset


# Convert string column to float
def str_column_to_int(dataset, column):
    for row in dataset:
        row[column] = int(row[column])


def str_column_to_int2(label):
    for i in range(len(label)):
        label[i] = round(float(label[i]))
        if label[i] <= 2:
            label[i] = 1
        elif label[i] <= 4:
            label[i] = 2
        elif label[i] <= 6:
            label[i] = 3
        elif label[i] <= 8:
            label[i] = 4
        else:
            label[i] = 5


filename = 'Responses.csv'
dataset = load_csv(filename)
label = []
for lst in dataset:
    label.append(lst[-1])
    del lst[-1]
for i in range(len(dataset[0])):
    str_column_to_int(dataset, i)

# Our dataset and targets
X = np.array(dataset)

str_column_to_int2(label)
Y = label

# figure number
fignum = 1

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# fit the model
for kernel in ("linear", "poly", "rbf"):
    clf = OneVsRestClassifier(SVC(kernel=kernel, gamma=2)).fit(X_train, y_train)
    print(Y)
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(y_test)
    print(y_train)
    recall = recall_score(y_test, y_pred, average='micro')
    precision = precision_score(y_test, y_pred, average='micro')
    print('kernel is : ' + str(kernel))
    print('accuracy_score is: ' + str(accuracy))
    print('recall score: ' + str(recall))
    print('precision score: ' + str(precision))


def prediction(lst):
    clf = OneVsRestClassifier(SVC(kernel="linear", gamma=2))
    clf.fit(X, Y)
    pred = clf.predict([lst])
    return int(pred)
