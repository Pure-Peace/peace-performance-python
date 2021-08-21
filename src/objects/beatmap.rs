use std::ops::{Add, AddAssign, Div, Mul, Sub};

use peace_performance::{
    parse::{
        DifficultyPoint as RawDifficultyPoint, HitObject as RawHitObject,
        HitObjectKind as RawHitObjectKind, PathType, Pos2 as RawPos2,
        TimingPoint as RawTimingPoint,
    },
    Beatmap as RawBeatmap,
};
use pyo3::{
    prelude::{pyclass, pymethods, pyproto},
    types::PyDict,
    PyObjectProtocol, PyResult, Python,
};

use crate::methods::common::osu_mode_str;

#[pyclass]
#[derive(Clone, Default, Debug)]
pub struct Beatmap(pub RawBeatmap);
crate::pyo3_py_protocol!(Beatmap);
crate::pyo3_py_methods!(
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
            osu_mode_str(&self.0.mode)
        }

        #[getter]
        pub fn hit_objects(&self) -> Option<Vec<HitObject>> {
            Some(self.0
                .hit_objects
                .iter()
                .map(|obj| HitObject(obj.clone()))
                .collect())
        }

        #[cfg(any(feature = "osu", feature = "fruits"))]
        #[getter]
        pub fn timing_points(&self) -> Option<Vec<TimingPoint>> {
            Some(self.0
                .timing_points
                .iter()
                .map(|obj| TimingPoint(obj.clone()))
                .collect())
        }

        #[cfg(not(any(feature = "osu", feature = "fruits")))]
        #[getter]
        pub fn timing_points(&self) -> Option<Vec<TimingPoint>> {
            None
        }

        #[cfg(any(feature = "osu", feature = "fruits"))]
        #[getter]
        pub fn difficulty_points(&self) -> Option<Vec<DifficultyPoint>> {
            Some(self.0
                .difficulty_points
                .iter()
                .map(|obj| DifficultyPoint(obj.clone()))
                .collect())
        }

        #[cfg(not(any(feature = "osu", feature = "fruits")))]
        #[getter]
        pub fn difficulty_points(&self) -> Option<Vec<DifficultyPoint>> {
            None
        }

        #[cfg(all(feature = "osu", feature = "all_included"))]
        #[getter]
        pub fn stack_leniency(&self) -> Option<f32> {
            Some(self.0.stack_leniency)
        }

        #[cfg(not(all(feature = "osu", feature = "all_included")))]
        #[getter]
        pub fn stack_leniency(&self) -> Option<f32> {
            None
        }

        #[getter]
        #[inline(always)]
        pub fn as_string(&self) -> String {
            format!(
                "mode: {}, mode_str: {}, version: {}, n_circles: {}, n_sliders: {}, n_spinners: {}, ar: {}, od: {}, cs: {},  hp: {}, sv: {}, tick_rate: {}, stack_leniency: {:?}, hit_objects: (...), timing_points: (...), difficulty_points: (...)",
                self.0.mode as u8,
                self.mode_str(),
                self.0.version,
                self.0.n_circles,
                self.0.n_sliders,
                self.0.n_spinners,
                self.0.ar,
                self.0.od,
                self.0.cs,
                self.0.hp,
                self.0.sv,
                self.0.tick_rate,
                self.stack_leniency()
            )
        }

        #[getter]
        #[inline(always)]
        pub fn as_dict<'a>(&self, py: Python<'a>) -> PyResult<&'a PyDict> {
            let d = crate::pyo3_py_dict!(py, self.0; {
                version, n_circles, n_sliders, n_spinners, ar, od, cs, hp, sv, tick_rate
            }; fn self {mode_str, stack_leniency});
            d.set_item("mode", self.0.mode as u8)?;
            Ok(d)
        }
    }
);

#[cfg(any(feature = "osu", feature = "fruits"))]
#[pyclass]
#[derive(Clone, Debug)]
pub struct DifficultyPoint(pub RawDifficultyPoint);
#[cfg(any(feature = "osu", feature = "fruits"))]
crate::pyo3_py_protocol!(DifficultyPoint);
#[cfg(any(feature = "osu", feature = "fruits"))]
crate::pyo3_py_methods!(DifficultyPoint, {time: f32, speed_multiplier: f32}, impl {
    #[getter]
    #[inline(always)]
    pub fn as_string(&self) -> String {
        format!("time: {}, speed_multiplier: {}", self.0.time, self.0.speed_multiplier)
    }

    #[getter]
    #[inline(always)]
    pub fn as_dict<'a>(&self, py: Python<'a>) -> PyResult<&'a PyDict> {
        let d = crate::pyo3_py_dict!(py, self.0; {time, speed_multiplier});
        Ok(d)
    }
});

#[pyclass]
#[derive(Clone, Debug)]
pub struct TimingPoint(pub RawTimingPoint);
crate::pyo3_py_protocol!(TimingPoint);
crate::pyo3_py_methods!(TimingPoint, {time: f32, beat_len: f32}, impl {
    #[getter]
    #[inline(always)]
    pub fn as_string(&self) -> String {
        format!("time: {}, beat_len: {}", self.0.time, self.0.beat_len)
    }

    #[getter]
    #[inline(always)]
    pub fn as_dict<'a>(&self, py: Python<'a>) -> PyResult<&'a PyDict> {
        let d = crate::pyo3_py_dict!(py, self.0; {time, beat_len});
        Ok(d)
    }
});

#[pyclass]
#[derive(Clone, Default, Debug)]
pub struct Pos2(pub RawPos2);
crate::pyo3_py_protocol!(Pos2);
crate::pyo3_py_methods!(Pos2, {x: f32, y: f32}; fn {
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
    #[inline(always)]
    pub fn as_string(&self) -> String {
        format!("x: {}, y: {}", self.0.x, self.0.y)
    }

    #[getter]
    #[inline(always)]
    pub fn as_dict<'a>(&self, py: Python<'a>) -> PyResult<&'a PyDict> {
        let d = crate::pyo3_py_dict!(py, self.0; {x, y});
        Ok(d)
    }

    #[getter]
    #[inline(always)]
    pub fn as_tuple(&self) -> (f32, f32) {
        (self.0.x, self.0.y)
    }
});

#[pyclass]
#[derive(Clone, Default, Debug)]
pub struct HitObjectKind {
    #[pyo3(get)]
    pub kind: String,
    #[pyo3(get)]
    pub pixel_len: Option<f32>,
    #[pyo3(get)]
    pub repeats: Option<usize>,
    #[pyo3(get)]
    pub curve_points: Option<Vec<Pos2>>,
    #[pyo3(get)]
    pub path_type: Option<String>,
    #[pyo3(get)]
    pub end_time: Option<f32>,
}
crate::pyo3_py_protocol!(HitObjectKind);
crate::pyo3_py_methods!(HitObjectKind, impl {
    #[getter]
    #[inline(always)]
    pub fn as_string(&self) -> String {
        format!(
            "kind: {}, pixel_len: {:?}, repeats: {:?}, path_type: {:?}, end_time: {:?}",
            self.kind, self.pixel_len, self.repeats, self.path_type, self.end_time
        )
    }

    #[getter]
    #[inline(always)]
    pub fn as_dict<'a>(&self, py: Python<'a>) -> PyResult<&'a PyDict> {
        let d = crate::pyo3_py_dict!(py, self; {kind, pixel_len, repeats, path_type, end_time});
        d.set_item(
            "curve_points",
            self.curve_points.as_ref().map(|poss| {
                poss.iter()
                    .map(|pos| (pos.0.x, pos.0.y))
                    .collect::<Vec<(f32, f32)>>()
            }),
        )?;
        Ok(d)
    }
});

#[pyclass]
#[derive(Clone, Debug)]
pub struct HitObject(pub RawHitObject);
crate::pyo3_py_protocol!(HitObject);
crate::pyo3_py_methods!(HitObject, {start_time: f32, sound: u8}; fn {
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
    pub fn kind_str(&self) -> String {
        match &self.0.kind {
            RawHitObjectKind::Circle => "circle",
            RawHitObjectKind::Slider { .. } => "slider",
            RawHitObjectKind::Spinner { .. } => "spinner",
            RawHitObjectKind::Hold { .. } => "hold",
        }.into()
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
                kind: "slider".into(),
                pixel_len: Some(*pixel_len),
                repeats: Some(*repeats),
                ..Default::default()
            },
            RawHitObjectKind::Spinner { end_time } => HitObjectKind {
                kind: "spinner".into(),
                end_time: Some(*end_time),
                ..Default::default()
            },
            RawHitObjectKind::Hold { end_time } => HitObjectKind {
                kind: "hold".into(),
                end_time: Some(*end_time),
                ..Default::default()
            },
        }
    }

    #[getter]
    #[inline(always)]
    pub fn as_string(&self) -> String {
        format!("start_time: {}, sound: {}, end_time: {}, kind: {}, pos: ({}, {})",
            self.0.start_time,
            self.0.sound,
            self.end_time(),
            self.kind_str(),
            self.0.pos.x,
            self.0.pos.y
        )
    }

    #[getter]
    #[inline(always)]
    pub fn as_dict<'a>(&self, py: Python<'a>) -> PyResult<&'a PyDict> {
        let d = crate::pyo3_py_dict!(py, self.0; {start_time, sound}; fn self {
            end_time
        });
        d.set_item("kind", self.kind().as_dict(py)?)?;
        d.set_item("pos", (self.0.pos.x, self.0.pos.y))?;
        Ok(d)
    }
});
