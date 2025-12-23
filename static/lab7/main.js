function fillFilmList() {
    fetch('/lab7/rest-api/films/')
    .then(function (response) {
        return response.json();
    })
    .then(function (data) {
        let films = data.films || [];
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '';

        for(let i = 0; i < films.length; i++) {
            let tr = document.createElement('tr');

            let tdTitle = document.createElement('td');
            let tdTitleRus = document.createElement('td');
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td');

            tdTitle.innerText = films[i].title === films[i].title_ru ? '' : films[i].title;
            tdTitleRus.innerText = films[i].title_ru;
            tdYear.innerText = films[i].year;

            let editButton = document.createElement('button');
            editButton.innerText = 'редактировать';
            editButton.onclick = function() {
                editFilm(films[i].id);
            };

            let delButton = document.createElement('button');
            delButton.innerText = 'удалить';
            delButton.onclick = function() {
                deleteFilm(films[i].id, films[i].title_ru);
            };

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
    });
}

function deleteFilm(id, title) {
    if(! confirm(`Вы точно хотите удалить фильм "${title}"?`))
        return;

    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})
        .then(function () {
            fillFilmList();
        })
        .catch(function (error) {
            console.error('Ошибка при удалении фильма:', error);
            alert('Ошибка при удалении фильма');
        });  
}

function showModal() {
    document.querySelector('div.modal').style.display = 'block';
}

function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
}

function cancel () {
    hideModal();
}

function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    showModal();
}

function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
    .then(function (response) {
        return response.json();
    })
    .then(function (data) {
        if (data.success && data.film) {
            const film = data.film;
            document.getElementById('id').value = film.id;
            document.getElementById('title').value = film.title;
            document.getElementById('title-ru').value = film.title_ru;
            document.getElementById('year').value = film.year;
            document.getElementById('description').value = film.description;
            showModal();
        }
    })
    .catch(function (error) {
        console.error('Ошибка при загрузке фильма:', error);
    });
}

function sendFilm() {
    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title-ru').value,
        year: document.getElementById('year').value,
        description: document.getElementById('description').value
    }

    const id = document.getElementById('id').value;
    let url = `/lab7/rest-api/films`;
    let method = 'POST';

    if (id) {
        url = `/lab7/rest-api/films/${id}`;
        method = 'PUT';
        film.id = parseInt(id);
    }

    fetch(url, {
        method: method, 
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(film)
    })
    .then(function () {
        fillFilmList();
        hideModal();
    })
    .catch(function (error) {
        console.error('Ошибка при сохранении фильма:', error);
        alert('Ошибка при сохранении фильма');
    });          
}