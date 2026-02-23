"""
Landing Page Generator
Generates beautiful, responsive landing pages for startups
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class LandingPageGenerator:
    def __init__(self):
        self.templates_dir = Path("templates/landing_pages")
        self.output_dir = Path("generated/landing_pages")
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_landing_page(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a complete landing page"""
        try:
            # Extract configuration
            company_name = config.get("company_name", "Your Startup")
            tagline = config.get("tagline", "Building the future")
            description = config.get("description", "We're creating something amazing")
            industry = config.get("industry", "technology")
            
            # Generate HTML content
            html_content = self._generate_html(config)
            css_content = self._generate_css(config)
            js_content = self._generate_js(config)
            
            # Save files
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            page_dir = self.output_dir / f"{company_name.lower().replace(' ', '_')}_{timestamp}"
            page_dir.mkdir(exist_ok=True)
            
            # Write files
            (page_dir / "index.html").write_text(html_content, encoding='utf-8')
            (page_dir / "styles.css").write_text(css_content, encoding='utf-8')
            (page_dir / "script.js").write_text(js_content, encoding='utf-8')
            
            # Generate config file
            page_config = {
                "company_name": company_name,
                "generated_at": datetime.now().isoformat(),
                "files": ["index.html", "styles.css", "script.js"],
                "config": config
            }
            
            (page_dir / "config.json").write_text(json.dumps(page_config, indent=2), encoding='utf-8')
            
            return {
                "success": True,
                "page_directory": str(page_dir),
                "files": {
                    "html": str(page_dir / "index.html"),
                    "css": str(page_dir / "styles.css"),
                    "js": str(page_dir / "script.js"),
                    "config": str(page_dir / "config.json")
                },
                "preview_url": f"file://{page_dir / 'index.html'}",
                "company_name": company_name
            }
            
        except Exception as e:
            logger.error(f"Failed to generate landing page: {e}")
            return {
                "success": False,
                "error": str(e)
            }
            
    def _generate_html(self, config: Dict[str, Any]) -> str:
        """Generate HTML content"""
        company_name = config.get("company_name", "Your Startup")
        tagline = config.get("tagline", "Building the future")
        description = config.get("description", "We're creating something amazing")
        features = config.get("features", ["Feature 1", "Feature 2", "Feature 3"])
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{company_name} - {tagline}</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <!-- Header -->
    <header class="header">
        <nav class="nav">
            <div class="nav-brand">
                <h1>{company_name}</h1>
            </div>
            <div class="nav-links">
                <a href="#features">Features</a>
                <a href="#about">About</a>
                <a href="#contact">Contact</a>
                <button class="cta-button" onclick="openWaitlistModal()">Join Waitlist</button>
            </div>
        </nav>
    </header>

    <!-- Hero Section -->
    <section class="hero">
        <div class="hero-content">
            <h1 class="hero-title">{tagline}</h1>
            <p class="hero-description">{description}</p>
            <div class="hero-actions">
                <button class="primary-button" onclick="openWaitlistModal()">Get Early Access</button>
                <button class="secondary-button" onclick="scrollToSection('features')">Learn More</button>
            </div>
        </div>
        <div class="hero-visual">
            <div class="hero-placeholder">
                <p>🚀 Product Demo</p>
            </div>
        </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="features">
        <div class="container">
            <h2>Why Choose {company_name}?</h2>
            <div class="features-grid">"""
        
        for i, feature in enumerate(features[:3]):
            html += f"""
                <div class="feature-card">
                    <div class="feature-icon">⭐</div>
                    <h3>{feature}</h3>
                    <p>Experience the power of {feature.lower()} with our innovative solution.</p>
                </div>"""
        
        html += f"""
            </div>
        </div>
    </section>

    <!-- About Section -->
    <section id="about" class="about">
        <div class="container">
            <div class="about-content">
                <h2>About {company_name}</h2>
                <p>We're on a mission to revolutionize the industry with cutting-edge technology and innovative solutions. Our team is passionate about creating products that make a real difference.</p>
                <div class="stats">
                    <div class="stat">
                        <h3>1000+</h3>
                        <p>Early Users</p>
                    </div>
                    <div class="stat">
                        <h3>99%</h3>
                        <p>Satisfaction</p>
                    </div>
                    <div class="stat">
                        <h3>24/7</h3>
                        <p>Support</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" class="contact">
        <div class="container">
            <h2>Get In Touch</h2>
            <p>Ready to join the revolution? We'd love to hear from you.</p>
            <button class="primary-button" onclick="openWaitlistModal()">Join Our Waitlist</button>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-brand">
                    <h3>{company_name}</h3>
                    <p>{tagline}</p>
                </div>
                <div class="footer-links">
                    <a href="#privacy">Privacy Policy</a>
                    <a href="#terms">Terms of Service</a>
                    <a href="#contact">Contact</a>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 {company_name}. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <!-- Waitlist Modal -->
    <div id="waitlistModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeWaitlistModal()">&times;</span>
            <h2>Join Our Waitlist</h2>
            <p>Be the first to know when we launch!</p>
            <form id="waitlistForm" onsubmit="submitWaitlist(event)">
                <input type="email" id="email" placeholder="Enter your email" required>
                <input type="text" id="name" placeholder="Your name (optional)">
                <button type="submit" class="primary-button">Join Waitlist</button>
            </form>
            <div id="waitlistSuccess" class="success-message" style="display: none;">
                <p>✅ Thanks! You're on the list. We'll be in touch soon.</p>
            </div>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""
        return html
        
    def _generate_css(self, config: Dict[str, Any]) -> str:
        """Generate CSS styles"""
        primary_color = config.get("primary_color", "#3B82F6")
        secondary_color = config.get("secondary_color", "#1F2937")
        
        css = f"""/* Reset and Base Styles */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    line-height: 1.6;
    color: #333;
    overflow-x: hidden;
}}

.container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}}

/* Header */
.header {{
    position: fixed;
    top: 0;
    width: 100%;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    z-index: 1000;
    border-bottom: 1px solid #e5e7eb;
}}

.nav {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    max-width: 1200px;
    margin: 0 auto;
}}

.nav-brand h1 {{
    color: {primary_color};
    font-size: 1.5rem;
    font-weight: 700;
}}

.nav-links {{
    display: flex;
    align-items: center;
    gap: 2rem;
}}

.nav-links a {{
    text-decoration: none;
    color: #6b7280;
    font-weight: 500;
    transition: color 0.3s;
}}

.nav-links a:hover {{
    color: {primary_color};
}}

.cta-button {{
    background: {primary_color};
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.3s;
}}

.cta-button:hover {{
    background: #2563eb;
}}

/* Hero Section */
.hero {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    align-items: center;
    min-height: 100vh;
    padding: 6rem 2rem 2rem;
    max-width: 1200px;
    margin: 0 auto;
    gap: 4rem;
}}

.hero-title {{
    font-size: 3.5rem;
    font-weight: 700;
    color: {secondary_color};
    margin-bottom: 1rem;
    line-height: 1.1;
}}

.hero-description {{
    font-size: 1.25rem;
    color: #6b7280;
    margin-bottom: 2rem;
    line-height: 1.6;
}}

.hero-actions {{
    display: flex;
    gap: 1rem;
}}

.primary-button {{
    background: {primary_color};
    color: white;
    border: none;
    padding: 1rem 2rem;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s;
}}

.primary-button:hover {{
    background: #2563eb;
    transform: translateY(-2px);
}}

.secondary-button {{
    background: transparent;
    color: {primary_color};
    border: 2px solid {primary_color};
    padding: 1rem 2rem;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s;
}}

.secondary-button:hover {{
    background: {primary_color};
    color: white;
}}

.hero-visual {{
    display: flex;
    justify-content: center;
    align-items: center;
}}

.hero-placeholder {{
    width: 400px;
    height: 300px;
    background: linear-gradient(135deg, {primary_color}, #8b5cf6);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 1.5rem;
    font-weight: 600;
}}

/* Features Section */
.features {{
    padding: 6rem 2rem;
    background: #f9fafb;
}}

.features h2 {{
    text-align: center;
    font-size: 2.5rem;
    color: {secondary_color};
    margin-bottom: 3rem;
}}

.features-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    max-width: 1000px;
    margin: 0 auto;
}}

.feature-card {{
    background: white;
    padding: 2rem;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    transition: transform 0.3s;
}}

.feature-card:hover {{
    transform: translateY(-4px);
}}

.feature-icon {{
    font-size: 3rem;
    margin-bottom: 1rem;
}}

.feature-card h3 {{
    font-size: 1.5rem;
    color: {secondary_color};
    margin-bottom: 1rem;
}}

/* About Section */
.about {{
    padding: 6rem 2rem;
}}

.about-content {{
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
}}

.about h2 {{
    font-size: 2.5rem;
    color: {secondary_color};
    margin-bottom: 2rem;
}}

.about p {{
    font-size: 1.125rem;
    color: #6b7280;
    margin-bottom: 3rem;
}}

.stats {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
    margin-top: 3rem;
}}

.stat {{
    text-align: center;
}}

.stat h3 {{
    font-size: 2.5rem;
    color: {primary_color};
    font-weight: 700;
}}

.stat p {{
    color: #6b7280;
    font-weight: 500;
}}

/* Contact Section */
.contact {{
    padding: 6rem 2rem;
    background: {secondary_color};
    color: white;
    text-align: center;
}}

.contact h2 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
}}

.contact p {{
    font-size: 1.125rem;
    margin-bottom: 2rem;
    opacity: 0.9;
}}

/* Footer */
.footer {{
    background: #111827;
    color: white;
    padding: 3rem 2rem 1rem;
}}

.footer-content {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
}}

.footer-brand h3 {{
    color: {primary_color};
    margin-bottom: 0.5rem;
}}

.footer-links {{
    display: flex;
    gap: 2rem;
}}

.footer-links a {{
    color: #9ca3af;
    text-decoration: none;
    transition: color 0.3s;
}}

.footer-links a:hover {{
    color: white;
}}

.footer-bottom {{
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid #374151;
    color: #9ca3af;
}}

/* Modal */
.modal {{
    display: none;
    position: fixed;
    z-index: 2000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
}}

.modal-content {{
    background-color: white;
    margin: 10% auto;
    padding: 2rem;
    border-radius: 12px;
    width: 90%;
    max-width: 500px;
    position: relative;
}}

.close {{
    position: absolute;
    right: 1rem;
    top: 1rem;
    font-size: 2rem;
    cursor: pointer;
    color: #9ca3af;
}}

.close:hover {{
    color: #374151;
}}

.modal h2 {{
    margin-bottom: 1rem;
    color: {secondary_color};
}}

.modal form {{
    display: flex;
    flex-direction: column;
    gap: 1rem;
}}

.modal input {{
    padding: 1rem;
    border: 2px solid #e5e7eb;
    border-radius: 8px;
    font-size: 1rem;
}}

.modal input:focus {{
    outline: none;
    border-color: {primary_color};
}}

.success-message {{
    text-align: center;
    color: #059669;
    font-weight: 600;
}}

/* Responsive Design */
@media (max-width: 768px) {{
    .hero {{
        grid-template-columns: 1fr;
        text-align: center;
        padding: 4rem 1rem 2rem;
    }}
    
    .hero-title {{
        font-size: 2.5rem;
    }}
    
    .nav-links {{
        display: none;
    }}
    
    .features-grid {{
        grid-template-columns: 1fr;
    }}
    
    .stats {{
        grid-template-columns: 1fr;
    }}
    
    .footer-content {{
        flex-direction: column;
        gap: 2rem;
    }}
}}"""
        return css
        
    def _generate_js(self, config: Dict[str, Any]) -> str:
        """Generate JavaScript functionality"""
        js = """// Landing Page JavaScript

// Smooth scrolling
function scrollToSection(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        element.scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Waitlist Modal
function openWaitlistModal() {
    document.getElementById('waitlistModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeWaitlistModal() {
    document.getElementById('waitlistModal').style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('waitlistModal');
    if (event.target === modal) {
        closeWaitlistModal();
    }
}

// Waitlist form submission
function submitWaitlist(event) {
    event.preventDefault();
    
    const email = document.getElementById('email').value;
    const name = document.getElementById('name').value;
    
    // Simulate API call
    setTimeout(() => {
        document.getElementById('waitlistForm').style.display = 'none';
        document.getElementById('waitlistSuccess').style.display = 'block';
        
        // Store in localStorage for demo
        const waitlistData = {
            email: email,
            name: name,
            timestamp: new Date().toISOString()
        };
        
        let waitlist = JSON.parse(localStorage.getItem('waitlist') || '[]');
        waitlist.push(waitlistData);
        localStorage.setItem('waitlist', JSON.stringify(waitlist));
        
        console.log('Waitlist signup:', waitlistData);
        
        // Close modal after 2 seconds
        setTimeout(() => {
            closeWaitlistModal();
            // Reset form
            document.getElementById('waitlistForm').style.display = 'block';
            document.getElementById('waitlistSuccess').style.display = 'none';
            document.getElementById('waitlistForm').reset();
        }, 2000);
    }, 500);
}

// Header scroll effect
window.addEventListener('scroll', function() {
    const header = document.querySelector('.header');
    if (window.scrollY > 100) {
        header.style.background = 'rgba(255, 255, 255, 0.98)';
    } else {
        header.style.background = 'rgba(255, 255, 255, 0.95)';
    }
});

// Animation on scroll
function animateOnScroll() {
    const elements = document.querySelectorAll('.feature-card, .stat');
    
    elements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementVisible = 150;
        
        if (elementTop < window.innerHeight - elementVisible) {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }
    });
}

// Initialize animations
document.addEventListener('DOMContentLoaded', function() {
    // Set initial state for animated elements
    const elements = document.querySelectorAll('.feature-card, .stat');
    elements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    });
    
    // Trigger animations on scroll
    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll(); // Initial check
});

// Console welcome message
console.log('🚀 Landing page loaded successfully!');
console.log('💡 Check localStorage for waitlist signups');"""
        return js
        
    def get_templates(self) -> List[str]:
        """Get available landing page templates"""
        return ["modern", "minimal", "startup", "saas", "ecommerce"]
        
    def customize_template(self, template_name: str, customizations: Dict[str, Any]) -> Dict[str, Any]:
        """Customize a template with specific options"""
        # This would load and customize existing templates
        return {
            "template": template_name,
            "customizations": customizations,
            "success": True
        }

# Example usage
def main():
    """Example usage of LandingPageGenerator"""
    generator = LandingPageGenerator()
    
    config = {
        "company_name": "TechFlow",
        "tagline": "Streamline Your Workflow",
        "description": "The all-in-one platform that helps teams collaborate, automate, and scale their operations effortlessly.",
        "industry": "productivity",
        "features": ["Smart Automation", "Team Collaboration", "Advanced Analytics"],
        "primary_color": "#6366f1",
        "secondary_color": "#1f2937"
    }
    
    result = generator.generate_landing_page(config)
    print("Landing page generation result:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()