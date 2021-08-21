use peace_performance::PpResult;
use pyo3::{
    prelude::{pyclass, pymethods, pyproto},
    types::PyDict,
    PyAny, PyCell, PyObjectProtocol, PyResult, Python,
};

use super::CalcResult;
use crate::{methods::pp, objects::Beatmap, set_calculator};

macro_rules! generate_func {
    ({$($attr:ident: $type:ty),*}) => {
        paste::paste! {
            $(
                pub fn [<get_ $attr>](&self) -> $type { self.$attr }
                pub fn [<set_ $attr>](&mut self, value: $type) { self.$attr = value; }
                pub fn [<del_ $attr>](&mut self) { self.$attr = None; }
            )*
        }
    };
}

#[pyclass(subclass)]
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
    pub score: Option<u32>,
}
crate::pyo3_py_protocol!(Calculator);

#[pymethods]
impl Calculator {
    generate_func!({
        mode: Option<u8>,
        mods: Option<u32>,
        n50: Option<usize>,
        n100: Option<usize>,
        n300: Option<usize>,
        katu: Option<usize>,
        acc: Option<f32>,
        passed_obj: Option<usize>,
        combo: Option<usize>,
        miss: Option<usize>,
        score: Option<u32>
    });

    #[new]
    #[args(data = "None", kwargs = "**")]
    pub fn new(data: Option<&PyDict>, kwargs: Option<&PyDict>) -> PyResult<Self> {
        let mut slf = Self::default();
        if let Some(d) = data.or(kwargs) {
            Self::set_with_dict(&mut slf, d)?;
        }
        Ok(slf)
    }

    #[staticmethod]
    pub fn new_empty() -> Self {
        Self::default()
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
        self.score = None;
    }

    #[inline(always)]
    pub fn calculate_raw(&self, beatmap: &Beatmap) -> CalcResult {
        CalcResult(self.calc(beatmap))
    }

    pub fn getattr<'a>(slf: &'a PyCell<Self>, attr: &PyAny) -> PyResult<&'a PyAny> {
        slf.as_ref().getattr(attr)
    }

    pub fn setattr<'a>(slf: &PyCell<Self>, attr: &PyAny, value: &PyAny) -> PyResult<()> {
        slf.as_ref().setattr(attr, value)
    }

    #[inline(always)]
    pub fn set_with_str(&mut self, attr: &str, value: &PyAny) -> PyResult<()> {
        crate::set_with_py_str!(self, attr, value; {
            mode,
            mods,
            n50,
            n100,
            n300,
            katu,
            acc,
            passed_obj,
            combo,
            miss,
            score
        });
        Ok(())
    }

    #[inline(always)]
    pub fn set_with_dict(&mut self, data: &PyDict) -> PyResult<()> {
        for (k, v) in data.iter() {
            self.set_with_str(&k.extract::<String>()?, v)?;
        }
        Ok(())
    }

    #[getter]
    pub fn attrs(&self) -> String {
        self.as_string()
    }

    #[getter]
    pub fn attrs_dict<'a>(&self, py: Python<'a>) -> PyResult<&'a PyDict> {
        self.as_dict(py)
    }

    #[getter]
    #[inline(always)]
    pub fn as_string(&self) -> String {
        format!(
            "mode: {:?}, mods: {:?}, n50: {:?}, n100: {:?}, n300: {:?}, katu: {:?}, acc: {:?}, passed_obj: {:?}, combo: {:?}, miss: {:?}, score: {:?}",
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
            self.score,
        )
    }

    #[getter]
    #[inline(always)]
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
            miss,
            score
        });
        Ok(d)
    }
}

impl Calculator {
    #[inline(always)]
    #[cfg_attr(feature = "rust_logger", timed::timed(duration(printer = "trace!")))]
    pub fn calc(&self, beatmap: &Beatmap) -> PpResult {
        let c = pp::mode_any_pp(self.mode.unwrap_or(4), &beatmap.0);
        let c = set_calculator!(self.mods, c);
        // Irrelevant for osu!mania
        let c = set_calculator!(self.combo, c);
        // Irrelevant for osu!mania and osu!taiko
        let c = set_calculator!(self.n50, c);
        // Irrelevant for osu!mania
        let c = set_calculator!(self.n100, c);
        // Irrelevant for osu!mania
        let c = set_calculator!(self.n300, c);
        // Only relevant for osu!ctb
        let c = set_calculator!(self.katu, n_katu, c);
        // Irrelevant for osu!mania
        let c = set_calculator!(self.miss, misses, c);
        let c = set_calculator!(self.passed_obj, passed_objects, c);
        // Only relevant for osu!mania
        let mut c = set_calculator!(self.score, c);
        // Irrelevant for osu!mania
        if let Some(acc) = self.acc {
            c.set_accuracy(acc)
        };
        pp::calc_with_any_pp(&mut c)
    }
}
