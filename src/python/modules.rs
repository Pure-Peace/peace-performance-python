use pyo3::{prelude::pymodule, types::PyModule, wrap_pyfunction, wrap_pymodule, PyResult, Python};

use crate::python::functions::*;

#[pymodule]
pub fn common(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(rust_sleep, m)?)?;
    m.add_function(wrap_pyfunction!(set_log_level, m)?)?;
    m.add_function(wrap_pyfunction!(init_logger, m)?)?;

    Ok(())
}

#[pymodule]
pub fn pp(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(read_beatmap, m)?)?;
    Ok(())
}

#[pymodule]
fn _peace_performance(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pymodule!(common))?;
    m.add_wrapped(wrap_pymodule!(pp))?;
    Ok(())
}
