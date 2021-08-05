use std::{collections::HashMap, path::PathBuf};

use pyo3::{create_exception, exceptions::PyException, prelude::*, wrap_pyfunction};
use tokio::fs::File;

use peace_performance::{
    AnyPP, Beatmap as RawBeatmap, FruitsPP, ManiaPP, OsuPP, PpResult, TaikoPP,
};

create_exception!(peace_performance, ParseBeatmapError, PyException);
create_exception!(peace_performance, ReadFileError, PyException);

#[pyclass]
#[derive(Clone)]
pub struct Beatmap(pub RawBeatmap);

#[pyclass]
pub struct CalcResult(pub PpResult);

#[pyclass]
#[derive(Debug, Default, Clone)]
pub struct Calculator {
    #[pyo3(get, set)]
    pub mode: Option<u8>,
    #[pyo3(get, set)]
    pub mods: Option<u32>,
    #[pyo3(get, set)]
    pub n50: Option<usize>,
    #[pyo3(get, set)]
    pub n100: Option<usize>,
    #[pyo3(get, set)]
    pub n300: Option<usize>,
    #[pyo3(get, set)]
    pub katu: Option<usize>,
    #[pyo3(get, set)]
    pub acc: Option<f32>,
    #[pyo3(get, set)]
    pub passed_obj: Option<usize>,
    #[pyo3(get, set)]
    pub combo: Option<usize>,
    #[pyo3(get, set)]
    pub miss: Option<usize>,
    #[pyo3(get, set)]
    pub simple: Option<i32>,
    #[pyo3(get, set)]
    pub acc_list: Option<i32>,
    #[pyo3(get, set)]
    pub no_miss: Option<i32>,
}

#[pymethods]
impl Calculator {
    pub fn calculate(&self, beatmap: &Beatmap) -> CalcResult {
        CalcResult(self.calc(beatmap))
    }
}

impl Calculator {
    #[inline(always)]
    pub fn calc(&self, beatmap: &Beatmap) -> PpResult {
        let c = mode_any_pp(self.mode.unwrap_or(4), &beatmap.0);
        let c = match self.mods {
            Some(mods) => c.mods(mods),
            None => c,
        };
        let c = match self.combo {
            Some(combo) => c.combo(combo),
            None => c,
        };
        let c = match self.n50 {
            Some(n50) => c.n50(n50),
            None => c,
        };
        let c = match self.n100 {
            Some(n100) => c.n100(n100),
            None => c,
        };
        let c = match self.n300 {
            Some(n300) => c.n300(n300),
            None => c,
        };
        let c = match self.katu {
            Some(katu) => c.n_katu(katu),
            None => c,
        };
        let c = match self.miss {
            Some(miss) => c.misses(miss),
            None => c,
        };
        let mut c = match self.passed_obj {
            Some(passed_obj) => c.passed_objects(passed_obj),
            None => c,
        };
        if let Some(acc) = self.acc {
            c.set_accuracy(acc)
        };
        calc(&mut c)
    }
}

#[inline(always)]
pub fn calc(any_pp: &mut AnyPP) -> PpResult {
    match any_pp {
        AnyPP::Fruits(f) => f.calculate(),
        AnyPP::Mania(m) => m.calculate(),
        AnyPP::Osu(o) => o.calculate(),
        AnyPP::Taiko(t) => t.calculate(),
    }
}

#[inline(always)]
pub fn calculate_acc_list(
    beatmap: &RawBeatmap,
    mode: Option<u8>,
    mods: Option<u32>,
) -> HashMap<String, f32> {
    let c = mode_any_pp(mode.unwrap_or(4), &beatmap);
    let mut c = match mods {
        Some(mods) => c.mods(mods),
        None => c,
    };

    let mut map = HashMap::new();
    for acc in [100.0, 99.0, 98.0, 95.0] {
        c.set_accuracy(acc);
        map.insert((acc as i32).to_string(), calc(&mut c).pp());
    }
    map
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
pub async fn parse_beatmap(file: File) -> PyResult<RawBeatmap> {
    match RawBeatmap::parse(file).await {
        Ok(beatmap) => Ok(beatmap),
        Err(err) => Err(ParseBeatmapError::new_err(format!(
            "Could not parse beatmap: {}",
            err
        ))),
    }
}

#[inline(always)]
pub fn mode_any_pp(mode: u8, beatmap: &RawBeatmap) -> AnyPP {
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
pub fn read_beatmap(py: Python, path: PathBuf) -> PyResult<&PyAny> {
    pyo3_asyncio::tokio::future_into_py(py, async {
        let file = read_file(path).await?;
        let beatmap = parse_beatmap(file).await?;
        Python::with_gil(|py| Ok(Beatmap(beatmap).into_py(py)))
    })
}

#[pymodule]
pub fn wrapper(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(read_beatmap, m)?)?;
    Ok(())
}
