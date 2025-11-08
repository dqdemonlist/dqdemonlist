const demons = [

];

// Функция для получения демона по ID
function getDemonById(id) {
    return demons.find(demon => demon.id === id);
}

// Функция для получения всех демонов
function getAllDemons() {
    return demons;
}
