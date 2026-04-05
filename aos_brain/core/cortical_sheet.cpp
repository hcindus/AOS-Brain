// cortical_sheet.cpp

#include "cortical_sheet.hpp"
#include "../external/json.hpp"

namespace aos_brain {

using json = nlohmann::json;

json SheetSummary::to_json() const {
    return json{
        {"pos_count", pos_count},
        {"neg_count", neg_count},
        {"zero_count", zero_count},
        {"center", {cx, cy, cz}},
        {"energy", energy}
    };
}

TernaryCorticalSheet3D::TernaryCorticalSheet3D(int nx, int ny, int nz)
    : nx_(nx), ny_(ny), nz_(nz),
      state_(nx * ny * nz, 0),
      next_state_(nx * ny * nz, 0),
      weight_(nx * ny * nz, 1.0) {}

int TernaryCorticalSheet3D::index(int x, int y, int z) const {
    return x + nx_ * (y + ny_ * z);
}

bool TernaryCorticalSheet3D::in_bounds(int x, int y, int z) const {
    return x >= 0 && x < nx_ && 
           y >= 0 && y < ny_ && 
           z >= 0 && z < nz_;
}

void TernaryCorticalSheet3D::set_state(int x, int y, int z, int val) {
    if (in_bounds(x, y, z)) {
        state_[index(x, y, z)] = val;
    }
}

void TernaryCorticalSheet3D::excite_region(int cx, int cy, int cz, int radius, int value) {
    for (int x = cx - radius; x <= cx + radius; ++x) {
        for (int y = cy - radius; y <= cy + radius; ++y) {
            for (int z = cz - radius; z <= cz + radius; ++z) {
                if (!in_bounds(x, y, z)) continue;
                int dx = x - cx, dy = y - cy, dz = z - cz;
                if (dx*dx + dy*dy + dz*dz <= radius*radius) {
                    state_[index(x, y, z)] = value;
                }
            }
        }
    }
}

void TernaryCorticalSheet3D::inhibit_region(int cx, int cy, int cz, int radius) {
    excite_region(cx, cy, cz, radius, -1);
}

void TernaryCorticalSheet3D::clear_region(int cx, int cy, int cz, int radius) {
    excite_region(cx, cy, cz, radius, 0);
}

void TernaryCorticalSheet3D::step_wave(double decay) {
    for (int x = 0; x < nx_; ++x) {
        for (int y = 0; y < ny_; ++y) {
            for (int z = 0; z < nz_; ++z) {
                int idx = index(x, y, z);
                
                // Self contribution with weight
                double sum = weight_[idx] * state_[idx];
                
                // Neighbor contributions
                for (const auto& off : NEIGHBORS) {
                    int nx = x + off[0];
                    int ny = y + off[1];
                    int nz = z + off[2];
                    if (!in_bounds(nx, ny, nz)) continue;
                    sum += 0.5 * state_[index(nx, ny, nz)];
                }
                
                sum *= decay;
                
                // Ternary activation
                if (sum > 0.3) next_state_[idx] = +1;
                else if (sum < -0.3) next_state_[idx] = -1;
                else next_state_[idx] = 0;
            }
        }
    }
    
    state_.swap(next_state_);
}

void TernaryCorticalSheet3D::step_wave_gated(int gate_state, double decay_pos, double decay_neutral) {
    if (gate_state == -1) {
        // Full suppression
        std::fill(state_.begin(), state_.end(), 0);
        return;
    }
    
    double decay = (gate_state == +1) ? decay_pos : decay_neutral;
    step_wave(decay);
}

void TernaryCorticalSheet3D::hebbian_update(double eta) {
    for (size_t i = 0; i < state_.size(); ++i) {
        int s = state_[i];
        if (s == 0) continue;
        weight_[i] += eta * s;
        // Clamp weights
        if (weight_[i] > 5.0) weight_[i] = 5.0;
        if (weight_[i] < -5.0) weight_[i] = -5.0;
    }
}

void TernaryCorticalSheet3D::consolidate() {
    // Strengthen persistent patterns
    for (size_t i = 0; i < state_.size(); ++i) {
        if (state_[i] != 0) {
            weight_[i] *= 1.05;  // slight boost
            if (weight_[i] > 10.0) weight_[i] = 10.0;
        }
    }
}

SheetSummary TernaryCorticalSheet3D::summarize() const {
    SheetSummary s;
    double sx = 0, sy = 0, sz = 0;
    
    for (int x = 0; x < nx_; ++x) {
        for (int y = 0; y < ny_; ++y) {
            for (int z = 0; z < nz_; ++z) {
                int idx = index(x, y, z);
                int v = state_[idx];
                
                if (v == +1) {
                    s.pos_count++;
                    sx += x; sy += y; sz += z;
                } else if (v == -1) {
                    s.neg_count++;
                } else {
                    s.zero_count++;
                }
                
                s.energy += std::abs(v);
            }
        }
    }
    
    if (s.pos_count > 0) {
        s.cx = sx / s.pos_count;
        s.cy = sy / s.pos_count;
        s.cz = sz / s.pos_count;
    }
    
    return s;
}

double TernaryCorticalSheet3D::coherence() const {
    // Measure how synchronized the sheet is
    int active = 0;
    int same_neighbors = 0;
    
    for (int x = 1; x < nx_ - 1; ++x) {
        for (int y = 1; y < ny_ - 1; ++y) {
            for (int z = 1; z < nz_ - 1; ++z) {
                int idx = index(x, y, z);
                int v = state_[idx];
                if (v == 0) continue;
                
                active++;
                for (const auto& off : NEIGHBORS) {
                    int nv = state_[index(x + off[0], y + off[1], z + off[2])];
                    if (nv == v) same_neighbors++;
                }
            }
        }
    }
    
    return active > 0 ? static_cast<double>(same_neighbors) / (active * 6.0) : 0.0;
}

// TernaryNeuron implementation
int TernaryNeuron::activate(double x, double pos_thresh, double neg_thresh) {
    if (x > pos_thresh) return +1;
    if (x < neg_thresh) return -1;
    return 0;
}

int TernaryNeuron::gated_activate(double x, int gate, double pos_thresh) {
    if (gate == -1) return 0;
    double scale = (gate == +1) ? 1.0 : 0.5;
    return activate(x * scale, pos_thresh * scale);
}

} // namespace aos_brain
