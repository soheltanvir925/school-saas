-- Update school-level admins to remove is_superuser flag
UPDATE users_user 
SET is_superuser=FALSE 
WHERE school_id IS NOT NULL AND is_superuser=TRUE;

-- Verify the changes
SELECT username, school_id, is_superuser 
FROM users_user 
ORDER BY username;
