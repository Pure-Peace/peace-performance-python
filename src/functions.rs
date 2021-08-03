use pyo3::{prelude::*, wrap_pyfunction};

#[pyfunction]
pub fn rust_sleep(py: Python) -> PyResult<PyObject> {
    pyo3_asyncio::tokio::into_coroutine(py, async {
        tokio::time::sleep(std::time::Duration::from_secs(1)).await;
        Ok(Python::with_gil(|py| py.None()))
    })
}

#[pymodule]
pub fn functions(py: Python, m: &PyModule) -> PyResult<()> {
    pyo3_asyncio::try_init(py)?;
    // Tokio needs explicit initialization before any pyo3-asyncio conversions.
    // The module import is a prime place to do this.
    pyo3_asyncio::tokio::init_multi_thread_once();

    m.add_function(wrap_pyfunction!(rust_sleep, m)?)?;

    Ok(())
}
