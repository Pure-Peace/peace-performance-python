use pyo3::{create_exception, exceptions::PyException};

create_exception!(peace_performance, ParseBeatmapError, PyException);
create_exception!(peace_performance, ReadFileError, PyException);
