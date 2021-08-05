use std::path::PathBuf;

use pyo3::{create_exception, exceptions::PyException, prelude::*, wrap_pyfunction};
use tokio::fs::File;

use peace_performance::{AnyPP, Beatmap, FruitsPP, ManiaPP, OsuPP, TaikoPP};

create_exception!(peace_performance, ParseBeatmapError, PyException);
create_exception!(peace_performance, ReadFileError, PyException);

#[pyclass]
pub struct Wrapper {
    #[pyo3(get, set)]
    pub hello: String,
}

#[pymethods]
impl Wrapper {
    #[new]
    pub fn init(hello: String) -> Self {
        Self { hello }
    }

    pub fn print(&self, e: u32, f: String) {
        log::info!("{} {} {}", self.hello, e, f)
    }
}

/// Read .osu file
#[timed::timed(duration(printer = "debug!"))]
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
#[timed::timed(duration(printer = "debug!"))]
pub async fn parse_beatmap(file: File) -> PyResult<Beatmap> {
    match Beatmap::parse(file).await {
        Ok(beatmap) => Ok(beatmap),
        Err(err) => Err(ParseBeatmapError::new_err(format!(
            "Could not parse beatmap: {}",
            err
        ))),
    }
}

#[inline(always)]
pub fn mode_calculator(mode: u8, beatmap: &Beatmap) -> AnyPP {
    match mode {
        0 => AnyPP::Osu(OsuPP::new(beatmap)),
        1 => AnyPP::Taiko(TaikoPP::new(beatmap)),
        2 => AnyPP::Fruits(FruitsPP::new(beatmap)),
        3 => AnyPP::Mania(ManiaPP::new(beatmap)),
        _ => AnyPP::new(beatmap),
    }
}

pub async fn calc_pp() {}

#[pyfunction]
pub fn read_beatmap<'p>(py: Python<'p>, path: PathBuf) -> PyResult<&PyAny> {
    pyo3_asyncio::tokio::future_into_py(py, async {
        let file = read_file(path).await?;
        let beatmap = parse_beatmap(file).await?;
        let mut calculator = mode_calculator(4, &beatmap);
        calculator.calculate().await;
        Python::with_gil(|py| Ok(py.None()))
    })
}

#[pymodule]
pub fn wrapper(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(read_beatmap, m)?)?;
    m.add_class::<Wrapper>()?;
    Ok(())
}
