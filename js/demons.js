const demons = [
  {
    "id": 1,
    "name": "Beetle",
    "creator": "Cirtrax",
    "verifier": 1,
    "verifyDate": "2025-10-02",
    "completers": [
      {
        "playerId": 1,
        "date": "2025-10-02"
      },
      {
        "playerId": 3,
        "date": "2025-11-04"
      }
    ]
  },
  {
    "id": 2,
    "name": "Acropolis",
    "creator": "Zobros",
    "verifier": 1,
    "verifyDate": "2025-09-29",
    "completers": [
      {
        "playerId": 1,
        "date": "2025-09-29"
      },
      {
        "playerId": 3,
        "date": "2025-07-09"
      }
    ]
  },
  {
    "id": 3,
    "name": "Crazy II",
    "creator": "DavJT",
    "verifier": 2,
    "verifyDate": "2025-10-29",
    "completers": [
      {
        "playerId": 2,
        "date": "2025-10-29"
      },
      {
        "playerId": 3,
        "date": "2025-05-12"
      }
    ]
  },
  {
    "id": 4,
    "name": "Quantum Variations",
    "creator": "Darwin",
    "verifier": 1,
    "verifyDate": "2025-10-28",
    "completers": [
      {
        "playerId": 1,
        "date": "2025-10-28"
      }
    ]
  },
  {
    "id": 5,
    "name": "Psychosis",
    "creator": "Hinds",
    "verifier": 1,
    "verifyDate": "2025-09-29",
    "completers": [
      {
        "playerId": 1,
        "date": "2025-09-29"
      }
    ]
  },
  {
    "id": 6,
    "name": "The Furious",
    "creator": "Knobbelboy",
    "verifier": 1,
    "verifyDate": "2024-07-12",
    "completers": [
      {
        "playerId": 1,
        "date": "2024-07-12"
      }
    ]
  },
  {
    "id": 7,
    "name": "Ruuun",
    "creator": "CherryTeam",
    "verifier": 1,
    "verifyDate": "2025-06-01",
    "completers": [
      {
        "playerId": 1,
        "date": "2025-06-01"
      },
      {
        "playerId": 2,
        "date": "2025-04-08"
      }
    ]
  },
  {
    "id": 8,
    "name": "Ascent",
    "creator": "JustBasic",
    "verifier": 1,
    "verifyDate": "2025-09-18",
    "completers": [
      {
        "playerId": 1,
        "date": "2025-09-18"
      }
    ]
  },
  {
    "id": 9,
    "name": "Necropolis",
    "creator": "IIINepTuneIII",
    "verifier": 3,
    "verifyDate": "2025-11-10",
    "completers": [
      {
        "playerId": 3,
        "date": "2025-11-10"
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
