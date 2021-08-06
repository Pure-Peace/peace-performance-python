use peace_performance::Beatmap as RawBeatmap;
use pyo3::prelude::pyclass;

#[pyclass]
#[derive(Clone)]
pub struct Beatmap(pub RawBeatmap);
