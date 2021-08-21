use pyo3::{
    prelude::pymodule,
    types::{PyDict, PyModule},
    PyResult, Python,
};

use crate::python::functions::*;
use crate::{
    objects::*, pyo3_add_classes, pyo3_add_functions, pyo3_add_modules, pyo3_set_sys_modules,
};

#[pymodule]
pub fn common(_py: Python, m: &PyModule) -> PyResult<()> {
    pyo3_add_functions!(m; {rust_sleep, set_log_level, init_logger, osu_mode_int_str, osu_mode_str_int});
    Ok(())
}

#[pymodule]
pub fn pp(_py: Python, m: &PyModule) -> PyResult<()> {
    pyo3_add_functions!(m; {new_calculator});
    pyo3_add_classes!(m; {Calculator, CalcResult, RawPP, RawStars});
    Ok(())
}

#[pymodule]
pub fn beatmap(_py: Python, m: &PyModule) -> PyResult<()> {
    pyo3_add_functions!(m; {read_beatmap_async, read_beatmap_sync});
    pyo3_add_classes!(m; {
        Beatmap,
        DifficultyPoint,
        TimingPoint,
        Pos2,
        HitObject,
        HitObjectKind
    });
    Ok(())
}

#[pymodule]
fn _peace_performance(py: Python, m: &PyModule) -> PyResult<()> {
    pyo3_add_modules!(m; {common, pp, beatmap});
    // Inserting to sys.modules allows importing submodules nicely from Python
    // e.g. from peace_performance_python._peace_performance.xxx import xxx
    pyo3_set_sys_modules!(m, py; {"common", "pp", "beatmap"});
    Ok(())
}
