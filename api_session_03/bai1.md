/posts                                   GET, POST
/posts/{post_id}                         GET, PUT, PATCH, DELETE
/posts/{post_id}/comments                GET, POST
/posts/{post_id}/comments/{comment_id}   GET, PATCH, DELETE
/posts/{post_id}/tags                    GET
/posts/{post_id}/tags/{tag_id}           PUT, DELETE
/tags                                    GET, POST
/tags/{tag_id}                           GET, PATCH, DELETE
/users                                   GET, POST
/users/{user_id}                         GET, PATCH
/users/{user_id}/posts                   GET
/users/{user_id}/following               GET
/users/{user_id}/following/{target_id}   PUT, DELETE
/users/{user_id}/followers               GET
