use pyo3::{create_exception, exceptions::PyBaseException};

create_exception!(peace_performance, ParseBeatmapError, PyBaseException);
create_exception!(peace_performance, ReadFileError, PyBaseException);
