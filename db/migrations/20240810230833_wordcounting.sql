-- migrate:up
CREATE FUNCTION wordcount(txt text) RETURNS integer
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT
    RETURN array_length(regexp_split_to_array(txt, '\s+'), 1);

-- migrate:down
DROP FUNCTION wordcount(text);
