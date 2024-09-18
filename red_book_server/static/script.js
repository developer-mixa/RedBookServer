fetch('data.json')
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! статус: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (Array.isArray(data.gallery)) {
            data.gallery.forEach(item => {
                if (item.category === 'plant') {
                    displayGalleryItem(item, 'plants-gallery');
                } else if (item.category === 'animal') {
                    displayGalleryItem(item, 'animals-gallery');
                } else {
                    console.warn(`Неизвестная категория "${item.category}" для элемента с ID "${item.id}"`);
                }
            });
        } else {
            console.error('Ожидается, что "gallery" будет массивом.');
        }
    })
    .catch(error => console.error('Ошибка загрузки данных:', error));

function displayGalleryItem(item, galleryId) {
    const gallery = document.getElementById(galleryId);

    if (!gallery) {
        console.error(`Элемент с ID "${galleryId}" не найден.`);
        return;
    }

    const div = document.createElement('div');
    div.className = 'gallery-item';
    div.setAttribute('data-id', item.id);
    div.setAttribute('data-name', item.name);
    div.setAttribute('data-description', item.description);
    div.setAttribute('data-count', item.count);
    div.setAttribute('data-image', item.image);
    div.setAttribute('data-category', item.category);

    div.innerHTML = `
        <img src="${item.image}" alt="${item.name}">
        <p>${item.name}</p>
    `;

    div.addEventListener('click', () => {
        openModal(item);
    });

    gallery.appendChild(div);
}

function openModal(item) {
    const modal = document.getElementById('modal');

    modal.style.display = 'block';

    document.getElementById('modal-title').textContent = item.name;
    document.getElementById('modal-image').src = item.image;
    document.getElementById('modal-image').alt = item.name;
    document.getElementById('modal-description').textContent = item.description;
    document.getElementById('modal-count').textContent = item.count;
    modal.classList.add('show');
}

document.getElementById('modal-close').addEventListener('click', closeModal);

window.addEventListener('click', event => {
    const modal = document.getElementById('modal');
    if (event.target === modal) {
        closeModal();
    }
});

function closeModal() {
    const modal = document.getElementById('modal');
    modal.classList.remove('show');

    setTimeout(() => {
        modal.style.display = 'none';
    }, 500); 
}

function setActiveNav() {
    const sections = document.querySelectorAll('section, header');
    const navButtons = document.querySelectorAll('.nav-button');

    const options = {
        root: null,
        rootMargin: '0px',
        threshold: 0.6 // Порог, когда считать секцию активной
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.getAttribute('id');
                navButtons.forEach(btn => {
                    btn.classList.remove('active');
                    if (btn.getAttribute('href') === `#${id}`) {
                        btn.classList.add('active');
                    }
                });
            }
        });
    }, options);

    sections.forEach(section => {
        observer.observe(section);
    });
}

function handleNavClicks() {
    const navButtons = document.querySelectorAll('.nav-button');

    navButtons.forEach(button => {
        button.addEventListener('click', function() {
            navButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    setActiveNav();
    handleNavClicks();
});
