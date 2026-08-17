document.addEventListener('DOMContentLoaded', () => {
    const root = document.documentElement;
    const themeToggle = document.getElementById('theme-toggle');
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.getElementById('nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');

    // Theme
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const initialTheme = savedTheme || (prefersDark ? 'dark' : 'light');

    function setTheme(theme) {
        if (theme === 'dark') {
            root.setAttribute('data-theme', 'dark');
            themeToggle.textContent = '☀️';
            themeToggle.setAttribute('aria-label', 'Switch to light mode');
            themeToggle.title = 'Switch to light mode';
        } else {
            root.removeAttribute('data-theme');
            themeToggle.textContent = '🌙';
            themeToggle.setAttribute('aria-label', 'Switch to dark mode');
            themeToggle.title = 'Switch to dark mode';
        }
        localStorage.setItem('theme', theme);
    }

    setTheme(initialTheme);

    themeToggle.addEventListener('click', () => {
        const current = root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
        setTheme(current === 'dark' ? 'light' : 'dark');
    });

    // Mobile navigation
    function closeMenu() {
        navMenu.classList.remove('active');
        hamburger.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
        hamburger.setAttribute('aria-label', 'Open navigation menu');
    }

    hamburger.addEventListener('click', () => {
        const isOpen = navMenu.classList.toggle('active');
        hamburger.classList.toggle('open', isOpen);
        hamburger.setAttribute('aria-expanded', String(isOpen));
        hamburger.setAttribute('aria-label', isOpen ? 'Close navigation menu' : 'Open navigation menu');
    });

    navLinks.forEach(link => link.addEventListener('click', closeMenu));

    document.addEventListener('click', event => {
        if (window.innerWidth <= 720 && !navMenu.contains(event.target) && !hamburger.contains(event.target)) {
            closeMenu();
        }
    });

    // Active navigation link
    const sections = document.querySelectorAll('main section[id]');
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                navLinks.forEach(link => {
                    link.classList.toggle('active', link.getAttribute('href') === `#${entry.target.id}`);
                });
            }
        });
    }, { rootMargin: '-35% 0px -55% 0px', threshold: 0 });

    sections.forEach(section => observer.observe(section));

    // Contact form validation
    const form = document.getElementById('contact-form');
    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    const messageInput = document.getElementById('message');
    const nameError = document.getElementById('name-error');
    const emailError = document.getElementById('email-error');
    const messageError = document.getElementById('message-error');
    const formStatus = document.getElementById('form-status');

    function validEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    function clearErrors() {
        nameError.textContent = '';
        emailError.textContent = '';
        messageError.textContent = '';
        formStatus.textContent = '';
    }

    form.addEventListener('submit', event => {
        event.preventDefault();
        clearErrors();
        let valid = true;

        if (nameInput.value.trim().length < 2) {
            nameError.textContent = 'Please enter your name.';
            valid = false;
        }

        if (!validEmail(emailInput.value.trim())) {
            emailError.textContent = 'Please enter a valid email address.';
            valid = false;
        }

        if (messageInput.value.trim().length < 10) {
            messageError.textContent = 'Please enter at least 10 characters.';
            valid = false;
        }

        if (!valid) {
            formStatus.style.color = 'var(--error)';
            formStatus.textContent = 'Please fix the highlighted fields.';
            return;
        }

        // This is a front-end demo. It opens the user's email client with the form data.
        const subject = encodeURIComponent(`Portfolio message from ${nameInput.value.trim()}`);
        const body = encodeURIComponent(
            `Name: ${nameInput.value.trim()}\nEmail: ${emailInput.value.trim()}\n\nMessage:\n${messageInput.value.trim()}`
        );
        window.location.href = `mailto:seavlong0099@gmail.com?subject=${subject}&body=${body}`;

        formStatus.style.color = 'var(--success)';
        formStatus.textContent = 'Opening your email app...';
    });
});
