-- CREATE TABLE public.locations_temp (
--   id text NOT NULL,
--   created_at timestamp with time zone NOT NULL DEFAULT now(),
--   type text NOT NULL,
--   name text,
--   image text,
--   thumbnail text,
--   phone text,
--   website text,
--   address text,
--   rating text,
--   category text,
--   longitude numeric,
--   latitude numeric,
--   metadata jsonb NOT NULL,
  
--   CONSTRAINT locations_new_pkey PRIMARY KEY (id)
-- );

SELECT 
  metadata->>'id' AS id,
  metadata->>'title' AS name,
  metadata->'images'->1->>'image' AS image,
  metadata->>'thumbnail' AS thumbnail,
  metadata->>'phone' AS phone,
  metadata->>'website' AS website,
  metadata->>'address' AS address,
  metadata->>'review_rating' AS review_rating,
  metadata->>'price_range' AS price_range
FROM locations
WHERE type = 'scraped_gmaps'


GRANT USAGE ON SCHEMA host_scraper TO service_role;
GRANT ALL ON ALL TABLES IN SCHEMA host_scraper TO service_role;
GRANT ALL ON ALL ROUTINES IN SCHEMA host_scraper TO service_role;
GRANT ALL ON ALL SEQUENCES IN SCHEMA host_scraper TO service_role;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA host_scraper TO service_role;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA host_scraper GRANT ALL ON TABLES TO service_role;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA host_scraper GRANT ALL ON ROUTINES TO service_role;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA host_scraper GRANT ALL ON SEQUENCES TO service_role;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA host_scraper GRANT ALL ON FUNCTIONS TO service_role;
