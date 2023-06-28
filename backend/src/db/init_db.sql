CREATE TYPE status AS ENUM ('not run', 'complete', 'failed');

CREATE TABLE pipeline_status (
    contract_id INTEGER PRIMARY KEY,
    download_stage status DEFAULT 'not run',
    split_stage status DEFAULT 'not run',
    clean_stage status DEFAULT 'not run',
);