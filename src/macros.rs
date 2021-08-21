#[macro_export]
macro_rules! pyo3_py_methods {
    ($type:ident, impl {$($others:tt)*}) => {
        #[pymethods] impl $type {
            $($others)*
            #[getter]pub fn attrs(&self) -> String { self.as_string() }
            #[getter]pub fn attrs_dict<'a>(&self, py: Python<'a>) -> PyResult<&'a PyDict> { self.as_dict(py) }
        }
    };
    ($type:ident, {$($attr:ident: $returns:ident),*}, impl {$($others:tt)*}) => {
        #[pymethods] impl $type {
            $(#[getter]pub fn $attr(&self) -> $returns {self.0.$attr})* $($others)*
            #[getter]pub fn attrs(&self) -> String { self.as_string() }
            #[getter]pub fn attrs_dict<'a>(&self, py: Python<'a>) -> PyResult<&'a PyDict> { self.as_dict(py) }
        }
    };
    ($type:ident, {$($attr:ident: $returns:ident),*}) => {
        #[pymethods] impl $type {
            $(#[getter]pub fn $attr(&self) -> $returns {self.0.$attr})*
            #[getter]pub fn attrs(&self) -> String { self.as_string() }
            #[getter]pub fn attrs_dict<'a>(&self, py: Python<'a>) -> PyResult<&'a PyDict> { self.as_dict(py) }
       }
    };
    ($type:ident, {$($attr:ident: $returns:ident),*}; fn {$( $func:ident: $ret:ident),*}) => {
        #[pymethods] impl $type {
            $(#[getter]pub fn $attr(&self) -> $returns {self.0.$attr})*
            $(#[getter]pub fn $func(&self) -> $ret {self.0.$func()})*
            #[getter]pub fn attrs(&self) -> String { self.as_string() }
            #[getter]pub fn attrs_dict<'a>(&self, py: Python<'a>) -> PyResult<&'a PyDict> { self.as_dict(py) }
        }
    };
    ($type:ident, {$($attr:ident: $returns:ident),*}; fn {$( $func:ident: $ret:ident),*}; impl {$($others:tt)*}) => {
        #[pymethods] impl $type {
            $(#[getter]pub fn $attr(&self) -> $returns {self.0.$attr})*
            $(#[getter]pub fn $func(&self) -> $ret {self.0.$func()})*
            $($others)*
            #[getter]pub fn attrs(&self) -> String { self.as_string() }
            #[getter]pub fn attrs_dict<'a>(&self, py: Python<'a>) -> PyResult<&'a PyDict> { self.as_dict(py) }
        }
    };
}

#[macro_export]
macro_rules! pyo3_py_protocol {
    ($obj:ident) => {
        #[pyproto] impl PyObjectProtocol for $obj {
            fn __repr__(&self) -> PyResult<String> { Ok(format!(concat!('<', stringify!($obj), " ({})>"), self.attrs())) }
        }
    };
    ($obj:ident, impl {$($others:item)*}) => {
        use pyo3::PyObjectProtocol;
        #[pyproto] impl PyObjectProtocol for $obj {
            fn __repr__(&self) -> PyResult<String> { Ok(format!(concat!('<', stringify!($obj), " ({})>"), self.attrs())) }
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
            "Any async features (`async_tokio`, `async_std`) are not enabled.",
        )
    };
}

#[macro_export]
macro_rules! rust_logger_not_enabled_err {
    () => {
        crate::python::exceptions::AsyncNotEnabledError::new_err(
            "`rust_logger` features are not enabled.",
        )
    };
}

#[macro_export]
macro_rules! invalid_gamemode_err {
    () => {
        crate::python::exceptions::InvalidGameMode::new_err("Invalid osu! gamemode")
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

#[macro_export]
macro_rules! pyo3_set_sys_modules {
    ($m:ident, $py:ident; {$($module:expr),*}) => {
        let sys = PyModule::import($py, "sys")?;
        let sys_modules: &PyDict = sys.getattr("modules")?.downcast()?;
        let name = $m.name()?;
        let dot = name.find('.');
        $(sys_modules.set_item(if let Some(d) = dot {
            format!("{}._peace_performance.{}", &name[..d], $module)
        } else {
            format!("_peace_performance.{}", $module)
        }, $m.getattr($module)?)?;)*
    };
}

#[macro_export]
macro_rules! pyo3_add_functions {
    ($m:ident; {$($func:ident),*}) => {
        $($m.add_function(pyo3::wrap_pyfunction!($func, $m)?)?;)*
    };
}

#[macro_export]
macro_rules! pyo3_add_modules {
    ($m:ident; {$($module:ident),*}) => {
        $($m.add_wrapped(pyo3::wrap_pymodule!($module))?;)*
    };
}

#[macro_export]
macro_rules! pyo3_add_classes {
    ($m:ident; {$($class:ident),*}) => {
        $($m.add_class::<$class>()?;)*
    };
}

#[macro_export]
macro_rules! set_with_py_str {
    ($obj:ident, $attr:ident, $value:ident; {$($a:ident),*}) => {
        match $attr {
            $(stringify!($a) => $obj.$a = if $value.is_none() {
                None
            } else {
                Some($value.extract()?)
            },)*
            _ => {}
        }
    };
}
