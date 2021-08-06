use peace_performance::{PpResult, StarResult};
use pyo3::prelude::{pyclass, pymethods};

use crate::{methods::pp, objects::Beatmap};

#[pyclass]
#[derive(Default)]
pub struct RawStars {
    #[pyo3(get)]
    pub stars: Option<f32>,
    #[pyo3(get)]
    pub max_combo: Option<usize>,
    #[pyo3(get)]
    pub ar: Option<f32>,
    #[pyo3(get)]
    pub n_fruits: Option<usize>,
    #[pyo3(get)]
    pub n_droplets: Option<usize>,
    #[pyo3(get)]
    pub n_tiny_droplets: Option<usize>,
    #[pyo3(get)]
    pub od: Option<f32>,
    #[pyo3(get)]
    pub speed_strain: Option<f32>,
    #[pyo3(get)]
    pub aim_strain: Option<f32>,
    #[pyo3(get)]
    pub n_circles: Option<usize>,
    #[pyo3(get)]
    pub n_spinners: Option<usize>,
}

#[pyclass]
pub struct RawPP {
    #[pyo3(get)]
    pub aim: Option<f32>,
    #[pyo3(get)]
    pub spd: Option<f32>,
    #[pyo3(get)]
    pub str: Option<f32>,
    #[pyo3(get)]
    pub acc: Option<f32>,
    #[pyo3(get)]
    pub total: f32,
}

#[pyclass]
pub struct CalcResult(pub PpResult);

#[pymethods]
impl CalcResult {
    #[getter]
    pub fn mode(&self) -> u8 {
        self.0.mode
    }

    #[getter]
    pub fn mods(&self) -> u32 {
        self.0.mods
    }

    #[getter]
    pub fn pp(&self) -> f32 {
        self.0.pp
    }

    #[getter]
    pub fn raw_pp(&self) -> RawPP {
        RawPP {
            aim: self.0.raw.aim,
            spd: self.0.raw.spd,
            str: self.0.raw.str,
            acc: self.0.raw.acc,
            total: self.0.raw.total,
        }
    }

    #[getter]
    pub fn stars(&self) -> f32 {
        self.0.stars()
    }

    #[getter]
    pub fn raw_stars(&self) -> RawStars {
        let mut raw = RawStars::default();
        match &self.0.attributes {
            StarResult::Fruits(attr) => {
                raw.stars = Some(attr.stars);
                raw.max_combo = Some(attr.max_combo);
                raw.ar = Some(attr.ar);
                raw.n_fruits = Some(attr.n_fruits);
                raw.n_droplets = Some(attr.n_droplets);
                raw.n_tiny_droplets = Some(attr.n_tiny_droplets);
            }
            StarResult::Mania(attr) => raw.stars = Some(attr.stars),
            StarResult::Osu(attr) => {
                raw.stars = Some(attr.stars);
                raw.ar = Some(attr.ar);
                raw.od = Some(attr.od);
                raw.speed_strain = Some(attr.speed_strain);
                raw.aim_strain = Some(attr.aim_strain);
                raw.max_combo = Some(attr.max_combo);
                raw.n_circles = Some(attr.n_circles);
                raw.n_spinners = Some(attr.n_spinners);
            }
            StarResult::Taiko(attr) => raw.stars = Some(attr.stars),
        };
        raw
    }
}

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
}

#[pymethods]
impl Calculator {
    #[new]
    pub fn new() -> Self {
        Self::default()
    }

    #[inline(always)]
    pub fn calculate(&self, beatmap: &Beatmap) -> CalcResult {
        CalcResult(self.calc(beatmap))
    }

    #[inline(always)]
    pub fn reset(&mut self) {
        self.mode = None;
        self.mods = None;
        self.n50 = None;
        self.n100 = None;
        self.n300 = None;
        self.katu = None;
        self.acc = None;
        self.passed_obj = None;
        self.combo = None;
        self.miss = None;
    }
}

impl Calculator {
    #[inline(always)]
    #[timed::timed(duration(printer = "trace!"))]
    pub fn calc(&self, beatmap: &Beatmap) -> PpResult {
        let c = pp::mode_any_pp(self.mode.unwrap_or(4), &beatmap.0);
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
        pp::calc_with_any_pp(&mut c)
    }
}
