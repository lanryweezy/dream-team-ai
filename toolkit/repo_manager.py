"""
Repository Manager
Handles GitHub repository creation, management, and automation
"""

import os
import json
import logging
import subprocess
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class RepoManager:
    def __init__(self, github_token: Optional[str] = None):
        self.github_token = github_token or os.getenv('GITHUB_TOKEN')
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        } if self.github_token else {}
        
    def create_repository(self, 
                         repo_name: str,
                         description: str = "",
                         private: bool = False,
                         auto_init: bool = True,
                         gitignore_template: str = "Node",
                         license_template: str = "mit") -> Dict[str, Any]:
        """Create a new GitHub repository"""
        
        try:
            if not self.github_token:
                return {
                    "success": False,
                    "error": "GitHub token not provided. Set GITHUB_TOKEN environment variable."
                }
            
            # Repository data
            repo_data = {
                "name": repo_name,
                "description": description,
                "private": private,
                "auto_init": auto_init,
                "gitignore_template": gitignore_template,
                "license_template": license_template
            }
            
            # Create repository
            response = requests.post(
                f"{self.base_url}/user/repos",
                headers=self.headers,
                json=repo_data
            )
            
            if response.status_code == 201:
                repo_info = response.json()
                return {
                    "success": True,
                    "repo_url": repo_info["html_url"],
                    "clone_url": repo_info["clone_url"],
                    "ssh_url": repo_info["ssh_url"],
                    "repo_name": repo_name,
                    "full_name": repo_info["full_name"],
                    "created_at": repo_info["created_at"]
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to create repository: {response.json().get('message', 'Unknown error')}"
                }
                
        except Exception as e:
            logger.error(f"Failed to create repository: {e}")
            return {
                "success": False,
                "error": str(e)
            }
            
    def clone_repository(self, repo_url: str, local_path: str) -> Dict[str, Any]:
        """Clone a repository to local directory"""
        
        try:
            # Ensure local path exists
            Path(local_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Clone repository
            result = subprocess.run(
                ["git", "clone", repo_url, local_path],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "local_path": local_path,
                    "message": "Repository cloned successfully"
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr
                }
                
        except Exception as e:
            logger.error(f"Failed to clone repository: {e}")
            return {
                "success": False,
                "error": str(e)
            }
            
    def initialize_project(self, 
                          project_path: str,
                          project_type: str = "web",
                          framework: str = "react") -> Dict[str, Any]:
        """Initialize a new project with boilerplate code"""
        
        try:
            path_obj = Path(project_path)
            path_obj.mkdir(parents=True, exist_ok=True)
            
            if project_type == "web":
                return self._initialize_web_project(path_obj, framework)
            elif project_type == "api":
                return self._initialize_api_project(path_obj, framework)
            elif project_type == "mobile":
                return self._initialize_basic_project(path_obj)  # Fallback for now
            else:
                return self._initialize_basic_project(path_obj)
                
        except Exception as e:
            logger.error(f"Failed to initialize project: {e}")
            return {
                "success": False,
                "error": str(e)
            }
            
    def _initialize_web_project(self, project_path: Path, framework: str) -> Dict[str, Any]:
        """Initialize a web project"""
        
        if framework.lower() == "react":
            return self._create_react_project(project_path)
        elif framework.lower() == "nextjs":
            return self._create_nextjs_project(project_path)
        else:
            return self._create_react_project(project_path)  # Default to React
            
    def _create_react_project(self, project_path: Path) -> Dict[str, Any]:
        """Create a React project structure"""
        
        # Package.json
        package_json = {
            "name": project_path.name,
            "version": "1.0.0",
            "private": True,
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "react-scripts": "5.0.1",
                "web-vitals": "^2.1.4"
            },
            "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build",
                "test": "react-scripts test",
                "eject": "react-scripts eject"
            },
            "eslintConfig": {
                "extends": ["react-app", "react-app/jest"]
            },
            "browserslist": {
                "production": [">0.2%", "not dead", "not op_mini all"],
                "development": ["last 1 chrome version", "last 1 firefox version", "last 1 safari version"]
            }
        }
        
        # Create directories
        (project_path / "src").mkdir(exist_ok=True)
        (project_path / "public").mkdir(exist_ok=True)
        
        # Write package.json
        with open(project_path / "package.json", "w") as f:
            json.dump(package_json, f, indent=2)
            
        # Create App.js
        app_js = '''import React from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to Your New App</h1>
        <p>Start building something amazing!</p>
      </header>
    </div>
  );
}

export default App;'''
        
        with open(project_path / "src" / "App.js", "w") as f:
            f.write(app_js)
            
        # Create App.css
        app_css = '''.App {
  text-align: center;
}

.App-header {
  background-color: #282c34;
  padding: 20px;
  color: white;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: calc(10px + 2vmin);
}

.App-header h1 {
  margin-bottom: 20px;
}

.App-header p {
  font-size: 18px;
  opacity: 0.8;
}'''
        
        with open(project_path / "src" / "App.css", "w") as f:
            f.write(app_css)
            
        # Create index.js
        index_js = '''import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);'''
        
        with open(project_path / "src" / "index.js", "w") as f:
            f.write(index_js)
            
        # Create index.css
        index_css = '''body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}'''
        
        with open(project_path / "src" / "index.css", "w") as f:
            f.write(index_css)
            
        # Create public/index.html
        index_html = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="Web site created using Create React App" />
    <title>React App</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>'''
        
        with open(project_path / "public" / "index.html", "w") as f:
            f.write(index_html)
            
        return {
            "success": True,
            "project_type": "React",
            "files_created": ["package.json", "src/App.js", "src/App.css", "src/index.js", "src/index.css", "public/index.html"],
            "next_steps": ["npm install", "npm start"]
        }
        
    def _create_nextjs_project(self, project_path: Path) -> Dict[str, Any]:
        """Create a Next.js project structure"""
        
        # Package.json
        package_json = {
            "name": project_path.name,
            "version": "0.1.0",
            "private": True,
            "scripts": {
                "dev": "next dev",
                "build": "next build",
                "start": "next start",
                "lint": "next lint"
            },
            "dependencies": {
                "next": "14.0.0",
                "react": "^18",
                "react-dom": "^18"
            },
            "devDependencies": {
                "typescript": "^5",
                "@types/node": "^20",
                "@types/react": "^18",
                "@types/react-dom": "^18",
                "eslint": "^8",
                "eslint-config-next": "14.0.0"
            }
        }
        
        # Create directories
        (project_path / "pages").mkdir(exist_ok=True)
        (project_path / "styles").mkdir(exist_ok=True)
        (project_path / "components").mkdir(exist_ok=True)
        
        # Write package.json
        with open(project_path / "package.json", "w") as f:
            json.dump(package_json, f, indent=2)
            
        # Create pages/index.js
        index_page = '''import Head from 'next/head'
import styles from '../styles/Home.module.css'

export default function Home() {
  return (
    <div className={styles.container}>
      <Head>
        <title>Create Next App</title>
        <meta name="description" content="Generated by create next app" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>
          Welcome to <a href="https://nextjs.org">Next.js!</a>
        </h1>

        <p className={styles.description}>
          Get started by editing{' '}
          <code className={styles.code}>pages/index.js</code>
        </p>

        <div className={styles.grid}>
          <a href="https://nextjs.org/docs" className={styles.card}>
            <h2>Documentation &rarr;</h2>
            <p>Find in-depth information about Next.js features and API.</p>
          </a>

          <a href="https://nextjs.org/learn" className={styles.card}>
            <h2>Learn &rarr;</h2>
            <p>Learn about Next.js in an interactive course with quizzes!</p>
          </a>
        </div>
      </main>
    </div>
  )
}'''
        
        with open(project_path / "pages" / "index.js", "w") as f:
            f.write(index_page)
            
        # Create styles/Home.module.css
        home_css = '''.container {
  padding: 0 2rem;
}

.main {
  min-height: 100vh;
  padding: 4rem 0;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.title {
  margin: 0;
  line-height: 1.15;
  font-size: 4rem;
  text-align: center;
}

.title a {
  color: #0070f3;
  text-decoration: none;
}

.title a:hover,
.title a:focus,
.title a:active {
  text-decoration: underline;
}

.description {
  margin: 4rem 0;
  line-height: 1.5;
  font-size: 1.5rem;
  text-align: center;
}

.code {
  background: #fafafa;
  border-radius: 5px;
  padding: 0.75rem;
  font-size: 1.1rem;
  font-family: Menlo, Monaco, Lucida Console, Liberation Mono, DejaVu Sans Mono,
    Bitstream Vera Sans Mono, Courier New, monospace;
}

.grid {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  max-width: 800px;
}

.card {
  margin: 1rem;
  padding: 1.5rem;
  text-align: left;
  color: inherit;
  text-decoration: none;
  border: 1px solid #eaeaea;
  border-radius: 10px;
  transition: color 0.15s ease, border-color 0.15s ease;
  max-width: 300px;
}

.card:hover,
.card:focus,
.card:active {
  color: #0070f3;
  border-color: #0070f3;
}

.card h2 {
  margin: 0 0 1rem 0;
  font-size: 1.5rem;
}

.card p {
  margin: 0;
  font-size: 1.25rem;
  line-height: 1.5;
}'''
        
        with open(project_path / "styles" / "Home.module.css", "w") as f:
            f.write(home_css)
            
        # Create styles/globals.css
        globals_css = '''html,
body {
  padding: 0;
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen,
    Ubuntu, Cantarell, Fira Sans, Droid Sans, Helvetica Neue, sans-serif;
}

a {
  color: inherit;
  text-decoration: none;
}

* {
  box-sizing: border-box;
}'''
        
        with open(project_path / "styles" / "globals.css", "w") as f:
            f.write(globals_css)
            
        # Create pages/_app.js
        app_js = '''import '../styles/globals.css'

export default function App({ Component, pageProps }) {
  return <Component {...pageProps} />
}'''
        
        with open(project_path / "pages" / "_app.js", "w") as f:
            f.write(app_js)
            
        return {
            "success": True,
            "project_type": "Next.js",
            "files_created": ["package.json", "pages/index.js", "pages/_app.js", "styles/Home.module.css", "styles/globals.css"],
            "next_steps": ["npm install", "npm run dev"]
        }
        
    def _initialize_api_project(self, project_path: Path, framework: str) -> Dict[str, Any]:
        """Initialize an API project"""
        
        if framework.lower() == "fastapi":
            return self._create_fastapi_project(project_path)
        else:
            return self._create_fastapi_project(project_path)  # Default to FastAPI
            
    def _create_fastapi_project(self, project_path: Path) -> Dict[str, Any]:
        """Create a FastAPI project structure"""
        
        # Create directories
        (project_path / "app").mkdir(exist_ok=True)
        (project_path / "app" / "routers").mkdir(exist_ok=True)
        
        # Requirements.txt
        requirements = '''fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-decouple==3.8'''
        
        with open(project_path / "requirements.txt", "w") as f:
            f.write(requirements)
            
        # Main application
        main_py = '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, users

app = FastAPI(
    title="API Server",
    description="A FastAPI server with authentication",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(users.router, prefix="/users", tags=["users"])

@app.get("/")
async def root():
    return {"message": "Welcome to the API server!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}'''
        
        with open(project_path / "main.py", "w") as f:
            f.write(main_py)
            
        # App __init__.py
        with open(project_path / "app" / "__init__.py", "w") as f:
            f.write("")
            
        # Auth router
        auth_router = '''from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest):
    # Implement your authentication logic here
    if login_data.username == "admin" and login_data.password == "password":
        return {"access_token": "fake-jwt-token", "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/register")
async def register(login_data: LoginRequest):
    # Implement user registration logic here
    return {"message": "User registered successfully"}'''
        
        with open(project_path / "app" / "routers" / "auth.py", "w") as f:
            f.write(auth_router)
            
        # Users router
        users_router = '''from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

class User(BaseModel):
    id: int
    username: str
    email: str

# Mock data
users_db = [
    {"id": 1, "username": "john_doe", "email": "john@example.com"},
    {"id": 2, "username": "jane_smith", "email": "jane@example.com"}
]

@router.get("/", response_model=List[User])
async def get_users():
    return users_db

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=User)
async def create_user(user: User):
    users_db.append(user.dict())
    return user'''
        
        with open(project_path / "app" / "routers" / "users.py", "w") as f:
            f.write(users_router)
            
        # Routers __init__.py
        with open(project_path / "app" / "routers" / "__init__.py", "w") as f:
            f.write("")
            
        return {
            "success": True,
            "project_type": "FastAPI",
            "files_created": ["main.py", "requirements.txt", "app/routers/auth.py", "app/routers/users.py"],
            "next_steps": ["pip install -r requirements.txt", "uvicorn main:app --reload"]
        }
        
    def _initialize_basic_project(self, project_path: Path) -> Dict[str, Any]:
        """Initialize a basic project structure"""
        
        # Create basic directories
        (project_path / "src").mkdir(exist_ok=True)
        (project_path / "tests").mkdir(exist_ok=True)
        (project_path / "docs").mkdir(exist_ok=True)
        
        # Create README.md
        readme = f'''# {project_path.name}

## Description
A new project created with Dream Machine.

## Getting Started

### Prerequisites
- Node.js (for web projects)
- Python (for API projects)

### Installation
1. Clone the repository
2. Install dependencies
3. Run the project

## Usage
Describe how to use your project here.

## Contributing
1. Fork the project
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License
This project is licensed under the MIT License.
'''
        
        with open(project_path / "README.md", "w") as f:
            f.write(readme)
            
        # Create .gitignore
        gitignore = '''# Dependencies
node_modules/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Runtime data
pids/
*.pid
*.seed

# Coverage directory used by tools like istanbul
coverage/

# Build outputs
dist/
build/
*.egg-info/

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local'''
        
        with open(project_path / ".gitignore", "w") as f:
            f.write(gitignore)
            
        return {
            "success": True,
            "project_type": "Basic",
            "files_created": ["README.md", ".gitignore", "src/", "tests/", "docs/"],
            "next_steps": ["Add your project files", "Initialize git repository"]
        }
        
    def commit_and_push(self, 
                       repo_path: str,
                       commit_message: str = "Initial commit",
                       branch: str = "main") -> Dict[str, Any]:
        """Commit changes and push to repository"""
        
        try:
            os.chdir(repo_path)
            
            # Add all files
            subprocess.run(["git", "add", "."], check=True)
            
            # Commit changes
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            
            # Push to remote
            subprocess.run(["git", "push", "origin", branch], check=True)
            
            return {
                "success": True,
                "message": f"Changes committed and pushed to {branch} branch"
            }
            
        except subprocess.CalledProcessError as e:
            return {
                "success": False,
                "error": f"Git operation failed: {e}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
            
    def create_branch(self, repo_path: str, branch_name: str) -> Dict[str, Any]:
        """Create and switch to a new branch"""
        
        try:
            os.chdir(repo_path)
            
            # Create and switch to new branch
            subprocess.run(["git", "checkout", "-b", branch_name], check=True)
            
            return {
                "success": True,
                "branch": branch_name,
                "message": f"Created and switched to branch '{branch_name}'"
            }
            
        except subprocess.CalledProcessError as e:
            return {
                "success": False,
                "error": f"Failed to create branch: {e}"
            }
            
    def setup_ci_cd(self, repo_path: str, platform: str = "github") -> Dict[str, Any]:
        """Setup CI/CD pipeline"""
        
        try:
            if platform.lower() == "github":
                return self._setup_github_actions(repo_path)
            else:
                return {
                    "success": False,
                    "error": f"Platform '{platform}' not supported yet"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
            
    def _setup_github_actions(self, repo_path: str) -> Dict[str, Any]:
        """Setup GitHub Actions workflow"""
        
        # Create .github/workflows directory
        workflows_dir = Path(repo_path) / ".github" / "workflows"
        workflows_dir.mkdir(parents=True, exist_ok=True)
        
        # Create CI workflow
        ci_workflow = '''name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        node-version: [16.x, 18.x]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v3
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'
    
    - run: npm ci
    - run: npm run build --if-present
    - run: npm test --if-present
    
  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to production
      run: |
        echo "Deploy to production server"
        # Add your deployment commands here
'''
        
        with open(workflows_dir / "ci.yml", "w") as f:
            f.write(ci_workflow)
            
        return {
            "success": True,
            "workflow_file": str(workflows_dir / "ci.yml"),
            "message": "GitHub Actions CI/CD pipeline created"
        }

# Example usage
def main():
    """Example usage of RepoManager"""
    
    manager = RepoManager()
    
    # Create repository
    repo_result = manager.create_repository(
        repo_name="my-awesome-app",
        description="An awesome web application",
        private=False
    )
    
    print("Repository creation result:")
    print(json.dumps(repo_result, indent=2))
    
    # Initialize project
    if repo_result["success"]:
        project_result = manager.initialize_project(
            project_path="./my-awesome-app",
            project_type="web",
            framework="react"
        )
        
        print("\nProject initialization result:")
        print(json.dumps(project_result, indent=2))

if __name__ == "__main__":
    main()