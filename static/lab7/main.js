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

            if (films[i].title === films[i].title_ru) {
                tdTitle.innerText = ''; 
            } else {
                tdTitle.innerText = films[i].title;
            }
            
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
                deleteFilm(films[i].id);
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
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '<tr><td colspan="4">Ошибка при загрузке данных</td></tr>';
    });
}

function addFilm() {
    alert('Функция добавления фильма');
}

function editFilm(id) {
    alert('Редактировать фильм с ID: ' + id);
}

function deleteFilm(id) {
    if (confirm('Вы уверены, что хотите удалить этот фильм?')) {
        fetch(`/lab7/rest-api/films/${id}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.status === 204) {
                alert('Фильм удален!');
                fillFilmList(); 
            } else {
                alert('Ошибка при удалении');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Ошибка сети');
        });
    }
}