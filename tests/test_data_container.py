from ms_feature_validation import data_container
import numpy as np
import pandas as pd
import pytest


def test_data_path_setter_unexistent_path(data_container_example):
    data = data_container_example
    with pytest.raises(FileNotFoundError):
        data.data_path = "wrong_path"


def test_class_getter(data_container_example):
    data = data_container_example
    class_series = pd.Series(data=data.classes, index=data.classes.index)
    assert data.classes.equals(class_series)


def test_class_setter(data_container_example):
    data = data_container_example
    class_series = pd.Series(data=data.classes, index=data.classes.index)
    #set classes to an arbitrary value
    data.classes = 4
    data.classes = class_series
    assert data.classes.equals(class_series)


def test_batch_getter(data_container_example):
    data = data_container_example
    batch_series = pd.Series(data=data.batch, index=data.batch.index)
    print(data.batch)
    assert data.batch.equals(batch_series)


def test_batch_setter(data_container_example):
    data = data_container_example
    b = np.arange(data.data_matrix.shape[0])
    batch_series = pd.Series(data=b, index=data.batch.index)
    data.batch = b
    assert data.batch.equals(batch_series)


def test_order_getter(data_container_example):
    data = data_container_example
    order_series = pd.Series(data=data.order, index=data.order.index)
    assert data.order.equals(order_series)


def test_order_setter(data_container_example):
    data = data_container_example
    order_series = pd.Series(data=data.order, index=data.order.index)
    #set classes to an arbitrary value
    data.order = 4
    data.order = order_series
    assert data.order.equals(order_series)


def test_is_valid_class_name_with_valid_names(data_container_example):
    data = data_container_example
    assert data.is_valid_class_name("healthy")


def test_is_valid_class_name_with_invalid_names(data_container_example):
    data = data_container_example
    assert not data.is_valid_class_name("invalid_name")


def test_mapping_setter(data_container_example):
    data = data_container_example
    mapping = {"sample": ["healthy", "disease"],
               "blank": ["SV"]}
    expected_mapping = {"sample": ["healthy", "disease"],
                        "blank": ["SV"], "qc": None, "zero": None,
                        "suitability": None}
    data.mapping = mapping
    assert data.mapping == expected_mapping

def test_mapping_setter_bad_sample_type(data_container_example):
    data = data_container_example
    mapping = {"sample": ["healthy", "disease"],
               "blank": ["SV"], "bad_sample_type": ["healthy"]}
    with pytest.raises(ValueError):
        data.mapping = mapping


def test_mapping_setter_bad_sample_class(data_container_example):
    data = data_container_example
    mapping = {"sample": ["healthy", "disease"],
               "blank": ["SV", "bad_sample_class"]}
    with pytest.raises(ValueError):
        data.mapping = mapping


def test_remove_empty_feature_list(data_container_example):
    data = data_container_example
    features = data.data_matrix.columns.copy()
    data.remove([], "features")
    assert data.data_matrix.columns.equals(features)


def test_remove_empty_sample_list(data_container_example):
    data = data_container_example
    samples = data.data_matrix.index.copy()
    data.remove([], "samples")
    assert data.data_matrix.index.equals(samples)


def test_remove_correct_samples(data_container_example):
    data = data_container_example
    samples = data.data_matrix.index.copy()
    rm_samples = ["sample 1", "sample 2"]
    data.remove(rm_samples, "samples")
    assert data.data_matrix.index.equals(samples.difference(rm_samples))


def test_remove_correct_features(data_container_example):
    data = data_container_example
    features = data.data_matrix.columns.copy()
    rm_features = ["FT01", "FT02"]
    data.remove(rm_features, "features")
    assert data.data_matrix.columns.equals(features.difference(rm_features))
    

def test_equal_feature_index(data_container_example):
    data = data_container_example
    assert data.feature_metadata.index.equals(data.data_matrix.columns)


def test_equal_sample_index(data_container_example):
    data = data_container_example
    assert data.data_matrix.index.equals(data.sample_metadata.index)


def test_remove_nonexistent_feature(data_container_example):
    data = data_container_example
    with pytest.raises(ValueError):
        data.remove(["bad_feature_name"], "features")


def test_remove_nonexistent_sample(data_container_example):
    data = data_container_example
    with pytest.raises(ValueError):
        data.remove(["bad_sample_name"], "samples")


# TODO: think about how to test data_path and get_available_samples