use pyo3::{prelude::pyfunction, IntoPy, PyAny, PyResult, Python};
use std::{env, path::PathBuf};

use crate::{
    methods::{common, pp},
    objects::{Beatmap, Calculator},
};

#[pyfunction]
pub fn rust_sleep(py: Python, secs: u64) -> PyResult<&PyAny> {
    pyo3_asyncio::tokio::future_into_py(py, async move {
        common::sleep(secs).await;
        Ok(Python::with_gil(|py| py.None()))
    })
}

#[pyfunction]
pub fn set_log_level(log_level: &str) {
    env::set_var("RUST_LOG", log_level);
}

#[pyfunction]
pub fn init_logger() {
    pretty_env_logger::init();
}

#[pyfunction]
pub fn read_beatmap(py: Python, path: PathBuf) -> PyResult<&PyAny> {
    pyo3_asyncio::tokio::future_into_py(py, async {
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

#[pyfunction]
pub fn new_calculator() -> Calculator {
    Calculator::new()
}
