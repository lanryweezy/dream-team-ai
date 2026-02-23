// Landing Page JavaScript

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
console.log('💡 Check localStorage for waitlist signups');