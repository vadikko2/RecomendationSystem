import sys
sys.path.insert(0, r'../')
import src.dataset as ds

X, Y = ds.make_dataset_for_classifier(path_with_jsons='../jsons/')
print(X.shape, Y.shape)
