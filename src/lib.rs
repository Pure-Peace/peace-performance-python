#[macro_use]
extern crate log;
use pyo3::{prelude::*, wrap_pymodule};

pub mod functions;
pub mod wrapper;

use functions::*;
use wrapper::*;

#[pymodule]
fn _peace_performance(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pymodule!(functions))?;
    m.add_wrapped(wrap_pymodule!(wrapper))?;
    Ok(())
}
