BEGIN;

CREATE TABLE usernames (
    id       BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name     TEXT NOT NULL UNIQUE,
    banned   BOOLEAN NOT NULL DEFAULT FALSE
);

INSERT INTO schema_migrations (version)
VALUES ('0002_usernames.sql');

COMMIT;
