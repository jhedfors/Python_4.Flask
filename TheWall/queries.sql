SELECT * FROM users; # Should display two friends

SELECT * FROM comments; # Should display two friends

SELECT * FROM messages; # Should display two friends

SELECT messages.id AS message_id, first_name, last_name, message, messages.created_on, messages.users_id AS messages_users_id FROM messages LEFT JOIN users ON users.id = 23;

INSERT INTO messages (message, created_on, modified_on, users_id) VALUES ('message', NOW(), NOW(), '23');

INSERT INTO comments (comment, created_on, modified_on, users_id, messages_id, messages_users_id) VALUES (:message, NOW(), NOW(), :active_id,:message_id, :message_users_id);



[parameters: [{'comment': u'hello', 'message_users_id': u'23', 'message_id': u'22', 'active_id': 22}]]modifed_on