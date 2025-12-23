function fillFilmList() {
    fetch('/lab7/rest-api/films/')
    .then(function (response) {
        if (!response.ok) {
            throw new Error('Ошибка сети: ' + response.status);
        }
        return response.json();
    })
    .then(function (data) {
        let films = data.films || [];
        let tbody = document.getElementById('film-list');
        
        if (!tbody) {
            console.error('Элемент tbody с id="film-list" не найден');
            return;
        }
        
        tbody.innerHTML = '';

        if (films.length === 0) {
            let tr = document.createElement('tr');
            let td = document.createElement('td');
            td.colSpan = 4;
            td.textContent = 'Фильмов нет';
            td.style.textAlign = 'center';
            tr.appendChild(td);
            tbody.appendChild(tr);
            return;
        }

        for(let i = 0; i < films.length; i++) {
            let tr = document.createElement('tr');

            let tdTitle = document.createElement('td');
            let tdTitleRus = document.createElement('td');
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td');

            tdTitle.innerText = (films[i].title === films[i].title_ru || !films[i].title) ? '' : (films[i].title || '');
            tdTitleRus.innerText = films[i].title_ru || '';
            tdYear.innerText = films[i].year || '';

            let editButton = document.createElement('button');
            editButton.innerText = 'редактировать';
            editButton.onclick = (function(id) {
                return function() {
                    editFilm(id);
                };
            })(films[i].id); 

            let delButton = document.createElement('button');
            delButton.innerText = 'удалить';
            delButton.onclick = (function(id, title) {
                return function() {
                    deleteFilm(id, title);
                };
            })(films[i].id, films[i].title_ru || '');

            tdActions.appendChild(editButton);
            tdActions.appendChild(delButton);

            tr.appendChild(tdTitle);
            tr.appendChild(tdTitleRus);
            tr.appendChild(tdYear);
            tr.appendChild(tdActions);

            tbody.appendChild(tr);
        }
    })
    .catch(function (error) {
        console.error('Ошибка при загрузке фильмов:', error);
        alert('Не удалось загрузить фильмы. Проверьте консоль для подробностей.');
    });
}

function deleteFilm(id, title) {
    if(!confirm(`Вы точно хотите удалить фильм "${title}"?`))
        return;

    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})
        .then(function (response) {
            if (!response.ok) {
                throw new Error('Ошибка при удалении: ' + response.status);
            }
            return response.json();
        })
        .then(function(data) {
            if (data.success) {
                fillFilmList();
            } else {
                alert('Ошибка при удалении: ' + (data.error || 'Неизвестная ошибка'));
            }
        })
        .catch(function (error) {
            console.error('Ошибка при удалении фильма:', error);
            alert('Ошибка при удалении фильма');
        });  
}

function showModal() {
    document.querySelector('.modal').style.display = 'block';
    document.getElementById('title-ru-error').innerText = '';
    document.getElementById('title-error').innerText = '';
    document.getElementById('year-error').innerText = '';
    document.getElementById('description-error').innerText = '';
}

function hideModal() {
    document.querySelector('.modal').style.display = 'none';
}

function cancel() {
    hideModal();
}

function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    
    document.getElementById('modal-title').textContent = 'Добавить фильм';
    
    document.getElementById('title-ru-error').innerText = '';
    document.getElementById('title-error').innerText = '';
    document.getElementById('year-error').innerText = '';
    document.getElementById('description-error').innerText = '';
    
    showModal();
}

function editFilm(id) {
    if (!id) {
        alert('ID фильма не указан');
        return;
    }
    
    fetch(`/lab7/rest-api/films/${id}`)
    .then(function (response) {
        if (!response.ok) {
            throw new Error('Ошибка загрузки: ' + response.status);
        }
        return response.json();
    })
    .then(function (data) {
        if (data.success && data.film) {
            const film = data.film;
            
            document.getElementById('id').value = film.id || '';
            document.getElementById('title').value = film.title || '';
            document.getElementById('title-ru').value = film.title_ru || '';
            document.getElementById('year').value = film.year || '';
            document.getElementById('description').value = film.description || '';
            
            document.getElementById('modal-title').textContent = 'Редактировать фильм';
            
            document.getElementById('title-ru-error').innerText = '';
            document.getElementById('title-error').innerText = '';
            document.getElementById('year-error').innerText = '';
            document.getElementById('description-error').innerText = '';
            
            showModal();
        } else {
            alert('Ошибка при загрузке фильма: ' + (data.error || 'Неизвестная ошибка'));
        }
    })
    .catch(function (error) {
        console.error('Ошибка при загрузке фильма:', error);
        alert('Ошибка сети при загрузке фильма');
    });
}

function sendFilm() {
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value.trim(),
        title_ru: document.getElementById('title-ru').value.trim(),
        year: document.getElementById('year').value.trim(),
        description: document.getElementById('description').value.trim()
    };

    if (!film.title_ru) {
        document.getElementById('title-ru-error').innerText = 'Название на русском обязательно';
        return;
    }
    
    if (!film.year) {
        document.getElementById('year-error').innerText = 'Год выпуска обязателен';
        return;
    }

    if (!film.title) {
        film.title = film.title_ru;
    }

    let url = `/lab7/rest-api/films`;
    let method = 'POST';

    if (id) {
        url = `/lab7/rest-api/films/${id}`;
        method = 'PUT';
        film.id = parseInt(id); 
    }

    document.getElementById('title-ru-error').innerText = '';
    document.getElementById('title-error').innerText = '';
    document.getElementById('year-error').innerText = '';
    document.getElementById('description-error').innerText = '';

    fetch(url, {
        method: method, 
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(film)
    })
    .then(function (response) {
        if (!response.ok) {
            throw new Error('Ошибка сети: ' + response.status);
        }
        return response.json();
    })
    .then(function(data) {
        if (data.success) {
            fillFilmList();
            hideModal();
        } else {
            if (data.errors) {
                if (data.errors.title_ru) {
                    document.getElementById('title-ru-error').innerText = data.errors.title_ru;
                }
                if (data.errors.year) {
                    document.getElementById('year-error').innerText = data.errors.year;
                }
                if (data.errors.description) {
                    document.getElementById('description-error').innerText = data.errors.description;
                }
                if (data.errors.general) {
                    alert(data.errors.general);
                }
            } else if (data.error) {
                alert('Ошибка: ' + data.error);
            } else {
                alert('Неизвестная ошибка');
            }
        }
    })
    .catch(function (error) {
        console.error('Ошибка при сохранении фильма:', error);
        alert('Ошибка при сохранении фильма: ' + error.message);
    });          
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', fillFilmList);
} else {
    fillFilmList(); 
}