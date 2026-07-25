
document.addEventListener('DOMContentLoaded', function() {
    const animateElements = document.querySelectorAll('.animate-on-scroll');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, {
        threshold: 0.1
    });
    
    animateElements.forEach(el => observer.observe(el));
});

document.addEventListener('DOMContentLoaded', function() {
    const dateInput = document.getElementById('date');
    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.setAttribute('min', today);
    }
});


document.addEventListener('DOMContentLoaded', function() {
    const statItems = document.querySelectorAll('.stat-item h2');
    
    const counterObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                const text = el.textContent;
                const num = parseInt(text.replace(/[^0-9.]/g, ''));
                if (!isNaN(num)) {
                    let current = 0;
                    const increment = Math.ceil(num / 50);
                    const timer = setInterval(() => {
                        current += increment;
                        if (current >= num) {
                            current = num;
                            clearInterval(timer);
                        }
                        if (text.includes('★')) {
                            el.textContent = current + '★';
                        } else if (text.includes('+')) {
                            el.textContent = current + '+';
                        } else {
                            el.textContent = current;
                        }
                    }, 30);
                }
                counterObserver.unobserve(el);
            }
        });
    }, { threshold: 0.5 });
    
    statItems.forEach(item => counterObserver.observe(item));
});

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href !== '#') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                const navHeight = document.querySelector('.custom-navbar').offsetHeight;
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navHeight;
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const sourceInput = document.getElementById('source');
    const destInput = document.getElementById('destination');
    
    const stations = [
        'New Delhi', 'Mumbai Central', 'Kolkata', 'Chennai', 
        'Bangalore', 'Hyderabad', 'Chandigarh', 'Varanasi',
        'Ahmedabad', 'Pune', 'Jaipur', 'Lucknow', 'Kanpur',
        'Nagpur', 'Indore', 'Bhopal', 'Patna', 'Surat'
    ];
    
    function setupAutocomplete(input) {
        if (!input) return;
        
        let datalist = document.getElementById(input.id + '-list');
        if (!datalist) {
            datalist = document.createElement('datalist');
            datalist.id = input.id + '-list';
            input.setAttribute('list', datalist.id);
            input.parentNode.appendChild(datalist);
        }
        
        input.addEventListener('input', function() {
            const value = this.value.toLowerCase();
            const filtered = stations.filter(s => 
                s.toLowerCase().includes(value)
            );
            datalist.innerHTML = '';
            filtered.forEach(station => {
                const option = document.createElement('option');
                option.value = station;
                datalist.appendChild(option);
            });
        });
    }
    
    setupAutocomplete(sourceInput);
    setupAutocomplete(destInput);
});