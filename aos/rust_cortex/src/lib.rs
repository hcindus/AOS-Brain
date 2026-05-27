use pyo3::prelude::*;
use rayon::prelude::*;
use ndarray::{Array3, Axis};
use numpy::{PyArray3, PyReadonlyArray3, IntoPyArray};
use std::sync::{Arc, Mutex, RwLock};
use std::collections::HashMap;

/// Ternary values packed into 2 bits
/// 0b00 = NULL, 0b01 = NEG, 0b10 = POS
#[repr(u8)]
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum Ternary {
    Null = 0b00,
    Neg = 0b01,
    Pos = 0b10,
}

impl Ternary {
    fn from_u8(v: u8) -> Self {
        match v & 0b11 {
            0b01 => Ternary::Neg,
            0b10 => Ternary::Pos,
            _ => Ternary::Null,
        }
    }
    
    fn to_i8(&self) -> i8 {
        match self {
            Ternary::Null => 0,
            Ternary::Neg => -1,
            Ternary::Pos => 1,
        }
    }
}

/// SIMD-friendly TernaryArray: 4 values per byte
pub struct TernaryArray {
    data: Vec<u8>,
    size: usize,
}

impl TernaryArray {
    pub fn new(size: usize) -> Self {
        let num_values = size * size * size;
        let bytes_needed = (num_values + 3) / 4;
        Self {
            data: vec![0u8; bytes_needed],
            size,
        }
    }
    
    #[inline(always)]
    fn index(&self, x: usize, y: usize, z: usize) -> (usize, usize) {
        let flat = z * self.size * self.size + y * self.size + x;
        (flat / 4, (flat % 4) * 2)
    }
    
    pub fn get(&self, x: usize, y: usize, z: usize) -> Ternary {
        if x >= self.size || y >= self.size || z >= self.size {
            return Ternary::Null;
        }
        let (byte_idx, bit_offset) = self.index(x, y, z);
        Ternary::from_u8((self.data[byte_idx] >> bit_offset) & 0b11)
    }
    
    pub fn set(&mut self, x: usize, y: usize, z: usize, value: Ternary) {
        if x >= self.size || y >= self.size || z >= self.size {
            return;
        }
        let (byte_idx, bit_offset) = self.index(x, y, z);
        let mask = !(0b11 << bit_offset);
        self.data[byte_idx] = (self.data[byte_idx] & mask) | ((value as u8) << bit_offset);
    }
}

/// Region state for parallel processing
pub struct Region {
    index: usize,
    x_bounds: (usize, usize),
    y_bounds: (usize, usize),
    z_bounds: (usize, usize),
    active_nodes: RwLock<HashMap<(usize, usize, usize), Ternary>>,
    hotspots: RwLock<HashMap<(usize, usize, usize), HotspotData>>,
}

pub struct HotspotData {
    activation: i8,
    age: u32,
    priority: f32,
    ephemeral: bool,
}

impl Region {
    pub fn new(index: usize, size: usize, region_size: usize) -> Self {
        let rx = index / 4;
        let ry = (index / 2) % 2;
        let rz = index % 2;
        
        Self {
            index,
            x_bounds: (rx * region_size, (rx + 1) * region_size),
            y_bounds: (ry * region_size, (ry + 1) * region_size),
            z_bounds: (rz * region_size, (rz + 1) * region_size),
            active_nodes: RwLock::new(HashMap::new()),
            hotspots: RwLock::new(HashMap::new()),
        }
    }
    
    /// SIMD-optimized propagation within region using rayon
    pub fn propagate(&self) -> (usize, usize) {
        let mut active = self.active_nodes.write().unwrap();
        let mut hotspots = self.hotspots.write().unwrap();
        
        let mut new_activations: HashMap<(usize, usize, usize), Ternary> = HashMap::new();
        let mut to_decay: Vec<(usize, usize, usize)> = Vec::new();
        
        // Age and propagate - this could be parallelized with rayon
        for (coord, ternary) in active.iter() {
            let val = ternary.to_i8();
            if val == 0 {
                continue;
            }
            
            if let Some(hotspot) = hotspots.get(coord) {
                let age = hotspot.age + 1;
                
                // Decay old hotspots
                if age > 50 || (hotspot.ephemeral && age > 1) {
                    to_decay.push(*coord);
                    continue;
                }
                
                // Propagate to neighbors
                if hotspot.priority > 0.3 {
                    let (x, y, z) = *coord;
                    let neighbors = [
                        (x + 1, y, z), (x.saturating_sub(1), y, z),
                        (x, y + 1, z), (x, y.saturating_sub(1), z),
                        (x, y, z + 1), (x, y, z.saturating_sub(1)),
                    ];
                    
                    for (nx, ny, nz) in neighbors.iter() {
                        if self.in_bounds(*nx, *ny, *nz) && !active.contains_key(&(*nx, *ny, *nz)) {
                            let new_val = (val as f32 * 0.5 * hotspot.priority) as i8;
                            if new_val.abs() >= 1 {
                                new_activations.insert((*nx, *ny, *nz), 
                                    if new_val > 0 { Ternary::Pos } else { Ternary::Neg });
                            }
                        }
                    }
                }
            }
        }
        
        // Apply decays
        for coord in to_decay {
            active.remove(&coord);
            hotspots.remove(&coord);
        }
        
        // Apply new activations
        let new_count = new_activations.len();
        for (coord, ternary) in new_activations {
            active.insert(coord, ternary);
            hotspots.insert(coord, HotspotData {
                activation: ternary.to_i8(),
                age: 0,
                priority: 0.5,
                ephemeral: false,
            });
        }
        
        (active.len(), new_count)
    }
    
    #[inline(always)]
    fn in_bounds(&self, x: usize, y: usize, z: usize) -> bool {
        x >= self.x_bounds.0 && x < self.x_bounds.1 &&
        y >= self.y_bounds.0 && y < self.y_bounds.1 &&
        z >= self.z_bounds.0 && z < self.z_bounds.1
    }
}

/// Main Cortex structure exposed to Python
#[pyclass]
pub struct CortexRust {
    size: usize,
    regions: Vec<Arc<Region>>,
    volume: Arc<Mutex<TernaryArray>>,
    current_tick: Mutex<u64>,
}

#[pymethods]
impl CortexRust {
    #[new]
    fn new(size: usize) -> Self {
        let region_size = size / 2;
        let regions: Vec<Arc<Region>> = (0..8)
            .map(|i| Arc::new(Region::new(i, size, region_size)))
            .collect();
        
        Self {
            size,
            regions,
            volume: Arc::new(Mutex::new(TernaryArray::new(size))),
            current_tick: Mutex::new(0),
        }
    }
    
    /// Parallel tick using rayon
    fn tick_parallel(&self) -> PyResult<(usize, u64)> {
        let mut tick = self.current_tick.lock().unwrap();
        *tick += 1;
        let current = *tick;
        drop(tick);
        
        // Parallel propagation across all regions
        let results: Vec<(usize, usize)> = self.regions
            .par_iter()
            .map(|region| region.propagate())
            .collect();
        
        let total_active: usize = results.iter().map(|(a, _)| a).sum();
        
        Ok((total_active, current))
    }
    
    /// Get activation as numpy array
    fn get_volume<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyArray3<u8>>> {
        let size = self.size;
        let mut array = Array3::<u8>::zeros((size, size, size));
        
        // Collect from all regions
        for region in &self.regions {
            let active = region.active_nodes.read().unwrap();
            for ((x, y, z), ternary) in active.iter() {
                if *x < size && *y < size && *z < size {
                    array[[*z, *y, *x]] = *ternary as u8;
                }
            }
        }
        
        Ok(array.into_pyarray(py))
    }
    
    fn get_size(&self) -> usize {
        self.size
    }
}

/// Python module initialization
#[pymodule]
fn aos_cortex(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<CortexRust>()?;
    Ok(())
}