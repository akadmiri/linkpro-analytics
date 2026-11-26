-- Optional synthetic data for a fresh local database. Run after starting the API.
BEGIN;

INSERT INTO link_profiles (username, title)
VALUES ('portfolio-demo', 'Portfolio demo')
ON CONFLICT (username) DO NOTHING;

INSERT INTO links (profile_id, title, url, position)
SELECT profile.id, demo.title, demo.url, demo.position
FROM link_profiles AS profile
CROSS JOIN (VALUES
    ('Project notes', 'https://example.com/notes', 1),
    ('Resources', 'https://example.com/resources', 2)
) AS demo(title, url, position)
WHERE profile.username = 'portfolio-demo'
  AND NOT EXISTS (
      SELECT 1 FROM links
      WHERE profile_id = profile.id AND url = demo.url
  );

INSERT INTO page_views (profile_id, viewed_at, ip_address, referrer)
SELECT profile.id, now() - day * INTERVAL '1 day' - event * INTERVAL '20 minutes',
       ('192.0.2.' || event)::inet,
       CASE event % 3 WHEN 0 THEN 'https://www.instagram.com/'
                      WHEN 1 THEN 'https://www.tiktok.com/' END
FROM link_profiles AS profile
CROSS JOIN generate_series(0, 13) AS days(day)
CROSS JOIN LATERAL generate_series(1, 10 + (13 - day) % 5) AS events(event)
WHERE profile.username = 'portfolio-demo'
  AND NOT EXISTS (SELECT 1 FROM page_views WHERE profile_id = profile.id);

INSERT INTO click_events (link_id, profile_id, clicked_at, ip_address, referrer)
SELECT link.id, profile.id, now() - day * INTERVAL '1 day' - event * INTERVAL '30 minutes',
       ('192.0.2.' || event)::inet,
       CASE event % 3 WHEN 0 THEN 'https://www.instagram.com/'
                      WHEN 1 THEN 'https://www.tiktok.com/' END
FROM link_profiles AS profile
JOIN links AS link ON link.profile_id = profile.id
CROSS JOIN generate_series(0, 13) AS days(day)
CROSS JOIN LATERAL generate_series(1, 1 + (13 - day) % 4 + (2 - link.position)) AS events(event)
WHERE profile.username = 'portfolio-demo'
  AND link.url IN ('https://example.com/notes', 'https://example.com/resources')
  AND NOT EXISTS (SELECT 1 FROM click_events WHERE profile_id = profile.id);

COMMIT;

SELECT id AS demo_profile_id FROM link_profiles WHERE username = 'portfolio-demo';
