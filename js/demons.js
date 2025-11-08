const demons = [
  {
    "id": 1,
    "name": "Beetle",
    "creator": "Cirtrax",
    "verifier": 1,
    "verifyDate": "2025-11-08",
    "completers": [
      {
        "playerId": 1,
        "date": "2025-11-08"
      }
    ]
  },
  {
    "id": 2,
    "name": "Acropolis",
    "creator": "Zobros",
    "verifier": 1,
    "verifyDate": "2025-11-08",
    "completers": [
      {
        "playerId": 1,
        "date": "2025-11-08"
      }
    ]
  },
  {
    "id": 3,
    "name": "Crazy II",
    "creator": "DavJT",
    "verifier": 2,
    "verifyDate": "2025-11-08",
    "completers": [
      {
        "playerId": 2,
        "date": "2025-11-08"
      }
    ]
  },
  {
    "id": 4,
    "name": "Psychosis",
    "creator": "Hinds",
    "verifier": 1,
    "verifyDate": "2025-11-08",
    "completers": [
      {
        "playerId": 1,
        "date": "2025-11-08"
      }
    ]
  },
  {
    "id": 5,
    "name": "The Furious",
    "creator": "Knobbelboy",
    "verifier": 1,
    "verifyDate": "2025-11-08",
    "completers": [
      {
        "playerId": 1,
        "date": "2025-11-08"
      }
    ]
  },
  {
    "id": 6,
    "name": "Ruuun",
    "creator": "CherryTeam",
    "verifier": 1,
    "verifyDate": "2025-11-08",
    "completers": [
      {
        "playerId": 1,
        "date": "2025-11-08"
      },
      {
        "playerId": 2,
        "date": "2025-11-08"
      }
    ]
  },
  {
    "id": 7,
    "name": "Ascent",
    "creator": "JustBasic",
    "verifier": 1,
    "verifyDate": "2025-11-08",
    "completers": [
      {
        "playerId": 1,
        "date": "2025-11-08"
      }
    ]
  }
];

// Функция для получения демона по ID
function getDemonById(id) {
    return demons.find(demon => demon.id === id);
}

// Функция для получения всех демонов
function getAllDemons() {
    return demons;
}
