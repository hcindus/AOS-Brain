// brain/brain_server.hpp
// HTTP and Unix socket server for C++ brain

#ifndef BRAIN_SERVER_HPP
#define BRAIN_SERVER_HPP

#include <string>
#include <memory>
#include <functional>
#include <thread>
#include <atomic>
#include <map>

namespace aos_brain {

class SevenRegionBrain;

// Simple HTTP request/response
struct HttpRequest {
    std::string method;
    std::string path;
    std::map<std::string, std::string> headers;
    std::string body;
};

struct HttpResponse {
    int status_code = 200;
    std::map<std::string, std::string> headers;
    std::string body;
};

// Brain server class
class BrainServer {
public:
    BrainServer(SevenRegionBrain* brain, int http_port = 5000,
                const std::string& socket_path = "/tmp/aos_brain.sock");
    ~BrainServer();
    
    // Start both HTTP and Unix socket servers
    void start();
    
    // Stop servers
    void stop();
    
    // Check if running
    bool is_running() const { return running_.load(); }
    
private:
    SevenRegionBrain* brain_;
    int http_port_;
    std::string socket_path_;
    std::atomic<bool> running_{false};
    
    std::thread http_thread_;
    std::thread socket_thread_;
    
    // HTTP server loop
    void http_server_loop();
    
    // Unix socket server loop
    void socket_server_loop();
    
    // Handle HTTP request
    HttpResponse handle_request(const HttpRequest& req);
    
    // Route handlers
    HttpResponse handle_health();
    HttpResponse handle_status();
    HttpResponse handle_think(const HttpRequest& req);
    HttpResponse handle_memory();
    HttpResponse handle_sheet();
    
    // JSON parsing helper
    std::map<std::string, std::string> parse_json_body(const std::string& body);
};

} // namespace aos_brain

#endif // BRAIN_SERVER_HPP
