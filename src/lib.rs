use pyo3::prelude::*;

mod treemap;
mod iterators;

#[pymodule]
fn _blart(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<treemap::PyTreeMap>()?;
    m.add_class::<iterators::PyTreeMapIter>()?;
    m.add_class::<iterators::PyTreeMapKeys>()?;
    m.add_class::<iterators::PyTreeMapValues>()?;
    m.add_class::<iterators::PyTreeMapItems>()?;
    m.add_class::<iterators::PyPrefixIter>()?;
    Ok(())
}
