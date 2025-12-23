function fillFilmList() {
    console.log('Загрузка фильмов...');
    
    fetch('/lab7/rest-api/films/')
    .then(function (response) {
        console.log('Статус ответа:', response.status);
        if (!response.ok) {
            throw new Error('Ошибка сервера: ' + response.status);
        }
        return response.json();
    })
    .then(function (data) {
        console.log('Полученные данные:', data);

        let films = [];
        if (data && data.films && Array.isArray(data.films)) {
            films = data.films;
        } else if (Array.isArray(data)) {
            films = data;
        } else {
            console.error('Неизвестный формат данных:', data);
            alert('Ошибка: неправильный формат данных от сервера');
            return;
        }
        
        console.log('Фильмы для отображения:', films);
        
        let tbody = document.getElementById('film-list');
        if (!tbody) {
            console.error('Элемент tbody не найден');
            return;
        }
        
        tbody.innerHTML = '';
        
        if (films.length === 0) {
            let tr = document.createElement('tr');
            let td = document.createElement('td');
            td.colSpan = 4;
            td.textContent = 'Фильмов нет';
            td.style.textAlign = 'center';
            td.style.padding = '20px';
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

            if (films[i].title && films[i].title !== films[i].title_ru) {
                tdTitle.innerText = films[i].title;
            } else {
                tdTitle.innerText = '';
            }

            tdTitleRus.innerText = films[i].title_ru || '';

            tdYear.innerText = films[i].year || '';

            let editButton = document.createElement('button');
            editButton.innerText = 'редактировать';
            editButton.className = 'edit-btn';
            editButton.onclick = (function(filmId) {
                return function() {
                    editFilm(filmId);
                };
            })(films[i].id);

            let delButton = document.createElement('button');
            delButton.innerText = 'удалить';
            delButton.className = 'delete-btn';
            delButton.onclick = (function(filmId, filmTitle) {
                return function() {
                    deleteFilm(filmId, filmTitle);
                };
            })(films[i].id, films[i].title_ru || films[i].title || 'Без названия');

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
        alert('Не удалось загрузить фильмы: ' + error.message);
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
                alert('Фильм успешно удален');
            } else {
                alert('Ошибка при удалении: ' + (data.error || 'Неизвестная ошибка'));
            }
        })
        .catch(function (error) {
            console.error('Ошибка при удалении фильма:', error);
            alert('Ошибка при удалении фильма: ' + error.message);
        });
}

function showModal() {
    let modal = document.querySelector('.modal');
    if (modal) {
        modal.style.display = 'block';
    }
    clearErrors();
}

function hideModal() {
    let modal = document.querySelector('.modal');
    if (modal) {
        modal.style.display = 'none';
    }
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
    clearErrors();
    showModal();
}

function sendFilm() {
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value.trim(),
        title_ru: document.getElementById('title-ru').value.trim(),
        year: document.getElementById('year').value.trim(),
        description: document.getElementById('description').value.trim()
    }

    let isValid = true;
    clearErrors();
    
    if (!film.title_ru) {
        document.getElementById('title-ru-error').innerText = 'Русское название обязательно';
        isValid = false;
    }
    
    if (!film.year) {
        document.getElementById('year-error').innerText = 'Год обязателен';
        isValid = false;
    }
    
    if (!film.description) {
        document.getElementById('description-error').innerText = 'Описание обязательно';
        isValid = false;
    }
    
    if (!isValid) {
        return;
    }

    if (!film.title) {
        film.title = film.title_ru;
    }

    const url = id === '' ? `/lab7/rest-api/films` : `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST' : 'PUT';
    
    if (id) {
        film.id = parseInt(id);
    }

    fetch(url, {
        method: method, 
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(film)
    })
    .then(function (response) {
        console.log('Статус ответа:', response.status);
        if (!response.ok) {
            return response.json().then(err => { 
                throw new Error(err.error || JSON.stringify(err) || 'Ошибка сервера'); 
            });
        }
        return response.json();
    })
    .then(function(data) {
        console.log('Ответ от сервера:', data);
        if (data.success) {
            fillFilmList();
            hideModal();
            alert('Фильм успешно сохранен!');
        } else {
            if (data.errors) {
                if (data.errors.description) {
                    document.getElementById('description-error').innerText = data.errors.description;
                }
                if (data.errors.title_ru) {
                    document.getElementById('title-ru-error').innerText = data.errors.title_ru;
                }
                if (data.errors.title) {
                    document.getElementById('title-error').innerText = data.errors.title;
                }
                if (data.errors.year) {
                    document.getElementById('year-error').innerText = data.errors.year;
                }
            } else if (data.error) {
                alert('Ошибка: ' + data.error);
            }
        }
    })
    .catch(function (error) {
        console.error('Ошибка при сохранении фильма:', error);
        alert('Ошибка при сохранении фильма: ' + error.message);
    });
}

function clearErrors() {
    document.getElementById('description-error').innerText = '';
    document.getElementById('title-ru-error').innerText = '';
    document.getElementById('title-error').innerText = '';
    document.getElementById('year-error').innerText = '';
}

function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
    .then(function (response) {
        if (!response.ok) {
            throw new Error('Ошибка загрузки: ' + response.status);
        }
        return response.json();
    })
    .then(function (data) {
        console.log('Данные фильма для редактирования:', data);
        
        if (data.success && data.film) {
            const film = data.film;
            document.getElementById('id').value = film.id;
            document.getElementById('title').value = film.title || '';
            document.getElementById('title-ru').value = film.title_ru || '';
            document.getElementById('year').value = film.year || '';
            document.getElementById('description').value = film.description || '';
            document.getElementById('modal-title').textContent = 'Редактировать фильм';
            clearErrors();
            showModal();
        } else {
            alert('Ошибка при загрузке фильма: ' + (data.error || 'Неизвестная ошибка'));
        }
    })
    .catch(function (error) {
        console.error('Ошибка при загрузке фильма:', error);
        alert('Ошибка при загрузке фильма: ' + error.message);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM загружен, запускаем fillFilmList');
    fillFilmList();
});