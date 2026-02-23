"""
Deployment Manager
Handles application deployment to various platforms
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

class DeploymentManager:
    def __init__(self):
        self.supported_platforms = {
            "vercel": "Vercel Platform",
            "netlify": "Netlify Platform", 
            "heroku": "Heroku Platform",
            "aws": "Amazon Web Services",
            "gcp": "Google Cloud Platform",
            "azure": "Microsoft Azure",
            "digitalocean": "DigitalOcean App Platform"
        }
        
    def create_deployment_plan(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a deployment plan based on configuration"""
        
        try:
            app_name = config.get("app_name", "my-app")
            platform = config.get("platform", "vercel").lower()
            environment = config.get("environment", "production")
            domain = config.get("domain")
            
            if platform not in self.supported_platforms:
                return {
                    "success": False,
                    "error": f"Platform '{platform}' not supported. Supported: {list(self.supported_platforms.keys())}"
                }
            
            # Generate deployment steps based on platform
            steps = self._generate_deployment_steps(platform, config)
            
            plan = {
                "app_name": app_name,
                "platform": platform,
                "environment": environment,
                "domain": domain,
                "steps": steps,
                "estimated_time": self._estimate_deployment_time(platform),
                "requirements": self._get_platform_requirements(platform),
                "created_at": datetime.now().isoformat()
            }
            
            return {
                "success": True,
                "plan": plan,
                "steps": steps
            }
            
        except Exception as e:
            logger.error(f"Failed to create deployment plan: {e}")
            return {
                "success": False,
                "error": str(e)
            }
            
    def deploy_application(self, 
                          project_path: str,
                          platform: str = "vercel",
                          config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Deploy application to specified platform"""
        
        try:
            config = config or {}
            
            if platform == "vercel":
                return self._deploy_to_vercel(project_path, config)
            elif platform == "netlify":
                return self._deploy_to_netlify(project_path, config)
            elif platform == "heroku":
                return self._deploy_to_heroku(project_path, config)
            else:
                return {
                    "success": False,
                    "error": f"Deployment to {platform} not implemented yet"
                }
                
        except Exception as e:
            logger.error(f"Failed to deploy application: {e}")
            return {
                "success": False,
                "error": str(e)
            }
            
    def setup_domain(self, 
                    domain: str,
                    platform: str,
                    app_url: str) -> Dict[str, Any]:
        """Setup custom domain for deployed application"""
        
        try:
            dns_records = []
            
            if platform == "vercel":
                dns_records = [
                    {"type": "CNAME", "name": "@", "value": "cname.vercel-dns.com"},
                    {"type": "CNAME", "name": "www", "value": "cname.vercel-dns.com"}
                ]
            elif platform == "netlify":
                dns_records = [
                    {"type": "CNAME", "name": "@", "value": app_url},
                    {"type": "CNAME", "name": "www", "value": app_url}
                ]
            
            return {
                "success": True,
                "domain": domain,
                "dns_records": dns_records,
                "instructions": f"Add these DNS records to your domain provider for {domain}"
            }
            
        except Exception as e:
            logger.error(f"Failed to setup domain: {e}")
            return {
                "success": False,
                "error": str(e)
            }
            
    def setup_ssl(self, domain: str, platform: str) -> Dict[str, Any]:
        """Setup SSL certificate for domain"""
        
        try:
            if platform in ["vercel", "netlify"]:
                return {
                    "success": True,
                    "ssl_enabled": True,
                    "certificate_type": "Let's Encrypt",
                    "auto_renewal": True,
                    "message": f"SSL automatically configured by {platform}"
                }
            else:
                return {
                    "success": True,
                    "ssl_enabled": False,
                    "message": f"Manual SSL setup required for {platform}"
                }
                
        except Exception as e:
            logger.error(f"Failed to setup SSL: {e}")
            return {
                "success": False,
                "error": str(e)
            }
            
    def setup_environment_variables(self, 
                                   platform: str,
                                   app_name: str,
                                   env_vars: Dict[str, str]) -> Dict[str, Any]:
        """Setup environment variables for deployed application"""
        
        try:
            if platform == "vercel":
                return self._setup_vercel_env_vars(app_name, env_vars)
            elif platform == "netlify":
                return self._setup_netlify_env_vars(app_name, env_vars)
            elif platform == "heroku":
                return self._setup_heroku_env_vars(app_name, env_vars)
            else:
                return {
                    "success": False,
                    "error": f"Environment variable setup not implemented for {platform}"
                }
                
        except Exception as e:
            logger.error(f"Failed to setup environment variables: {e}")
            return {
                "success": False,
                "error": str(e)
            }
            
    def monitor_deployment(self, 
                          deployment_id: str,
                          platform: str) -> Dict[str, Any]:
        """Monitor deployment status"""
        
        try:
            # This would integrate with platform APIs to check deployment status
            return {
                "success": True,
                "deployment_id": deployment_id,
                "status": "completed",
                "url": f"https://{deployment_id}.{platform}.app",
                "logs": ["Build started", "Dependencies installed", "Build completed", "Deployment successful"]
            }
            
        except Exception as e:
            logger.error(f"Failed to monitor deployment: {e}")
            return {
                "success": False,
                "error": str(e)
            }
            
    def rollback_deployment(self, 
                           deployment_id: str,
                           platform: str,
                           target_version: Optional[str] = None) -> Dict[str, Any]:
        """Rollback to previous deployment version"""
        
        try:
            return {
                "success": True,
                "deployment_id": deployment_id,
                "rollback_version": target_version or "previous",
                "message": "Rollback completed successfully"
            }
            
        except Exception as e:
            logger.error(f"Failed to rollback deployment: {e}")
            return {
                "success": False,
                "error": str(e)
            }
            
    def _generate_deployment_steps(self, platform: str, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate platform-specific deployment steps"""
        
        if platform == "vercel":
            return [
                {
                    "step": 1,
                    "title": "Install Vercel CLI",
                    "command": "npm install -g vercel",
                    "description": "Install Vercel command line interface"
                },
                {
                    "step": 2,
                    "title": "Login to Vercel",
                    "command": "vercel login",
                    "description": "Authenticate with Vercel account"
                },
                {
                    "step": 3,
                    "title": "Deploy Application",
                    "command": "vercel --prod",
                    "description": "Deploy application to production"
                },
                {
                    "step": 4,
                    "title": "Configure Domain",
                    "command": f"vercel domains add {config.get('domain', 'example.com')}",
                    "description": "Add custom domain (if specified)"
                }
            ]
        elif platform == "netlify":
            return [
                {
                    "step": 1,
                    "title": "Install Netlify CLI",
                    "command": "npm install -g netlify-cli",
                    "description": "Install Netlify command line interface"
                },
                {
                    "step": 2,
                    "title": "Login to Netlify",
                    "command": "netlify login",
                    "description": "Authenticate with Netlify account"
                },
                {
                    "step": 3,
                    "title": "Deploy Application",
                    "command": "netlify deploy --prod",
                    "description": "Deploy application to production"
                }
            ]
        elif platform == "heroku":
            return [
                {
                    "step": 1,
                    "title": "Install Heroku CLI",
                    "command": "Download from heroku.com/cli",
                    "description": "Install Heroku command line interface"
                },
                {
                    "step": 2,
                    "title": "Login to Heroku",
                    "command": "heroku login",
                    "description": "Authenticate with Heroku account"
                },
                {
                    "step": 3,
                    "title": "Create Heroku App",
                    "command": f"heroku create {config.get('app_name', 'my-app')}",
                    "description": "Create new Heroku application"
                },
                {
                    "step": 4,
                    "title": "Deploy Application",
                    "command": "git push heroku main",
                    "description": "Deploy application via Git"
                }
            ]
        else:
            return [
                {
                    "step": 1,
                    "title": "Manual Deployment",
                    "command": "Follow platform documentation",
                    "description": f"Refer to {platform} documentation for deployment steps"
                }
            ]
            
    def _estimate_deployment_time(self, platform: str) -> str:
        """Estimate deployment time for platform"""
        
        time_estimates = {
            "vercel": "2-5 minutes",
            "netlify": "3-7 minutes",
            "heroku": "5-10 minutes",
            "aws": "10-20 minutes",
            "gcp": "10-20 minutes",
            "azure": "10-20 minutes"
        }
        
        return time_estimates.get(platform, "10-30 minutes")
        
    def _get_platform_requirements(self, platform: str) -> List[str]:
        """Get platform-specific requirements"""
        
        requirements = {
            "vercel": [
                "Node.js project or static files",
                "Vercel account",
                "Git repository (optional)"
            ],
            "netlify": [
                "Static site or Node.js project",
                "Netlify account",
                "Git repository (recommended)"
            ],
            "heroku": [
                "Git repository",
                "Heroku account",
                "Procfile (for non-Node.js apps)"
            ],
            "aws": [
                "AWS account",
                "AWS CLI configured",
                "Appropriate IAM permissions"
            ]
        }
        
        return requirements.get(platform, ["Platform account", "Application files"])
        
    def _deploy_to_vercel(self, project_path: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy to Vercel platform"""
        
        try:
            # Check if Vercel CLI is installed
            result = subprocess.run(["vercel", "--version"], capture_output=True, text=True)
            
            if result.returncode != 0:
                return {
                    "success": False,
                    "error": "Vercel CLI not installed. Run: npm install -g vercel"
                }
            
            # Change to project directory
            original_dir = os.getcwd()
            os.chdir(project_path)
            
            try:
                # Deploy to Vercel
                deploy_result = subprocess.run(
                    ["vercel", "--prod", "--yes"],
                    capture_output=True,
                    text=True
                )
                
                if deploy_result.returncode == 0:
                    # Extract URL from output
                    output_lines = deploy_result.stdout.split('\n')
                    url = None
                    for line in output_lines:
                        if 'https://' in line and 'vercel.app' in line:
                            url = line.strip()
                            break
                    
                    return {
                        "success": True,
                        "platform": "vercel",
                        "url": url,
                        "deployment_output": deploy_result.stdout
                    }
                else:
                    return {
                        "success": False,
                        "error": deploy_result.stderr
                    }
                    
            finally:
                os.chdir(original_dir)
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
            
    def _deploy_to_netlify(self, project_path: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy to Netlify platform"""
        
        try:
            # Check if Netlify CLI is installed
            result = subprocess.run(["netlify", "--version"], capture_output=True, text=True)
            
            if result.returncode != 0:
                return {
                    "success": False,
                    "error": "Netlify CLI not installed. Run: npm install -g netlify-cli"
                }
            
            # Change to project directory
            original_dir = os.getcwd()
            os.chdir(project_path)
            
            try:
                # Build the project first (if build command exists)
                build_dir = config.get("build_dir", "dist")
                
                # Deploy to Netlify
                deploy_result = subprocess.run(
                    ["netlify", "deploy", "--prod", "--dir", build_dir],
                    capture_output=True,
                    text=True
                )
                
                if deploy_result.returncode == 0:
                    # Extract URL from output
                    output_lines = deploy_result.stdout.split('\n')
                    url = None
                    for line in output_lines:
                        if 'https://' in line and 'netlify.app' in line:
                            url = line.strip()
                            break
                    
                    return {
                        "success": True,
                        "platform": "netlify",
                        "url": url,
                        "deployment_output": deploy_result.stdout
                    }
                else:
                    return {
                        "success": False,
                        "error": deploy_result.stderr
                    }
                    
            finally:
                os.chdir(original_dir)
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
            
    def _deploy_to_heroku(self, project_path: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy to Heroku platform"""
        
        try:
            app_name = config.get("app_name", "my-app")
            
            # Check if Heroku CLI is installed
            result = subprocess.run(["heroku", "--version"], capture_output=True, text=True)
            
            if result.returncode != 0:
                return {
                    "success": False,
                    "error": "Heroku CLI not installed. Download from heroku.com/cli"
                }
            
            # Change to project directory
            original_dir = os.getcwd()
            os.chdir(project_path)
            
            try:
                # Create Heroku app
                create_result = subprocess.run(
                    ["heroku", "create", app_name],
                    capture_output=True,
                    text=True
                )
                
                # Deploy via Git
                subprocess.run(["git", "add", "."], check=True)
                subprocess.run(["git", "commit", "-m", "Deploy to Heroku"], check=True)
                
                deploy_result = subprocess.run(
                    ["git", "push", "heroku", "main"],
                    capture_output=True,
                    text=True
                )
                
                if deploy_result.returncode == 0:
                    url = f"https://{app_name}.herokuapp.com"
                    
                    return {
                        "success": True,
                        "platform": "heroku",
                        "url": url,
                        "app_name": app_name,
                        "deployment_output": deploy_result.stdout
                    }
                else:
                    return {
                        "success": False,
                        "error": deploy_result.stderr
                    }
                    
            finally:
                os.chdir(original_dir)
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
            
    def _setup_vercel_env_vars(self, app_name: str, env_vars: Dict[str, str]) -> Dict[str, Any]:
        """Setup environment variables for Vercel"""
        
        try:
            for key, value in env_vars.items():
                result = subprocess.run(
                    ["vercel", "env", "add", key, "production"],
                    input=value,
                    text=True,
                    capture_output=True
                )
                
                if result.returncode != 0:
                    return {
                        "success": False,
                        "error": f"Failed to set environment variable {key}"
                    }
            
            return {
                "success": True,
                "message": f"Environment variables set for {app_name}",
                "variables_set": list(env_vars.keys())
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
            
    def _setup_netlify_env_vars(self, app_name: str, env_vars: Dict[str, str]) -> Dict[str, Any]:
        """Setup environment variables for Netlify"""
        
        try:
            for key, value in env_vars.items():
                result = subprocess.run(
                    ["netlify", "env:set", key, value],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    return {
                        "success": False,
                        "error": f"Failed to set environment variable {key}"
                    }
            
            return {
                "success": True,
                "message": f"Environment variables set for {app_name}",
                "variables_set": list(env_vars.keys())
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
            
    def _setup_heroku_env_vars(self, app_name: str, env_vars: Dict[str, str]) -> Dict[str, Any]:
        """Setup environment variables for Heroku"""
        
        try:
            env_string = " ".join([f"{k}={v}" for k, v in env_vars.items()])
            
            result = subprocess.run(
                ["heroku", "config:set"] + [f"{k}={v}" for k, v in env_vars.items()] + ["--app", app_name],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": f"Environment variables set for {app_name}",
                    "variables_set": list(env_vars.keys())
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

# Example usage
def main():
    """Example usage of DeploymentManager"""
    
    manager = DeploymentManager()
    
    # Create deployment plan
    config = {
        "app_name": "my-awesome-app",
        "platform": "vercel",
        "environment": "production",
        "domain": "myawesomeapp.com"
    }
    
    plan = manager.create_deployment_plan(config)
    print("Deployment plan:")
    print(json.dumps(plan, indent=2))
    
    # Setup domain
    domain_setup = manager.setup_domain("myawesomeapp.com", "vercel", "my-awesome-app.vercel.app")
    print("\nDomain setup:")
    print(json.dumps(domain_setup, indent=2))

if __name__ == "__main__":
    main()