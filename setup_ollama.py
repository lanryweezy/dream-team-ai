"""
Setup script for Ollama integration
Helps users set up Ollama for local LLM testing
"""

import asyncio
import subprocess
import sys
import platform
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaSetup:
    """Helper class for Ollama setup"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.recommended_models = [
            "llama2",           # Good general purpose model
            "codellama",        # Good for code generation
            "mistral",          # Fast and efficient
            "llama2:13b",       # Larger model for better quality
        ]
        
    def check_ollama_installed(self) -> bool:
        """Check if Ollama is installed"""
        try:
            result = subprocess.run(
                ["ollama", "--version"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            if result.returncode == 0:
                print(f"✅ Ollama is installed: {result.stdout.strip()}")
                return True
            else:
                print("❌ Ollama is not installed or not in PATH")
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("❌ Ollama is not installed or not in PATH")
            return False
            
    def check_ollama_running(self) -> bool:
        """Check if Ollama service is running"""
        try:
            result = subprocess.run(
                ["ollama", "list"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            if result.returncode == 0:
                print("✅ Ollama service is running")
                return True
            else:
                print("❌ Ollama service is not running")
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("❌ Cannot connect to Ollama service")
            return False
            
    def list_installed_models(self) -> list:
        """List installed Ollama models"""
        try:
            result = subprocess.run(
                ["ollama", "list"], 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                models = []
                for line in lines:
                    if line.strip():
                        model_name = line.split()[0]
                        models.append(model_name)
                return models
            return []
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []
            
    def pull_model(self, model_name: str) -> bool:
        """Pull/download a model"""
        try:
            print(f"📥 Pulling model: {model_name}")
            print("This may take several minutes depending on model size...")
            
            result = subprocess.run(
                ["ollama", "pull", model_name], 
                timeout=1800  # 30 minutes timeout
            )
            
            if result.returncode == 0:
                print(f"✅ Successfully pulled model: {model_name}")
                return True
            else:
                print(f"❌ Failed to pull model: {model_name}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"⏰ Timeout pulling model: {model_name}")
            return False
        except Exception as e:
            print(f"❌ Error pulling model {model_name}: {e}")
            return False
            
    def start_ollama_service(self) -> bool:
        """Start Ollama service"""
        try:
            if self.system == "windows":
                print("🔧 On Windows, Ollama should start automatically after installation")
                print("If not, try running 'ollama serve' in a separate terminal")
                return True
            elif self.system in ["linux", "darwin"]:  # macOS is darwin
                print("🔧 Starting Ollama service...")
                subprocess.Popen(["ollama", "serve"])
                # Give it a moment to start
                import time
                time.sleep(3)
                return self.check_ollama_running()
            else:
                print(f"❓ Unknown system: {self.system}")
                return False
        except Exception as e:
            print(f"❌ Error starting Ollama service: {e}")
            return False
            
    def print_installation_instructions(self):
        """Print installation instructions for different platforms"""
        print("\n📋 Ollama Installation Instructions")
        print("=" * 40)
        
        if self.system == "windows":
            print("Windows:")
            print("1. Download from: https://ollama.ai/download/windows")
            print("2. Run the installer")
            print("3. Restart your terminal")
            
        elif self.system == "darwin":  # macOS
            print("macOS:")
            print("1. Download from: https://ollama.ai/download/mac")
            print("2. Or use Homebrew: brew install ollama")
            
        elif self.system == "linux":
            print("Linux:")
            print("1. Run: curl -fsSL https://ollama.ai/install.sh | sh")
            print("2. Or download from: https://ollama.ai/download/linux")
            
        print("\nAfter installation:")
        print("1. Open a new terminal")
        print("2. Run: ollama serve")
        print("3. In another terminal, run: ollama pull llama2")
        
    async def setup_interactive(self):
        """Interactive setup process"""
        print("🚀 Dream Machine - Ollama Setup")
        print("=" * 40)
        
        # Check if Ollama is installed
        if not self.check_ollama_installed():
            self.print_installation_instructions()
            return False
            
        # Check if service is running
        if not self.check_ollama_running():
            print("\n🔧 Attempting to start Ollama service...")
            if not self.start_ollama_service():
                print("❌ Could not start Ollama service")
                print("💡 Try running 'ollama serve' in a separate terminal")
                return False
                
        # List installed models
        models = self.list_installed_models()
        if models:
            print(f"\n✅ Installed models: {', '.join(models)}")
        else:
            print("\n❌ No models installed")
            
            # Ask user if they want to install a model
            print("\n🤖 Recommended models for Dream Machine:")
            for i, model in enumerate(self.recommended_models, 1):
                print(f"  {i}. {model}")
                
            try:
                choice = input("\nEnter number to install a model (or 'skip' to skip): ").strip()
                
                if choice.lower() != 'skip':
                    try:
                        model_index = int(choice) - 1
                        if 0 <= model_index < len(self.recommended_models):
                            model_name = self.recommended_models[model_index]
                            success = self.pull_model(model_name)
                            if success:
                                models = [model_name]
                            else:
                                return False
                        else:
                            print("❌ Invalid choice")
                            return False
                    except ValueError:
                        print("❌ Invalid input")
                        return False
                        
            except KeyboardInterrupt:
                print("\n👋 Setup cancelled")
                return False
                
        if models:
            print(f"\n🎉 Ollama setup complete!")
            print(f"Available models: {', '.join(models)}")
            print("\n🧪 Run 'python test_ollama_integration.py' to test the integration")
            return True
        else:
            print("\n❌ No models available. Please install at least one model.")
            return False

async def main():
    """Main setup function"""
    setup = OllamaSetup()
    success = await setup.setup_interactive()
    
    if success:
        print("\n✅ Setup completed successfully!")
        
        # Ask if user wants to run tests
        try:
            run_tests = input("\n🧪 Run integration tests now? (y/n): ").strip().lower()
            if run_tests in ['y', 'yes']:
                print("\n" + "="*50)
                from test_ollama_integration import main as test_main
                await test_main()
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
    else:
        print("\n❌ Setup failed. Please check the instructions above.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())