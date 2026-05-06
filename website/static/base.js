// Scroll animation (fade-in effect using IntersectionObserver)
document.addEventListener("DOMContentLoaded", () => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.2 });

  document.querySelectorAll('.fade-in').forEach(section => observer.observe(section));

  // Slide show logic (if any)
  const slides = document.querySelectorAll('.slide');
  const dots = document.querySelectorAll('.dot');
  let currentSlide = 0;

  if (slides.length) {
    function showSlide(n) {
      slides.forEach(slide => slide.classList.remove('active'));
      dots.forEach(dot => dot.classList.remove('active'));
      slides[n].classList.add('active');
      dots[n].classList.add('active');
    }

    function nextSlide() {
      currentSlide = (currentSlide + 1) % slides.length;
      showSlide(currentSlide);
    }

    setInterval(nextSlide, 4000);

    dots.forEach((dot, index) => {
      dot.addEventListener('click', () => {
        currentSlide = index;
        showSlide(currentSlide);
      });
    });
  }

  // Dark mode toggle
  const themeBtn = document.createElement('button');
  themeBtn.id = 'theme-toggle';
  themeBtn.innerText = '🌙 Dark Mode';
  document.body.appendChild(themeBtn);

  themeBtn.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    themeBtn.innerText = document.body.classList.contains('dark-mode') ? '☀️ Light Mode' : '🌙 Dark Mode';
  });
});
