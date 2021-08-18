#[macro_export]
macro_rules! pyo3_py_methods {
    ($type:ident, {$($attr:ident: $returns:ident),*}, impl {$($others:item)*}) => {
        #[pymethods] impl $type {$(#[getter]pub fn $attr(&self) -> $returns {self.0.$attr})* $($others)*}
    };
    ($type:ident, {$($attr:ident: $returns:ident),*}) => {
        #[pymethods] impl $type {$(#[getter]pub fn $attr(&self) -> $returns {self.0.$attr})*}
    };
    ($type:ident, {$($attr:ident: $returns:ident),*}; fn {$( $func:ident: $ret:ident),*}) => {
        #[pymethods] impl $type {
            $(#[getter]pub fn $attr(&self) -> $returns {self.0.$attr})*
            $(#[getter]pub fn $func(&self) -> $ret {self.0.$func()})*
        }
    };
    ($type:ident, {$($attr:ident: $returns:ident),*}; fn {$( $func:ident: $ret:ident),*}; impl {$($others:item)*}) => {
        #[pymethods] impl $type {
            $(#[getter]pub fn $attr(&self) -> $returns {self.0.$attr})*
            $(#[getter]pub fn $func(&self) -> $ret {self.0.$func()})*
            $($others)*
        }
    };
}

#[macro_export]
macro_rules! pyo3_py_dict {
    ($py:ident, $obj:expr; {$($attr:ident),*}) => {{let d = PyDict::new($py);$(d.set_item(stringify!($attr), $obj.$attr.clone())?;)*d}};
    ($py:ident, $obj:expr; {$($attr:ident),*}; fn $obj1:ident {$($func:ident),*}) => {{
        let d = PyDict::new($py);$(d.set_item(stringify!($attr), $obj.$attr.clone())?;)*$(d.set_item(stringify!($func), $obj1.$func())?;)*d
    }};
}

#[macro_export]
macro_rules! async_not_enabled_err {
    () => {
        crate::python::exceptions::AsyncNotEnabledError::new_err(
            "Any async features (async_tokio, async_std) are not enabled.",
        )
    };
}

#[macro_export]
macro_rules! set_calculator {
    ($target:ident.$attr:ident, $calculator:ident) => {
        match $target.$attr {
            Some($attr) => $calculator.$attr($attr),
            None => $calculator,
        }
    };
    ($target:ident.$attr:ident, $func:ident, $calculator:ident) => {
        match $target.$attr {
            Some($attr) => $calculator.$func($attr),
            None => $calculator,
        }
    };
}
