use peace_performance::{PpResult, StarResult};
use pyo3::prelude::{pyclass, pymethods};

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

crate::pyo3_getters_generator!(
    CalcResult, {
        mode: u8,
        mods: u32,
        pp: f32
    }; fn {
        stars: f32
    }; impl {
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
);
