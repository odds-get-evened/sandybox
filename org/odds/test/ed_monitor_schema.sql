SELECT 'DROP TABLES IF EXISTS "' || name || '";'
FROM sqlite_master
WHERE type = 'table';

CREATE TABLE IF NOT EXISTS "scans" (
	"id" INTEGER PRIMARY KEY AUTO_INCREMENT,
	"sig" TEXT NOT NULL UNIQUE,
	"body_id" INTEGER NOT NULL,
	"distance_from_arrival" REAL,
	"tidal_lock" INTEGER NOT NULL DEFAULT 0,
	"terraform_state_id" INTEGER,
	"planet_class_id" INTEGER,
	"atmosphere_id" INTEGER,
	"volcanism_id" INTEGER,
	"mass_em" REAL,
	"radius" REAL,
	"surface_gravity" REAL,
	"surface_temp" REAL,
	"surface_pressure" REAL,
	"landable" INTEGER NOT NULL DEFAULT 0,
	"semi_major_axis" REAL,
	"ecentricity" REAL,
	"orbital_inclination" REAL,
	"periapsis" REAL,
	"system_address" INTEGER NOT NULL,
	"timestamp" INTEGER NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY ("system_address") REFERENCES "systems"("system_address")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "systems" (
	"system_address" BIGINT PRIMARY KEY,
	"system_name" TEXT NOT NULL UNIQUE,
	PRIMARY KEY("system_address")
);

CREATE TABLE IF NOT EXISTS "materials" (
	"id" INTEGER PRIMARY KEY AUTO_INCREMENT,
	"mat_name" TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "body_classes" (
    "id" INTEGER PRIMARY KEY AUTO_INCREMENT,
    "class_name" TEXT UNIQUE NOT NULL,
);

CREATE TABLE IF NOT EXISTS "body_materials" (
	"id" INTEGER PRIMARY KEY AUTO_INCREMENT,
	"material_id" INTEGER NOT NULL,
	"percent" REAL NOT NULL,
	"scan_id" INTEGER NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY ("material_id") REFERENCES "materials"("id")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY ("scan_id") REFERENCES "scans"("id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE INDEX IF NOT EXISTS "body_materials_index_0"
ON "body_materials" ("material_id");

CREATE INDEX IF NOT EXISTS "body_materials_index_1"
ON "body_materials" ("scan_id");