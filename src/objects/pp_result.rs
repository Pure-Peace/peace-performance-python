use peace_performance::{PpResult, StarResult};
use pyo3::{
    prelude::{pyclass, pymethods},
    types::PyDict,
    PyResult, Python,
};

use crate::methods::common::osu_mode_int_str;

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

#[pymethods]
impl RawStars {
    #[getter]
    pub fn as_string(&self) -> String {
        format!(
            "stars: {:?}, max_combo: {:?}, ar: {:?}, 
            n_fruits: {:?}, n_droplets: {:?}, n_tiny_droplets: {:?}, 
            od: {:?}, speed_strain: {:?}, n_circles: {:?}, n_spinners: {:?}",
            self.stars,
            self.max_combo,
            self.ar,
            self.n_fruits,
            self.n_droplets,
            self.n_tiny_droplets,
            self.od,
            self.speed_strain,
            self.n_circles,
            self.n_spinners,
        )
    }

    #[getter]
    pub fn as_dict<'a>(&self, py: Python<'a>) -> PyResult<&'a PyDict> {
        let d = crate::pyo3_py_dict!(py, self; {
            stars,
            max_combo,
            ar,
            n_fruits,
            n_droplets,
            n_tiny_droplets,
            od,
            speed_strain,
            n_circles,
            n_spinners
        });
        Ok(d)
    }
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

#[pymethods]
impl RawPP {
    #[getter]
    pub fn as_string(&self) -> String {
        format!(
            "aim: {:?}, spd: {:?}, str: {:?}, 
            acc: {:?}, total: {:?}",
            self.aim, self.spd, self.str, self.acc, self.total
        )
    }

    #[getter]
    pub fn as_dict<'a>(&self, py: Python<'a>) -> PyResult<&'a PyDict> {
        let d = crate::pyo3_py_dict!(py, self; {
            aim,
            spd,
            str,
            acc,
            total
        });
        Ok(d)
    }
}

#[pyclass]
pub struct CalcResult(pub PpResult);
crate::pyo3_py_methods!(
    CalcResult, {mode: u8, mods: u32, pp: f32}; fn {stars: f32}; impl {
        #[getter]
        pub fn mode_str(&self) -> String {
            osu_mode_int_str(self.0.mode)
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
        pub fn raw_stars(&self) -> RawStars {
            match &self.0.attributes {
                StarResult::Fruits(attr) => RawStars {
                    stars: Some(attr.stars),
                    max_combo: Some(attr.max_combo),
                    ar: Some(attr.ar),
                    n_fruits: Some(attr.n_fruits),
                    n_droplets: Some(attr.n_droplets),
                    n_tiny_droplets: Some(attr.n_tiny_droplets),
                    ..Default::default()
                },
                StarResult::Mania(attr) => RawStars { stars: Some(attr.stars), ..Default::default() },
                StarResult::Osu(attr) => RawStars {
                    stars: Some(attr.stars),
                    ar: Some(attr.ar),
                    od: Some(attr.od),
                    speed_strain: Some(attr.speed_strain),
                    aim_strain: Some(attr.aim_strain),
                    max_combo: Some(attr.max_combo),
                    n_circles: Some(attr.n_circles),
                    n_spinners: Some(attr.n_spinners),
                    ..Default::default()
                },
                StarResult::Taiko(attr) => RawStars { stars: Some(attr.stars), ..Default::default() },
            }
        }

        #[getter]
        pub fn as_string(&self) -> String {
            format!(
                "mode: {}, mode_str: {}, mods: {}, pp: {}, stars: {}",
                self.0.mode,
                osu_mode_int_str(self.0.mode),
                self.0.mods,
                self.0.pp,
                self.0.stars(),
            )
        }

        #[getter]
        pub fn as_dict<'a>(&self, py: Python<'a>) -> PyResult<&'a PyDict> {
            let d = crate::pyo3_py_dict!(py, self.0; {
                mode,
                mods,
                pp
            }; fn self {mode_str, stars});
            d.set_item("raw_pp", self.raw_pp().as_dict(py)?)?;
            d.set_item("raw_stars", self.raw_stars().as_dict(py)?)?;
            Ok(d)
        }
    }
);
