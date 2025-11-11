-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant necessary permissions to the application user
GRANT ALL PRIVILEGES ON DATABASE lakeplatform TO lakeuser;
GRANT ALL PRIVILEGES ON SCHEMA public TO lakeuser;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO lakeuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO lakeuser;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO lakeuser;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO lakeuser;
