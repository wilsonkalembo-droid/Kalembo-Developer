// SokoConnect - JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Mobile Menu Toggle
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger) {
        hamburger.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }

    // Close mobile menu when a link is clicked
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (navMenu) {
                navMenu.classList.remove('active');
            }
        });
    });

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Check if this is a registration form
            const passwordField = form.querySelector('#password');
            const confirmPasswordField = form.querySelector('#confirm_password');
            
            if (passwordField && confirmPasswordField) {
                const password = passwordField.value;
                const confirmPassword = confirmPasswordField.value;
                
                // Simple password validation - only check length and match
                if (password.length < 8) {
                    e.preventDefault();
                    showNotification('Password must be at least 8 characters long', 'error');
                    passwordField.focus();
                    return;
                }
                
                // Passwords match check
                if (password !== confirmPassword) {
                    e.preventDefault();
                    showNotification('Passwords do not match', 'error');
                    confirmPasswordField.focus();
                    return;
                }
            }
            console.log('Form submitted successfully');
        });
    });
                    return;
                }
            }
            console.log('Form submitted');
        });
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Add animation to elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe cards for animation
    document.querySelectorAll('.feature-card, .team-card, .testimonial-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
});

// Navbar background on scroll
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.boxShadow = '0 5px 20px rgba(0, 0, 0, 0.1)';
    } else {
        navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.05)';
    }
});

// Email validation helper
function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Phone validation helper
function isValidPhone(phone) {
    const re = /^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$/im;
    return re.test(phone);
}

// Show notification
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background-color: ${type === 'success' ? '#10b981' : '#ef4444'};
        color: white;
        border-radius: 8px;
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Password Strength Checker
function checkPasswordStrength() {
    const password = document.getElementById('password');
    const strengthBar = document.getElementById('strength-indicator');
    const strengthText = document.getElementById('password-text');
    
    if (!password) return;
    
    const pwd = password.value;
    let strength = 0;
    let feedback = [];
    
    // Check length (20 points for 8+ chars)
    if (pwd.length >= 8) {
        strength += 20;
    } else {
        feedback.push(pwd.length + '/8 characters');
    }
    
    // Check length (30 points for 12+ chars)
    if (pwd.length >= 12) {
        strength += 30;
    }
    
    // Check for lowercase (15 points)
    if (/[a-z]/.test(pwd)) {
        strength += 15;
    } else {
        feedback.push('add lowercase');
    }
    
    // Check for uppercase (15 points)
    if (/[A-Z]/.test(pwd)) {
        strength += 15;
    } else {
        feedback.push('add uppercase');
    }
    
    // Check for numbers (15 points)
    if (/[0-9]/.test(pwd)) {
        strength += 15;
    } else {
        feedback.push('add number');
    }
    
    // Check for special characters (10 points - optional)
    if (/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(pwd)) {
        strength += 10;
    }
    
    // Update strength bar color and width
    if (pwd.length === 0) {
        strengthBar.style.backgroundColor = '#e5e7eb';
        strengthText.textContent = 'Minimum 8 characters';
        strengthBar.style.width = '0%';
    } else if (strength < 25) {
        strengthBar.style.backgroundColor = '#ef4444'; // Red
        strengthText.textContent = 'Weak. ' + feedback.join(', ');
        strengthBar.style.width = strength + '%';
    } else if (strength < 50) {
        strengthBar.style.backgroundColor = '#f59e0b'; // Orange
        strengthText.textContent = 'Fair. ' + feedback.join(', ');
        strengthBar.style.width = strength + '%';
    } else if (strength < 75) {
        strengthBar.style.backgroundColor = '#eab308'; // Yellow
        strengthText.textContent = 'Good password ✓';
        strengthBar.style.width = strength + '%';
    } else {
        strengthBar.style.backgroundColor = '#10b981'; // Green
        strengthText.textContent = 'Strong password ✓';
        strengthBar.style.width = '100%';
    }
}

// Password Match Checker
function checkPasswordMatch() {
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm_password');
    const matchText = document.getElementById('match-text');
    
    if (!password || !confirmPassword) return;
    
    if (confirmPassword.value === '') {
        matchText.textContent = '';
        matchText.style.color = '#6b7280';
    } else if (password.value === confirmPassword.value) {
        matchText.textContent = '✓ Passwords match';
        matchText.style.color = '#10b981';
    } else {
        matchText.textContent = '✗ Passwords do not match';
        matchText.style.color = '#ef4444';
    }
}
