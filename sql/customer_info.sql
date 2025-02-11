CREATE DATABASE IF NOT EXISTS customer_info;
use customer_info

CREATE TABLE IF NOT EXISTS agent (
  id INT AUTO_INCREMENT,
  name TEXT CHARACTER SET utf8mb4 NOT NULL,
  location TEXT CHARACTER SET utf8mb4 NOT NULL,
  public_key LONGTEXT CHARACTER SET utf8mb4 NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (name)
);
CREATE TABLE IF NOT EXISTS site (
  id INT AUTO_INCREMENT,
  name TEXT CHARACTER SET utf8mb4 NOT NULL,
  location TEXT CHARACTER SET utf8mb4 NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (name)
);
CREATE TABLE IF NOT EXISTS customer (
  id INT AUTO_INCREMENT,
  name TEXT CHARACTER SET utf8mb4 NOT NULL,
  price_plan TEXT CHARACTER SET utf8mb4 NOT NULL,
  num_users INT NOT NULL,
  mb_storage INT NOT NULL,
  contract_start date NOT NULL,
  contract_end date NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (name)
);
CREATE TABLE IF NOT EXISTS project (
  id INT AUTO_INCREMENT,
  customer_id INT NOT NULL,
  site_id INT NOT NULL,
  name TEXT CHARACTER SET utf8mb4 NOT NULL,
  endpoint TEXT CHARACTER SET utf8mb4 NOT NULL,
  access_key_id TEXT CHARACTER SET utf8mb4 NOT NULL,
  secret_access_key TEXT CHARACTER SET utf8mb4 NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (name),
  FOREIGN KEY (customer_id) REFERENCES customer (id) ON DELETE CASCADE,
  FOREIGN KEY (site_id) REFERENCES site (id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS bucket (
  id INT AUTO_INCREMENT,
  customer_id INT NOT NULL,
  project_id INT NOT NULL,
  name TEXT CHARACTER SET utf8mb4 NOT NULL,
  type ENUM ('primary', 'primary_mirror', 'project', 'project_mirror', 'user', 'user_mirror') NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (customer_id) REFERENCES customer (id) ON DELETE CASCADE,
  FOREIGN KEY (project_id) REFERENCES project (id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS backup_job (
  id INT AUTO_INCREMENT,
  customer_id INT NOT NULL,
  source_bucket INT NOT NULL,
  destination_bucket INT NOT NULL,
  name TEXT CHARACTER SET utf8mb4 NOT NULL,
  schedule TEXT CHARACTER SET utf8mb4 NOT NULL,
  retention_days INT NOT NULL,
  status LONGTEXT CHARACTER SET utf8mb4 NOT NULL,
  last_started datetime NOT NULL,
  last_completed datetime NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (name),
  FOREIGN KEY (customer_id) REFERENCES customer (id) ON DELETE CASCADE,
  FOREIGN KEY (source_bucket) REFERENCES bucket (id) ON DELETE CASCADE,
  FOREIGN KEY (destination_bucket) REFERENCES bucket (id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS db_backup_job (
  id INT AUTO_INCREMENT,
  customer_id INT NOT NULL,
  destination_bucket INT NOT NULL,
  db_host TEXT CHARACTER SET utf8mb4 NOT NULL,
  db_name TEXT CHARACTER SET utf8mb4 NOT NULL,
  db_user TEXT CHARACTER SET utf8mb4 NOT NULL,
  db_password TEXT CHARACTER SET utf8mb4 NOT NULL,
  name TEXT CHARACTER SET utf8mb4 NOT NULL,
  schedule TEXT CHARACTER SET utf8mb4 NOT NULL,
  retention_days INT NOT NULL,
  status LONGTEXT CHARACTER SET utf8mb4 NOT NULL,
  last_started datetime NOT NULL,
  last_completed datetime NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (name),
  FOREIGN KEY (destination_bucket) REFERENCES bucket (id) ON DELETE CASCADE,
  FOREIGN KEY (customer_id) REFERENCES customer (id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS make_bucket_job (
  id INT AUTO_INCREMENT,
  customer_id INT NOT NULL,
  source_project INT NOT NULL,
  destination_project INT NOT NULL,
  name TEXT CHARACTER SET utf8mb4 NOT NULL,
  schedule TEXT CHARACTER SET utf8mb4 NOT NULL,
  status LONGTEXT CHARACTER SET utf8mb4 NOT NULL,
  last_started datetime NOT NULL,
  last_completed datetime NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (name),
  FOREIGN KEY (customer_id) REFERENCES customer (id) ON DELETE CASCADE,
  FOREIGN KEY (source_project) REFERENCES project (id) ON DELETE CASCADE,
  FOREIGN KEY (destination_project) REFERENCES project (id) ON DELETE CASCADE
);
