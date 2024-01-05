const navigationLinks = document.querySelectorAll('.nav-area a');
            navigationLinks.forEach(link => {
            link.addEventListener('click', () => {
            navigationLinks.forEach(item => item.classList.remove('active'));
            link.classList.add('active');
          });
        });