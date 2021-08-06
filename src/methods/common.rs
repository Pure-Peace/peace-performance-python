use pyo3::PyErr;
use std::path::PathBuf;
use tokio::fs::File as AsyncFile;

use crate::python::exceptions::ReadFileError;

/// Async read file
#[inline(always)]
#[timed::timed(duration(printer = "trace!"))]
pub async fn async_read_file(path: PathBuf) -> Result<AsyncFile, PyErr> {
    match AsyncFile::open(path).await {
        Ok(file) => Ok(file),
        Err(err) => Err(ReadFileError::new_err(format!(
            "Could not read file: {}",
            err
        ))),
    }
}

/// Async sleep
#[inline(always)]
pub async fn sleep(secs: u64) {
    tokio::time::sleep(std::time::Duration::from_secs(secs)).await;
}
