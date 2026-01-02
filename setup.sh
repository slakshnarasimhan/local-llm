#!/bin/bash
# Quick setup script for RAG Chatbot Demo

set -e

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                                                                   ║"
echo "║        RAG CHATBOT SETUP - Cloud ☁️  ↔️  Local 💻                ║"
echo "║                                                                   ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi
echo "✅ Python found"
echo ""

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp config.env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your OpenAI API key if you want to use cloud LLM"
    echo "   Or set LLM_PROVIDER=ollama to use local LLM only"
else
    echo "✅ .env file already exists"
fi
echo ""

# Check if Ollama is installed
echo "Checking for Ollama installation..."
if command -v ollama &> /dev/null; then
    echo "✅ Ollama is installed"
    
    # Check if models are available
    echo ""
    echo "Checking for Ollama models..."
    if ollama list | grep -q "llama3"; then
        echo "✅ llama3 model found"
    else
        echo "⚠️  llama3 model not found"
        echo ""
        read -p "Would you like to download llama3 now? (y/n) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "Downloading llama3 (this may take several minutes)..."
            ollama pull llama3
            echo "✅ llama3 downloaded"
        else
            echo "⏭️  Skipping model download"
            echo "   You can download it later with: ollama pull llama3"
        fi
    fi
else
    echo "⚠️  Ollama not found"
    echo ""
    echo "To use local LLMs, install Ollama:"
    echo "  curl -fsSL https://ollama.com/install.sh | sh"
    echo ""
    echo "Then download a model:"
    echo "  ollama pull llama3"
fi
echo ""

echo "═══════════════════════════════════════════════════════════════════"
echo "✅ Setup Complete!"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo ""
echo "1. Activate the virtual environment (if not already active):"
echo "   source venv/bin/activate"
echo ""
echo "2. Configure your settings:"
echo "   - Edit .env file to set your OpenAI API key (for cloud mode)"
echo "   - Or set LLM_PROVIDER=ollama (for local mode)"
echo ""
echo "3. Run the demo:"
echo "   python demo.py              # Quick demo with local LLM"
echo "   python demo.py compare      # Compare cloud vs local"
echo "   python chatbot_cli.py       # Interactive chat mode"
echo ""
echo "4. Read the documentation:"
echo "   cat README.md"
echo ""
echo "═══════════════════════════════════════════════════════════════════"

