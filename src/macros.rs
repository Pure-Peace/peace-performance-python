#[macro_export]
macro_rules! py_impl_base {
    ($type:ident, $($attr:ident)*; $($returns:ident)*; $($func:ident)*; $($ret:ident)*; $($others:tt)*) => {
        #[pymethods] impl $type {
            $(#[getter]pub fn $attr(&self) -> $returns {self.0.$attr})*
            $(#[getter]pub fn $func(&self) -> $ret {self.0.$func()})*
            #[getter] pub fn attrs(&self) -> String { self.as_string() }
            #[getter] pub fn attrs_dict<'a>(&self, py: Python<'a>) -> PyResult<&'a PyDict> { self.as_dict(py) }
            fn __repr__(&self) -> PyResult<String> { Ok(format!(concat!('<', stringify!($obj), " ({})>"), self.attrs())) }
            $($others)*
        }
    };
}


#[macro_export]
macro_rules! py_impl {
    (for $type:ident, @attrs {$($attr:ident: $returns:ident),*}; @getters {$( $func:ident: $ret:ident),*}; @methods {$($others:tt)*}) => {
            $crate::py_impl_base!($type, $($attr)*; $($returns)*; $($func)*; $($ret)*; $($others)*);
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
macro_rules! __set_calculator {
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
macro_rules! set_calculator {
    ($calculator:ident, $($target:ident.$attr:ident),*, {$($target1:ident.$attr1:ident: $func1:ident),*}) => ({
        $(let $calculator = $crate::__set_calculator!($target.$attr, $calculator);)*
        $(let $calculator = $crate::__set_calculator!($target1.$attr1, $func1, $calculator);)*
        $calculator
    });
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

#[macro_export]
macro_rules! cfg_async_tokio {
    ($($item:item)*) => {
        $(
            #[cfg(feature = "async_tokio")]
            #[cfg_attr(docsrs, doc(cfg(feature = "async_tokio")))]
            $item
        )*
    }
}

#[macro_export]
macro_rules! cfg_async_std {
    ($($item:item)*) => {
        $(
            #[cfg(feature = "async_std")]
            #[cfg_attr(docsrs, doc(cfg(feature = "async_std")))]
            $item
        )*
    }
}

#[macro_export]
macro_rules! cfg_any_async {
    ($($item:item)*) => {
        $(
            #[cfg(any(feature = "async_tokio", feature = "async_std"))]
            #[cfg_attr(docsrs, doc(cfg(any(feature = "async_tokio", feature = "async_std"))))]
            $item
        )*
    }
}

#[macro_export]
macro_rules! cfg_not_async {
    ($($item:item)*) => {
        $(
            #[cfg(not(any(feature = "async_tokio", feature = "async_std")))]
            #[cfg_attr(docsrs, doc(cfg(not(any(feature = "async_tokio", feature = "async_std")))))]
            $item
        )*
    }
}

#[macro_export]
macro_rules! cfg_rust_logger {
    ($($item:item)*) => {
        $(
            #[cfg(feature = "rust_logger")]
            #[cfg_attr(docsrs, doc(cfg(feature = "rust_logger")))]
            $item
        )*
    }
}

#[macro_export]
macro_rules! cfg_not_rust_logger {
    ($($item:item)*) => {
        $(
            #[cfg(not(feature = "rust_logger"))]
            #[cfg_attr(docsrs, doc(cfg(not(feature = "rust_logger"))))]
            $item
        )*
    }
}
