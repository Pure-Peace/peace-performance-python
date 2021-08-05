use std::env;

use pyo3::{prelude::*, wrap_pyfunction};

#[pyfunction]
pub fn rust_sleep<'p>(py: Python<'p>, secs: u64) -> PyResult<&PyAny> {
    pyo3_asyncio::tokio::future_into_py(py, async move {
        sleep(secs).await;
        Ok(Python::with_gil(|py| py.None()))
    })
}

pub async fn sleep(secs: u64) {
    tokio::time::sleep(std::time::Duration::from_secs(secs)).await;
}

#[pyfunction]
pub fn set_log_level(log_level: &str) {
    let _ = env::set_var("RUST_LOG", log_level);
}

#[pyfunction]
pub fn init_logger() {
    pretty_env_logger::init();
}

#[pymodule]
pub fn functions(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(rust_sleep, m)?)?;
    m.add_function(wrap_pyfunction!(set_log_level, m)?)?;
    m.add_function(wrap_pyfunction!(init_logger, m)?)?;

    Ok(())
}
