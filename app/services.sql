CREATE TABLE IF NOT EXISTS service_logs (
    id INTEGER PRIMARY KEY,
    service_name TEXT NOT NULL,
    status TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    duration FLOAT DEFAULT NULL
);
