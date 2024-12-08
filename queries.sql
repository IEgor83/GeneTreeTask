-- Количество человек в семье для конкретного пользователя
WITH RECURSIVE family_tree AS (
    SELECT person_id AS relative_id
    FROM relatives_relationship
    WHERE person_id = 16 OR parent_id = 16
    UNION
    SELECT r.person_id
    FROM relatives_relationship r
    INNER JOIN family_tree ft ON r.parent_id = ft.relative_id
    UNION
    SELECT r.parent_id
    FROM relatives_relationship r
    INNER JOIN family_tree ft ON r.person_id = ft.relative_id
)
SELECT
    CASE
        WHEN COUNT(*) > 0 THEN COUNT(*)
        ELSE
            (SELECT COUNT(*)
             FROM relatives_person
             WHERE id = 16)
    END AS total_relatives
FROM family_tree;

-- Количество женщин и мужчин в семье
WITH RECURSIVE family_tree AS (
    SELECT person_id AS relative_id
    FROM relatives_relationship
    WHERE person_id = 17 OR parent_id = 17
    UNION
    SELECT r.person_id
    FROM relatives_relationship r
    INNER JOIN family_tree ft ON r.parent_id = ft.relative_id
    UNION
    SELECT r.parent_id
    FROM relatives_relationship r
    INNER JOIN family_tree ft ON r.person_id = ft.relative_id
)
SELECT
    SUM(CASE WHEN gender = 'M' THEN 1 ELSE 0 END) AS male_count,
    SUM(CASE WHEN gender = 'F' THEN 1 ELSE 0 END) AS female_count
FROM relatives_person
WHERE id IN (SELECT relative_id FROM family_tree);

