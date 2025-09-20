CREATE TABLE articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    summary TEXT,
    keywords VARCHAR(255),
    published_date DATE,
    url VARCHAR(500)
);