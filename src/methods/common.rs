use pyo3::{PyAny, PyErr};
use rosu_pp::{GameMode, ParseError};
use std::path::PathBuf;

use crate::python::exceptions::{ParseBeatmapError, ReadFileError};

/// osu! mode to string
#[inline(always)]
pub fn osu_mode_str(mode: &GameMode) -> String {
    match mode {
        GameMode::Osu => "std",
        GameMode::Taiko => "taiko",
        GameMode::Catch => "ctb",
        GameMode::Mania => "mania",
    }
    .into()
}

#[inline(always)]
pub fn str_into_osu_mode(str: &str) -> Result<GameMode, PyErr> {
    Ok(match str {
        "std" => GameMode::Osu,
        "taiko" => GameMode::Taiko,
        "ctb" => GameMode::Catch,
        "mania" => GameMode::Mania,
        _ => return Err(crate::invalid_gamemode_err!()),
    })
}

#[inline(always)]
pub fn int_into_osu_mode(int: u8) -> Result<GameMode, PyErr> {
    Ok(match int {
        0 => GameMode::Osu,
        1 => GameMode::Taiko,
        2 => GameMode::Catch,
        3 => GameMode::Mania,
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

crate::cfg_any_async! {
    use std::future::Future;

    crate::cfg_async_std! {
        use async_std::fs::File as AsyncFile;

        pub fn block_on<F: Future>(future: F) -> F::Output {
            async_std::task::block_on(future)
        }
    }

    crate::cfg_async_tokio! {
        use tokio::fs::File as AsyncFile;

        pub fn block_on<F: Future>(future: F) -> F::Output {
            use tokio::runtime::Runtime;
            Runtime::new().unwrap().block_on(future)
        }
    }

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

    /// Async sleep
    #[inline(always)]
    pub async fn sleep(secs: u64) {
        tokio::time::sleep(std::time::Duration::from_secs(secs)).await;
    }


}

crate::cfg_not_async! {
    use std::fs::File as SyncFile;

    pub async fn sleep(_secs: u64) -> Result<(), PyErr> {
        Err(crate::async_not_enabled_err!())
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
}

pub fn map_parse_err(err: ParseError) -> PyErr {
    ParseBeatmapError::new_err(format!("Could not async parse beatmap: {}", err))
}
