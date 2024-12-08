CREATE TABLE IF NOT EXISTS media_responses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  datetime TEXT DEFAULT (datetime('now', 'localtime')),
  type TEXT NOT NULL,
  response TEXT NOT NULL,
  client TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS questions_responses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  datetime TEXT DEFAULT (datetime('now')),
  expert TEXT NOT NULL,
  question TEXT NOT NULL, 
  response TEXT NOT NULL,
  client TEXT NOT NULL
);
