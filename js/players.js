const players = [
  {
    "id": 1,
    "name": "DoloresKingGMD",
    "completedDemons": [
      1,
      2,
      4,
      5,
      6,
      7,
      8
    ]
  },
  {
    "id": 2,
    "name": "Walen0k",
    "completedDemons": [
      3,
      7
    ]
  },
  {
    "id": 3,
    "name": "What",
    "completedDemons": [
      1
    ]
  }
];

// Функция для получения игрока по ID
function getPlayerById(id) {
    return players.find(player => player.id === id);
}

// Функция для получения всех игроков
function getAllPlayers() {
    return players;
}

// Функция для получения демонов игрока
function getPlayerDemons(playerId) {
    const player = getPlayerById(playerId);
    if (!player) return [];
    
    return player.completedDemons.map(demonId => {
        const demon = getDemonById(demonId);
        return {
            ...demon,
            completionDate: getCompletionDate(playerId, demonId)
        };
    });
}

// Функция для получения даты прохождения демона игроком
function getCompletionDate(playerId, demonId) {
    const demon = getDemonById(demonId);
    if (!demon) return null;
    
    const completion = demon.completers.find(comp => comp.playerId === playerId);
    return completion ? completion.date : null;
}

// Функция для расчета очков игрока
function calculatePlayerPoints(playerId) {
    const player = getPlayerById(playerId);
    if (!player) return 0;
    
    let totalPoints = 0;
    player.completedDemons.forEach(demonId => {
        const demonIndex = demonList.indexOf(demonId);
        if (demonIndex !== -1) {
            const position = demonIndex + 1;
            totalPoints += calculateDemonPoints(position);
        }
    });
    return totalPoints;
}
