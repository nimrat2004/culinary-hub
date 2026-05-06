document.addEventListener('DOMContentLoaded', function () {

    // ===== SLIDESHOW FUNCTIONALITY =====
    const slides = document.querySelectorAll('.slide');
    const dots = document.querySelectorAll('.dot');
    let currentSlide = 0;
    let slideInterval;

    function showSlide(n) {
        if (slides.length === 0) return;

        // Remove active class from all slides and dots
        slides.forEach(slide => slide.classList.remove('active'));
        dots.forEach(dot => dot.classList.remove('active'));

        // Add active class to current slide and dot
        slides[n].classList.add('active');
        if (dots[n]) {
            dots[n].classList.add('active');
        }
    }

    function nextSlide() {
        if (slides.length === 0) return;
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide);
    }

    function startSlideshow() {
        if (slides.length > 0) {
            slideInterval = setInterval(nextSlide, 4000);
        }
    }

    function stopSlideshow() {
        if (slideInterval) {
            clearInterval(slideInterval);
        }
    }

    // Initialize slideshow
    if (slides.length > 0) {
        showSlide(0);
        startSlideshow();
    }

    // Dot click functionality
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            currentSlide = index;
            showSlide(currentSlide);
            stopSlideshow();
            setTimeout(startSlideshow, 100);
        });
    });

    // Pause slideshow on hover
    const slideshow = document.querySelector('.slideshow');
    if (slideshow) {
        slideshow.addEventListener('mouseenter', stopSlideshow);
        slideshow.addEventListener('mouseleave', startSlideshow);
    }

    // ===== NAVBAR SCROLL EFFECT =====
    const navbar = document.querySelector('.nav-container');
    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 100) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // ===== SECTION FADE-IN ON SCROLL =====
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);

    // Observe all sections that should fade in
    const fadeInSections = document.querySelectorAll('.our-story, .private-dining, .our-chefs, .image-section');
    fadeInSections.forEach(section => {
        observer.observe(section);
    });


    // ===== SMOOTH SCROLLING FOR ANCHOR LINKS =====
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // ===== LOADING ANIMATION =====
    window.addEventListener('load', function() {
        document.body.classList.add('loaded');
    });

    // ===== CHEF CARD HOVER EFFECTS =====
    const chefCards = document.querySelectorAll('.chef-card');
    chefCards.forEach(card => {
        // CSS handles these now
    });

    // ===== BUTTON CLICK EFFECTS =====
    const buttons = document.querySelectorAll('.cta-button');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Create ripple effect
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');

            this.appendChild(ripple);

            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });

    // ===== SEARCH FUNCTIONALITY ENHANCEMENT =====
    const searchForm = document.querySelector('form[action*="menu"]');
    const searchInput = document.querySelector('input[name="q"]');

    if (searchForm && searchInput) {
        searchInput.addEventListener('focus', function() {
            this.style.transform = 'scale(1.02)';
        });

        searchInput.addEventListener('blur', function() {
            this.style.transform = 'scale(1)';
        });
    }

    // ===== MOBILE MENU ENHANCEMENTS =====
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');

    if (navbarToggler && navbarCollapse) {
        navbarToggler.addEventListener('click', function() {
            setTimeout(() => {
                if (navbarCollapse.classList.contains('show')) {
                    document.body.style.overflow = 'hidden';
                } else {
                    document.body.style.overflow = 'auto';
                }
            }, 100);
        });
    }

    // ===== PERFORMANCE OPTIMIZATION =====
    // Lazy load images
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));

    // ===== ACCESSIBILITY IMPROVEMENTS =====
    // Keyboard navigation for slideshow
    document.addEventListener('keydown', function(e) {
        if (slides.length === 0) return;

        if (e.key === 'ArrowLeft') {
            currentSlide = (currentSlide - 1 + slides.length) % slides.length;
            showSlide(currentSlide);
            stopSlideshow();
            setTimeout(startSlideshow, 100);
        } else if (e.key === 'ArrowRight') {
            nextSlide();
            stopSlideshow();
            setTimeout(startSlideshow, 100);
        }
    });

    // ===== ERROR HANDLING =====
    window.addEventListener('error', function(e) {
        console.error('JavaScript error:', e.error);
    });

    // ===== PERFORMANCE MONITORING =====
    if ('performance' in window) {
        window.addEventListener('load', function() {
            setTimeout(function() {
                const perfData = performance.getEntriesByType('navigation')[0];
                if (perfData) {
                    console.log('Page load time:', perfData.loadEventEnd - perfData.loadEventStart, 'ms');
                }
            }, 0);
        });
    }
});

// ===== CSS FOR RIPPLE EFFECT (kept as is, consider moving to CSS file) =====
const rippleStyles = `
    .cta-button {
        position: relative;
        overflow: hidden;
    }

    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        pointer-events: none;
    }

    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;

// Add ripple styles to document
const styleSheet = document.createElement('style');
styleSheet.textContent = rippleStyles;
document.head.appendChild(styleSheet);


document.addEventListener("DOMContentLoaded", () => {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.2 });

    document.querySelectorAll('.fade-in').forEach(section => observer.observe(section));
});