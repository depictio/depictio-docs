// Animated Triangular Logo Script for MkDocs - DEMO PAGE ONLY
// Based on the sequential pulsing animation from the Python Dash script
// ONLY affects specific demo containers, NOT the site logo

document.addEventListener('DOMContentLoaded', function() {
    // Only run on the animated-logo demo page
    if (!window.location.pathname.includes('animated-logo')) {
        return;
    }

    console.log('🎨 Initializing triangular logo demo...');

    // Load the actual animated SVG content
    function loadAnimatedSVG() {
        return fetch('https://depictio.github.io/depictio-docs/images/logo/animated_favicon.svg')
            .then(response => response.text())
            .catch(error => {
                console.log('Could not load animated_favicon.svg');
                return null;
            });
    }

    // ONLY initialize demo functionality - no site-wide changes
    function initializeDemoOnly() {
        // Only work with the specific demo container
        const demoContainer = document.getElementById('svg-logo-container');
        if (!demoContainer) {
            console.log('Demo container not found');
            return;
        }

        // Make global functions available for buttons
        window.loadTriangularSVG = function() {
            console.log('🎨 Loading triangular SVG...');

            loadAnimatedSVG().then(svgContent => {
                if (!svgContent) {
                    demoContainer.innerHTML = '<p style="color: red;">Could not load animated SVG</p>';
                    return;
                }

                demoContainer.innerHTML = svgContent;
                console.log('✅ Triangular SVG loaded successfully!');

                // Debug: Check if shapes are found
                const shapes = demoContainer.querySelectorAll('[id^="shape-"]');
                console.log('🔍 Found shapes:', shapes.length);
                shapes.forEach((shape, index) => {
                    console.log(`Shape ${index + 1}:`, shape.id, shape.tagName);
                });
            });
        };

        window.triggerTriangularAnimation = function() {
            console.log('🎨 Triggering triangular animation...');
            if (demoContainer) {
                demoContainer.classList.add('triangular-logo-active');

                setTimeout(() => {
                    demoContainer.classList.remove('triangular-logo-active');
                    console.log('✅ Animation completed');
                }, 4000);
            }
        };

        // Auto-load SVG for demo
        setTimeout(() => {
            if (typeof window.loadTriangularSVG === 'function') {
                window.loadTriangularSVG();
            }
        }, 500);

        // Set up periodic animation for demo
        setInterval(() => {
            if (typeof window.triggerTriangularAnimation === 'function') {
                window.triggerTriangularAnimation();
            }
        }, 12000); // Every 12 seconds

        console.log('✅ Demo functionality initialized');
    }

    // Only initialize demo functionality
    initializeDemoOnly();

    console.log('🚀 Triangular logo demo initialized (page-specific only)!');
});
