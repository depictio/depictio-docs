// Triangular Animation Script - Based on Depictio's progressive loading script
// Animates the 7 triangular shapes sequentially

// Get the base path for assets (works both locally and on GitHub Pages)
function getBasePath() {
    const path = window.location.pathname;
    if (path.includes('/depictio-docs/')) {
        return '/depictio-docs/';
    }
    // For local development or other deployments
    return '/';
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('🎨 Initializing triangular animation system...');
    
    // Find all SVG elements that contain the triangular shapes
    function findTriangularSVGs() {
        // Look for SVGs that contain shape elements
        const svgElements = document.querySelectorAll('svg');
        const triangularSVGs = [];
        
        svgElements.forEach(svg => {
            const shapes = svg.querySelectorAll('[id^="shape-"]');
            if (shapes.length > 0) {
                triangularSVGs.push(svg);
                
                // Set overflow visible and add padding for header logos
                svg.style.overflow = 'visible';
                const headerLogo = svg.closest('.md-header__button.md-logo');
                if (headerLogo) {
                    headerLogo.style.overflow = 'visible';
                    headerLogo.style.padding = '8px';
                    console.log('🔍 Found triangular SVG in header with', shapes.length, 'shapes');
                } else {
                    console.log('🔍 Found triangular SVG with', shapes.length, 'shapes');
                }
            }
        });
        
        return triangularSVGs;
    }
    
    // Add interactive controls to triangular SVGs
    function addInteractiveControls() {
        const triangularSVGs = findTriangularSVGs();
        
        triangularSVGs.forEach((svg, index) => {
            // Add click handler for enhanced animation
            svg.addEventListener('click', function() {
                console.log('🎨 Triggering enhanced triangular animation...');
                
                // Add active class for enhanced animation
                this.classList.add('triangular-active');
                
                // Remove active class after animation cycle
                setTimeout(() => {
                    this.classList.remove('triangular-active');
                    console.log('✅ Enhanced animation completed');
                }, 3000);
            });
            
            // Add hover effects
            svg.addEventListener('mouseenter', function() {
                this.style.cursor = 'pointer';
            });
            
            svg.addEventListener('mouseleave', function() {
                // No additional effects
            });
            
            // Debug: Log found shapes
            const shapes = svg.querySelectorAll('[id^="shape-"]');
            shapes.forEach((shape, shapeIndex) => {
                console.log(`Shape ${shapeIndex + 1}:`, shape.id, `Fill: ${shape.style.fill}`);
            });
        });
        
        return triangularSVGs.length;
    }
    
    // Periodic auto-animation - DISABLED, only hover now
    function startPeriodicAnimation() {
        // Disabled - animation now only on hover
        console.log('📴 Periodic animation disabled - hover only mode');
    }
    
    // Load SVG inline for proper animation control
    function loadInlineSVG() {
        const container = document.getElementById('inline-svg-container');
        if (!container) return;
        
        fetch(getBasePath() + 'images/logo/animated_favicon.svg')
            .then(response => response.text())
            .then(svgContent => {
                container.innerHTML = svgContent;
                
                // Set the size of the loaded SVG and fix clipping issues
                const svg = container.querySelector('svg');
                if (svg) {
                    svg.style.width = '120px';
                    svg.style.height = '120px';
                    svg.style.cursor = 'pointer';
                    svg.style.overflow = 'visible';
                    
                    // Expand viewBox to prevent clipping during animation
                    const currentViewBox = svg.getAttribute('viewBox') || '0 0 823 809';
                    const [x, y, width, height] = currentViewBox.split(' ').map(Number);
                    
                    // Add padding around the viewBox (10% on all sides)
                    const padding = Math.max(width, height) * 0.1;
                    const newViewBox = `${x - padding} ${y - padding} ${width + 2 * padding} ${height + 2 * padding}`;
                    svg.setAttribute('viewBox', newViewBox);
                    
                    console.log('✅ Inline SVG loaded, sized, and viewBox expanded');
                }
                
                // Now add interactive controls
                const svgCount = addInteractiveControls();
                console.log(`✅ Interactive controls added to ${svgCount} triangular SVGs`);
            })
            .catch(error => {
                console.log('Could not load SVG inline:', error);
                container.innerHTML = '<p>SVG loading failed</p>';
            });
    }
    
    // Replace header logo with inline SVG
    function replaceHeaderLogo() {
        const logoButton = document.querySelector('.md-header__button.md-logo');
        const headerLogo = document.querySelector('.md-header__button.md-logo img');
        
        if (!headerLogo || !logoButton) {
            console.log('Header logo not found');
            return;
        }
        
        // Immediately set the correct size to prevent flash
        headerLogo.style.width = '48px';
        headerLogo.style.height = '48px';
        
        fetch(getBasePath() + 'images/logo/animated_favicon.svg')
            .then(response => response.text())
            .then(svgContent => {
                // Create a wrapper div
                const wrapper = document.createElement('div');
                wrapper.innerHTML = svgContent;
                
                // Set up the SVG
                const svg = wrapper.querySelector('svg');
                if (svg) {
                    svg.style.width = '48px';
                    svg.style.height = '48px';
                    svg.style.overflow = 'visible';
                    svg.style.cursor = 'pointer';
                    
                    // Expand viewBox to prevent clipping
                    const currentViewBox = svg.getAttribute('viewBox') || '0 0 823 809';
                    const [x, y, width, height] = currentViewBox.split(' ').map(Number);
                    const padding = Math.max(width, height) * 0.1;
                    const newViewBox = `${x - padding} ${y - padding} ${width + 2 * padding} ${height + 2 * padding}`;
                    svg.setAttribute('viewBox', newViewBox);
                    
                    // Replace the img with the SVG
                    headerLogo.parentNode.replaceChild(svg, headerLogo);
                    
                    // Show the logo now that it's ready
                    logoButton.classList.add('logo-ready');
                    console.log('✅ Header logo replaced with animated SVG');
                    
                    // Add interactive controls
                    setTimeout(() => {
                        addInteractiveControls();
                    }, 50);
                }
            })
            .catch(error => {
                console.log('Could not replace header logo:', error);
                // Show the original logo if SVG fails to load
                logoButton.classList.add('logo-ready');
            });
    }
    
    // Initialize everything as fast as possible
    function initialize() {
        loadInlineSVG(); // For demo page
        replaceHeaderLogo(); // For header
        console.log('🚀 Triangular animation system fully initialized!');
    }
    
    // Try multiple initialization points to catch the logo as early as possible
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initialize);
    } else {
        initialize();
    }
    
    // Also try after a short delay as fallback
    setTimeout(initialize, 100);
    
    // Listen for MkDocs Material instant navigation events
    document.addEventListener('DOMContentLoaded', function() {
        // Re-initialize when navigating with instant loading
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList' && mutation.target.classList.contains('md-content')) {
                    console.log('📄 Page navigation detected, re-initializing logo...');
                    setTimeout(initialize, 50);
                }
            });
        });
        
        const content = document.querySelector('.md-content');
        if (content) {
            observer.observe(content, { childList: true, subtree: true });
        }
    });
    
    // Also listen for location changes (backup method)
    let lastUrl = location.href;
    new MutationObserver(() => {
        const url = location.href;
        if (url !== lastUrl) {
            lastUrl = url;
            console.log('🔄 URL change detected, re-initializing logo...');
            setTimeout(initialize, 100);
        }
    }).observe(document, { subtree: true, childList: true });
    
    // Make functions available globally for manual triggering
    window.triggerTriangularAnimation = function() {
        const triangularSVGs = findTriangularSVGs();
        triangularSVGs.forEach(svg => {
            svg.classList.add('triangular-active');
            setTimeout(() => {
                svg.classList.remove('triangular-active');
            }, 3000);
        });
        console.log('🎨 Manual triangular animation triggered');
    };
    
    window.debugTriangularShapes = function() {
        const triangularSVGs = findTriangularSVGs();
        triangularSVGs.forEach((svg, index) => {
            console.log(`SVG ${index + 1}:`);
            const shapes = svg.querySelectorAll('[id^="shape-"]');
            shapes.forEach((shape, shapeIndex) => {
                const bbox = shape.getBBox ? shape.getBBox() : { x: 0, y: 0, width: 0, height: 0 };
                console.log(`  Shape ${shapeIndex + 1}: ${shape.id}, Fill: ${shape.style.fill}, Center: (${bbox.x + bbox.width/2}, ${bbox.y + bbox.height/2})`);
            });
        });
    };
});