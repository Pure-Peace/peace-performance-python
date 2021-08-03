use pyo3::{prelude::*, types::PyDict, wrap_pymodule};

pub mod functions;

use functions::*;

#[pymodule]
fn _peace_performance(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pymodule!(functions))?;

    Ok(())
}
