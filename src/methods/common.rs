use peace_performance::GameMode;
use pyo3::{PyAny, PyErr};
use std::path::PathBuf;

use std::fs::File as SyncFile;

#[cfg(feature = "async_tokio")]
use tokio::fs::File as AsyncFile;

#[cfg(feature = "async_std")]
use async_std::fs::File as AsyncFile;

use crate::python::exceptions::ReadFileError;

#[cfg(any(feature = "async_tokio", feature = "async_std"))]
/// Async read file
#[inline(always)]
#[cfg_attr(feature = "rust_logger", timed::timed(duration(printer = "trace!")))]
pub async fn async_read_file(path: PathBuf) -> Result<AsyncFile, PyErr> {
    match AsyncFile::open(path).await {
        Ok(file) => Ok(file),
        Err(err) => Err(ReadFileError::new_err(format!(
            "Could not read file async: {}",
            err
        ))),
    }
}

/// Sync read file
#[inline(always)]
#[cfg_attr(feature = "rust_logger", timed::timed(duration(printer = "trace!")))]
pub fn sync_read_file(path: PathBuf) -> Result<SyncFile, PyErr> {
    match SyncFile::open(path) {
        Ok(file) => Ok(file),
        Err(err) => Err(ReadFileError::new_err(format!(
            "Could not read file: {}",
            err
        ))),
    }
}

/// osu! mode to string
#[inline(always)]
pub fn osu_mode_str(mode: &GameMode) -> String {
    match mode {
        GameMode::STD => "std",
        GameMode::TKO => "taiko",
        GameMode::CTB => "ctb",
        GameMode::MNA => "mania",
    }
    .into()
}

#[inline(always)]
pub fn str_into_osu_mode(str: &str) -> Result<GameMode, PyErr> {
    Ok(match str {
        "std" => GameMode::STD,
        "taiko" => GameMode::TKO,
        "ctb" => GameMode::CTB,
        "mania" => GameMode::MNA,
        _ => return Err(crate::invalid_gamemode_err!()),
    })
}

#[inline(always)]
pub fn int_into_osu_mode(int: u8) -> Result<GameMode, PyErr> {
    Ok(match int {
        0 => GameMode::STD,
        1 => GameMode::TKO,
        2 => GameMode::CTB,
        3 => GameMode::MNA,
        _ => return Err(crate::invalid_gamemode_err!()),
    })
}

pub fn py_any_into_osu_mode(py_input: &PyAny) -> Result<GameMode, PyErr> {
    if let Ok(str) = py_input.extract::<String>() {
        return str_into_osu_mode(&str);
    } else if let Ok(int) = py_input.extract::<u8>() {
        return int_into_osu_mode(int);
    }
    Err(crate::invalid_gamemode_err!())
}

#[cfg(any(feature = "async_tokio", feature = "async_std"))]
/// Async sleep
#[inline(always)]
pub async fn sleep(secs: u64) {
    tokio::time::sleep(std::time::Duration::from_secs(secs)).await;
}

#[cfg(not(any(feature = "async_tokio", feature = "async_std")))]
pub async fn sleep(_secs: u64) -> Result<(), PyErr> {
    Err(crate::async_not_enabled_err!())
}
