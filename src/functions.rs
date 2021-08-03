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

#[pymodule]
pub fn functions(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(rust_sleep, m)?)?;

    Ok(())
}
