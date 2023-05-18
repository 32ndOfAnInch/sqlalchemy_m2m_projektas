-- DROP TABLE listing_;

-- SELECT * FROM listing_, user
-- WHERE user_id = user.id;

-- DROP TABLE type;

-- DROP TABLE category;

-- DELETE FROM category WHERE id = 1;
-- DELETE FROM type WHERE id = 1;

-- CATEGORY INSERTS

INSERT INTO category 
(id, operation_category, type_id)
VALUES (1, "taxes", 2);

INSERT INTO category 
(id, operation_category, type_id)
VALUES (2, "salary", 1);

INSERT INTO category 
(id, operation_category, type_id)
VALUES (3, "groceries", 2);

INSERT INTO category 
(id, operation_category, type_id)
VALUES (4, "fuel", 2);

INSERT INTO category 
(id, operation_category, type_id)
VALUES (5, "municipal taxes", 2);

INSERT INTO category 
(id, operation_category, type_id)
VALUES (5, "social security", 2);

INSERT INTO category 
(id, operation_category, type_id)
VALUES (6, "health insurance", 1);

INSERT INTO category 
(id, operation_category, type_id)
VALUES (7, "other", 1);

-- TYPE INSERTS

INSERT INTO type 
(id, operation_type)
VALUES (1, "earnings");

INSERT INTO type 
(id, operation_type)
VALUES (2, "expenses");



-- queries
-- SELECT category.id, category.operation_category 
-- FROM type, category
-- WHERE category.type_id = type.id
-- AND type.id = 2;