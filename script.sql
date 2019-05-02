CREATE TABLE Logins (
  login VARCHAR(100) PRIMARY KEY ,
  password VARCHAR(100) NOT NULL ,
  texts_added INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE Texts (
  id SERIAL PRIMARY KEY,
  text_title VARCHAR(100) NOT NULL,
  text_made VARCHAR(100) NOT NULL,
  tag VARCHAR(100) NOT NULL,
  owner VARCHAR(100) NOT NULL REFERENCES Logins(login)
);