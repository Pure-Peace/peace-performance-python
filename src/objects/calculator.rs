use peace_performance::PpResult;
use pyo3::prelude::{pyclass, pymethods};

use crate::{methods::pp, objects::Beatmap};

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
    #[inline(always)]
    pub fn calculate(&self, beatmap: &Beatmap) -> CalcResult {
        CalcResult(self.calc(beatmap))
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
