-- migrate:up
CREATE TABLE entries (
    id serial PRIMARY KEY,
    content text NOT NULL,
    for_day date DEFAULT current_date UNIQUE,
    created timestamp DEFAULT now(),
    updated timestamp DEFAULT now()
);

-- migrate:down
DROP TABLE entries;
