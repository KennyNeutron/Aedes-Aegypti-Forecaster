-- Create the detections table if it doesn't exist
CREATE TABLE IF NOT EXISTS detections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    faa_count INTEGER NOT NULL,
    temperature_c REAL NOT NULL,
    raw_image_path TEXT NOT NULL,
    output_image_path TEXT NOT NULL
);

-- Index for faster queries (optional)
CREATE INDEX IF NOT EXISTS idx_timestamp ON detections(timestamp);
