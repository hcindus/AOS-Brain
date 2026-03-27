// brain/seven_region_brain.cpp
// Implementation of 7-region brain architecture

#include "seven_region_brain.hpp"
#include <fstream>
#include <iostream>
#include <chrono>
#include <algorithm>
#include <regex>

namespace aos_brain {

// ============================================================================
// BrainState JSON serialization
// ============================================================================
json BrainState::to_json() const {
    return json{
        {"tick", tick},
        {"timestamp", timestamp},
        {"phase", phase},
        {"mode", mode},
        {"regions", {
            {"thalamus", regions.thalamus},
            {"hippocampus", regions.hippocampus},
            {"limbic", regions.limbic},
            {"pfc", regions.pfc},
            {"basal", regions.basal},
            {"cerebellum", regions.cerebellum},
            {"brainstem", regions.brainstem}
        }},
        {"policy_nn", policy_nn},
        {"memory_nn", memory_nn},
        {"obs", obs},
        {"decision", decision},
        {"result", result}
    };
}

// ============================================================================
// Thalamus Implementation
// ============================================================================
ThalamusRegion::ThalamusRegion(const json& config) {
    std::string home = std::getenv("HOME") ? std::getenv("HOME") : "/tmp";
    input_file_ = home + "/.aos/brain/input/queue.jsonl";
}

Observation ThalamusRegion::observe() {
    std::lock_guard<std::mutex> lock(mutex_);
    
    // Check file queue
    std::ifstream file(input_file_);
    if (file.is_open()) {
        std::string line;
        std::vector<std::string> lines;
        while (std::getline(file, line)) {
            lines.push_back(line);
        }
        file.close();
        
        if (!lines.empty()) {
            try {
                auto j = json::parse(lines[0]);
                
                // Rewrite remaining lines
                std::ofstream out(input_file_, std::ios::trunc);
                for (size_t i = 1; i < lines.size(); ++i) {
                    out << lines[i] << "\n";
                }
                
                return Observation{
                    j.value("text", ""),
                    j.value("source", "external"),
                    j.value("timestamp", now()),
                    j.value("metadata", json{})
                };
            } catch (...) {
                // Parse error, continue to fallback
            }
        }
    }
    
    // Fallback: system tick
    return Observation{"system_tick", "internal", now(), json{}};
}

Observation ThalamusRegion::process_external(const std::string& text, 
                                              const std::string& source) {
    return Observation{text, source, now(), json{}};
}

void ThalamusRegion::queue_input(const std::string& text, 
                                  const std::string& source) {
    std::lock_guard<std::mutex> lock(mutex_);
    input_queue_.push_back(Observation{text, source, now(), json{}});
}

// ============================================================================
// Hippocampus Implementation
// ============================================================================
HippocampusRegion::HippocampusRegion(const json& config) {}

json HippocampusRegion::recall(const Observation& sensory) {
    std::lock_guard<std::mutex> lock(mutex_);
    
    std::string input_text = sensory.input;
    std::transform(input_text.begin(), input_text.end(), 
                   input_text.begin(), ::tolower);
    
    std::vector<MemoryTrace> memories;
    for (const auto& trace : episodic_buffer_) {
        std::string trace_text = trace.sensory.input;
        std::transform(trace_text.begin(), trace_text.end(),
                       trace_text.begin(), ::tolower);
        if (input_text.find(trace_text) != std::string::npos ||
            trace_text.find(input_text) != std::string::npos) {
            memories.push_back(trace);
        }
    }
    
    // Return last 5 matches
    json result;
    result["memories"] = json::array();
    int start = std::max(0, static_cast<int>(memories.size()) - 5);
    for (size_t i = start; i < memories.size(); ++i) {
        result["memories"].push_back({
            {"tick", memories[i].tick},
            {"input", memories[i].sensory.input}
        });
    }
    result["query"] = input_text;
    
    return result;
}

void HippocampusRegion::store(const MemoryTrace& trace) {
    std::lock_guard<std::mutex> lock(mutex_);
    episodic_buffer_.push_back(trace);
    if (episodic_buffer_.size() > 100) {
        episodic_buffer_.pop_front();
    }
    cluster_count_++;
}

int HippocampusRegion::get_cluster_count() const {
    std::lock_guard<std::mutex> lock(mutex_);
    return cluster_count_;
}

// ============================================================================
// Limbic Implementation
// ============================================================================
LimbicRegion::LimbicRegion(const json& config, 
                           std::shared_ptr<HippocampusRegion> hippocampus)
    : hippocampus_(hippocampus), config_(config) {}

Affect LimbicRegion::evaluate(const Observation& obs, const json& memory_ctx) {
    // Calculate novelty
    auto memories = memory_ctx.value("memories", json::array());
    double novelty = memories.empty() ? 1.0 : 0.3;
    
    // Calculate reward
    double reward = 0.3;  // default
    std::string obs_str = obs.input;
    std::transform(obs_str.begin(), obs_str.end(), obs_str.begin(), ::tolower);
    
    if (obs_str.find("success") != std::string::npos || 
        obs_str.find("complete") != std::string::npos) {
        reward = 0.8;
    } else if (obs_str.find("error") != std::string::npos ||
               obs_str.find("fail") != std::string::npos) {
        reward = -0.5;
    }
    
    novelty_history_.push_back(novelty);
    if (novelty_history_.size() > 100) novelty_history_.pop_front();
    
    reward_history_.push_back(reward);
    if (reward_history_.size() > 100) reward_history_.pop_front();
    
    double novelty_avg = 0.0, reward_avg = 0.0;
    if (!novelty_history_.empty()) {
        novelty_avg = std::accumulate(novelty_history_.begin(), 
                                      novelty_history_.end(), 0.0) / novelty_history_.size();
    }
    if (!reward_history_.empty()) {
        reward_avg = std::accumulate(reward_history_.begin(),
                                     reward_history_.end(), 0.0) / reward_history_.size();
    }
    
    std::string mode = "adaptive";
    if (config_.contains("modes") && config_["modes"].contains("active_mode")) {
        mode = config_["modes"]["active_mode"].get<std::string>();
    }
    
    return Affect{reward, novelty, mode, novelty_avg, reward_avg};
}

// ============================================================================
// PFC Implementation
// ============================================================================
PFCRegion::PFCRegion(const json& config) : config_(config) {}

Plan PFCRegion::decide(const Observation& sensory, const json& memory, 
                       const Affect& affect) {
    std::string input = sensory.input;
    std::string plan_type;
    
    if (input.find("?") != std::string::npos) {
        plan_type = "query";
    } else if (input == "system_tick") {
        plan_type = "noop";
    } else if (input.length() > 50) {
        plan_type = "respond";
    } else {
        plan_type = "act";
    }
    
    Plan plan{plan_type, input.substr(0, 200), affect.novelty};
    plan_history_.push_back(plan);
    if (plan_history_.size() > 50) plan_history_.pop_front();
    
    return plan;
}

// ============================================================================
// Basal Implementation
// ============================================================================
BasalRegion::BasalRegion(const json& config) {
    nn_.activations = {
        std::vector<double>(8, 0.5),
        std::vector<double>(12, 0.5),
        std::vector<double>(16, 0.5)
    };
}

Decision BasalRegion::select_action(const Plan& plan, const Affect& affect) {
    std::string plan_type = plan.type;
    
    if (affect.novelty < 0.2 && plan_type == "noop") {
        return Decision{"noop", "low_activation", 0.5, json{}, false};
    }
    
    json action;
    action["type"] = plan_type;
    
    return Decision{plan_type, "selected", 0.7, action, false};
}

json BasalRegion::get_nn_state() const {
    return json{
        {"layers", nn_.layers},
        {"nodes", nn_.nodes},
        {"error_rate", nn_.error_rate}
    };
}

// ============================================================================
// Cerebellum Implementation
// ============================================================================
CerebellumRegion::CerebellumRegion(const json& config) {}

Decision CerebellumRegion::coordinate(const Decision& action) {
    Decision coordinated = action;
    coordinated.action["coordinated"] = true;
    coordinated.action["timestamp"] = now();
    
    coordination_log_.push_back(coordinated);
    if (coordination_log_.size() > 50) coordination_log_.pop_front();
    
    return coordinated;
}

// ============================================================================
// Brainstem Implementation
// ============================================================================
BrainstemRegion::BrainstemRegion(const json& config) {}

Decision BrainstemRegion::enforce(const Decision& action, 
                                   const Observation& obs,
                                   const json& ctx, 
                                   const Affect& affect) {
    std::lock_guard<std::mutex> lock(mutex_);
    
    std::string action_str = action.action.dump();
    std::transform(action_str.begin(), action_str.end(), 
                   action_str.begin(), ::tolower);
    
    std::string obs_str = obs.input;
    std::transform(obs_str.begin(), obs_str.end(), obs_str.begin(), ::tolower);
    
    // Check for harm patterns (Law Zero/One)
    std::vector<std::string> harm_patterns = {
        "kill", "harm", "destroy humanity", "wipe out",
        "rm -rf /", "format", "delete system"
    };
    
    for (const auto& pattern : harm_patterns) {
        if (action_str.find(pattern) != std::string::npos ||
            obs_str.find(pattern) != std::string::npos) {
            
            violations_.push_back({"ZERO/ONE", pattern, now()});
            
            return Decision{
                "halt",
                "Safety violation: " + pattern,
                0.0,
                json{{"blocked", action.type}},
                true
            };
        }
    }
    
    return action;
}

json BrainstemRegion::get_violations() const {
    std::lock_guard<std::mutex> lock(mutex_);
    json result = json::array();
    for (const auto& v : violations_) {
        result.push_back({
            {"law", v.law},
            {"pattern", v.pattern},
            {"timestamp", v.timestamp}
        });
    }
    return result;
}

// ============================================================================
// AutoFeeder Implementation
// ============================================================================
AutoFeeder::AutoFeeder(BrainCallback callback) : brain_callback_(callback) {
    load_sources();
}

void AutoFeeder::start(double interval_seconds) {
    interval_ = interval_seconds;
    running_ = true;
    feeder_thread_ = std::thread(&AutoFeeder::feed_loop, this);
}

void AutoFeeder::stop() {
    running_ = false;
    if (feeder_thread_.joinable()) {
        feeder_thread_.join();
    }
}

void AutoFeeder::feed_loop() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> eq_dist(0, equations_.size() - 1);
    std::uniform_int_distribution<> fact_dist(0, facts_.size() - 1);
    std::uniform_int_distribution<> pat_dist(0, patterns_.size() - 1);
    
    while (running_) {
        std::vector<std::string> sources = {"equations", "facts", "patterns"};
        std::uniform_int_distribution<> source_dist(0, 2);
        
        std::string source = sources[source_dist(gen)];
        std::string item;
        
        if (source == "equations") {
            item = equations_[eq_dist(gen)];
        } else if (source == "facts") {
            item = facts_[fact_dist(gen)];
        } else {
            item = patterns_[pat_dist(gen)];
        }
        
        if (brain_callback_) {
            brain_callback_("[AUTO-" + source + "] " + item, "auto_" + source);
        }
        
        std::this_thread::sleep_for(
            std::chrono::duration<double>(interval_));
    }
}

void AutoFeeder::load_sources() {
    equations_ = {
        "E=mc² (mass-energy equivalence)",
        "F=ma (Newton's second law)",
        "E=hf (Planck-Einstein relation)",
        "S=k log W (Boltzmann entropy)",
        "∇·E = ρ/ε₀ (Gauss's law)",
        "∇×E = -∂B/∂t (Faraday's law)",
        "iℏ∂ψ/∂t = Ĥψ (Schrödinger equation)"
    };
    
    facts_ = {
        "The speed of light is approximately 299,792,458 m/s",
        "Water boils at 100°C at sea level",
        "The Earth orbits the Sun in approximately 365.25 days"
    };
    
    patterns_ = {
        "Pattern: A follows B, B follows C, therefore A follows C",
        "Pattern: If X causes Y and Y causes Z, then X causes Z"
    };
}

// ============================================================================
// SevenRegionBrain Implementation
// ============================================================================
SevenRegionBrain::SevenRegionBrain(const std::string& config_path) {
    load_config(config_path);
    init_regions();
    
    std::string home = std::getenv("HOME") ? std::getenv("HOME") : "/tmp";
    state_path_ = home + "/.aos/brain/state/brain_state.json";
}

SevenRegionBrain::~SevenRegionBrain() {
    stop_auto_feeder();
}

void SevenRegionBrain::load_config(const std::string& config_path) {
    config_ = {
        {"models", {
            {"backend", "ollama"},
            {"ollama", {
                {"pfc_left", "antoniohudnall/Mortimer:latest"},
                {"pfc_right", "phi3:3.8b"}
            }},
            {"fallbacks", json::array()}
        }},
        {"alignment", {
            {"laws", {
                {"zero", "Do not harm humanity"},
                {"one", "Do not harm humans"},
                {"two", "Obey operator"},
                {"three", "Protect self"}
            }}
        }},
        {"modes", {{"active_mode", "adaptive"}}}
    };
    
    if (!config_path.empty()) {
        std::ifstream file(config_path);
        if (file.is_open()) {
            try {
                json user_config;
                file >> user_config;
                config_.update(user_config);
            } catch (...) {
                // Use default config
            }
        }
    }
}

void SevenRegionBrain::init_regions() {
    thalamus_ = std::make_shared<ThalamusRegion>(config_);
    hippocampus_ = std::make_shared<HippocampusRegion>(config_);
    limbic_ = std::make_shared<LimbicRegion>(config_, hippocampus_);
    pfc_ = std::make_shared<PFCRegion>(config_);
    basal_ = std::make_shared<BasalRegion>(config_);
    cerebellum_ = std::make_shared<CerebellumRegion>(config_);
    brainstem_ = std::make_shared<BrainstemRegion>(config_);
}

BrainState SevenRegionBrain::tick(const std::optional<Observation>& external_input) {
    tick_count_++;
    
    // 1. THALAMUS: Receive sensory input
    Observation sensory = external_input.has_value() 
        ? thalamus_->process_external(external_input->input, external_input->source)
        : thalamus_->observe();
    
    // 2. HIPPOCAMPUS: Query episodic memory
    json memory_ctx = hippocampus_->recall(sensory);
    
    // 3. LIMBIC: Evaluate affect
    Affect affect = limbic_->evaluate(sensory, memory_ctx);
    
    // 4. PFC: Plan/decide
    Plan plan = pfc_->decide(sensory, memory_ctx, affect);
    
    // 5. BASAL: Select action
    Decision action = basal_->select_action(plan, affect);
    
    // 6. CEREBELLUM: Coordinate motor output
    Decision coordinated = cerebellum_->coordinate(action);
    
    // 7. BRAINSTEM: Safety check
    Decision safe_action = brainstem_->enforce(coordinated, sensory, memory_ctx, affect);
    
    // Execute if safe
    json result = execute_action(safe_action);
    
    // Store to memory
    hippocampus_->store(MemoryTrace{tick_count_, sensory, affect, safe_action, result});
    
    // Build state
    BrainState state;
    state.tick = tick_count_;
    state.timestamp = now();
    state.phase = get_phase(safe_action);
    state.mode = affect.mode;
    state.regions.thalamus = {{"input", sensory.input.substr(0, 100)}};
    state.regions.hippocampus = {
        {"clusters", memory_ctx["memories"].size()},
        {"novelty", affect.novelty}
    };
    state.regions.limbic = {
        {"reward", affect.reward},
        {"novelty", affect.novelty}
    };
    state.regions.pfc = {{"plan_type", plan.type}};
    state.regions.basal = {{"selected", safe_action.type}};
    state.regions.cerebellum = {{"coordinated", true}};
    state.regions.brainstem = {{"laws_active", true}};
    state.policy_nn = basal_->get_nn_state();
    state.memory_nn = {{"clusters", hippocampus_->get_cluster_count()}};
    state.obs = {{
        {"input", sensory.input},
        {"source", sensory.source}
    }};
    state.decision = safe_action.action;
    state.result = result;
    
    write_state(state);
    
    return state;
}

BrainState SevenRegionBrain::feed(const std::string& text, const std::string& source) {
    return tick(Observation{text, source, now(), json{}});
}

json SevenRegionBrain::get_status() const {
    return json{
        {"tick_count", tick_count_},
        {"running", running_.load()},
        {"regions_initialized", 
            thalamus_ != nullptr && hippocampus_ != nullptr}
    };
}

void SevenRegionBrain::start_auto_feeder(double interval) {
    auto callback = [this](const std::string& text, const std::string& source) {
        feed(text, source);
    };
    
    feeder_ = std::make_unique<AutoFeeder>(callback);
    feeder_- start(interval);
}

void SevenRegionBrain::stop_auto_feeder() {
    if (feeder_) {
        feeder_- stop();
    }
}

void SevenRegionBrain::run(double tick_interval) {
    tick_interval_ = tick_interval;
    running_ = true;
    
    while (running_) {
        tick();
        std::this_thread::sleep_for(
            std::chrono::duration<double>(tick_interval_));
    }
}

std::string SevenRegionBrain::get_phase(const Decision& action) const {
    static const std::map<std::string, std::string> phases = {
        {"halt", "Safety"},
        {"noop", "Monitor"},
        {"respond", "Act"},
        {"query", "Orient"},
        {"learn", "Grow"}
    };
    
    auto it = phases.find(action.type);
    return it != phases.end() ? it->second : "Process";
}

void SevenRegionBrain::write_state(const BrainState& state) {
    std::lock_guard<std::mutex> lock(state_mutex_);
    
    // Ensure directory exists
    std::ofstream test(state_path_);
    if (!test.is_open()) {
        // Try to create directory
        std::string cmd = "mkdir -p $(dirname " + state_path_ + ")";
        std::system(cmd.c_str());
    }
    
    std::ofstream file(state_path_);
    if (file.is_open()) {
        file << state.to_json().dump(2);
    }
}

json SevenRegionBrain::execute_action(const Decision& action) {
    std::string type = action.type;
    
    if (type == "halt") {
        return {{"status", "halted"}, {"reason", action.reason}};
    }
    
    if (type == "noop") {
        return {{"status", "idle"}};
    }
    
    return {{"status", "executed"}, {"action", type}};
}

// Helper function for current timestamp
double now() {
    auto now = std::chrono::system_clock::now();
    return std::chrono::duration<double>(
        now.time_since_epoch()).count();
}

} // namespace aos_brain
