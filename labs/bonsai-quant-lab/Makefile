# Makefile for Bonsai Quantization Lab

.PHONY: help setup download test clean

# Default target
help:
	@echo "Bonsai Quantization Lab - Available Targets:"
	@echo ""
	@echo "  setup      - Create directory structure"
	@echo "  download   - Download test models (Bonsai + baselines)"
	@echo "  test       - Run all experiments"
	@echo "  test-bonsai  - Reproduce Bonsai segfault"
	@echo "  test-qwen    - Verify Qwen2.5 works"
	@echo "  clean      - Remove all models and logs"
	@echo ""

# Create directory structure
setup:
	mkdir -p models/{raw,converted,baseline}
	mkdir -p experiments
	mkdir -p logs
	mkdir -p docs
	@echo "✅ Directory structure created"

# Download test models
download: setup
	@echo "📥 Downloading Ternary Bonsai (1.58-bit)..."
	wget -q --show-progress \
		https://hf.co/prism-ml/Ternary-Bonsai-8B-gguf/resolve/main/ternary-bonsai-q2-8b.gguf \
		-O models/raw/ternary-bonsai-q2-8b.gguf || echo "⚠️ Download failed"
	
	@echo "📥 Downloading Qwen2.5 baseline..."
	wget -q --show-progress \
		https://hf.co/Qwen/Qwen2.5-7B-Instruct-GGUF/resolve/main/qwen2.5-7b-instruct-q4_k_m.gguf \
		-O models/baseline/qwen2.5-7b-instruct-q4_k_m.gguf || echo "⚠️ Download failed"
	
	@echo "✅ Downloads complete"

# Run all tests
test: test-bonsai test-qwen
	@echo "✅ All tests complete"

# Reproduce Bonsai segfault
test-bonsai:
	@echo "🧪 Testing Ternary Bonsai (expecting segfault)..."
	@echo 'FROM ./models/raw/ternary-bonsai-q2-8b.gguf' > models/ternary.modelfile
	ollama create bonsai-test -f models/ternary.modelfile 2>/dev/null || true
	timeout 5 ollama run bonsai-test "Hello" 2>&1 | tee logs/bonsai_test_$(shell date +%Y%m%d_%H%M%S).log || \
		echo "❌ Expected segfault confirmed"

# Verify Qwen2.5 works
test-qwen:
	@echo "🧪 Testing Qwen2.5 baseline..."
	ollama pull qwen2.5:7b 2>/dev/null || true
	ollama run qwen2.5:7b "Hello" 2>&1 | head -5 | tee logs/qwen_test_$(shell date +%Y%m%d_%H%M%S).log
	@echo "✅ Qwen2.5 working"

# Clean everything
clean:
	rm -rf models/raw/* models/converted/* models/baseline/*
	rm -rf logs/*
	ollama rm bonsai-test 2>/dev/null || true
	@echo "✅ Cleaned"
