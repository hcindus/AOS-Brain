// cortical_sheet.hpp
// 3D Ternary Cortical Sheet with wave propagation, Hebbian learning, and gating

#ifndef CORTICAL_SHEET_HPP
#define CORTICAL_SHEET_HPP

#include <vector>
#include <cmath>
#include <algorithm>

namespace aos_brain {

struct SheetSummary {
    int pos_count = 0;
    int neg_count = 0;
    int zero_count = 0;
    double cx = 0.0, cy = 0.0, cz = 0.0;  // center of mass for +1
    double energy = 0.0;  // total activity
    
    json to_json() const;
};

class TernaryCorticalSheet3D {
public:
    TernaryCorticalSheet3D(int nx, int ny, int nz);
    
    // Core accessors
    int index(int x, int y, int z) const;
    bool in_bounds(int x, int y, int z) const;
    int get_state(int x, int y, int z) const { return state_[index(x,y,z)]; }
    void set_state(int x, int y, int z, int val);
    
    // Activity injection
    void excite_region(int cx, int cy, int cz, int radius, int value = +1);
    void inhibit_region(int cx, int cy, int cz, int radius);
    void clear_region(int cx, int cy, int cz, int radius);
    
    // Dynamics
    void step_wave(double decay = 0.9);
    void step_wave_gated(int gate_state, double decay_pos = 0.95, double decay_neutral = 0.85);
    
    // Learning
    void hebbian_update(double eta = 0.01);
    void consolidate();  // strengthen persistent patterns
    
    // Analysis
    SheetSummary summarize() const;
    double coherence() const;  // how synchronized is the sheet
    
    // Dimensions
    int nx() const { return nx_; }
    int ny() const { return ny_; }
    int nz() const { return nz_; }
    int size() const { return nx_ * ny_ * nz_; }
    
    // Direct access for visualization
    const std::vector<int>& state() const { return state_; }
    const std::vector<double>& weights() const { return weight_; }
    
private:
    int nx_, ny_, nz_;
    std::vector<int> state_;
    std::vector<int> next_state_;
    std::vector<double> weight_;  // Hebbian self-weights
    
    static constexpr int NEIGHBORS[6][3] = {
        {1, 0, 0}, {-1, 0, 0},
        {0, 1, 0}, {0, -1, 0},
        {0, 0, 1}, {0, 0, -1}
    };
};

// Ternary neuron helper
struct TernaryNeuron {
    static int activate(double x, double pos_thresh = 0.3, double neg_thresh = -0.3);
    static int gated_activate(double x, int gate, double pos_thresh = 0.3);
};

} // namespace aos_brain

#endif // CORTICAL_SHEET_HPP
