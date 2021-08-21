use pyo3::{create_exception, exceptions::PyException};

create_exception!(peace_performance, ParseBeatmapError, PyException);
create_exception!(peace_performance, ReadFileError, PyException);
create_exception!(peace_performance, AsyncNotEnabledError, PyException);
create_exception!(peace_performance, FeatureEnabledError, PyException);
create_exception!(peace_performance, InvalidGameMode, PyException);
