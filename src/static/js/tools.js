async function loadTools(search = '', sort_by = 'id', order = 'asc', selectedDiameters = []) {
    const response = await fetch(`/api/tools?search=${search}&sort_by=${sort_by}&order=${order}&diameter=${selectedDiameters.join(',')}`);


    // Обработчик событий для фильтрации по диаметрам
document.getElementById('diameter-select').addEventListener('change', () => {
    const selectedDiameters = Array.from(document.getElementById('diameter-select').selectedOptions).map(option => option.value);
    loadTools('', 'id', 'asc', selectedDiameters);  // Перезагружаем инструменты с выбранными диаметрами
});

    if (!response.ok) {
        console.error('Error fetching tools:', response.statusText);
        alert('Ошибка загрузки инструментов. Попробуйте позже.');
        return;
    }

    const { tools, diameters } = await response.json();

    // Обновляем список доступных диаметров
    const diameterSelect = document.getElementById('diameter-select');
    diameterSelect.innerHTML = '';  // Очистить перед добавлением новых значений
    diameters.forEach(diameter => {
        const option = document.createElement('option');
        option.value = diameter;
        option.textContent = diameter;
        diameterSelect.appendChild(option);
    });

    const tableBody = document.getElementById('tools-table-body');
    tableBody.innerHTML = '';  // Очистить таблицу перед загрузкой новых данных

    if (tools.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="14" class="text-center">Нет инструментов для отображения.</td></tr>';
        return;
    }

    tools.forEach(tool => {
        const createAt = tool.create_at ? new Date(tool.create_at).toLocaleString('en-GB') : '';
        const updateAt = tool.update_at ? new Date(tool.update_at).toLocaleString('en-GB') : '';

        // Добавляем данные в таблицу
        tableBody.innerHTML += `
            <tr>
                <td>${tool.id}</td>
                <td>${tool.name}</td>
                <td>${tool.diameter || ''}</td>
                <td>${tool.length || ''}</td>
                <td>${tool.deep_of_drill || ''}</td>
                <td>${tool.plate || ''}</td>
                <td>${tool.screws || ''}</td>
                <td>${tool.key || ''}</td>
                <td>${tool.company || ''}</td>
                <td>${tool.storage || ''}</td>
                <td>${createAt}</td>
                <td>${updateAt}</td>
                <td>
                    <input type="checkbox" ${tool.is_broken ? 'checked' : ''} onchange="toggleBroken(${tool.id}, this.checked)">
                </td>
                <td><img src="${tool.image_path || ''}" alt="Image" width="50"></td>
                <td>
                    <a href="/update/${tool.id}" class="btn btn-warning btn-sm">✏️</a>
                    <button class="btn btn-danger btn-sm" onclick="deleteTool(${tool.id})">🗑️</button>
                </td>
            </tr>
        `;
    });
}
