use peace_performance::{
    AnyPP, Beatmap as RawBeatmap, FruitsPP, ManiaPP, OsuPP, PpResult, TaikoPP,
};
use pyo3::PyErr;
use std::collections::HashMap;

use std::fs::File as SyncFile;

#[cfg(feature = "async_tokio")]
use tokio::fs::File as AsyncFile;

#[cfg(feature = "async_std")]
use async_std::fs::File as AsyncFile;

use crate::python::exceptions::ParseBeatmapError;

#[inline(always)]
#[cfg_attr(feature = "rust_logger", timed::timed(duration(printer = "trace!")))]
pub fn calc_with_any_pp(any_pp: &mut AnyPP) -> PpResult {
    match any_pp {
        AnyPP::Fruits(f) => f.calculate(),
        AnyPP::Mania(m) => m.calculate(),
        AnyPP::Osu(o) => o.calculate(),
        AnyPP::Taiko(t) => t.calculate(),
    }
}

#[inline(always)]
#[cfg_attr(feature = "rust_logger", timed::timed(duration(printer = "trace!")))]
pub fn calc_acc_list(
    beatmap: &RawBeatmap,
    mode: Option<u8>,
    mods: Option<u32>,
    acc_list: Option<Vec<f32>>,
) -> HashMap<String, f32> {
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
        2 => AnyPP::Fruits(FruitsPP::new(beatmap)),
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

#[cfg(any(feature = "async_tokio", feature = "async_std"))]
parse_beatmap!(parse_sync);

#[cfg(not(any(feature = "async_tokio", feature = "async_std")))]
pub async fn async_parse_beatmap(_file: SyncFile) -> Result<RawBeatmap, PyErr> {
    Err(crate::async_not_enabled_err!())
}

#[cfg(not(any(feature = "async_tokio", feature = "async_std")))]
parse_beatmap!(parse);
