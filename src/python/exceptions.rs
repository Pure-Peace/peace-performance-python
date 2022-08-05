use pyo3::{create_exception, exceptions::PyException};

create_exception!(rosu_pp, ParseBeatmapError, PyException);
create_exception!(rosu_pp, ReadFileError, PyException);
create_exception!(rosu_pp, AsyncNotEnabledError, PyException);
create_exception!(rosu_pp, FeatureEnabledError, PyException);
create_exception!(rosu_pp, InvalidGameMode, PyException);
