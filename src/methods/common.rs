use peace_performance::GameMode;
use pyo3::PyErr;
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
#[timed::timed(duration(printer = "trace!"))]
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
#[timed::timed(duration(printer = "trace!"))]
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

/// osu! mode int to string
#[inline(always)]
pub fn osu_mode_int_str(mode: u8) -> String {
    match mode {
        0 => "std",
        1 => "taiko",
        2 => "ctb",
        3 => "mania",
        _ => "unknown",
    }
    .into()
}

#[cfg(any(feature = "async_tokio", feature = "async_std"))]
/// Async sleep
#[inline(always)]
pub async fn sleep(secs: u64) {
    tokio::time::sleep(std::time::Duration::from_secs(secs)).await;
}

#[cfg(not(any(feature = "async_tokio", feature = "async_std")))]
pub async fn sleep(_secs: u64) {
    Err(crate::async_not_enabled_err!())
}
