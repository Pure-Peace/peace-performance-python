use pyo3::{prelude::pyfunction, PyAny, PyResult, Python};
use std::path::PathBuf;

use crate::{
    methods::{common, pp},
    objects::{Beatmap, Calculator},
};

#[cfg(any(feature = "async_tokio", feature = "async_std"))]
use pyo3::IntoPy;
#[cfg(feature = "async_std")]
use pyo3_asyncio::async_std as pyo3_async_runtime;
#[cfg(feature = "async_tokio")]
use pyo3_asyncio::tokio as pyo3_async_runtime;

#[cfg(feature = "rust_logger")]
#[pyfunction]
#[inline(always)]
pub fn set_log_level(log_level: &str) {
    std::env::set_var("RUST_LOG", log_level);
}

#[cfg(not(feature = "rust_logger"))]
#[pyfunction]
pub fn set_log_level(_log_level: &str) -> PyResult<()> {
    Err(crate::rust_logger_not_enabled_err!())
}

#[cfg(feature = "rust_logger")]
#[pyfunction]
#[inline(always)]
pub fn init_logger() {
    pretty_env_logger::init();
}

#[cfg(not(feature = "rust_logger"))]
#[pyfunction]
pub fn init_logger() -> PyResult<()> {
    Err(crate::rust_logger_not_enabled_err!())
}

#[cfg(any(feature = "async_tokio", feature = "async_std"))]
#[pyfunction]
#[inline(always)]
pub fn rust_sleep(py: Python, secs: u64) -> PyResult<&PyAny> {
    pyo3_async_runtime::future_into_py(py, async move {
        common::sleep(secs).await;
        Ok(Python::with_gil(|py| py.None()))
    })
}

#[cfg(not(any(feature = "async_tokio", feature = "async_std")))]
#[pyfunction]
pub fn rust_sleep(_py: Python, _secs: u64) -> PyResult<&PyAny> {
    Err(crate::async_not_enabled_err!())
}

#[cfg(any(feature = "async_tokio", feature = "async_std"))]
#[pyfunction]
#[inline(always)]
pub fn read_beatmap_async(py: Python, path: PathBuf) -> PyResult<&PyAny> {
    pyo3_async_runtime::future_into_py(py, async {
        let file = common::async_read_file(path).await?;
        let beatmap = pp::async_parse_beatmap(file).await?;
        Python::with_gil(|py| Ok(Beatmap(beatmap).into_py(py)))
    })
}

#[pyfunction]
#[inline(always)]
pub fn read_beatmap_sync(path: PathBuf) -> PyResult<Beatmap> {
    let file = common::sync_read_file(path)?;
    Ok(Beatmap(pp::sync_parse_beatmap(file)?))
}

#[cfg(not(any(feature = "async_tokio", feature = "async_std")))]
#[pyfunction]
pub fn read_beatmap_async(_py: Python, _path: PathBuf) -> PyResult<&PyAny> {
    Err(crate::async_not_enabled_err!())
}

#[pyfunction]
#[inline(always)]
pub fn new_calculator() -> Calculator {
    Calculator::new_empty()
}

#[pyfunction]
#[inline(always)]
/// osu! mode int to string
pub fn osu_mode_int_str(mode: u8) -> Option<String> {
    Some(
        match mode {
            0 => "std",
            1 => "taiko",
            2 => "ctb",
            3 => "mania",
            _ => return None,
        }
        .into(),
    )
}

#[pyfunction]
#[inline(always)]
/// osu! mode int to string
pub fn osu_mode_str_int(mode: &str) -> Option<u8> {
    Some(match mode {
        "std" => 0,
        "taiko" => 1,
        "ctb" => 2,
        "mania" => 3,
        _ => return None,
    })
}
