from rank_hugo_themes import (
    engine, Hugothemes,
    Hugothemes_from_gitlab, sessionmaker
)


def get_theme_count():
    session = sessionmaker(bind=engine)()
    theme_count = session.query(Hugothemes).count()
    print(theme_count)
    return theme_count


def get_theme_count_from_gitlab():
    session = sessionmaker(bind=engine)()
    theme_count_from_gitlab = session.query(Hugothemes_from_gitlab).count()
    print(theme_count_from_gitlab)
    return theme_count_from_gitlab


def get_newest_update_time():
    session = sessionmaker(bind=engine)()
    newest_commit_time = session.query(
        Hugothemes.commit_date_in_seconds
    ).order_by(Hugothemes.commit_date_in_seconds.desc()).first()
    return newest_commit_time


def get_newest_update_time_from_gitlab():
    session = sessionmaker(bind=engine)()
    newest_commit_time = session.query(
        Hugothemes_from_gitlab.commit_date_in_seconds
    ).order_by(
        Hugothemes_from_gitlab.commit_date_in_seconds.desc()).first()
    return newest_commit_time


def get_themes():
    session = sessionmaker(bind=engine)()
    return session.query(Hugothemes).all()


def get_themes_from_gitlab_table():
    session = sessionmaker(bind=engine)()
    return session.query(Hugothemes_from_gitlab).all()


def get_themes_from_gitlab_table_by_date():
    session = sessionmaker(bind=engine)()
    return session.query(
        Hugothemes_from_gitlab).order_by(
        Hugothemes_from_gitlab.commit_date_in_seconds).all()


def get_gitlab_themes():
    session = sessionmaker(bind=engine)()
    return session.query(Hugothemes).filter(
        Hugothemes.url.contains("gitlab")).order_by(
        Hugothemes.commit_date_in_seconds).all()
