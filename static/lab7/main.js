function fillFilmList() {
    fetch('/lab7/rest-api/films/')
    .then(function (response) {
        if (!response.ok) {
            throw new Error('Ошибка сети: ' + response.status);
        }
        return response.json();
    })
    .then(function (data) {
        console.log('Данные от API:', data);
        let films = data.films || [];
        console.log('Фильмы:', films);
        
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
                    console.log('Редактировать фильм с ID:', filmId);
                    editFilm(filmId);
                };
            })(films[i].id);

            let delButton = document.createElement('button');
            delButton.innerText = 'удалить';
            delButton.className = 'delete-btn';
            delButton.onclick = (function(filmId, filmTitle) {
                return function() {
                    console.log('Удалить фильм с ID:', filmId, 'Название:', filmTitle);
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
        alert('Не удалось загрузить фильмы. Проверьте консоль для подробностей.');
    });
}

function deleteFilm(id, title) {
    console.log('Удаление фильма:', id, title);
    
    if (!confirm(`Вы точно хотите удалить фильм "${title}"?`)) {
        console.log('Удаление отменено пользователем');
        return;
    }

    fetch(`/lab7/rest-api/films/${id}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(function (response) {
        console.log('Ответ от сервера при удалении:', response.status);
        if (!response.ok) {
            throw new Error('Ошибка при удалении: ' + response.status);
        }
        return response.json();
    })
    .then(function(data) {
        console.log('Данные от сервера после удаления:', data);
        if (data.success) {
            alert('Фильм успешно удален!');
            fillFilmList();
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
    } else {
        console.error('Модальное окно не найдено');
    }
    document.getElementById('title-ru-error').innerText = '';
    document.getElementById('title-error').innerText = '';
    document.getElementById('year-error').innerText = '';
    document.getElementById('description-error').innerText = '';
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
    console.log('Добавление нового фильма');
    
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    
    document.getElementById('modal-title').textContent = 'Добавить фильм';
    
    showModal();
}

function editFilm(id) {
    console.log('Редактирование фильма с ID:', id);
    
    if (!id && id !== 0) {
        alert('ID фильма не указан');
        return;
    }
    
    fetch(`/lab7/rest-api/films/${id}`)
    .then(function (response) {
        console.log('Ответ при загрузке фильма для редактирования:', response.status);
        if (!response.ok) {
            throw new Error('Ошибка загрузки: ' + response.status);
        }
        return response.json();
    })
    .then(function (data) {
        console.log('Данные фильма для редактирования:', data);
        if (data.success && data.film) {
            const film = data.film;
            
            document.getElementById('id').value = film.id || '';
            document.getElementById('title').value = film.title || '';
            document.getElementById('title-ru').value = film.title_ru || '';
            document.getElementById('year').value = film.year || '';
            document.getElementById('description').value = film.description || '';
            
            document.getElementById('modal-title').textContent = 'Редактировать фильм';
            
            showModal();
        } else {
            alert('Ошибка при загрузке фильма: ' + (data.error || 'Неизвестная ошибка'));
        }
    })
    .catch(function (error) {
        console.error('Ошибка при загрузке фильма:', error);
        alert('Ошибка сети при загрузке фильма: ' + error.message);
    });
}

function sendFilm() {
    console.log('Отправка данных фильма');
    
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value.trim(),
        title_ru: document.getElementById('title-ru').value.trim(),
        year: document.getElementById('year').value.trim(),
        description: document.getElementById('description').value.trim()
    };

    console.log('Данные фильма:', film, 'ID:', id);

    let isValid = true;
    
    if (!film.title_ru) {
        document.getElementById('title-ru-error').innerText = 'Название на русском обязательно';
        isValid = false;
    } else {
        document.getElementById('title-ru-error').innerText = '';
    }
    
    if (!film.year) {
        document.getElementById('year-error').innerText = 'Год выпуска обязателен';
        isValid = false;
    } else if (!/^\d{4}$/.test(film.year)) {
        document.getElementById('year-error').innerText = 'Год должен быть 4-значным числом (например: 2024)';
        isValid = false;
    } else {
        document.getElementById('year-error').innerText = '';
    }
    
    if (!film.description) {
        document.getElementById('description-error').innerText = 'Описание обязательно';
        isValid = false;
    } else {
        document.getElementById('description-error').innerText = '';
    }
    
    if (!isValid) {
        console.log('Валидация не пройдена');
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

    console.log('Отправка запроса:', method, url, film);

    fetch(url, {
        method: method, 
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(film)
    })
    .then(function (response) {
        console.log('Ответ от сервера при сохранении:', response.status);
        if (!response.ok) {
            throw new Error('Ошибка сети: ' + response.status);
        }
        return response.json();
    })
    .then(function(data) {
        console.log('Данные от сервера после сохранения:', data);
        if (data.success) {
            alert('Фильм успешно сохранен!');
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

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM загружен, инициализируем приложение');

    const addFilmBtn = document.querySelector('button[onclick="addFilm()"]');
    if (addFilmBtn) {
        console.log('Кнопка "Добавить фильм" найдена');
    }

    const cancelBtn = document.querySelector('button[onclick="cancel()"]');
    if (cancelBtn) {
        console.log('Кнопка "Отмена" найдена');
    }

    const okBtn = document.querySelector('button[onclick="sendFilm()"]');
    if (okBtn) {
        console.log('Кнопка "Ок" найдена');
    }

    fillFilmList();
});

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        console.log('DOM загружен (альтернативный метод)');
        fillFilmList();
    });
} else {
    console.log('DOM уже загружен');
    fillFilmList();
}