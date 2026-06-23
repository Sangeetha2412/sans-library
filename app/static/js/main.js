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

document.addEventListener('DOMContentLoaded', function () {
    const stars = document.querySelectorAll('.star-input');
    const ratingInput = document.getElementById('ratingInput');

    // Book detail page illa na error varama stop aagum
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
});

/* ─── PREMIUM LIBRARY HERO EFFECTS ───────────────────────────── */

.hero-section {
    min-height: 100vh;
    overflow: hidden;
    position: relative;
    background:
        radial-gradient(circle at 15% 20%, rgba(91, 133, 255, 0.32), transparent 32%),
        radial-gradient(circle at 85% 15%, rgba(189, 121, 255, 0.30), transparent 35%),
        radial-gradient(circle at 50% 85%, rgba(87, 220, 255, 0.20), transparent 38%),
        linear-gradient(135deg, #eef5ff 0%, #f7f0ff 48%, #eafcff 100%);
}

.hero-section::before {
    content: "";
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(92, 104, 190, 0.07) 1px, transparent 1px),
        linear-gradient(90deg, rgba(92, 104, 190, 0.07) 1px, transparent 1px);
    background-size: 42px 42px;
    mask-image: linear-gradient(to bottom, black, transparent);
    pointer-events: none;
}

.hero-section::after {
    content: "";
    position: absolute;
    width: 550px;
    height: 550px;
    border-radius: 50%;
    background: rgba(126, 100, 255, 0.20);
    filter: blur(80px);
    left: 50%;
    top: 48%;
    transform: translate(-50%, -50%);
    animation: heroGlowPulse 5s ease-in-out infinite;
    pointer-events: none;
}

.hero-title {
    color: #22234a;
    text-shadow: 0 4px 20px rgba(91, 91, 180, 0.12);
    animation: titleRise 0.9s ease both;
}

.hero-sub {
    color: #59627f;
    animation: titleRise 1.1s ease both;
}

.hero-badge {
    color: #5d43d7;
    background: rgba(255, 255, 255, 0.65);
    border: 1px solid rgba(113, 88, 235, 0.30);
    box-shadow: 0 8px 25px rgba(103, 87, 220, 0.14);
    backdrop-filter: blur(12px);
    animation: badgeFloat 3s ease-in-out infinite;
}

.hero-library-icon {
    width: 92px;
    height: 92px;
    margin-left: auto;
    margin-right: auto;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 28px;
    font-size: 2.8rem;
    color: #6a50e8;
    background: linear-gradient(135deg, #ffffff, #e7e2ff);
    border: 1px solid rgba(109, 83, 235, 0.25);
    box-shadow:
        0 15px 35px rgba(89, 76, 204, 0.18),
        inset 0 1px 0 rgba(255,255,255,0.95);
    animation: libraryIconFloat 4s ease-in-out infinite;
}

.floating-book {
    position: absolute;
    z-index: 1;
    font-size: 2.2rem;
    color: rgba(102, 78, 224, 0.30);
    filter: drop-shadow(0 8px 10px rgba(90, 70, 190, 0.12));
    pointer-events: none;
}

.book-one {
    top: 18%;
    left: 10%;
    animation: floatBookOne 6s ease-in-out infinite;
}

.book-two {
    top: 62%;
    left: 15%;
    font-size: 1.8rem;
    color: rgba(55, 151, 224, 0.30);
    animation: floatBookTwo 7s ease-in-out infinite;
}

.book-three {
    top: 20%;
    right: 12%;
    font-size: 2.4rem;
    color: rgba(179, 87, 230, 0.28);
    animation: floatBookThree 6.5s ease-in-out infinite;
}

.book-four {
    top: 68%;
    right: 16%;
    font-size: 1.9rem;
    color: rgba(255, 120, 170, 0.30);
    animation: floatBookFour 7.5s ease-in-out infinite;
}

.feather-one {
    top: 43%;
    right: 7%;
    font-size: 2rem;
    color: rgba(68, 167, 220, 0.30);
    animation: featherMove 8s ease-in-out infinite;
}

.hero-bookshelf {
    width: min(560px, 90%);
    margin-left: auto;
    margin-right: auto;
    animation: shelfRise 1.4s ease both;
}

.shelf-books {
    height: 70px;
    display: flex;
    align-items: flex-end;
    justify-content: center;
    gap: 5px;
    padding: 0 20px;
}

.shelf-book {
    display: block;
    width: 30px;
    border-radius: 5px 5px 2px 2px;
    box-shadow: 0 5px 10px rgba(57, 53, 130, 0.18);
    transform-origin: bottom;
    animation: bookWiggle 4s ease-in-out infinite;
}

.book-a { height: 52px; background: linear-gradient(#8c79ff, #5c4ed9); }
.book-b { height: 64px; background: linear-gradient(#57c7f5, #318bc9); animation-delay: .4s; }
.book-c { height: 45px; background: linear-gradient(#ff9ac8, #e465a3); animation-delay: .8s; }
.book-d { height: 68px; background: linear-gradient(#9e8cff, #705bdc); animation-delay: 1.2s; }
.book-e { height: 54px; background: linear-gradient(#68d9c3, #38a995); animation-delay: 1.6s; }
.book-f { height: 63px; background: linear-gradient(#ffbd73, #e88a3f); animation-delay: 2s; }
.book-g { height: 48px; background: linear-gradient(#75a9ff, #4a70d9); animation-delay: 2.4s; }
.book-h { height: 60px; background: linear-gradient(#d696ff, #a25dd5); animation-delay: 2.8s; }

.shelf-line {
    height: 12px;
    border-radius: 10px;
    background: linear-gradient(90deg, #6859cc, #8e78ef, #6859cc);
    box-shadow: 0 8px 18px rgba(75, 65, 170, 0.22);
}

/* ─── ANIMATIONS ─────────────────────────────────────────────── */

@keyframes titleRise {
    from { opacity: 0; transform: translateY(28px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes shelfRise {
    from { opacity: 0; transform: translateY(35px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes heroGlowPulse {
    0%, 100% { opacity: 0.45; transform: translate(-50%, -50%) scale(0.95); }
    50% { opacity: 0.85; transform: translate(-50%, -50%) scale(1.08); }
}

@keyframes badgeFloat {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-6px); }
}

@keyframes libraryIconFloat {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    50% { transform: translateY(-10px) rotate(3deg); }
}

@keyframes floatBookOne {
    0%, 100% { transform: translate(0, 0) rotate(-8deg); }
    50% { transform: translate(15px, -24px) rotate(8deg); }
}

@keyframes floatBookTwo {
    0%, 100% { transform: translate(0, 0) rotate(10deg); }
    50% { transform: translate(-15px, -25px) rotate(-5deg); }
}

@keyframes floatBookThree {
    0%, 100% { transform: translate(0, 0) rotate(8deg); }
    50% { transform: translate(-18px, -22px) rotate(-10deg); }
}

@keyframes floatBookFour {
    0%, 100% { transform: translate(0, 0) rotate(-6deg); }
    50% { transform: translate(15px, -20px) rotate(10deg); }
}

@keyframes featherMove {
    0%, 100% { transform: translate(0, 0) rotate(-15deg); }
    50% { transform: translate(-20px, -28px) rotate(12deg); }
}

@keyframes bookWiggle {
    0%, 100% { transform: rotate(0deg) translateY(0); }
    50% { transform: rotate(1.5deg) translateY(-3px); }
}

@media (max-width: 768px) {
    .floating-book {
        font-size: 1.4rem;
        opacity: 0.7;
    }

    .book-one { left: 5%; }
    .book-three { right: 5%; }
    .book-two, .book-four, .feather-one { display: none; }

    .hero-library-icon {
        width: 75px;
        height: 75px;
        font-size: 2.2rem;
    }

    .shelf-book {
        width: 22px;
    }
}