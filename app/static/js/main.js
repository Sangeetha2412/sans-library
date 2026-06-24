// ─── COUNTER ANIMATION ──────────────────────────────────────────

function animateCounters() {
    const counters = document.querySelectorAll('.stat-number[data-target]');
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'));
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;
        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                counter.textContent = target.toLocaleString();
                clearInterval(timer);
            } else {
                counter.textContent = Math.floor(current).toLocaleString();
            }
        }, 16);
    });
}

const statsSection = document.querySelector('.stats-section');
if (statsSection) {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounters();
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.3 });
    observer.observe(statsSection);
}

// ─── IMAGE SLIDESHOW ────────────────────────────────────────────

function initSlideshow(container) {
    const images = container.querySelectorAll('.slide-img');
    const dots = container.querySelectorAll('.slide-dot');
    let current = 0;
    let timer;

    function goTo(index) {
        images.forEach(img => img.classList.remove('active'));
        dots.forEach(dot => dot.classList.remove('active'));
        current = (index + images.length) % images.length;
        images[current].classList.add('active');
        dots[current]?.classList.add('active');
    }

    function autoPlay() {
        timer = setInterval(() => goTo(current + 1), 4000);
    }

    if (images.length > 0) {
        images[0].classList.add('active');
        dots[0]?.classList.add('active');
        if (images.length > 1) autoPlay();
    }

    container.querySelector('.slide-prev')?.addEventListener('click', () => {
        clearInterval(timer);
        goTo(current - 1);
        autoPlay();
    });
    container.querySelector('.slide-next')?.addEventListener('click', () => {
        clearInterval(timer);
        goTo(current + 1);
        autoPlay();
    });
    dots.forEach((dot, i) => {
        dot.addEventListener('click', () => { clearInterval(timer); goTo(i); autoPlay(); });
    });
}

document.querySelectorAll('.book-slideshow').forEach(initSlideshow);

// ─── CATEGORY FILTER ────────────────────────────────────────────

document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        const genre = this.dataset.genre || '';
        const searchParams = new URLSearchParams(window.location.search);
        if (genre) {
            searchParams.set('genre', genre);
        } else {
            searchParams.delete('genre');
        }
        window.location.search = searchParams.toString();
    });
});

// ─── SEARCH INPUT ───────────────────────────────────────────────

const searchInput = document.getElementById('searchInput');
if (searchInput) {
    let searchTimer;
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimer);
        searchTimer = setTimeout(() => {
            const searchParams = new URLSearchParams(window.location.search);
            if (this.value) {
                searchParams.set('q', this.value);
            } else {
                searchParams.delete('q');
            }
            window.location.search = searchParams.toString();
        }, 600);
    });
}

// ─── STAR RATING INPUT ──────────────────────────────────────────

function initStarRating() {
    const stars = document.querySelectorAll('.star-input');
    const ratingInput = document.getElementById('ratingInput');

    // Book detail page illa na nothing to do
    if (!stars.length || !ratingInput) return;

    function paintStars(value) {
        stars.forEach((star, index) => {
            const isSelected = index < value;

            star.classList.toggle('bi-star-fill', isSelected);
            star.classList.toggle('bi-star', !isSelected);
            star.classList.toggle('text-warning', isSelected);
            star.classList.toggle('text-muted', !isSelected);
        });
    }

    stars.forEach((star) => {
        star.style.cursor = 'pointer';

        star.addEventListener('click', function () {
            const value = Number(this.dataset.value);
            ratingInput.value = value;
            paintStars(value);
        });

        star.addEventListener('mouseenter', function () {
            paintStars(Number(this.dataset.value));
        });
    });

    const ratingArea = stars[0].parentElement;

    ratingArea.addEventListener('mouseleave', function () {
        paintStars(Number(ratingInput.value || 0));
    });
}

// Script body bottom-la load aagudhu, so direct-ah call pannalam
initStarRating();