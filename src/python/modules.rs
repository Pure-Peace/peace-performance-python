use pyo3::{prelude::pymodule, types::PyModule, wrap_pyfunction, wrap_pymodule, PyResult, Python};

use crate::objects::*;
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
    m.add_function(wrap_pyfunction!(new_calculator, m)?)?;

    // Objects -----
    m.add_class::<Calculator>()?;
    m.add_class::<CalcResult>()?;
    m.add_class::<RawPP>()?;
    m.add_class::<RawStars>()?;
    Ok(())
}

#[pymodule]
pub fn beatmap(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(read_beatmap_async, m)?)?;
    m.add_function(wrap_pyfunction!(read_beatmap_sync, m)?)?;

    // Objects -----
    m.add_class::<Beatmap>()?;
    m.add_class::<DifficultyPoint>()?;
    m.add_class::<TimingPoint>()?;
    m.add_class::<Pos2>()?;
    m.add_class::<HitObject>()?;
    m.add_class::<HitObjectKind>()?;
    Ok(())
}

#[pymodule]
fn _peace_performance(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pymodule!(common))?;
    m.add_wrapped(wrap_pymodule!(pp))?;
    m.add_wrapped(wrap_pymodule!(beatmap))?;
    Ok(())
}
