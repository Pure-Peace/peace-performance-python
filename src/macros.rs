#[macro_export]
macro_rules! pyo3_getters_generator {
    ($type:ident, {$($attr:ident: $returns:ident),*}, impl {$($others:item)*}) => {
        #[pymethods] impl $type {$(pub fn $attr(&self) -> $returns {self.0.$attr})* $($others)*}
    };
    ($type:ident, {$($attr:ident: $returns:ident),*}) => {
        #[pymethods] impl $type {$(pub fn $attr(&self) -> $returns {self.0.$attr})*}
    };
    ($type:ident, {$($attr:ident: $returns:ident),*}; fn {$( $func:ident: $ret:ident),*}) => {
        #[pymethods] impl $type {
            $(pub fn $attr(&self) -> $returns {self.0.$attr})*
            $(pub fn $func(&self) -> $ret {self.0.$func()})*
        }
    };
    ($type:ident, {$($attr:ident: $returns:ident),*}; fn {$( $func:ident: $ret:ident),*}; impl {$($others:item)*}) => {
        #[pymethods] impl $type {
            $(pub fn $attr(&self) -> $returns {self.0.$attr})*
            $(pub fn $func(&self) -> $ret {self.0.$func()})*
            $($others)*
        }
    };
}
