use pyo3::{
    prelude::{pyclass, pymethods},
    types::PyDict,
    PyAny, PyCell, PyResult, Python,
};
use rosu_pp::PerformanceAttributes;

use super::CalcResult;
use crate::{
    methods::pp::{self, PpRaw, PpResult},
    objects::Beatmap,
    set_calculator,
};

macro_rules! create_py_methods {
    ($for:ident, fn get_set_del() {$($attr:ident: $type:ty),*}, impl {$($others:tt)*}) => {
        paste::paste! {
            #[pymethods] impl $for {
                #[new]
                #[args(data = "None", kwargs = "**")]
                pub fn new(data: Option<&PyDict>, kwargs: Option<&PyDict>) -> PyResult<Self> {
                    let mut slf = Self::default();
                    if let Some(d) = data.or(kwargs) {
                        Self::set_with_dict(&mut slf, d)?;
                    }
                    Ok(slf)
                }

                pub fn getattr<'a>(slf: &'a PyCell<Self>, attr: &PyAny) -> PyResult<&'a PyAny> {
                    slf.as_ref().getattr(attr)
                }

                pub fn setattr<'a>(slf: &PyCell<Self>, attr: &PyAny, value: &PyAny) -> PyResult<()> {
                    slf.as_ref().setattr(attr, value)
                }

                $(
                    pub fn [<r#get_ $attr>](&self) -> $type { self.$attr }
                    pub fn [<r#set_ $attr>](&mut self, value: $type) { self.$attr = value; }
                    pub fn [<r#del_ $attr>](&mut self) { self.$attr = None; }
                )*

                $($others)*
            }
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
    pub acc: Option<f64>,
    #[pyo3(get, set)]
    pub passed_obj: Option<usize>,
    #[pyo3(get, set)]
    pub combo: Option<usize>,
    #[pyo3(get, set)]
    pub miss: Option<usize>,
    #[pyo3(get, set)]
    pub score: Option<u32>,
}
create_py_methods!(
    Calculator,
    fn get_set_del() {
        mode: Option<u8>,
        mods: Option<u32>,
        n50: Option<usize>,
        n100: Option<usize>,
        n300: Option<usize>,
        katu: Option<usize>,
        acc: Option<f64>,
        passed_obj: Option<usize>,
        combo: Option<usize>,
        miss: Option<usize>,
        score: Option<u32>
    },
    impl {
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
);

impl Calculator {
    #[inline(always)]
    #[cfg_attr(feature = "rust_logger", timed::timed(duration(printer = "trace!")))]
    pub fn calc(&self, beatmap: &Beatmap) -> PpResult {
        let c = pp::mode_any_pp(self.mode, &beatmap.0);

        let c = set_calculator!(c, self.mods, self.combo, self.n50, self.n100, self.n300, {
            self.katu: n_katu,
            self.miss: misses,
            self.passed_obj: passed_objects
        });
        let c = set_calculator!(c, self.score, { self.acc: accuracy });

        let attributes = c.calculate();
        let (mode, raw) = match &attributes {
            PerformanceAttributes::Osu(attr) => (
                0,
                PpRaw::new(
                    Some(attr.pp_aim),
                    Some(attr.pp_speed),
                    None,
                    Some(attr.pp_acc),
                    attr.pp,
                ),
            ),
            PerformanceAttributes::Taiko(attr) => (
                1,
                PpRaw::new(None, None, Some(attr.pp_strain), Some(attr.pp_acc), attr.pp),
            ),
            PerformanceAttributes::Catch(attr) => {
                (2, PpRaw::new(Some(attr.pp), None, None, None, attr.pp))
            }
            PerformanceAttributes::Mania(attr) => (
                3,
                PpRaw::new(None, None, Some(attr.pp_strain), Some(attr.pp_acc), attr.pp),
            ),
        };
        PpResult {
            mode,
            mods: self.mods.unwrap_or(0),
            pp: attributes.pp(),
            raw,
            attributes,
        }
    }
}
