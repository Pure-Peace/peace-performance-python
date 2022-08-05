use rosu_pp::{
    AnyPP, Beatmap as RawBeatmap, CatchPP, ManiaPP, OsuPP, TaikoPP, PerformanceAttributes, DifficultyAttributes,
};
use pyo3::PyErr;
use std::collections::HashMap;

#[cfg(not(any(feature = "async_tokio", feature = "async_std")))]
use std::fs::File as SyncFile;

#[cfg(feature = "async_tokio")]
use tokio::fs::File as AsyncFile;

#[cfg(feature = "async_std")]
use async_std::fs::File as AsyncFile;

use crate::python::exceptions::ParseBeatmapError;

#[derive(Clone, Debug)]
pub struct PpRaw {
    pub aim: Option<f32>,
    pub spd: Option<f32>,
    pub str: Option<f32>,
    pub acc: Option<f32>,
    pub total: f32,
}

impl PpRaw {
    #[inline]
    pub fn new(
        aim: Option<f32>,
        spd: Option<f32>,
        str: Option<f32>,
        acc: Option<f32>,
        total: f32,
    ) -> Self {
        Self {
            aim,
            spd,
            str,
            acc,
            total,
        }
    }
}

/// Basic struct containing the result of a PP calculation.
#[derive(Clone, Debug)]
pub struct PpResult {
    pub mode: u8,
    pub mods: u32,
    pub pp: f64,
    pub raw: PerformanceAttributes,
    pub attributes: DifficultyAttributes,
}

impl PpResult {
    /// The final pp value.
    #[inline]
    pub fn pp(&self) -> f64 {
        self.pp
    }

    /// The final star value.
    #[inline]
    pub fn stars(&self) -> f64 {
        self.attributes.stars()
    }
}

#[inline(always)]
#[cfg_attr(feature = "rust_logger", timed::timed(duration(printer = "trace!")))]
pub fn calc_with_any_pp(any_pp: AnyPP) -> PpResult {
    any_pp.
}

#[inline(always)]
#[cfg_attr(feature = "rust_logger", timed::timed(duration(printer = "trace!")))]
pub fn calc_acc_list(
    beatmap: &RawBeatmap,
    mode: Option<u8>,
    mods: Option<u32>,
    acc_list: Option<Vec<f64>>,
) -> HashMap<String, f64> {
    let c = mode_any_pp(mode.unwrap_or(4), &beatmap);
    let mut c = match mods {
        Some(mods) => c.mods(mods),
        None => c,
    };

    let mut map = HashMap::new();
    for acc in acc_list.unwrap_or(vec![100.0, 99.0, 98.0, 95.0]) {
        c.set_accuracy(acc);
        map.insert((acc as i32).to_string(), calc_with_any_pp(&mut c).pp());
    }
    map
}

#[inline(always)]
pub fn mode_any_pp(mode: u8, beatmap: &RawBeatmap) -> AnyPP {
    match mode {
        0 => AnyPP::Osu(OsuPP::new(beatmap)),
        1 => AnyPP::Taiko(TaikoPP::new(beatmap)),
        2 => AnyPP::Catch(CatchPP::new(beatmap)),
        3 => AnyPP::Mania(ManiaPP::new(beatmap)),
        _ => AnyPP::new(beatmap),
    }
}

macro_rules! parse_beatmap_body {
    ($parse_method:ident, $file:ident) => {{
        RawBeatmap::$parse_method($file)
            .map_err(|err| ParseBeatmapError::new_err(format!("Could not parse beatmap: {}", err)))
    }};

    (async $parse_method:ident, $file:ident) => {{
        RawBeatmap::$parse_method($file).await.map_err(|err| {
            ParseBeatmapError::new_err(format!("Could not async parse beatmap: {}", err))
        })
    }};
}

macro_rules! parse_beatmap {
    ($parse_method:ident) => {
        #[inline(always)]
        #[cfg_attr(feature = "rust_logger", timed::timed(duration(printer = "trace!")))]
        pub fn sync_parse_beatmap(file: SyncFile) -> Result<RawBeatmap, PyErr> {
            parse_beatmap_body!($parse_method, file)
        }
    };

    (async $parse_method:ident) => {
        #[inline(always)]
        #[cfg_attr(feature = "rust_logger", timed::timed(duration(printer = "trace!")))]
        pub async fn async_parse_beatmap(file: AsyncFile) -> Result<RawBeatmap, PyErr> {
            parse_beatmap_body!(async $parse_method, file)
        }
    };
}

#[cfg(any(feature = "async_tokio", feature = "async_std"))]
parse_beatmap!(async parse);

#[cfg(not(any(feature = "async_tokio", feature = "async_std")))]
pub async fn async_parse_beatmap(_file: SyncFile) -> Result<RawBeatmap, PyErr> {
    Err(crate::async_not_enabled_err!())
}

#[cfg(not(any(feature = "async_tokio", feature = "async_std")))]
parse_beatmap!(parse);
