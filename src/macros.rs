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
