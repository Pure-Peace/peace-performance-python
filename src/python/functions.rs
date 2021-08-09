use pyo3::{prelude::pyfunction, PyAny, PyResult, Python};
use std::{env, path::PathBuf};

use crate::{
    methods::{common, pp},
    objects::{Beatmap, Calculator},
};

#[cfg(any(feature = "async_tokio", feature = "async_std"))]
use pyo3::IntoPy;
#[cfg(feature = "async_std")]
use pyo3_asyncio::async_std as pyo3_runtime;
#[cfg(feature = "async_tokio")]
use pyo3_asyncio::tokio as pyo3_runtime;

#[pyfunction]
pub fn set_log_level(log_level: &str) {
    env::set_var("RUST_LOG", log_level);
}

#[pyfunction]
pub fn init_logger() {
    pretty_env_logger::init();
}

#[cfg(any(feature = "async_tokio", feature = "async_std"))]
#[pyfunction]
pub fn rust_sleep(py: Python, secs: u64) -> PyResult<&PyAny> {
    pyo3_runtime::future_into_py(py, async move {
        common::sleep(secs).await;
        Ok(Python::with_gil(|py| py.None()))
    })
}

#[cfg(not(any(feature = "async_tokio", feature = "async_std")))]
#[pyfunction]
pub fn rust_sleep(_py: Python, _secs: u64) -> PyResult<&PyAny> {
    unimplemented!("Any async features (async_tokio, async_std) are not enabled.")
}

#[cfg(any(feature = "async_tokio", feature = "async_std"))]
#[pyfunction]
pub fn read_beatmap_async(py: Python, path: PathBuf) -> PyResult<&PyAny> {
    pyo3_runtime::future_into_py(py, async {
        let file = common::async_read_file(path).await?;
        let beatmap = pp::async_parse_beatmap(file).await?;
        Python::with_gil(|py| Ok(Beatmap(beatmap).into_py(py)))
    })
}

#[pyfunction]
pub fn read_beatmap_sync(path: PathBuf) -> PyResult<Beatmap> {
    let file = common::sync_read_file(path)?;
    Ok(Beatmap(pp::sync_parse_beatmap(file)?))
}

#[cfg(not(any(feature = "async_tokio", feature = "async_std")))]
#[pyfunction]
pub fn read_beatmap_async(_py: Python, _path: PathBuf) -> PyResult<&PyAny> {
    unimplemented!("Any async features (async_tokio, async_std) are not enabled.")
}

#[pyfunction]
pub fn new_calculator() -> Calculator {
    Calculator::new()
}
