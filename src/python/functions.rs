use pyo3::{prelude::pyfunction, PyAny, PyResult, Python};
use rosu_pp::Beatmap as RawBeatmap;
use std::path::PathBuf;

use crate::{
    methods::common,
    objects::{Beatmap, Calculator},
};

crate::cfg_rust_logger! {
    #[pyfunction]
    #[inline(always)]
    pub fn set_log_level(log_level: &str) {
        std::env::set_var("RUST_LOG", log_level);
    }

    #[pyfunction]
    #[inline(always)]
    pub fn init_logger() {
        pretty_env_logger::init();
    }
}

crate::cfg_not_rust_logger! {
    #[pyfunction]
    pub fn set_log_level(_log_level: &str) -> PyResult<()> {
        Err(crate::rust_logger_not_enabled_err!())
    }

    #[pyfunction]
    pub fn init_logger() -> PyResult<()> {
        Err(crate::rust_logger_not_enabled_err!())
    }
}

crate::cfg_not_async! {
    #[pyfunction]
    pub fn read_beatmap_sync(_py: Python, path: PathBuf) -> PyResult<Beatmap> {
        let file = common::sync_read_file(path)?;
        Ok(Beatmap(RawBeatmap::parse(file).map_err(common::map_parse_err)?))
    }

    #[pyfunction]
    pub fn read_beatmap_async(_py: Python, _path: PathBuf) -> PyResult<&PyAny> {
        Err(crate::async_not_enabled_err!())
    }

    #[pyfunction]
    pub fn rust_sleep(_py: Python, _secs: u64) -> PyResult<&PyAny> {
        Err(crate::async_not_enabled_err!())
    }
}

crate::cfg_any_async! {
    use pyo3::IntoPy;

    crate::cfg_async_std! {
        use pyo3_asyncio::async_std as pyo3_async_runtime;
    }

    crate::cfg_async_tokio! {
        use pyo3_asyncio::tokio as pyo3_async_runtime;
    }

    #[pyfunction]
    #[inline(always)]
    pub fn read_beatmap_async(py: Python, path: PathBuf) -> PyResult<&PyAny> {
        pyo3_async_runtime::future_into_py(py, async {
            let file = common::async_read_file(path).await?;
            let beatmap = RawBeatmap::parse(file).await.map_err(common::map_parse_err)?;
            Python::with_gil(|py| Ok(Beatmap(beatmap).into_py(py)))
        })
    }

    #[pyfunction]
    #[inline(always)]
    pub fn rust_sleep(py: Python, secs: u64) -> PyResult<&PyAny> {
        pyo3_async_runtime::future_into_py(py, async move {
            common::sleep(secs).await;
            Ok(Python::with_gil(|py| py.None()))
        })
    }

    #[pyfunction]
    #[inline(always)]
    pub fn read_beatmap_sync(path: PathBuf) -> PyResult<Beatmap> {
        common::block_on(async {
            let file = common::async_read_file(path).await?;
            Ok(Beatmap(RawBeatmap::parse(file).await.map_err(common::map_parse_err)?))
        })
    }
}

#[pyfunction]
#[inline(always)]
pub fn new_calculator() -> Calculator {
    Calculator::new_empty()
}

#[pyfunction]
#[inline(always)]
/// osu! mode int to string
pub fn osu_mode_int_str(mode: u8) -> Option<String> {
    Some(
        match mode {
            0 => "std",
            1 => "taiko",
            2 => "ctb",
            3 => "mania",
            _ => return None,
        }
        .into(),
    )
}

#[pyfunction]
#[inline(always)]
/// osu! mode int to string
pub fn osu_mode_str_int(mode: &str) -> Option<u8> {
    Some(match mode {
        "std" => 0,
        "taiko" => 1,
        "ctb" => 2,
        "mania" => 3,
        _ => return None,
    })
}
