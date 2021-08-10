use peace_performance::PpResult;
use pyo3::{PyResult, Python, prelude::{pyclass, pymethods}, types::PyDict};

use crate::{methods::pp, objects::Beatmap};
use super::CalcResult;

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

    #[getter]
    pub fn as_string(&self) -> String {
        format!(
            "mode: {:?}, mods: {:?}, n50: {:?}, n100: {:?}, n300: {:?}, katu: {:?}, 
                acc: {:?}, passed_obj: {:?}, combo: {:?}, miss: {:?}",
            self.mode,
            self.mods,
            self.n50,
            self.n100,
            self.n300,
            self.katu,
            self.acc,
            self.passed_obj,
            self.combo,
            self.miss,
        )
    }

    #[getter]
    pub fn as_dict<'a>(&self, py: Python<'a>) -> PyResult<&'a PyDict> {
        let d = crate::pyo3_py_dict!(py, self; {
            mode,
            mods,
            n50,
            n100,
            n300,
            katu,
            acc,
            passed_obj,
            combo,
            miss
        });
        Ok(d)
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
