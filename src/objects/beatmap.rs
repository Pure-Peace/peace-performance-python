use std::ops::{Add, AddAssign, Div, Mul, Sub};

use peace_performance::{
    parse::{
        DifficultyPoint as RawDifficultyPoint, HitObject as RawHitObject,
        HitObjectKind as RawHitObjectKind, PathType, Pos2 as RawPos2,
        TimingPoint as RawTimingPoint,
    },
    Beatmap as RawBeatmap, GameMode,
};
use pyo3::prelude::{pyclass, pymethods};

#[pyclass]
#[derive(Clone, Default, Debug)]
pub struct Beatmap(pub RawBeatmap);

crate::pyo3_getters_generator!(
    Beatmap, {
        version: u8,
        n_circles: u32,
        n_sliders: u32,
        n_spinners: u32,
        ar: f32,
        od: f32,
        cs: f32,
        hp: f32,
        sv: f32,
        tick_rate: f32
    }, impl {
        #[getter]
        pub fn mode(&self) -> u8 {
            self.0.mode as u8
        }

        #[getter]
        pub fn mode_str(&self) -> String {
            match self.0.mode {
                GameMode::STD => "std",
                GameMode::TKO => "taiko",
                GameMode::CTB => "ctb",
                GameMode::MNA => "mania",
            }.into()
        }

        #[getter]
        pub fn hit_objects(&self) -> Vec<HitObject> {
            self.0
                .hit_objects
                .iter()
                .map(|obj| HitObject(obj.clone()))
                .collect()
        }

        #[cfg(any(feature = "osu", feature = "fruits"))]
        #[getter]
        pub fn timing_points(&self) -> Vec<TimingPoint> {
            self.0
                .timing_points
                .iter()
                .map(|obj| TimingPoint(obj.clone()))
                .collect()
        }

        #[cfg(any(feature = "osu", feature = "fruits"))]
        #[getter]
        pub fn difficulty_points(&self) -> Vec<DifficultyPoint> {
            self.0
                .difficulty_points
                .iter()
                .map(|obj| DifficultyPoint(obj.clone()))
                .collect()
        }

        #[cfg(all(feature = "osu", feature = "all_included"))]
        #[getter]
        pub fn stack_leniency(&self) -> f32 {
            self.0.stack_leniency
        }
    }
);

#[cfg(any(feature = "osu", feature = "fruits"))]
#[pyclass]
#[derive(Clone, Debug)]
pub struct DifficultyPoint(pub RawDifficultyPoint);

#[cfg(any(feature = "osu", feature = "fruits"))]
crate::pyo3_getters_generator!(DifficultyPoint, {time: f32, speed_multiplier: f32});

#[pyclass]
#[derive(Clone, Debug)]
pub struct TimingPoint(pub RawTimingPoint);

crate::pyo3_getters_generator!(TimingPoint, {time: f32, beat_len: f32});

#[pyclass]
#[derive(Clone, Default, Debug)]
pub struct Pos2(pub RawPos2);

crate::pyo3_getters_generator!(Pos2, {x: f32, y: f32}; fn {
    length_squared: f32,
    length: f32
}; impl {
    pub fn dot(&self, other: Self) -> f32 {
        self.0.dot(other.0)
    }

    pub fn distance(&self, other: Self) -> f32 {
        self.0.distance(other.0)
    }

    pub fn normalize(&self) -> Self {
        Self(self.0.normalize())
    }

    pub fn add(&self, other: Self) -> Self {
        Self(self.0.add(other.0))
    }

    pub fn sub(&self, rhs: Self) -> Self {
        Self(self.0.sub(rhs.0))
    }

    pub fn mul(&self, rhs: f32) -> Self {
        Self(self.0.mul(rhs))
    }

    pub fn div(&self, rhs: f32) -> Self {
        Self(self.0.div(rhs))
    }

    pub fn add_assign(&mut self, other: Self) {
        self.0.add_assign(other.0)
    }

    #[getter]
    pub fn as_string(&self) -> String {
        format!("({}, {})", self.0.x, self.0.y)
    }
});

#[pyclass]
#[derive(Clone, Default, Debug)]
pub struct HitObjectKind {
    pub kind: String,
    pub pixel_len: Option<f32>,
    pub repeats: Option<usize>,
    pub curve_points: Option<Vec<Pos2>>,
    pub path_type: Option<String>,
    pub end_time: Option<f32>,
}

#[pyclass]
#[derive(Clone, Debug)]
pub struct HitObject(pub RawHitObject);

crate::pyo3_getters_generator!(HitObject, {start_time: f32, sound: u8}; fn {
    end_time: f32,
    is_circle: bool,
    is_slider: bool,
    is_spinner: bool
}; impl {
    #[getter]
    pub fn pos(&self) -> Pos2 {
        Pos2(self.0.pos)
    }

    #[getter]
    pub fn kind(&self) -> HitObjectKind {
        match &self.0.kind {
            RawHitObjectKind::Circle => HitObjectKind { kind: "circle".into(), ..Default::default() },
            #[cfg(any(
                feature = "fruits",
                all(feature = "osu", not(feature = "no_sliders_no_leniency"))
            ))]
            RawHitObjectKind::Slider { pixel_len, repeats, curve_points, path_type } =>
                HitObjectKind {
                    kind: "slider".into(),
                    pixel_len: Some(*pixel_len),
                    repeats: Some(*repeats),
                    curve_points: Some(curve_points.iter().map(|obj| Pos2(obj.clone())).collect()),
                    path_type: Some(match path_type {
                        PathType::Catmull => "catmull",
                        PathType::Bezier => "bezier",
                        PathType::Linear => "linear",
                        PathType::PerfectCurve => "perfect_curve",
                    }.into()),
                    ..Default::default()
                },
            #[cfg(not(any(
                feature = "fruits",
                all(feature = "osu", not(feature = "no_sliders_no_leniency"))
            )))]
            RawHitObjectKind::Slider { pixel_len, repeats } => HitObjectKind {
                pixel_len: Some(*pixel_len),
                repeats: Some(*repeats),
                ..Default::default()
            },
            RawHitObjectKind::Spinner { end_time } => HitObjectKind {
                end_time: Some(*end_time),
                ..Default::default()
            },
            RawHitObjectKind::Hold { end_time } => HitObjectKind {
                end_time: Some(*end_time),
                ..Default::default()
            },
        }
    }
});
