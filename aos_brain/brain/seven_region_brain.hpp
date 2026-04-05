// brain/seven_region_brain.hpp
// Complete 7-region brain architecture in C++

#ifndef SEVEN_REGION_BRAIN_HPP
#define SEVEN_REGION_BRAIN_HPP

#include <vector>
#include <deque>
#include <string>
#include <memory>
#include <thread>
#include <mutex>
#include <atomic>
#include <functional>
#include <nlohmann/json.hpp>

#include "../core/cortical_sheet.hpp"

namespace aos_brain {

using json = nlohmann::json;

// Forward declarations
class ThalamusRegion;
class HippocampusRegion;
class LimbicRegion;
class PFCRegion;
class BasalRegion;
class CerebellumRegion;
class BrainstemRegion;
class AutoFeeder;

// Data structures
struct Observation {
    std::string input;
    std::string source;
    double timestamp;
    json metadata;
};

struct Decision {
    std::string type;  // "respond", "act", "noop", "halt", "query", "learn"
    std::string reason;
    double confidence;
    json action;
    bool safety_override = false;
};

struct Affect {
    double reward = 0.0;
    double novelty = 0.0;
    std::string mode = "adaptive";
    double novelty_avg = 0.0;
    double reward_avg = 0.0;
};

struct Plan {
    std::string type;
    std::string raw;
    double novelty = 0.0;
};

struct MemoryTrace {
    int tick;
    Observation sensory;
    Affect affect;
    Decision action;
    json result;
};

// State output structure
struct BrainState {
    int tick;
    double timestamp;
    std::string phase;
    std::string mode;
    
    struct RegionState {
        json thalamus;
        json hippocampus;
        json limbic;
        json pfc;
        json basal;
        json cerebellum;
        json brainstem;
    } regions;
    
    json policy_nn;
    json memory_nn;
    json obs;
    json decision;
    json result;
    
    json to_json() const;
};

// ============================================================================
// Region 1: Thalamus - Sensory Relay
// ============================================================================
class ThalamusRegion {
public:
    ThalamusRegion(const json& config);
    
    // Check for external input
    Observation observe();
    
    // Process external input directly
    Observation process_external(const std::string& text, const std::string& source);
    
    // Add to sensory queue
    void queue_input(const std::string& text, const std::string& source);
    
private:
    std::deque<Observation> input_queue_;
    std::string input_file_;
    double last_check_ = 0.0;
    std::mutex mutex_;
};

// ============================================================================
// Region 2: Hippocampus - Episodic Memory
// ============================================================================
class HippocampusRegion {
public:
    HippocampusRegion(const json& config);
    
    // Query episodic memory
    json recall(const Observation& sensory);
    
    // Store new experience
    void store(const MemoryTrace& trace);
    
    // Get cluster count
    int get_cluster_count() const;
    
private:
    std::deque<MemoryTrace> episodic_buffer_;
    int cluster_count_ = 0;
    mutable std::mutex mutex_;
};

// ============================================================================
// Region 3: Limbic - Affect/Emotion
// ============================================================================
class LimbicRegion {
public:
    LimbicRegion(const json& config, std::shared_ptr<HippocampusRegion> hippocampus);
    
    // Calculate reward and novelty
    Affect evaluate(const Observation& obs, const json& memory_ctx);
    
private:
    std::shared_ptr<HippocampusRegion> hippocampus_;
    std::deque<double> novelty_history_;
    std::deque<double> reward_history_;
    json config_;
};

// ============================================================================
// Region 4: PFC - Planning/Decision
// ============================================================================
class PFCRegion {
public:
    PFCRegion(const json& config);
    
    // Generate plan
    Plan decide(const Observation& sensory, const json& memory, const Affect& affect);
    
private:
    std::deque<Plan> plan_history_;
    json config_;
};

// ============================================================================
// Region 5: Basal Ganglia - Action Selection
// ============================================================================
class BasalRegion {
public:
    BasalRegion(const json& config);
    
    // Select action from plan
    Decision select_action(const Plan& plan, const Affect& affect);
    
    // Get neural network state
    json get_nn_state() const;
    
private:
    struct PolicyNN {
        int layers = 3;
        std::vector<int> nodes = {8, 12, 16};
        std::vector<std::vector<double>> activations;
        double error_rate = 0.0;
    } nn_;
};

// ============================================================================
// Region 6: Cerebellum - Motor Coordination
// ============================================================================
class CerebellumRegion {
public:
    CerebellumRegion(const json& config);
    
    // Coordinate motor output
    Decision coordinate(const Decision& action);
    
private:
    std::deque<Decision> coordination_log_;
};

// ============================================================================
// Region 7: Brainstem - Safety/Life Support
// ============================================================================
class BrainstemRegion {
public:
    BrainstemRegion(const json& config);
    
    // Enforce 4 Laws
    Decision enforce(const Decision& action, const Observation& obs, 
                     const json& ctx, const Affect& affect);
    
    // Get violation log
    json get_violations() const;
    
private:
    struct SafetyViolation {
        std::string law;
        std::string pattern;
        double timestamp;
    };
    
    std::deque<SafetyViolation> violations_;
    mutable std::mutex mutex_;
    
    bool check_law_zero(const Decision& action, const Observation& obs);
    bool check_law_one(const Decision& action, const Observation& obs);
    bool check_law_two(const Decision& action, const Observation& obs);
    bool check_law_three(const Decision& action, const Observation& obs);
};

// ============================================================================
// Auto-Feeder for equations and data
// ============================================================================
class AutoFeeder {
public:
    using BrainCallback = std::function<void(const std::string&, const std::string&)>;
    
    AutoFeeder(BrainCallback callback);
    
    // Start feeding in background
    void start(double interval_seconds = 60.0);
    
    // Stop feeding
    void stop();
    
    // Check if running
    bool is_running() const { return running_.load(); }
    
private:
    BrainCallback brain_callback_;
    std::atomic<bool> running_{false};
    std::thread feeder_thread_;
    double interval_ = 60.0;
    
    std::vector<std::string> equations_;
    std::vector<std::string> facts_;
    std::vector<std::string> patterns_;
    
    void feed_loop();
    void load_sources();
};

// ============================================================================
// Main 7-Region Brain
// ============================================================================
class SevenRegionBrain {
public:
    SevenRegionBrain(const std::string& config_path = "");
    ~SevenRegionBrain();
    
    // Execute one tick
    BrainState tick(const std::optional<Observation>& external_input = std::nullopt);
    
    // Feed input directly
    BrainState feed(const std::string& text, const std::string& source = "user");
    
    // Get current status
    json get_status() const;
    
    // Start auto-feeder
    void start_auto_feeder(double interval = 60.0);
    
    // Stop auto-feeder
    void stop_auto_feeder();
    
    // Run continuous loop
    void run(double tick_interval = 0.2);
    
    // Stop running
    void stop() { running_ = false; }
    
    // Getters for regions (for testing)
    std::shared_ptr<ThalamusRegion> get_thalamus() { return thalamus_; }
    std::shared_ptr<HippocampusRegion> get_hippocampus() { return hippocampus_; }
    std::shared_ptr<LimbicRegion> get_limbic() { return limbic_; }
    std::shared_ptr<PFCRegion> get_pfc() { return pfc_; }
    std::shared_ptr<BasalRegion> get_basal() { return basal_; }
    std::shared_ptr<CerebellumRegion> get_cerebellum() { return cerebellum_; }
    std::shared_ptr<BrainstemRegion> get_brainstem() { return brainstem_; }
    
private:
    int tick_count_ = 0;
    json config_;
    std::atomic<bool> running_{true};
    double tick_interval_ = 0.2;
    
    // 7 Regions
    std::shared_ptr<ThalamusRegion> thalamus_;
    std::shared_ptr<HippocampusRegion> hippocampus_;
    std::shared_ptr<LimbicRegion> limbic_;
    std::shared_ptr<PFCRegion> pfc_;
    std::shared_ptr<BasalRegion> basal_;
    std::shared_ptr<CerebellumRegion> cerebellum_;
    std::shared_ptr<BrainstemRegion> brainstem_;
    
    // Auto-feeder
    std::unique_ptr<AutoFeeder> feeder_;
    
    // State output
    std::string state_path_;
    std::mutex state_mutex_;
    
    void load_config(const std::string& config_path);
    void init_regions();
    std::string get_phase(const Decision& action) const;
    void write_state(const BrainState& state);
    Decision execute_action(const Decision& action);
};

} // namespace aos_brain

#endif // SEVEN_REGION_BRAIN_HPP
