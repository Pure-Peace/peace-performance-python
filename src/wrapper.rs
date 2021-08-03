use std::path::PathBuf;

use pyo3::{create_exception, exceptions::PyException, prelude::*, wrap_pyfunction};
use tokio::fs::File;

use peace_performance::Beatmap;

create_exception!(peace_performance, ParseBeatmapError, PyException);
create_exception!(peace_performance, ReadFileError, PyException);

/// Read .osu file
pub async fn read_file(path: PathBuf) -> PyResult<File> {
    match File::open(path).await {
        Ok(file) => Ok(file),
        Err(err) => Err(ReadFileError::new_err(format!(
            "Could not read file: {}",
            err
        ))),
    }
}

/// Parse the beatmap file asynchronously
pub async fn parse_beatmap(file: File) -> PyResult<Beatmap> {
    match Beatmap::parse(file).await {
        Ok(beatmap) => Ok(beatmap),
        Err(err) => Err(ParseBeatmapError::new_err(format!(
            "Could not parse beatmap: {}",
            err
        ))),
    }
}

#[pyfunction]
pub fn read_beatmap<'p>(py: Python<'p>, path: PathBuf) -> PyResult<&PyAny> {
    pyo3_asyncio::tokio::future_into_py(py, async {
        let file = read_file(path).await?;
        let beatmap = parse_beatmap(file).await?;
        Python::with_gil(|py| Ok(py.None()))
    })
}

#[pymodule]
pub fn wrapper(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(read_beatmap, m)?)?;

    Ok(())
}
