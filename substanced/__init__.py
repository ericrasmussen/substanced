def includeme(config): # pragma: no cover
    config.include('pyramid_zodbconn')
    config.include('.sdi')
    config.include('.content')
    config.include('.acl')
    config.include('.objectmap')
    config.include('.catalog')
    config.include('.site')
    config.include('.evolution')
    config.include('.folder')
    config.include('.principal')
    config.include('.undo')
    config.include('.properties')
    
